#!/usr/bin/env python3
"""
语言支持模块
用于处理多语言切换功能
"""

# 语言定义
LANGUAGES = {
    "english": {
        "welcome": "🎉 GitHub Simulation Shell",
        "current_version": "Current version: {}",
        "welcome_user": "Welcome, current user: {}",
        "help_tip": "Type 'help' for command list, 'exit' to quit\n",
        "prompt": "github-shell:{}$",
        "exit_msg": "\n👋 Exiting GitHub Simulation Shell",
        "unknown_cmd": "❌ Unknown command: {}",
        "help_cmd": "Type 'help' to see available commands",
        "list_repos": "\n📦 Listing repos for {}:",
        "repo_info": "\n📋 Repository info: {}",
        "repo_name": "  Name: {}",
        "repo_owner": "  Owner: {}",
        "repo_desc": "  Description: {}",
        "repo_stars": "  Stars: {}",
        "repo_forks": "  Forks: {}",
        "repo_created": "  Created at: {}",
        "repo_updated": "  Updated at: {}",
        "repo_issues": "\n📝 Issues for {}:",
        "issue_format": "  #{number}: {title} (by: {author})",
        "repo_branches": "\n🌿 Branches for {}:",
        "branch_format": "  - {}",
        "repo_commits": "\n📜 Recent commits for {}:",
        "commit_format": "  [{sha}] {author} {date}: {message}",
        "repo_contributors": "\n👥 Contributors for {}:",
        "contributor_format": "  - {login} (💻 {contributions} commits)",
        "repo_prs": "\n🔀 Pull Requests for {}:",
        "pr_format": "  #{number}: {title} (by: {author})",
        "user_gists": "\n📝 Gists for {}:",
        "gist_format": "  - {description} ({created_at}) Files: {files}",
        "search_repos": "\n🔍 Searching repos: {}",
        "search_result": "  - {full_name} (⭐ {stars})\n    {description}",
        "org_info": "\n🏢 Organization info: {}",
        "org_name": "  Name: {}",
        "org_desc": "  Description: {}",
        "org_repos": "  Public repos: {}",
        "org_members": "  Members: {}",
        "user_info": "\n👤 User info: {}",
        "user_company": "  Company: {}",
        "user_location": "  Location: {}",
        "user_followers": "  Followers: {}",
        "user_following": "  Following: {}",
        "user_repos": "  Public repos: {}",
        "user_followers_list": "\n👥 Followers of {}:",
        "user_following_list": "\n👥 Following of {}:",
        "checking_updates": "\n🔄 Checking for updates...",
        "current_ver": "Current version: {}",
        "new_version_found": "Found new version: {}",
        "updating": "Updating...",
        "backup_created": "Backup created: {}",
        "update_success": "✅ Update successful! Please restart the script to use the new version.",
        "already_latest": "✅ Already the latest version",
        "update_failed": "❌ Update failed: {}",
        "show_version": "\n📋 GitHub Simulation Shell version: {}",
        "language_changed": "✅ Language changed to: {}",
        "help_text": """GitHub Simulation Shell Command List:

Repository Operations:
  repos                 - List current user's repositories
  repo <owner>/<repo>   - View specified repository information
  issues <repo>         - View repository issues
  branches <repo>       - View repository branches
  commits <repo>        - View recent commits
  contributors <repo>   - View repository contributors
  prs <repo>            - View Pull Requests
  gists <username>      - View user's Gists

Search Operations:
  search <query>        - Search GitHub repositories

Organization Operations:
  org <orgname>         - View specified organization information

User Operations:
  user <username>       - View specified user information
  followers             - View current user's followers
  following             - View users current user is following

System Commands:
  help                  - Show this help message
  clear                 - Clear the screen
  exit                  - Exit the simulation shell
  update                - Check and update to latest version
  version               - Show current version
  language <lang>       - Change language (en/zh)
"""
    },
    "chinese": {
        "welcome": "🎉 GitHub 仿真 Shell",
        "current_version": "当前版本: {}",
        "welcome_user": "欢迎使用，当前用户：{}",
        "help_tip": "输入 'help' 查看命令列表，输入 'exit' 退出\n",
        "prompt": "github-shell:{}$",
        "exit_msg": "\n👋 退出 GitHub 仿真 Shell",
        "unknown_cmd": "❌ 未知命令: {}",
        "help_cmd": "输入 'help' 查看可用命令",
        "list_repos": "\n📦 列出 {} 的仓库：",
        "repo_info": "\n📋 仓库信息：{}",
        "repo_name": "  名称: {}",
        "repo_owner": "  所有者: {}",
        "repo_desc": "  描述: {}",
        "repo_stars": "  星级: {}",
        "repo_forks": "  Forks: {}",
        "repo_created": "  创建时间: {}",
        "repo_updated": "  更新时间: {}",
        "repo_issues": "\n📝 {} 的Issues：",
        "issue_format": "  #{number}: {title} (创建者: {author})",
        "repo_branches": "\n🌿 {} 的分支：",
        "branch_format": "  - {}",
        "repo_commits": "\n📜 {} 的最近提交：",
        "commit_format": "  [{sha}] {author} {date}: {message}",
        "repo_contributors": "\n👥 {} 的贡献者：",
        "contributor_format": "  - {login} (💻 {contributions} 次提交)",
        "repo_prs": "\n🔀 {} 的Pull Requests：",
        "pr_format": "  #{number}: {title} (创建者: {author})",
        "user_gists": "\n📝 {} 的Gists：",
        "gist_format": "  - {description} ({created_at}) 文件: {files}",
        "search_repos": "\n🔍 搜索仓库: {}",
        "search_result": "  - {full_name} (⭐ {stars})\n    {description}",
        "org_info": "\n🏢 组织信息：{}",
        "org_name": "  名称: {}",
        "org_desc": "  描述: {}",
        "org_repos": "  公开仓库: {}",
        "org_members": "  成员数量: {}",
        "user_info": "\n👤 用户信息：{}",
        "user_company": "  公司: {}",
        "user_location": "  位置: {}",
        "user_followers": "  关注者: {}",
        "user_following": "  关注的人: {}",
        "user_repos": "  仓库数量: {}",
        "user_followers_list": "\n👥 {} 的关注者：",
        "user_following_list": "\n👥 {} 关注的人：",
        "checking_updates": "\n🔄 检查更新...",
        "current_ver": "当前版本: {}",
        "new_version_found": "发现新版本: {}",
        "updating": "正在更新...",
        "backup_created": "已备份当前版本到: {}",
        "update_success": "✅ 更新成功！请重新运行脚本以使用新版本。",
        "already_latest": "✅ 当前已是最新版本",
        "update_failed": "❌ 更新失败: {}",
        "show_version": "\n📋 GitHub 仿真 Shell 版本: {}",
        "language_changed": "✅ 语言已更改为: {}",
        "help_text": """GitHub 仿真 Shell 命令列表：

仓库操作：
  repos                 - 列出当前用户的仓库
  repo <owner>/<repo>   - 查看指定仓库信息
  issues <repo>         - 查看仓库的Issues
  branches <repo>       - 查看仓库的分支
  commits <repo>        - 查看仓库的最近提交
  contributors <repo>   - 查看仓库的贡献者
  prs <repo>            - 查看仓库的Pull Requests
  gists <username>      - 查看用户的Gists

搜索功能：
  search <query>        - 搜索GitHub仓库

组织操作：
  org <orgname>         - 查看指定组织信息

用户操作：
  user <username>       - 查看指定用户信息
  followers             - 查看当前用户的关注者
  following             - 查看当前用户关注的人

系统命令：
  help                  - 显示此帮助信息
  clear                 - 清除屏幕
  exit                  - 退出仿真Shell
  update                - 检查并更新到最新版本
  version               - 显示当前版本
  language <lang>       - 切换语言 (en/zh)
"""
    }
}

# 当前语言
_current_language = "english"

def get_language():
    """获取当前语言"""
    return _current_language

def set_language(lang):
    """设置当前语言
    
    Args:
        lang: 语言代码，支持 "english"（英语）和 "chinese"（中文）
        
    Returns:
        bool: 是否成功设置
    """
    global _current_language
    if lang in LANGUAGES:
        _current_language = lang
        return True
    return False

def _(key, *args, **kwargs):
    """获取翻译文本
    
    Args:
        key: 文本键名
        *args: 位置参数
        **kwargs: 关键字参数
        
    Returns:
        str: 翻译后的文本
    """
    lang_dict = LANGUAGES.get(_current_language, LANGUAGES["english"])
    return lang_dict.get(key, key).format(*args, **kwargs)
