#!/usr/bin/env python3
import os
import sys
import traceback
from pathlib import Path
import time # For potential pauses

try:
    # Import necessary functions from huggingface_hub
    from huggingface_hub import hf_hub_download, snapshot_download, model_info
    from huggingface_hub.utils import HfHubHTTPError, HFValidationError
except ImportError:
    print(
        "错误：未找到 huggingface_hub 库\n"
        "请使用以下命令安装：pip install huggingface_hub",
        file=sys.stderr
    )
    sys.exit(1)

try:
    # Import rich for styled output
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.prompt import Prompt, IntPrompt, Confirm # For better prompting
except ImportError:
    print(
        "错误：未找到 rich 库\n"
        "请使用以下命令安装：pip install rich",
        file=sys.stderr
    )
    # Define fallback simple input if rich prompt is not available
    class FallbackPrompt:
        @staticmethod
        def ask(prompt, default=None, **kwargs):
            full_prompt = prompt
            if default is not None:
                full_prompt += f" [默认: {default}]"
            full_prompt += ": "
            value = input(full_prompt)
            if not value and default is not None:
                return default
            return value

    class FallbackIntPrompt(FallbackPrompt):
         @staticmethod
         def ask(prompt, default=None, **kwargs):
            while True:
                val_str = FallbackPrompt.ask(prompt, default=str(default) if default is not None else None)
                try:
                    return int(val_str)
                except ValueError:
                    print("无效输入，请输入整数")

    class FallbackConfirm(FallbackPrompt):
         @staticmethod
         def ask(prompt, default=False, **kwargs):
             while True:
                val_str = FallbackPrompt.ask(prompt, default="y" if default else "n")
                if val_str.lower() in ['y', 'yes']: return True
                if val_str.lower() in ['n', 'no']: return False
                print("请输入 'y' 或 'n'")

    class FallbackConsole:
        def print(self, *args, **kwargs): print(*args)
        def rule(self, *args, **kwargs): print("-" * 20)
        def status(self, *args, **kwargs): return self # Dummy status context
        def __enter__(self): return self
        def __exit__(self, exc_type, exc_val, exc_tb): pass
        def update(self, *args, **kwargs): print(args[0] if args else "处理中...")

    Console = FallbackConsole # type: ignore
    Prompt = FallbackPrompt # type: ignore
    IntPrompt = FallbackIntPrompt # type: ignore
    Confirm = FallbackConfirm # type: ignore


# Initialize rich console
console = Console()

# --- Default Settings ---
DEFAULT_SAVE_DIR = Path.home() / "hf_models"
DEFAULT_WORKERS = 3
# Define default models/files for prompts
DEFAULT_SINGLE_FILE_REPO = "google-bert/bert-base-uncased"
DEFAULT_SINGLE_FILENAME = "config.json"
DEFAULT_MODEL_REPO = "distilbert-base-uncased"


# --- Helper Functions ---

def display_main_menu():
    """Prints the main menu options."""
    console.print(Panel(
        Text("1. 下载单个文件\n"
             "2. 下载完整模型\n"
             "3. 退出", justify="left"),
        title="[bold cyan]Hugging Face 下载器菜单[/bold cyan]",
        border_style="blue",
        padding=(1, 2)
    ))

def handle_download_error(e, repo_id, filename=None):
    """Handles common download errors and prints styled messages."""
    if isinstance(e, HfHubHTTPError):
        if "404" in str(e) or "not found" in str(e).lower() or "repository not found" in str(e).lower():
            target = f"文件 '{filename}' 在仓库" if filename else "仓库"
            console.print(f"[bold red]错误：[/bold red] {target} '{repo_id}' 未找到 (404)，请检查名称")
        else:
            console.print(f"[bold red]错误：[/bold red] 从 '{repo_id}' 下载时出现网络或服务器错误")
            console.print(f"[dim]{e}[/dim]")
    elif isinstance(e, HFValidationError):
         console.print(f"[bold red]错误：[/bold red] 无效的仓库或文件名: '{repo_id}'{f'/{filename}' if filename else ''}")
         console.print(f"[dim]{e}[/dim]")
    elif isinstance(e, FileNotFoundError):
         console.print(f"[bold red]错误：[/bold red] 无法创建本地目录，请检查权限")
         console.print(f"[dim]{e}[/dim]")
    else:
        console.print(f"[bold red]发生意外错误：[/bold red]")
        if not isinstance(e, (HfHubHTTPError, HFValidationError)):
             console.print(f"[dim]{traceback.format_exc()}[/dim]")
        else:
             console.print(f"[dim]{e}[/dim]")

def ensure_directory(path: Path):
    """Ensures a directory exists, creating it if necessary. Returns True on success."""
    try:
        path.mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        console.print(f"[bold red]错误：[/bold red] 无法创建目录 '{path}'，请检查权限")
        console.print(f"[dim]{e}[/dim]")
        return False

def run_single_download():
    """Prompts for single file info and initiates download."""
    console.rule("[#ADFF2F]下载单个文件[/#ADFF2F]")
    repo_id = Prompt.ask("[cyan]输入仓库 ID[/cyan]", default=DEFAULT_SINGLE_FILE_REPO)
    if not repo_id: console.print("[yellow]仓库 ID 不能为空，操作中止[/yellow]"); return

    filename = Prompt.ask("[cyan]输入文件名[/cyan]", default=DEFAULT_SINGLE_FILENAME)
    if not filename: console.print("[yellow]文件名不能为空，操作中止[/yellow]"); return

    local_dir_str = Prompt.ask(f"[cyan]输入保存目录[/cyan]", default=str(DEFAULT_SAVE_DIR))
    local_dir = Path(local_dir_str)

    if not ensure_directory(local_dir): return

    console.print(f"\n[magenta]开始下载...[/magenta]")
    console.print(f"  仓库 ID: [#ADFF2F]{repo_id}[/#ADFF2F]")
    console.print(f"  文件名: [#ADFF2F]{filename}[/#ADFF2F]")
    console.print(f"  保存目录: [#ADFF2F]{local_dir}[/#ADFF2F]")
    console.rule()

    try:
        file_path = hf_hub_download(
            repo_id=repo_id,
            filename=filename,
            local_dir=local_dir,
            cache_dir=local_dir / ".cache"
        )
        console.rule()
        console.print(f"[#ADFF2F]成功！[/#ADFF2F] 文件已下载到：")
        console.print(f"  [bold #F59E0B]{file_path}[/bold #F59E0B]")

    except Exception as e:
        console.rule()
        handle_download_error(e, repo_id, filename)

def run_model_download():
    """Prompts for model info and initiates download."""
    console.rule("[bold blue]下载完整模型[/bold blue]")
    repo_id = Prompt.ask("[cyan]输入仓库 ID[/cyan]", default=DEFAULT_MODEL_REPO)
    if not repo_id: console.print("[yellow]仓库 ID 不能为空，操作中止[/yellow]"); return

    local_dir_base_str = Prompt.ask(f"[cyan]输入基础保存目录[/cyan]", default=str(DEFAULT_SAVE_DIR))
    local_dir_base = Path(local_dir_base_str)

    workers = IntPrompt.ask(f"[cyan]输入工作线程数[/cyan]", default=DEFAULT_WORKERS, choices=[str(w) for w in [1, 2, 3, 4, 6, 8]])

    if not ensure_directory(local_dir_base): return

    # --- Get File Count ---
    num_files_str = ""
    try:
        with console.status(f"[cyan]正在获取 {repo_id} 的模型信息...[/]"):
             info = model_info(repo_id=repo_id)
        num_files = len(info.siblings)
        num_files_str = f" (预计 {num_files} 个文件)"
        console.print(f"  模型信息: [green]找到 {num_files} 个文件[/green]")
    except Exception as info_err:
         console.print(f"  模型信息: [yellow]警告: 无法获取文件数量: {info_err}[/yellow]")
    # ---

    console.print(f"\n[magenta]开始下载...[/magenta]")
    console.print(f"  仓库 ID: [bold]{repo_id}[/bold]")
    console.print(f"  基础保存目录: [bright_green]{local_dir_base}[/bright_green]")
    console.print(f"  工作线程数: [bright_green]{workers}[/bright_green]")
    console.rule(f"开始下载{num_files_str}")

    model_target_dir = local_dir_base / repo_id

    try:
        model_path = snapshot_download(
            repo_id=repo_id,
            local_dir=model_target_dir,
            max_workers=workers
        )
        console.rule()
        console.print(f"[green]成功！[/green] 模型已下载到目录：")
        console.print(f"  [bold cyan]{model_path}[/bold cyan]")

    except Exception as e:
        console.rule()
        handle_download_error(e, repo_id)


# --- Main Application Loop ---
def run_app():
    """Runs the main interactive menu loop."""
    while True:
        display_main_menu()
        choice = Prompt.ask("[bold #F59E0B]请选择操作[/bold #F59E0B]", choices=["1", "2", "3"])

        if choice == '1':
            run_single_download()
        elif choice == '2':
            run_model_download()
        elif choice == '3':
            console.print("[bold blue]程序退出[/bold blue]")
            break
        else:
            console.print("[red]无效选择，请重试[/red]")

        console.print("\n按 Enter 键继续...")
        input()
        console.print("\n" * 2)


if __name__ == "__main__":
    try:
        run_app()
    except KeyboardInterrupt:
        console.print("\n[yellow]用户中断操作，正在退出[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print("[bold red]发生意外严重错误：[/bold red]")
        if not isinstance(e, (HfHubHTTPError, HFValidationError, FileNotFoundError)):
             console.print_exception(show_locals=False)
        else:
             console.print(f"[dim]{e}[/dim]")
        sys.exit(1)
