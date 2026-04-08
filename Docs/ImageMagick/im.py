# im.py
import sys
import os
from pathlib import Path
from wand.image import Image

# --- 中文映射 ---
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
}

# 常见图片扩展名
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif', '.tiff', '.tif'}

def get_unique_out_file(base_dir: Path, fmt: str, prefix="out") -> Path:
    """
    单文件模式：获取唯一的 out-N.<fmt> 文件路径。
    逻辑：从 0 开始递增，找到不存在的文件名。
    例如：out-0.png, out-1.png, ...
    严禁创建文件夹！
    """
    n = 0
    while True:
        candidate = base_dir / f"{prefix}-{n}.{fmt}"
        if not candidate.exists():
            return candidate
        n += 1

def get_unique_out_dir(base_dir: Path, prefix="out") -> Path:
    """
    批量模式：创建 out-N 目录，N 自动递增。
    逻辑：从 0 开始尝试，直到找到不存在的目录名。
    严禁 out-0-0 这种字符串拼接错误！
    """
    n = 0
    while True:
        candidate = base_dir / f"{prefix}-{n}"
        if not candidate.exists():
            candidate.mkdir(parents=True, exist_ok=True)
            print(f"[+] 创建输出目录: {candidate.name}")
            return candidate
        n += 1

def apply_action(img, action_type, action_val):
    """应用 Wand 操作"""
    if action_type == "rotate":
        img.rotate(action_val)
    elif action_type == "flop":
        img.flop()
    elif action_type == "flip":
        img.flip()
    # 如果 action_type 为 None，不执行任何操作

def process_single_file(fname: str, fmt: str, action_type: str, action_val):
    """
    处理单个文件，输出为 out-N.<fmt>。
    """
    fpath = Path(fname)
    if not fpath.is_absolute():
        fpath = Path.cwd() / fpath
    
    if not fpath.exists():
        print(f"[!] 错误: 找不到 {fname}")
        return
    
    try:
        with Image(filename=str(fpath)) as img:
            apply_action(img, action_type, action_val)
            img.format = fmt
            
            out_file = get_unique_out_file(Path.cwd(), fmt)
            img.save(filename=str(out_file))
            print(f"[OK] {fname} -> {out_file.name}")
            
    except Exception as e:
        print(f"[!] 处理失败 {fname}: {e}")

def process_batch(fmt: str, action_type: str = None, action_val = None):
    """
    批量处理当前目录所有图片，不递归。
    支持可选的动作参数。
    创建 out-N 文件夹，输出所有转换后的文件。
    """
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
    print(f"[*] 发现 {len(files)} 个文件，批量转换为 {fmt}{action_desc} ...")
    
    for f in files:
        try:
            with Image(filename=str(f)) as img:
                apply_action(img, action_type, action_val)
                img.format = fmt
                out_file = out_dir / f"{f.stem}.{fmt}"
                img.save(filename=str(out_file))
                print(f"[OK] {f.name}")
        except Exception as e:
            print(f"[!] 跳过 {f.name}: {e}")

def main():
    args = sys.argv[1:]
    
    if len(args) < 2:
        print("用法: im.py <格式> <动作|批量> [文件|动作]")
        print("示例: im.py png 右旋 1.jpg")
        print("      im.py png 批量")
        print("      im.py png 批量 右旋")
        sys.exit(1)

    fmt = args[0].lower()
    cmd = args[1]
    
    if cmd not in ACTION_MAP:
        print(f"[!] 未知命令: {cmd}")
        print(f"可用命令: {', '.join(ACTION_MAP.keys())}")
        sys.exit(1)
    
    action_type, action_val = ACTION_MAP[cmd]
    
    # 批量模式
    if action_type == "batch":
        # 检查是否有后续动作参数
        batch_action_type = None
        batch_action_val = None
        
        if len(args) >= 3:
            batch_cmd = args[2]
            if batch_cmd in ACTION_MAP:
                ba_type, ba_val = ACTION_MAP[batch_cmd]
                if ba_type != "batch":  # 不能嵌套批量
                    batch_action_type = ba_type
                    batch_action_val = ba_val
            else:
                print(f"[!] 未知动作: {batch_cmd}")
                sys.exit(1)
        
        process_batch(fmt, batch_action_type, batch_action_val)
        return

    # 单文件模式（支持多文件）
    files = args[2:]
    if not files:
        print("[!] 请指定要处理的文件。")
        print("示例: png 右旋 1.jpg")
        sys.exit(1)
    
    for fname in files:
        process_single_file(fname, fmt, action_type, action_val)

if __name__ == "__main__":
    main()
