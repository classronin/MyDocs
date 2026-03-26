# sapp - Scoop 缓存下载器（Surge 加速版）

`sapp` 是一个命令行工具，用于提前下载 Scoop 应用的安装包到缓存目录，避免 Scoop 安装或更新时重复下载。它自动遍历所有本地 bucket，支持模糊匹配，并提供交互式选择菜单。

## 特性
- 🔍 自动识别所有已安装的 Scoop bucket（无需手动配置）
- 📦 支持应用名称部分匹配（如 `ollama` 匹配 `ollama` 和 `ollama-full`）
- 🎯 按 bucket 优先级排序（`main` > `extras` > 其他）
- ⬆️⬇️ 交互式箭头菜单选择（支持 ESC 取消）
- 🚀 使用 `surge` 加速 GitHub 资源下载
- ✅ 完美兼容 Scoop 缓存命名规则（正确处理 URL 锚点如 `#/dl.msi_`）



## 用法
```bash
uv run sapp.py <应用名称>
```

或（如果已加入 PATH）：sapp.bat
```
@echo off
cd /d "%SCRIPTS%\Scoop"
uv run Sapp.py %*
```

```
sapp <应用名称>
```

示例：
```
sapp git          # 搜索并下载 git 相关应用
sapp uv           # 搜索包含 uv 的应用
```


工作流程
搜索所有 bucket 中名称包含指定字符串的应用
按优先级排序并列出结果
用户用上下键选择，回车确认
下载文件并保存到 Scoop 缓存目录（文件名格式：应用名#版本#URL哈希.扩展名）

注意事项
运行前建议执行 scoop update 确保本地 bucket 最新


依赖

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

[![ uv ](https://img.shields.io/github/v/release/astral-sh/uv?label=UV)](https://github.com/astral-sh/uv/releases/latest)
```
scoop install uv
```

[![ python-build-standalone ](https://img.shields.io/github/v/release/astral-sh/python-build-standalone?label=Python)](https://github.com/astral-sh/python-build-standalone/releases/latest)
```
uv python install 3.12
```

[![Scoop 版本](https://img.shields.io/github/v/release/ScoopInstaller/Scoop?label=Scoop)](https://github.com/ScoopInstaller/Scoop/releases/latest)
```
scoop install surge
```

