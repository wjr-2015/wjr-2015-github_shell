#!/usr/bin/env python3

# 快速切换到开发者模式的脚本
import sys
import getpass
from github_shell.utils.config import set_mode, get_developer_password, get_developer_locked

print("GitHub Shell 开发者模式切换工具")
print("=" * 50)

# 检查是否已锁定
if get_developer_locked():
    print("❌ 开发者模式已锁定")
    print("请联系管理员解锁")
    sys.exit(1)

# 获取密码
password = get_developer_password()
if password:
    entered_password = getpass.getpass(prompt="🔑 请输入开发者密码: ")
    if entered_password != password:
        print("❌ 密码错误")
        sys.exit(1)

# 切换到开发者模式
if set_mode("developer"):
    print("✅ 成功切换到开发者模式")
    print("您现在可以使用所有开发者功能")
else:
    print("❌ 切换失败")
    sys.exit(1)
