
---

[![Scoop 版本](https://img.shields.io/github/v/release/ScoopInstaller/Scoop?label=Scoop)](https://github.com/ScoopInstaller/Scoop/releases/latest)

```
# Scoop 环境配置
SCOOP=E:\Scoop
设置后，运行以下二行命令会安装到环境变量指定的路径
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression

# 指定 Scoop 核心仓库的 Git 地址（可以是镜像源或自定义分支）
SCOOP_REPO=https://github.com/ScoopInstaller/Install 
SCOOP_REPO=https://ghfast.top/https://github.com/ScoopInstaller/Install
SCOOP_REPO=https://gitee.com/glsnames/scoop-installer
```
[Extras](https://github.com/ScoopInstaller/Extras) - [Main](https://github.com/ScoopInstaller/Main)

---

![Aria2 版本](https://img.shields.io/scoop/v/aria2?label=Aria2)
`scoop install aria2`

批量下载至CMD当前目录的路径 
—— [BA.bat](https://github.com/classronin/MyDocs/raw/refs/heads/main/Scripts/Aria2c/BA.bat)
```
ba https://.../10*.jpg   # 请输入网址模板 (使用 * 代替数字部分，如 https://.../10*.jpg)
01-21                    # 请输入数字范围 (格式如 01-21 )
```

---

![Surge 版本](https://img.shields.io/scoop/v/surge?label=Surge)
`scoop install surge`

批量下载至CMD当前目录的路径 
—— [BS.bat](https://github.com/classronin/MyDocs/raw/refs/heads/main/Scripts/Surge/BS.bat)
```
bs https://.../10*.jpg   # 请输入网址模板 (使用 * 代替数字部分，如 https://.../10*.jpg)
01-21                    # 请输入数字范围 (格式如 01-21 )
```
单文件下载，文件下载至CMD当前目录的路径 
—— [S.bat](https://github.com/classronin/MyDocs/raw/refs/heads/main/Scripts/Surge/S.bat)
```
s https://...zip   # 下载至CMD当前目录的路径
```


---
### CLI

[![最新 uv 版本](https://img.shields.io/github/v/release/astral-sh/uv?label=UV)](https://github.com/astral-sh/uv/releases/latest)
[![Windows 64位](https://img.shields.io/badge/Win64-blue)](https://github.com/astral-sh/uv/releases/latest/download/uv-x86_64-pc-windows-msvc.zip)

[![最新 python-build-standalone 版本](https://img.shields.io/github/v/release/astral-sh/python-build-standalone?label=Python)](https://github.com/astral-sh/python-build-standalone/releases/latest)
`uv python install 3.12`

[![最新Bun版本](https://img.shields.io/github/v/release/oven-sh/bun?label=Bun)](https://github.com/oven-sh/bun/releases/latest)
[![Windows 64位](https://img.shields.io/badge/Win64-blue)](https://github.com/oven-sh/bun/releases/latest/download/bun-windows-x64-baseline.zip)

[![最新 Deno 版本](https://img.shields.io/github/v/release/denoland/deno?label=Deno)](https://github.com/denoland/deno/releases/latest)
[![Windows 64位](https://img.shields.io/badge/Win64-blue)](https://github.com/denoland/deno/releases/latest/download/deno-x86_64-pc-windows-msvc.zip)

[![最新 Pixi 版本](https://img.shields.io/github/v/release/prefix-dev/pixi?label=Pixi)](https://github.com/prefix-dev/pixi/releases/latest)
[![Windows 64位](https://img.shields.io/badge/Win64-blue)](https://github.com/prefix-dev/pixi/releases/latest/download/pixi-x86_64-pc-windows-msvc.zip)

[![最新 pnpm 版本](https://img.shields.io/github/v/release/pnpm/pnpm?label=pnpm)](https://github.com/pnpm/pnpm/releases/latest)
[![Windows 64位](https://img.shields.io/badge/Win64-blue)](https://github.com/pnpm/pnpm/releases/latest/download/pnpm-win-x64.exe)

[![yt-dlp 版本](https://img.shields.io/github/v/release/yt-dlp/yt-dlp?label=yt-dlp)](https://github.com/yt-dlp/yt-dlp/releases/latest)
[![Windows 64位](https://img.shields.io/badge/Win64-blue)](https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp_win.zip)
`scoop install yt-dlp`

[![CMake 构建系统生成器](https://img.shields.io/github/v/release/Kitware/CMake?label=CMake-构建系统生成器)](https://github.com/Kitware/CMake/releases/latest)
`scoop install cmake`

[![fd 命令行搜索工具](https://img.shields.io/github/v/release/sharkdp/fd?label=fd-命令行搜索工具)](https://github.com/sharkdp/fd/releases/latest)
 `scoop install fd`   [中文文档](https://github.com/cha0ran/fd-zh?tab=readme-ov-file#command-line-options)

[![ImageMagick 命令行图像处理工具](https://img.shields.io/github/v/release/ImageMagick/ImageMagick?label=ImageMagick-命令行图像处理工具)](https://github.com/ImageMagick/ImageMagick/releases/latest)
`scoop install imagemagick` 

---

### 媒体处理工具

[![最新 FFmpeg 命令行音视频处理](https://img.shields.io/github/v/release/GyanD/codexffmpeg?label=FFmpeg-命令行音视频处理)](https://github.com/GyanD/codexffmpeg/releases/latest)
`scoop install ffmpeg`

[![HandBrake 视频转码](https://img.shields.io/github/v/release/HandBrake/HandBrake?label=HandBrake-视频转码)](https://github.com/HandBrake/HandBrake/releases/latest)
`scoop install HandBrake`

[![LosslessCut 无损剪辑](https://img.shields.io/github/v/release/mifi/lossless-cut?label=LosslessCut-无损剪辑)](https://github.com/mifi/lossless-cut/releases/latest)
[![Windows 64位](https://img.shields.io/badge/Win64-blue)](https://github.com/mifi/lossless-cut/releases/latest/download/LosslessCut-win-x64.7z)
`scoop install losslesscut`

[![最新 Shotcut 视频编辑](https://img.shields.io/github/v/release/mltframework/shotcut?label=Shotcut-视频编辑)](https://github.com/mltframework/shotcut/releases/latest)
`scoop install shotcut`

[![最新 Blender 3D建模含视频编辑](https://img.shields.io/github/v/tag/blender/blender?label=Blender-3D建模含视频编辑)](https://github.com/blender/blender/tags)
[下载](https://www.blender.org/download/)
`scoop install Blender`

[![MPV 视频播放器](https://img.shields.io/github/v/release/mpv-player/mpv?label=MPV-视频播放器)](https://github.com/mpv-player/mpv/releases/latest)


[![VLC 视频播放器](https://img.shields.io/github/v/tag/videolan/vlc?label=VLC-视频播放器)](https://github.com/videolan/vlc/tags)
`scoop install vlc`


---

### 浏览器

ungoogled-chromium 去谷歌化的浏览器
[![最新版本](https://img.shields.io/github/v/release/ungoogled-software/ungoogled-chromium-windows?label=Chromium)](https://github.com/ungoogled-software/ungoogled-chromium-windows/releases/latest)


Tor 浏览器
![Tor Browser 版本](https://img.shields.io/scoop/v/tor-browser?bucket=extras&label=Tor%20Browser)
`scoop install Tor-Browser`


---
### 应用程序

GIMP 图像编辑器
[![最新 GIMP 版本](https://img.shields.io/github/v/tag/GNOME/gimp?label=GIMP)](https://github.com/GNOME/gimp/tags)
[下载](https://www.gimp.org/downloads/)

Notepad++ 文本编辑器
[![最新 Notepad++ 版本](https://img.shields.io/github/v/release/notepad-plus-plus/notepad-plus-plus?label=Notepad%2B%2B)](https://github.com/notepad-plus-plus/notepad-plus-plus/releases/latest)
下载选npp.x.x.x.portable.x64.zip

Obsidian 知识笔记
[![最新 Obsidian 版本](https://img.shields.io/github/v/release/obsidianmd/obsidian-releases?label=Obsidian)](https://github.com/obsidianmd/obsidian-releases/releases/latest)
下载选Obsidian-x.x.x.exe

Logseq 日记笔记
[![最新 Logseq 版本](https://img.shields.io/github/v/release/logseq/logseq?label=Logseq)](https://github.com/logseq/logseq/releases/latest)
下载选Logseq-win-x64-x.x.x.zip

ShareX 截图与共享工具
[![最新 ShareX 版本](https://img.shields.io/github/v/release/ShareX/ShareX?label=ShareX)](https://github.com/ShareX/ShareX/releases/latest)
下载选ShareX-x.x.x-portable.zip

KeePassXC 密码管理器
[![最新 KeePassXC 版本](https://img.shields.io/github/v/release/keepassxreboot/keepassxc?label=KeePassXC)](https://github.com/keepassxreboot/keepassxc/releases/latest)
下载选KeePassXC-x.x.x-Win64.zip

JPEGView 图像浏览器
[![最新 JPEGView 版本](https://img.shields.io/github/v/release/sylikc/jpegview?label=JPEGView)](https://github.com/sylikc/jpegview/releases/latest)
Win64下载选JPEGView64_x.x.x.7z


[![LibreOffice版本](https://img.shields.io/github/v/tag/LibreOffice/core?label=LibreOffice-开源办公套件)](https://github.com/LibreOffice/core/tags)
[下载](https://zh-cn.libreoffice.org/download/libreoffice/)

[![最新 SumatraPDF 版本](https://img.shields.io/github/v/release/sumatrapdfreader/sumatrapdf?label=SumatraPDF-PDF阅读器)](https://github.com/sumatrapdfreader/sumatrapdf/releases/latest)
`scoop install SumatraPDF`

![RapidEE](https://img.shields.io/scoop/v/rapidee?bucket=extras&label=RapidEE-环境变量工具)
`scoop install RapidEE`

---
### AI

[![最新 Ollama 版本](https://img.shields.io/github/v/release/ollama/ollama?label=Ollama)](https://github.com/ollama/ollama/releases/latest)
[![下载 Ollama for Windows](https://img.shields.io/badge/Win64-blue)](https://github.com/ollama/ollama/releases/latest/download/OllamaSetup.exe)


[![最新 ComfyUI 版本](https://img.shields.io/github/v/release/Comfy-Org/ComfyUI?label=ComfyUI)](https://github.com/Comfy-Org/ComfyUI/releases/latest)


[![最新 open-webui 版本](https://img.shields.io/github/v/release/open-webui/open-webui?label=open-webui)](https://github.com/open-webui/open-webui/releases/latest)


[![最新 text-generation-webui 版本](https://img.shields.io/github/v/release/oobabooga/text-generation-webui?label=text-generation-webui)](https://github.com/oobabooga/text-generation-webui/releases/latest)


---
### Python库

Gradio 交互界面库
[![最新 gradio 版本](https://img.shields.io/github/v/release/gradio-app/gradio?label=gradio)](https://github.com/gradio-app/gradio/releases/latest)


Chroma 向量数据库
[![最新 chroma 版本](https://img.shields.io/github/v/release/chroma-core/chroma?label=chroma)](https://github.com/chroma-core/chroma/releases/latest)


Zensical 现代静态网站生成器
[![最新 zensical 版本](https://img.shields.io/github/v/release/zensical/zensical?label=Zensical)](https://github.com/zensical/zensical/releases/latest)


Hugging Face Hub  交互，支持模型、数据集、空间的上传、下载与管理。
`
uv pip install huggingface_hub huggingface_hub[hf_xet] hf_xet
`
[![最新 huggingface_hub 版本](https://img.shields.io/github/v/release/huggingface/huggingface_hub?label=huggingface_hub)](https://github.com/huggingface/huggingface_hub/releases/latest)


JupyterLab 基于 Web 的交互式开发环境，支持多文档、可扩展的笔记本、代码控制台与文件管理，是 Jupyter Notebook 的下一代界面。
[![最新 jupyterlab 版本](https://img.shields.io/github/v/release/jupyterlab/jupyterlab?label=jupyterlab)](https://github.com/jupyterlab/jupyterlab/releases/latest)



