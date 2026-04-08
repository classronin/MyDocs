@echo off
setlocal

:: 配置脚本根目录
set "SCRIPT_ROOT=E:\Env\Scripts\im"

:: 检查参数
if "%~1"=="" (
    echo [!] 用法: png ^<动作^> [文件...]
    echo 示例: png 右旋 1.jpg
    echo       png 批量
    exit /b 1
)

:: --- 核心修正 ---
:: 使用 --project 指定 uv 的项目目录，这样 uv 能找到 .venv
:: 但不会改变当前 CMD 的工作目录！
:: Python 脚本会在你当前所在的目录运行，完美解决路径问题 ??
uv run --project "%SCRIPT_ROOT%" python "%SCRIPT_ROOT%\im.py" png %*

endlocal
