@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

if "%1"=="" goto :batch

echo "%1" | find "*" >nul
if not errorlevel 1 goto :batch_with_url

:single
set "url=%1"
echo "%url%" | find "github.com" >nul
if not errorlevel 1 set "url=%url:https://github.com/=https://ghfast.top/https://github.com/%"
wget2 "%url%"
exit /b

:batch_with_url
set "url_template=%1"
goto :after_url

:batch
set /p "url_template=请输入网址模板 (使用 * 代替数字): "

:after_url
echo "%url_template%" | find "*" >nul
if errorlevel 1 (
    echo 错误：网址模板必须包含 *
    exit /b 1
)

set /p "range=请输入数字范围 (格式如 01-21): "
for /f "tokens=1,2 delims=-" %%a in ("%range%") do (
    set start_str=%%a
    set end_str=%%b
)
if "%end_str%"=="" (
    echo 范围格式错误
    exit /b 1
)

set start_str=%start_str: =%
set end_str=%end_str: =%

set len=0
set "num=%start_str%"
:count_len
if not "%num%"=="" (
    set num=%num:~1%
    set /a len+=1
    goto count_len
)

set /a start_num=%start_str% 2>nul
set /a end_num=%end_str% 2>nul
if %start_num% gtr %end_num% (
    echo 起始数字不能大于结束数字
    exit /b 1
)

for /f "tokens=1,* delims=*" %%a in ("%url_template%") do (
    set url_prefix=%%a
    set url_suffix=%%b
)

set "file_list=%temp%\urls_%random%.txt"
if exist "%file_list%" del "%file_list%"

for /l %%i in (%start_num%,1,%end_num%) do (
    set padded_num=%%i
    if %len% equ 2 if %%i lss 10 set padded_num=0%%i
    if %len% equ 3 (
        if %%i lss 10 (set padded_num=00%%i) else if %%i lss 100 set padded_num=0%%i
    )
    if %len% equ 4 (
        if %%i lss 10 (set padded_num=000%%i) else if %%i lss 100 (set padded_num=00%%i) else if %%i lss 1000 set padded_num=0%%i
    )
    echo !url_prefix!!padded_num!!url_suffix! >> "%file_list%"
)

wget2 -i "%file_list%" --continue --tries=5 --progress=bar
del "%file_list%" 2>nul
exit /b
