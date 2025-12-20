import os
import sys
from github_shell.commands.repo_commands import RepoCommands
from github_shell.commands.user_commands import UserCommands
from github_shell.commands.search_commands import SearchCommands
from github_shell.commands.org_commands import OrgCommands
from github_shell.commands.update_commands import UpdateCommands
from github_shell.commands.rate_limit import RateLimitCommand
from github_shell.utils.config import USERNAME, UPDATE_CONFIG
from github_shell.utils.language import _, get_language, set_language
from github_shell.utils.dependency_manager import check_and_install_dependencies
from github_shell.utils.history import add_to_history, show_history, clear_history
from github_shell.utils.config import load_config, save_config, set_config, reset_config

class GitHubShell:
    """GitHub仿真Shell主类"""
    
    def __init__(self):
        self.repo_commands = RepoCommands()
        self.user_commands = UserCommands()
        self.search_commands = SearchCommands()
        self.org_commands = OrgCommands()
        self.update_commands = UpdateCommands()
        self.rate_limit_cmd = RateLimitCommand()
        # 加载配置
        self.config = load_config()
        # 设置初始语言
        set_language(self.config.get("language", "en"))
    
    def clear_screen(self):
        """清除屏幕"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def run(self):
        """运行仿真Shell"""
        print(_("welcome"))
        print(_("current_version", UPDATE_CONFIG['version']))
        print(_("welcome_user", USERNAME))
        print(_("help_tip"))
        
        while True:
            try:
                # 获取用户输入
                command = input(_("prompt", USERNAME)).strip()
                
                # 添加命令到历史记录
                add_to_history(command)
                
                # 解析命令
                parts = command.split()
                if not parts:
                    continue
                
                cmd = parts[0].lower()
                args = parts[1:]
                
                # 处理命令
                if cmd == "exit":
                    print(_("exit_msg"))
                    break
                elif cmd == "help":
                    print(_("help_text"))
                elif cmd == "clear":
                    self.clear_screen()
                elif cmd == "repos":
                    self.repo_commands.list_repos()
                elif cmd == "repo" and args:
                    self.repo_commands.show_repo(args[0])
                elif cmd == "issues" and args:
                    repo = args[0]
                    if "/" not in repo:
                        repo = f"{USERNAME}/{repo}"
                    self.repo_commands.show_issues(repo)
                elif cmd == "branches" and args:
                    repo = args[0]
                    if "/" not in repo:
                        repo = f"{USERNAME}/{repo}"
                    self.repo_commands.show_branches(repo)
                elif cmd == "commits" and args:
                    repo = args[0]
                    if "/" not in repo:
                        repo = f"{USERNAME}/{repo}"
                    self.repo_commands.show_commits(repo)
                elif cmd == "user" and args:
                    self.user_commands.show_user(args[0])
                elif cmd == "followers":
                    self.user_commands.list_followers()
                elif cmd == "following":
                    self.user_commands.list_following()
                elif cmd == "contributors" and args:
                    repo = args[0]
                    if "/" not in repo:
                        repo = f"{USERNAME}/{repo}"
                    self.repo_commands.show_contributors(repo)
                elif cmd == "prs" and args:
                    repo = args[0]
                    if "/" not in repo:
                        repo = f"{USERNAME}/{repo}"
                    self.repo_commands.show_prs(repo)
                elif cmd == "gists" and args:
                    self.repo_commands.show_gists(args[0])
                elif cmd == "search" and args:
                    self.search_commands.search_repos(" ".join(args))
                elif cmd == "org" and args:
                    self.org_commands.show_org(args[0])
                elif cmd == "update":
                    self.update_commands.check_for_updates()
                elif cmd == "version":
                    self.update_commands.show_version()
                elif cmd == "language" and args:
                    # 语言切换命令
                    lang = args[0]
                    if set_language(lang):
                        print(_("language_changed", lang))
                        # 保存语言设置到配置文件
                        set_config("language", lang)
                    else:
                        print(f"❌ Invalid language: {lang}. Supported: en, zh")
                # 新功能：速率限制
                elif cmd == "rate" or cmd == "limit" or cmd == "rate-limit":
                    self.rate_limit_cmd.show_rate_limit()
                # 新功能：历史命令
                elif cmd == "history":
                    show_history()
                # 新功能：清空历史
                elif cmd == "clear-history":
                    clear_history()
                # 新功能：配置相关
                elif cmd == "config" and len(args) >= 2:
                    # 设置配置项
                    key = args[0]
                    value = args[1]
                    set_config(key, value)
                    print(f"✅ 配置已设置：{key} = {value}")
                elif cmd == "config" and len(args) == 1:
                    # 查看配置项
                    key = args[0]
                    config = load_config()
                    if key in config:
                        print(f"  {key}: {config[key]}")
                    else:
                        print(f"❌ 配置项不存在：{key}")
                elif cmd == "config" and len(args) == 0:
                    # 查看所有配置
                    config = load_config()
                    print("\n⚙️ 当前配置：")
                    for key, value in config.items():
                        print(f"  {key}: {value}")
                elif cmd == "reset-config":
                    # 重置配置
                    reset_config()
                    print("✅ 配置已重置为默认值")
                else:
                    print(_("unknown_cmd", cmd))
                    print(_("help_cmd"))
            
            except KeyboardInterrupt:
                print("\n👋 退出 GitHub 仿真 Shell")
                break
            except Exception as e:
                print(f"❌ 发生错误: {e}")

def main():
    """主入口函数"""
    # 检查并安装缺失的依赖
    if not check_and_install_dependencies():
        print("\n❌ 依赖安装失败，无法启动程序")
        sys.exit(1)
    
    shell = GitHubShell()
    shell.run()

if __name__ == "__main__":
    main()
