# sapp - Scoop 缓存下载器（surge 加速版）

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
若 Scoop 安装/更新时仍重新下载，可先执行 scoop uninstall <应用> 清除安装状态，再重新安装

依赖
Python 3.12+
[![Scoop 版本](https://img.shields.io/github/v/release/ScoopInstaller/Scoop?label=Scoop)](https://github.com/ScoopInstaller/Scoop/releases/latest)

