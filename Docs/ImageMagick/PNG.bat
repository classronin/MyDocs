@echo off
if "%~1"=="" (
    echo 用法: png ^<动作^> [文件...]
    echo 示例: png 右旋 1.jpg
    echo       png 批量
    exit /b 1
)
uv run --project "%SCRIPTS%\im" python "%SCRIPTS%\im\im.py" png %*
