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
import msvcrt
from pathlib import Path
from urllib.parse import urlparse, urlsplit

# ==================== 配置 ====================
MIRROR = 'https://gh-proxy.com'

# ==================== 工具函数 ====================
def get_scoop_base():
    return Path(os.environ.get('SCOOP', Path.home() / 'scoop'))

def get_cache_dir():
    cache_dir = get_scoop_base() / 'cache'
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir

def get_all_buckets():
    buckets_dir = get_scoop_base() / 'buckets'
    if not buckets_dir.is_dir():
        return []
    return [d.name for d in buckets_dir.iterdir() if d.is_dir()]

def get_local_app_names(bucket):
    bucket_dir = get_scoop_base() / 'buckets' / bucket / 'bucket'
    if not bucket_dir.is_dir():
        return []
    return [p.stem for p in bucket_dir.glob('*.json')]

def read_manifest(bucket, name):
    manifest_path = get_scoop_base() / 'buckets' / bucket / 'bucket' / f"{name}.json"
    if not manifest_path.is_file():
        return None
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

def parse_manifest(data):
    """返回 (版本, 完整URL) ，URL包含可能的锚点"""
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

def split_url_fragment(url):
    """将URL拆分为 (基础URL, 锚点)，锚点可能为空"""
    parsed = urlsplit(url)
    base = parsed._replace(fragment='').geturl()
    fragment = parsed.fragment
    return base, fragment

def compute_url_hash(url):
    """计算完整URL的SHA256并返回前7位"""
    sha256 = hashlib.sha256(url.encode()).hexdigest()
    return sha256[:7]

def get_extension(url):
    """
    从 URL 提取扩展名，正确处理 #/ 锚点。
    如果 URL 包含 #/，则取锚点部分的扩展名（如 .msi_）。
    """
    if '#/' in url:
        fragment = url.split('#/')[-1]
        # 去掉可能的多余锚点
        if '#' in fragment:
            fragment = fragment.split('#')[0]
        ext = os.path.splitext(fragment)[1]
        if ext:
            return ext
    # 否则从路径中提取
    path = urlparse(url).path
    ext = os.path.splitext(path)[1]
    return ext if ext else '.zip'

def extract_filename_from_url(url):
    """
    从 URL 提取最终的文件名（考虑 #/ 锚点）。
    如果 URL 包含 #/，返回锚点指定的文件名（如 dl.msi_）；否则返回路径的最后一部分。
    """
    if '#/' in url:
        fragment = url.split('#/')[-1]
        if '#' in fragment:
            fragment = fragment.split('#')[0]
        return fragment
    # 去掉查询参数和锚点
    if '#' in url:
        url = url.split('#')[0]
    path = urlparse(url).path
    return os.path.basename(path)

def download_with_surge(url, dest_path):
    """
    使用 surge 下载文件，保存到 dest_path。
    正确处理 #/ 锚点：下载基础 URL，但用锚点指定的文件名保存。
    """
    # 分离基础 URL 和锚点
    base_url = url
    expected_filename = extract_filename_from_url(url)  # 获取期望的文件名（如 dl.msi_）
    if '#/' in url:
        base_url = url.split('#')[0]  # 去掉锚点部分
    actual_url = base_url
    if MIRROR and base_url.startswith('https://github.com/'):
        actual_url = f"{MIRROR}/{base_url}"

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

        # 查找下载的文件（可能名称与预期不同）
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

def sort_matches(matches):
    priority = {'main': 0, 'extras': 1}
    def key_func(item):
        bucket = item[1]
        return (priority.get(bucket, 2), bucket, item[0])
    return sorted(matches, key=key_func)

def select_match(matches):
    def print_menu(selected):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"找到 {len(matches)} 个匹配项，使用 ↑/↓ 选择，回车确认:")
        for i, (name, bucket, data, version, url) in enumerate(matches):
            prefix = " → " if i == selected else "   "
            print(f"{prefix}{i+1}. {name} (bucket: {bucket}) 版本: {version}")
        print("按 ESC 取消")

    selected = 0
    print_menu(selected)
    while True:
        key = msvcrt.getch()
        if key == b'\xe0':
            key = msvcrt.getch()
            if key == b'H':
                selected = (selected - 1) % len(matches)
                print_menu(selected)
            elif key == b'P':
                selected = (selected + 1) % len(matches)
                print_menu(selected)
        elif key == b'\r':
            return selected
        elif key == b'\x1b':
            return None
        elif key in (b'q', b'Q'):
            return None

def main():
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

    matches = sort_matches(matches)
    selected_idx = select_match(matches)
    if selected_idx is None:
        print("取消下载")
        sys.exit(0)

    name, bucket, data, version, url = matches[selected_idx]

    # 生成缓存文件名（使用 Python 手动计算，确保正确处理 #/ 锚点）
    hash7 = compute_url_hash(url)
    ext = get_extension(url)          # 现在会返回 .msi_
    cache_filename = f"{name}#{version}#{hash7}{ext}"
    cache_dir = get_cache_dir()
    cache_path = cache_dir / cache_filename

    if cache_path.exists():
        print(f"文件已存在: {cache_path}")
        sys.exit(0)

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
