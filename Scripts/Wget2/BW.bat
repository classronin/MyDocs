@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ============================================
echo     批量下载工具 (使用 wget2)
echo ============================================
echo.

rem 处理命令行参数：如果提供了第一个参数，则作为网址模板
if not "%1"=="" (
    set "url_template=%~1"
    rem 验证模板是否包含 *
    echo "!url_template!" | find "*" >nul
    if errorlevel 1 (
        echo 错误：网址模板必须包含 * 号作为数字占位符。
        echo 用法：%~nx0 "网址模板"
        exit /b 1
    )
    goto after_url_input
)

:input_url
set /p "url_template=请输入网址模板 (使用 * 代替数字部分，如 https://.../10*.jpg): "
if "!url_template!"=="" (
    echo 输入不能为空，请重新输入。
    goto input_url
)
echo "!url_template!" | find "*" >nul
if errorlevel 1 (
    echo 错误：网址模板中必须包含 * 号作为数字占位符！请重新输入。
    goto input_url
)

:after_url_input
echo 当前网址模板: !url_template!
echo.

:input_range
set /p "range=请输入数字范围 (格式如 01-21 ): "
if "!range!"=="" (
    echo 输入不能为空，请重新输入。
    goto input_range
)

rem 解析起始和结束数字
for /f "tokens=1,2 delims=-" %%a in ("!range!") do (
    set start_str=%%a
    set end_str=%%b
)

rem 检查输入是否有效
if "!end_str!"=="" (
    echo 范围格式错误，请使用如 01-21 的格式。
    goto input_range
)

rem 去除可能的前导空格
set start_str=!start_str: =!
set end_str=!end_str: =!

rem 获取数字的位数
set len=0
set "num=!start_str!"

:count_len
if not "!num!"=="" (
    set num=!num:~1!
    set /a len+=1
    goto count_len
)

if !len! equ 0 (
    echo 无法确定数字位数，请确保起始数字如 01 或 1 的格式。
    goto input_range
)

echo.
echo 开始解析下载任务...
echo 网址模板: !url_template!
echo 数字范围: !start_str! 到 !end_str! (位数: !len!)
echo.

rem 将字符串转换为数字进行比较
set /a start_num=!start_str! 2>nul
set /a end_num=!end_str! 2>nul

rem 检查转换是否成功（如果数字有前导0，批处理会当作八进制，需要特殊处理）
if !start_num! gtr !end_num! (
    echo 错误：起始数字不能大于结束数字。
    goto input_range
)

rem 分割网址模板为前缀和后缀
for /f "tokens=1,* delims=*" %%a in ("!url_template!") do (
    set "url_prefix=%%a"
    set "url_suffix=%%b"
)

if "!url_suffix!"=="" (
    echo 错误：网址模板中必须包含 * 号作为数字占位符！
    goto input_range
)

rem 生成下载链接列表并调用 wget2
set "file_list=temp_urls_!random!.txt"
if exist !file_list! del !file_list!

echo 正在生成下载链接...

for /l %%i in (!start_num!,1,!end_num!) do (
    rem 获取当前数字
    set "current_num=%%i"
    
    rem 补前导零
    set "padded_num=!current_num!"
    if !len! equ 2 (
        if !current_num! lss 10 set "padded_num=0!current_num!"
    )
    if !len! equ 3 (
        if !current_num! lss 10 set "padded_num=00!current_num!"
        if !current_num! geq 10 if !current_num! lss 100 set "padded_num=0!current_num!"
    )
    if !len! equ 4 (
        if !current_num! lss 10 set "padded_num=000!current_num!"
        if !current_num! geq 10 if !current_num! lss 100 set "padded_num=00!current_num!"
        if !current_num! geq 100 if !current_num! lss 1000 set "padded_num=0!current_num!"
    )
    
    rem 拼接完整的URL
    set "full_url=!url_prefix!!padded_num!!url_suffix!"
    
    rem 将 URL 写入临时文件
    echo !full_url! >> !file_list!
    echo 已添加: !full_url!
)

echo.
echo 正在调用 wget2 进行下载...
echo.

rem 显示将要下载的文件列表
echo 下载列表：
type !file_list!
echo.
echo 开始下载...

rem 检查wget2是否可用
where wget2 >nul 2>nul
if errorlevel 1 (
    echo wget2 未找到，尝试在当前目录运行...
    if not exist "wget2.exe" (
        echo 错误：找不到 wget2.exe
        echo 请将 wget2.exe 放在本脚本同目录下，或添加到系统PATH中。
        goto cleanup
    )
    set "wget2_cmd=wget2.exe"
) else (
    set "wget2_cmd=wget2"
)

rem 调用 wget2 进行下载
!wget2_cmd! -i "!file_list!" --continue --tries=5 --progress=bar

if errorlevel 1 (
    echo.
    echo wget2 执行失败，返回错误码：!errorlevel!
) else (
    echo.
    echo 下载完成。
)

:cleanup
rem 清理临时文件
if exist !file_list! del !file_list!

rem 脚本结束
