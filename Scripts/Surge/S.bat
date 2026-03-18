@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

rem 检查是否提供了URL参数
if "%1"=="" (
    echo 错误：请提供下载网址
    echo.
    echo 用法：surge ^<URL^>
    echo 示例：surge https://example.com/file.jpg
    echo.
    pause
    exit /b 1
)

rem 获取当前目录
set "current_dir=%cd%"

rem 检查surge是否可用
where surge >nul 2>nul
if errorlevel 1 (
    echo Surge 未找到，尝试在当前目录运行...
    if not exist "surge.exe" (
        echo 错误：找不到 surge.exe
        echo 请将 surge.exe 放在本脚本同目录下，或添加到系统PATH中。
        pause
        exit /b 1
    )
    set "surge_cmd=surge.exe"
) else (
    set "surge_cmd=surge"
)

rem 显示简洁信息
echo 下载: %1
echo 保存到: %current_dir%
echo.

!surge_cmd! "%1" --output "%current_dir%" --exit-when-done

if errorlevel 1 (
    echo.
    echo 下载失败：%1
    pause
    exit /b 1
)
