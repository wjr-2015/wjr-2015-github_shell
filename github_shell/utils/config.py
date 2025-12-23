import os
import json

# 配置文件路径
CONFIG_FILE = os.path.expanduser("~/.github_shell_config.json")

# GitHub API基础URL
GITHUB_API = "https://api.github.com"

# 自动更新配置
UPDATE_CONFIG = {
    "repo_owner": "wjr-2015",
    "repo_name": "github-shell",
    "remote_url": "https://raw.githubusercontent.com/wjr-2015/github-shell/main/github_shell/utils/config.py",
    "version": "1.1.0"  # 当前版本
}

# 配置管理功能
def load_config():
    """加载配置"""
    # 默认配置 - 移除了默认的隐私设置
    default_config = {
        "language": "english",
        "history_size": 100,
        "theme": "default",
        "github_username": "",
        "github_email": "",
        "github_token": "",
        "mode": "user",  # 默认用户模式，可选值：user, developer
        "developer_password": "wjr@2015",  # 开发者模式默认密码：wjr@2015
        "developer_locked": False  # 开发者模式是否锁定
    }
    
    # 如果配置文件存在，加载配置
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                loaded_config = json.load(f)
                # 合并默认配置和加载的配置
                default_config.update(loaded_config)
                return default_config
        except (json.JSONDecodeError, IOError):
            pass
    
    return default_config

def save_config(config):
    """保存配置"""
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except IOError:
        return False

def get_config(key, default=None):
    """获取配置项"""
    config = load_config()
    return config.get(key, default)

def set_config(key, value):
    """设置配置项"""
    # 检查是否在用户模式下尝试修改核心配置
    current_mode = get_mode()
    # 核心配置项，只有开发者模式可以修改
    core_configs = [
        "developer_password",
        "developer_locked"
    ]
    
    if current_mode == "user" and key in core_configs:
        return False
    
    config = load_config()
    config[key] = value
    return save_config(config)

def reset_config():
    """重置配置"""
    # 重置配置只能在开发者模式下进行
    current_mode = get_mode()
    if current_mode != "developer":
        return False
    
    default_config = {
        "language": "english",
        "history_size": 100,
        "theme": "default",
        "github_username": "",
        "github_email": "",
        "github_token": "",
        "mode": "user",
        "developer_password": "wjr@2015",  # 默认密码保持为wjr@2015
        "developer_locked": False
    }
    save_config(default_config)
    return default_config

# 获取开发者模式密码
def get_developer_password():
    """获取开发者模式密码"""
    return get_config("developer_password", "")

# 设置开发者模式密码
def set_developer_password(password):
    """设置开发者模式密码
    
    Args:
        password: 开发者模式密码
        
    Returns:
        bool: 操作是否成功
    """
    return set_config("developer_password", password)

# 清除开发者模式密码
def clear_developer_password():
    """清除开发者模式密码
    
    Returns:
        bool: 操作是否成功
    """
    return set_config("developer_password", "")

# 获取开发者模式锁定状态
def get_developer_locked():
    """获取开发者模式锁定状态
    
    Returns:
        bool: 是否锁定
    """
    return get_config("developer_locked", False)

# 设置开发者模式锁定状态
def set_developer_locked(locked):
    """设置开发者模式锁定状态
    
    Args:
        locked: 是否锁定
        
    Returns:
        bool: 操作是否成功
    """
    return set_config("developer_locked", locked)

# 获取当前模式
def get_mode():
    """获取当前模式"""
    return get_config("mode", "user")

# 设置模式
def set_mode(mode):
    """设置当前模式
    
    Args:
        mode: 模式名称，可选值：user (用户模式), developer (开发者模式)
        
    Returns:
        bool: 操作是否成功
    """
    if mode in ["user", "developer"]:
        return set_config("mode", mode)
    return False

# 获取GitHub用户名
def get_github_username():
    """获取GitHub用户名"""
    return get_config("github_username", "")

# 设置GitHub用户名
def set_github_username(username):
    """设置GitHub用户名"""
    return set_config("github_username", username)

# 获取GitHub邮箱
def get_github_email():
    """获取GitHub邮箱"""
    return get_config("github_email", "")

# 设置GitHub邮箱
def set_github_email(email):
    """设置GitHub邮箱"""
    return set_config("github_email", email)

# 获取GitHub令牌
def get_github_token():
    """获取GitHub令牌"""
    return get_config("github_token", "")

# 设置GitHub令牌
def set_github_token(token):
    """设置GitHub令牌"""
    return set_config("github_token", token)

# 清除GitHub令牌
def clear_github_token():
    """清除GitHub令牌"""
    return set_config("github_token", "")

# 命令帮助信息
HELP_TEXT = """
GitHub 仿真 Shell 命令列表：

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
"""
