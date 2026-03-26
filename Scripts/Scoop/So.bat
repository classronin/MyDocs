@echo off
setlocal enabledelayedexpansion

if "%1"=="" (
    echo 用法: %~nx0 ^<应用名^>
    echo 示例: %~nx0 surge
    echo 示例: %~nx0 ollama
    exit /b 1
)

:: 检查 curl 是否存在
where curl >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到 curl 命令
    echo 请先安装 curl，例如通过 Scoop: scoop install curl
    echo 或从 https://curl.se/windows/ 下载并添加到 PATH
    exit /b 1
)

set "ORIG_APP=%1"
set "BUCKETS=main extras"
set "BASE_URL=https://raw.githubusercontent.com/ScoopInstaller"
set "TEMP_DIR=%temp%\scoop_search_%ORIG_APP%"
set "TIMEOUT=5"               :: 单个 URL 的超时秒数

:: 镜像列表（顺序决定尝试优先级，第一个是原始地址，后续是镜像）
set "MIRRORS=https://gh-proxy.com/%BASE_URL%"

:: 创建临时目录
if not exist "%TEMP_DIR%" mkdir "%TEMP_DIR%"

:: 别名映射（自动扩展搜索）
set "ALIAS.ollama=ollama-full"

:: 构建要搜索的名称列表（原始名称 + 别名）
set "SEARCH_NAMES=%ORIG_APP%"
if defined ALIAS.%ORIG_APP% set "SEARCH_NAMES=!SEARCH_NAMES! !ALIAS.%ORIG_APP%!"

echo ==========================================
echo 正在搜索应用: %ORIG_APP%
echo 将检查以下名称: %SEARCH_NAMES%
echo ==========================================

:: 遍历每个 bucket 和每个可能的名称
set "RESULT_COUNT=0"
for %%b in (%BUCKETS%) do (
    for %%n in (%SEARCH_NAMES%) do (
        set "REL_PATH=%%b/master/bucket/%%n.json"
        set "TEMP_JSON=%TEMP_DIR%\%%b_%%n.json"
        
        :: 尝试使用不同镜像下载
        call :download_manifest "!REL_PATH!" "!TEMP_JSON!"
        if !errorlevel! equ 0 (
            set /a RESULT_COUNT+=1
            echo [信息] 在 %%b bucket 中找到 %%n
            call :display_result "%%n" "%%b" "!TEMP_JSON!"
        )
    )
)

if %RESULT_COUNT% equ 0 (
    echo.
    echo [错误] 未找到任何匹配 "%ORIG_APP%" 的应用
    echo 已搜索的 bucket: %BUCKETS%
) else (
    echo.
    echo ==========================================
    echo 共找到 %RESULT_COUNT% 个匹配结果
    echo ==========================================
)

:: 清理临时目录
rd /s /q "%TEMP_DIR%" 2>nul
pause
endlocal
exit /b

:: ========== 下载 manifest，支持镜像切换 ==========
:download_manifest
set "REL_PATH=%~1"
set "OUT_FILE=%~2"
set "SUCCESS=0"

:: 遍历镜像列表
for %%m in (%MIRRORS%) do (
    set "FULL_URL=%%m/!REL_PATH!"
    :: 使用 curl 下载，超时 TIMEOUT 秒
    curl -s --connect-timeout %TIMEOUT% --max-time %TIMEOUT% -o "!OUT_FILE!" "!FULL_URL!" 2>nul
    if exist "!OUT_FILE!" (
        for %%s in ("!OUT_FILE!") do if %%~zs neq 0 (
            findstr /i /c:"\"url\"" "!OUT_FILE!" >nul 2>&1
            if !errorlevel! equ 0 (
                set "SUCCESS=1"
                goto :download_done
            )
        )
        :: 文件无效（空或不含 url），删除
        del "!OUT_FILE!" 2>nul
    )
)
:download_done
if %SUCCESS% equ 0 exit /b 1
exit /b 0

:: ========== 显示单个结果 ==========
:display_result
set "APPNAME=%~1"
set "BUCKET=%~2"
set "JSON_FILE=%~3"

:: 提取版本号
set "VERSION="
for /f "usebackq delims=" %%a in ("%JSON_FILE%") do (
    set "line=%%a"
    for /f "tokens=*" %%b in ("!line!") do set "line=%%b"
    echo !line! | findstr /i /c:"\"version\"" >nul
    if !errorlevel! equ 0 (
        set "line=!line:*"version" =!"
        set "line=!line:*:=!"
        set "line=!line: =!"
        set "line=!line:"=!"
        set "line=!line:,=!"
        set "VERSION=!line!"
        goto :version_done
    )
)
:version_done

:: 提取64位下载网址
set "URL="
set "IN_64BIT=0"
for /f "usebackq delims=" %%a in ("%JSON_FILE%") do (
    set "line=%%a"
    for /f "tokens=*" %%b in ("!line!") do set "line=%%b"
    if !IN_64BIT! equ 1 (
        echo !line! | findstr /i /c:"\"url\"" >nul
        if !errorlevel! equ 0 (
            set "line=!line:*"url" =!"
            set "line=!line:*:=!"
            set "line=!line: =!"
            set "line=!line:"=!"
            set "line=!line:,=!"
            set "URL=!line!"
            goto :url_done
        )
        echo !line! | findstr /c:"}" >nul
        if !errorlevel! equ 0 set "IN_64BIT=0"
    ) else (
        echo !line! | findstr /i /c:"\"64bit\"" >nul
        if !errorlevel! equ 0 set "IN_64BIT=1"
    )
)
if not defined URL (
    for /f "usebackq delims=" %%a in ("%JSON_FILE%") do (
        set "line=%%a"
        for /f "tokens=*" %%b in ("!line!") do set "line=%%b"
        echo !line! | findstr /i /c:"\"url\"" >nul
        if !errorlevel! equ 0 (
            set "line=!line:*"url" =!"
            set "line=!line:*:=!"
            set "line=!line: =!"
            set "line=!line:"=!"
            set "line=!line:,=!"
            set "URL=!line!"
            goto :url_done
        )
    )
)
:url_done

if not defined URL (
    echo 警告: %APPNAME% 无下载网址，跳过
    goto :eof
)

:: 计算 URL 的完整 SHA256（无换行符）
set "URL_HASH="
set "TEMP_FILE=%temp%\url_hash_%RANDOM%.tmp"
<nul set /p "=%URL%" > "%TEMP_FILE%" 2>nul
for /f "skip=1 tokens=*" %%h in ('certutil -hashfile "%TEMP_FILE%" SHA256 2^>nul') do (
    set "URL_HASH=%%h"
    goto :hash_done
)
:hash_done
del "%TEMP_FILE%" 2>nul

if not defined URL_HASH (
    echo 警告: %APPNAME% 无法计算哈希，跳过
    goto :eof
)
for /f "tokens=*" %%a in ("%URL_HASH%") do set "URL_HASH=%%a"
set "HASH7=!URL_HASH:~0,7!"

:: 提取文件扩展名
set "EXT="
for %%f in ("%URL%") do set "EXT=%%~xf"
if "%EXT%"=="" set "EXT=.zip"

:: 输出结果
echo.
echo ------------------------------------------
echo 应用: %APPNAME% (来源: %BUCKET%)
echo 版本: %VERSION%
echo 下载网址: %URL%
echo 完整SHA256: %URL_HASH%
echo 哈希前7位: %HASH7%
echo 缓存文件名: %APPNAME%#%VERSION%#%HASH7%%EXT%
echo ------------------------------------------

goto :eof
