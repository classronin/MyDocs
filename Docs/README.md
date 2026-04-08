


# [CopyQ](https://hluk.github.io/CopyQ/)  具备高级功能的剪贴板管理器
安装及环境变量
```
scoop install copyq # 安装
COPYQ_SETTINGS_PATH - 配置路径
COPYQ_ITEM_DATA_PATH - 数据路径
```
CopyQ 主题 [CopyQ-GitHub-Theme](https://github.com/classronin/CopyQ-GitHub-Theme)

---




# [vcpkg](https://github.com/microsoft/vcpkg) 设置镜像
路径：...\vcpkg\scripts\cmake\vcpkg_download_distfile.cmake
```
function(vcpkg_download_distfile out_var)
    cmake_parse_arguments(PARSE_ARGV 1 arg
        "SKIP_SHA512;SILENT_EXIT;QUIET;ALWAYS_REDOWNLOAD"
        "FILENAME;SHA512"
        "URLS;HEADERS"
    )

    if(NOT DEFINED arg_URLS)
        message(FATAL_ERROR "vcpkg_download_distfile requires a URLS argument.")
    endif()
    if(NOT DEFINED arg_FILENAME)
        message(FATAL_ERROR "vcpkg_download_distfile requires a FILENAME argument.")
    endif()
    if(arg_SILENT_EXIT)
        message(WARNING "SILENT_EXIT no longer has any effect. To resolve this warning, remove SILENT_EXIT.")
    endif()

    # ========== 在这里添加镜像转换代码 ==========
    # 为所有 GitHub URL 添加镜像前缀
    set(mirror_prefix "https://gh-proxy.com/")
    set(converted_urls "")
    foreach(url IN LISTS arg_URLS)
        if(url MATCHES "^https://github\.com/")
            # 将 https://github.com/xxx 替换为 https://gh-proxy.com/https://github.com/xxx
            string(REPLACE "https://github.com/" "${mirror_prefix}https://github.com/" new_url "${url}")
            list(APPEND converted_urls "${new_url}")
            message(STATUS "Converted GitHub URL: ${url} -> ${new_url}")
        else()
            list(APPEND converted_urls "${url}")
        endif()
    endforeach()
    set(arg_URLS ${converted_urls})
    # ========== 镜像转换代码结束 ==========


    # Note that arg_ALWAYS_REDOWNLOAD implies arg_SKIP_SHA512, and NOT arg_SKIP_SHA512 implies NOT arg_ALWAYS_REDOWNLOAD
    if(arg_ALWAYS_REDOWNLOAD AND NOT arg_SKIP_SHA512)
        message(FATAL_ERROR "ALWAYS_REDOWNLOAD requires SKIP_SHA512")
```














