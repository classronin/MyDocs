


# 🖼️ IM - 图像处理工具

基于 **ImageMagick + Wand** 的命令行图像处理工具。支持中文指令、自动递增输出、批量处理。

## 📦 安装依赖

```bash
# 1. 安装 ImageMagick 和 uv
scoop install imagemagick
scoop install uv

# 2. 初始化 Python 环境与依赖
cd /d E:\Env\Scripts\im
uv python install 3.12
uv add wand
```
📂 目录结构
```
E:\Env\Scripts\im\
├── im.py           # 核心逻辑脚本
├── pyproject.toml  # uv 项目配置
├── .venv\          # 虚拟环境
└── png.bat         # 入口脚本 (可复制为 jpg.bat/webp.bat)
```

🚀 快速使用
💡 提示：确保 png.bat 所在目录已加入系统 PATH，或在脚本目录运行。

✅ 单文件处理
逻辑：生成 out-N.png 文件，不创建文件夹，文件名自动递增。
```
png 右 1.jpg          # 生成 out-0.png (右旋90度)
png 左 2.jpg          # 生成 out-1.png (左旋90度)
png 左右 1.jpg        # 生成 out-2.png (左右翻转)
```

✅ 批量处理
逻辑：创建 out-N/ 文件夹，自动递增，不递归子目录。
```
png 批量              # 仅转换格式 → out-0/
png 批量 右           # 转换 + 右旋 → out-1/
png 批量 左右         # 转换 + 翻转 → out-2/
```

🧭 中文命令映射
## 🧭 中文命令映射

| 命令   | 别名 | 操作         | 说明   |
|--------|------|--------------|--------|
| 右旋   | 右   | `rotate 90`  | 顺时针 |
| 左旋   | 左   | `rotate -90` | 逆时针 |
| 左右翻转 | 左右 | `flop`       | 水平镜像 |
| 上下翻转 | 上下 | `flip`       | 垂直镜像 |
| 批量   | -    | `batch`      | 批量模式 |


🔧 扩展格式支持
复制 png.bat 并重命名即可支持其他格式：
```
copy png.bat jpg.bat
copy png.bat webp.bat
```
使用方式完全一致：
```
jpg 右 1.png      # 生成 out-N.jpg
webp 批量 上下    # 生成 out-N/ 内含 webp 文件
```

⚠️ 注意事项
out-N 递增规则：单文件检测 out-N.png，批量检测 out-N/ 文件夹。

基于数字递增，绝不产生 out-0-0 等错误。

路径处理：bat 使用 uv run --project 确保环境正确，同时保持当前工作目录不变。

可在任意目录调用，输出始终在当前目录。

错误处理：文件不存在时提示 [!] 错误: 找不到 xxx，不中断其他文件处理。


