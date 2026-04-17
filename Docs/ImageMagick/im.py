# im.py
import sys
import subprocess
import shutil
import re
from pathlib import Path

# --- 中文映射 (保持不变) ---
ACTION_MAP = {
    "右旋": ("rotate", 90),
    "右": ("rotate", 90),
    "左旋": ("rotate", -90),
    "左": ("rotate", -90),
    "左右翻转": ("flop", None),
    "左右": ("flop", None),
    "上下翻转": ("flip", None),
    "上下": ("flip", None),
    "批量": ("batch", None),
    "批": ("batch", None),
    "转换": (None, None),
    "转": (None, None),
}

# 常见图片扩展名
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif', '.tiff', '.tif'}


def find_imagemagick_cmd():
    """查找可用的 ImageMagick 命令。优先 magick，其次 convert。"""
    if shutil.which("magick"):
        return "magick"
    if shutil.which("convert"):
        return "convert"
    print("[!] 错误: 未找到 ImageMagick 命令 (magick 或 convert)。")
    print("     请安装 ImageMagick 并将其添加到系统 PATH 环境变量。")
    sys.exit(1)


IM_CMD = find_imagemagick_cmd()


def parse_size(size_str: str):
    """
    解析尺寸描述，返回 ImageMagick 的 -resize 参数字符串。
    支持格式：
      - 纯数字：500          → "500"
      - 宽度缩写：500x       → "500"
      - 高度缩写：x500       → "x500"
      - 固定盒子：500x800    → "500x800"
      - 中文宽度：宽500      → "500"
      - 中文高度：高500      → "x500"
    若无法解析则返回 None。
    """
    size_str = size_str.strip()
    # 纯数字
    if size_str.isdigit():
        return size_str
    # 500x800 格式
    if re.match(r'^\d+x\d+$', size_str):
        return size_str
    # 500x 格式
    if re.match(r'^\d+x$', size_str):
        return size_str.rstrip('x')
    # x500 格式
    if re.match(r'^x\d+$', size_str):
        return size_str
    # 宽 / 宽度
    m = re.match(r'^(宽|宽度)(\d+)$', size_str)
    if m:
        return m.group(2)
    # 高 / 高度
    m = re.match(r'^(高|高度)(\d+)$', size_str)
    if m:
        return f"x{m.group(2)}"
    return None


def get_unique_filepath(directory: Path, stem: str, ext: str, source_path: Path = None) -> Path:
    """
    生成不冲突的文件路径。
    """
    base_candidate = directory / f"{stem}.{ext}"
    if not base_candidate.exists():
        if source_path and base_candidate == source_path:
            pass
        else:
            return base_candidate

    n = 0
    while True:
        candidate = directory / f"{stem}-{n}.{ext}"
        if not candidate.exists():
            if source_path and candidate == source_path:
                n += 1
                continue
            print(f"[WARN] 文件已存在: {base_candidate.name}，改为输出: {candidate.name}")
            return candidate
        n += 1


def get_unique_out_dir(base_dir: Path, prefix="out") -> Path:
    """批量模式：创建 out-N 目录，自动递增。"""
    n = 0
    while True:
        candidate = base_dir / f"{prefix}-{n}"
        if not candidate.exists():
            candidate.mkdir(parents=True, exist_ok=True)
            print(f"[+] 创建输出目录: {candidate.name}")
            return candidate
        n += 1


def build_imagemagick_args(input_path: Path, output_path: Path,
                           action_type: str, action_val, size_spec: str = None):
    """
    构建 ImageMagick 命令参数。
    内部顺序固定为：输入 → 旋转/翻转 → 缩放 → 输出。
    """
    args = [IM_CMD, str(input_path)]

    # 1. 旋转/翻转
    if action_type == "rotate":
        args.extend(["-rotate", str(action_val)])
    elif action_type == "flop":
        args.append("-flop")
    elif action_type == "flip":
        args.append("-flip")

    # 2. 缩放
    if size_spec:
        args.extend(["-resize", size_spec])

    args.append(str(output_path))
    return args


def run_imagemagick(input_path: Path, output_path: Path,
                    action_type: str, action_val, size_spec: str = None):
    """执行 ImageMagick 命令，返回 (success, error_message)。"""
    cmd_args = build_imagemagick_args(input_path, output_path, action_type, action_val, size_spec)
    try:
        result = subprocess.run(
            cmd_args,
            capture_output=True,
            text=True,
            check=False,
            timeout=30
        )
        if result.returncode != 0:
            return False, result.stderr.strip()
        return True, None
    except subprocess.TimeoutExpired:
        return False, "命令执行超时"
    except Exception as e:
        return False, str(e)


def process_single_file(fname: str, fmt: str, action_type: str, action_val, size_spec: str = None):
    """处理单个文件，输出到当前目录。"""
    fpath = Path(fname)
    if not fpath.is_absolute():
        fpath = Path.cwd() / fpath

    if not fpath.exists():
        print(f"[!] 错误: 找不到 {fname}")
        return

    out_dir = Path.cwd()
    stem = fpath.stem
    source_ref = fpath if fpath.suffix.lower() == f".{fmt}" else None
    out_file = get_unique_filepath(out_dir, stem, fmt, source_path=source_ref)

    success, error = run_imagemagick(fpath, out_file, action_type, action_val, size_spec)
    if success:
        print(f"[OK] {fname} -> {out_file.name}")
    else:
        print(f"[!] 处理失败 {fname}: {error}")


def process_batch(fmt: str, action_type: str = None, action_val=None, size_spec: str = None):
    """批量处理当前目录所有图片，不递归。"""
    cwd = Path.cwd()
    out_dir = get_unique_out_dir(cwd)

    files = [f for f in cwd.iterdir() if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS]

    if not files:
        print("[!] 当前目录下没有找到可处理的图像文件。")
        try:
            out_dir.rmdir()
        except:
            pass
        return

    action_desc = f" + {action_type}" if action_type else ""
    size_desc = f" + 缩放 {size_spec}" if size_spec else ""
    print(f"[*] 发现 {len(files)} 个文件，批量转换为 {fmt}{action_desc}{size_desc} ...")
    print(f"[*] 输出目录: {out_dir}")

    for f in files:
        try:
            stem = f.stem
            out_file = get_unique_filepath(out_dir, stem, fmt, source_path=None)
            success, error = run_imagemagick(f, out_file, action_type, action_val, size_spec)
            if success:
                print(f"[OK] {f.name} -> {out_file.name}")
            else:
                print(f"[!] 跳过 {f.name}: {error}")
        except Exception as e:
            print(f"[!] 跳过 {f.name}: {e}")


def main():
    args = sys.argv[1:]

    if len(args) < 2:
        print("用法: im.py <格式> <动作|批量> [文件|动作]")
        print("示例: im.py png 右旋 1.jpg")
        print("      im.py png 批量")
        print("      im.py png 批量 右旋")
        print("      im.py png 500 1.webp")
        print("      im.py jpg 500x photo.png")
        print("      im.py webp x500 photo.jpg")
        sys.exit(1)

    fmt = args[0].lower()

    # 参数分类扫描
    batch_mode = False
    action_type = None
    action_val = None
    size_spec = None
    files = []

    i = 1
    while i < len(args):
        arg = args[i]

        # 批量关键词
        if arg in ("批量", "批"):
            batch_mode = True
            i += 1
            continue

        # 动作词
        if arg in ACTION_MAP:
            a_type, a_val = ACTION_MAP[arg]
            if a_type != "batch":
                if action_type is not None:
                    print(f"[WARN] 检测到多个动作，将使用最后一个: {arg}")
                action_type = a_type
                action_val = a_val
                i += 1
                continue

        # 尺寸描述（包含纯数字、500x、x500、宽500等）
        parsed = parse_size(arg)
        if parsed is not None:
            if size_spec is not None:
                print(f"[WARN] 检测到多个尺寸参数，将覆盖为: {arg}")
            size_spec = parsed
            i += 1
            continue

        # 其余视为文件
        files.append(arg)
        i += 1

    # 执行处理
    if batch_mode:
        process_batch(fmt, action_type, action_val, size_spec)
    else:
        if not files:
            print("[!] 请指定要处理的文件。")
            print("示例: png 右旋 1.jpg")
            sys.exit(1)
        for fname in files:
            process_single_file(fname, fmt, action_type, action_val, size_spec)


if __name__ == "__main__":
    main()
