# GitHub API基础URL
GITHUB_API = "https://api.github.com"

# 配置信息（可修改）
USERNAME = "wjr-2015"  # 替换为你的GitHub用户名
TOKEN = ""  # 如果需要访问私有仓库，可以添加GitHub令牌

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
    return {
        "language": "english",
        "history_size": 100,
        "theme": "default"
    }

def save_config(config):
    """保存配置"""
    pass

def get_config(key, default=None):
    """获取配置项"""
    config = load_config()
    return config.get(key, default)

def set_config(key, value):
    """设置配置项"""
    pass

def reset_config():
    """重置配置"""
    return load_config()

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
