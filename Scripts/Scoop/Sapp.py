#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import hashlib
import argparse
import tempfile
import shutil
import subprocess
from pathlib import Path
from urllib.parse import urlparse

# ==================== 配置 ====================
MIRROR = 'https://gh-proxy.com'        # GitHub 镜像（用户测试可用）

# ==================== 工具函数 ====================
def get_scoop_base():
    """获取 Scoop 根目录"""
    return Path(os.environ.get('SCOOP', Path.home() / 'scoop'))

def get_cache_dir():
    """获取 Scoop 缓存目录"""
    cache_dir = get_scoop_base() / 'cache'
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir
    
def get_all_buckets():
    """获取所有本地 bucket 名称（buckets 目录下的子目录名）"""
    buckets_dir = get_scoop_base() / 'buckets'
    if not buckets_dir.is_dir():
        return []
    return [d.name for d in buckets_dir.iterdir() if d.is_dir()]

def find_matches(app_name):
    """
    从本地 bucket 中搜索包含 app_name 的应用（不区分大小写）。
    返回列表，每个元素为 (应用名, bucket, data, 版本, url)
    """
    matches = []
    app_lower = app_name.lower()
    for bucket in get_all_buckets():                     # 动态获取所有 bucket
        names = get_local_app_names(bucket)
        if not names:
            continue
        for name in names:
            if app_lower in name.lower():
                data = read_manifest(bucket, name)
                if data:
                    version, url = parse_manifest(data)
                    if url:
                        matches.append((name, bucket, data, version, url))
    return matches

def get_local_app_names(bucket):
    """从本地 bucket 目录读取所有应用名（返回列表）"""
    bucket_dir = get_scoop_base() / 'buckets' / bucket / 'bucket'
    if not bucket_dir.is_dir():
        return []
    return [p.stem for p in bucket_dir.glob('*.json')]

def read_manifest(bucket, name):
    """从本地 bucket 读取 manifest JSON 文件"""
    manifest_path = get_scoop_base() / 'buckets' / bucket / 'bucket' / f"{name}.json"
    if not manifest_path.is_file():
        return None
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

def parse_manifest(data):
    """从 manifest 提取版本和下载 URL（优先 64bit）"""
    version = data.get('version', '')
    url = None
    if 'architecture' in data and '64bit' in data['architecture']:
        url = data['architecture']['64bit'].get('url')
    if not url:
        url = data.get('url')
    if not url:
        for key in ['url', 'downloadUrl']:
            if key in data:
                url = data[key]
                break
    return version, url

def compute_url_hash(url):
    """计算 URL 的 SHA256 并返回前7位"""
    sha256 = hashlib.sha256(url.encode()).hexdigest()
    return sha256[:7]

def get_extension(url):
    """从 URL 提取扩展名，默认 .zip"""
    path = urlparse(url).path
    ext = os.path.splitext(path)[1]
    return ext if ext else '.zip'

def extract_filename_from_url(url):
    """从 URL 中提取文件名（忽略查询参数和锚点）"""
    if '#' in url:
        url = url.split('#')[0]
    path = urlparse(url).path
    filename = os.path.basename(path)
    return filename

def download_with_surge(url, dest_path):
    """使用 surge 下载文件，保存到 dest_path"""
    actual_url = url
    if MIRROR and url.startswith('https://github.com/'):
        actual_url = f"{MIRROR}/{url}"

    expected_filename = extract_filename_from_url(actual_url)
    tmp_dir = Path(tempfile.mkdtemp())
    try:
        cmd = [
            'surge',
            actual_url,
            '--output', str(tmp_dir),
            '--exit-when-done'
        ]
        print(f"正在调用 surge: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)

        downloaded_file = tmp_dir / expected_filename
        if not downloaded_file.exists():
            files = list(tmp_dir.iterdir())
            if len(files) == 1:
                downloaded_file = files[0]
            else:
                raise Exception(f"无法确定下载的文件，临时目录内容: {[f.name for f in files]}")

        shutil.move(str(downloaded_file), str(dest_path))
        return True
    except subprocess.CalledProcessError as e:
        print(f"surge 下载失败: {e}")
        return False
    except Exception as e:
        print(f"处理临时文件失败: {e}")
        return False
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

def find_matches(app_name):
    """
    从本地 bucket 中搜索包含 app_name 的应用（不区分大小写）。
    返回列表，每个元素为 (应用名, bucket, data, 版本, url)
    """
    matches = []
    app_lower = app_name.lower()
    for bucket in get_all_buckets():
        names = get_local_app_names(bucket)
        if not names:
            continue
        for name in names:
            if app_lower in name.lower():
                data = read_manifest(bucket, name)
                if data:
                    version, url = parse_manifest(data)
                    if url:
                        matches.append((name, bucket, data, version, url))
    return matches

def main():
    # 检查是否缺少必要参数
    if len(sys.argv) < 2:
        print("用法: sapp.py <应用名称>")
        print("示例: sapp.py git")
        print("说明: 支持部分匹配，如 'ollama' 会匹配 ollama 和 ollama-full")
        sys.exit(1)

    parser = argparse.ArgumentParser(
        description='Scoop 缓存下载器（surge 加速版）',
        usage='%(prog)s <应用名称>'
    )
    parser.add_argument('app', help='应用名称（支持部分匹配）')
    args = parser.parse_args()

    print(f"正在搜索应用 '{args.app}' ...")
    matches = find_matches(args.app)

    if not matches:
        print(f"错误: 未找到任何包含 '{args.app}' 的应用")
        print("提示: 请确保已添加对应的 bucket（如 main, extras）并运行过 scoop update")
        sys.exit(1)

    # 显示所有匹配项
    print(f"\n找到 {len(matches)} 个匹配项:")
    for idx, (name, bucket, data, version, url) in enumerate(matches, 1):
        print(f"  {idx}. {name} (bucket: {bucket}) 版本: {version}")
    print("  0 或 q. 取消")

    # 用户选择
    while True:
        try:
            choice = input("请选择要下载的编号: ").strip()
        except KeyboardInterrupt:
            print("\n用户取消")
            sys.exit(1)
        if not choice:
            continue
        # 检查取消
        if choice.lower() in ('0', 'q'):
            print("取消下载")
            sys.exit(0)
        try:
            idx = int(choice)
            if 1 <= idx <= len(matches):
                name, bucket, data, version, url = matches[idx-1]
                break
            else:
                print(f"请输入 1 到 {len(matches)} 之间的数字，或输入 0/q 取消")
        except ValueError:
            print("输入无效，请输入数字或 q 取消")

    # 生成缓存文件名
    hash7 = compute_url_hash(url)
    ext = get_extension(url)
    cache_filename = f"{name}#{version}#{hash7}{ext}"
    cache_dir = get_cache_dir()
    cache_path = cache_dir / cache_filename

    if cache_path.exists():
        print(f"文件已存在: {cache_path}")
        sys.exit(0)

    # 临时下载
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = Path(tmp.name)

    print("开始下载...")
    if download_with_surge(url, tmp_path):
        shutil.move(str(tmp_path), str(cache_path))
        print(f"保存成功: {cache_path}")
    else:
        print("下载失败")
        if tmp_path.exists():
            tmp_path.unlink()
        sys.exit(1)

if __name__ == '__main__':
    main()
