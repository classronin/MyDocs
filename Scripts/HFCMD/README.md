

HFCMD – Hugging Face 命令行下载器

HFCMD 是一个简单易用的命令行工具，用于从 Hugging Face Hub 下载模型文件或整个模型仓库。它提供了交互式菜单界面，支持单个文件下载和完整模型下载，并可自定义保存目录与并发线程数。

功能特点

✅ 交互式菜单，操作简单

✅ 支持下载单个文件（任意文件）

✅ 支持下载整个模型仓库（自动递归所有文件）

✅ 可指定本地保存目录

✅ 可设置并发线程数（加快下载速度）

✅ 自动创建目录，处理常见错误

✅ 友好的输出提示（使用 rich 库，若未安装则自动降级）




安装依赖 
[![最新 huggingface_hub 版本](https://img.shields.io/github/v/release/huggingface/huggingface_hub?label=huggingface_hub)](https://github.com/huggingface/huggingface_hub/releases/latest)

```
uv pip install huggingface_hub[hf_xet] rich
```
运行
```
uv run HFCMD.py
```

启动后会出现主菜单

─────────────────────────────────────────────────

Hugging Face 下载器菜单

─────────────────────────────────────────────────

1. 下载单个文件
2. 下载完整模型
3. 退出
   
─────────────────────────────────────────────────

HFCMD.bat
```
@echo off
cd /d "%SCRIPTS%\HFCMD"
uv run HFCMD.py
```

