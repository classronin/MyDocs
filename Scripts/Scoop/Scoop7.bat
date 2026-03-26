@echo off
if "%1"=="" (
    echo 用法: a.bat URL
    exit /b 1
)

set "url=%1"
set "tempfile=%temp%\url_%RANDOM%.txt"

:: 将 URL 写入临时文件（不带换行符）
<nul set /p "=%url%" > "%tempfile%" 2>nul

:: 计算 SHA256
set "hashline="
for /f "skip=1 tokens=*" %%i in ('certutil -hashfile "%tempfile%" SHA256 2^>nul') do (
    if not defined hashline set "hashline=%%i"
)

:: 删除临时文件
del "%tempfile%" 2>nul

:: 检查是否获取到哈希值
if not defined hashline (
    echo 错误：无法获取 SHA256，请检查 URL 或 certutil 是否可用。
    exit /b 1
)

:: 去除可能的前导空格或控制字符
for /f "tokens=*" %%a in ("%hashline%") do set "hashline=%%a"

:: 输出前 7 位
set "hash7=%hashline:~0,7%"
if "%hash7%"=="" (
    echo 错误：哈希值长度不足 7 位。
    exit /b 1
)
echo %hash7%
