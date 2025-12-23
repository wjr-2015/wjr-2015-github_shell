#!/usr/bin/env python3

# 测试用户模式源代码保护功能
import subprocess
import sys

# 测试默认密码设置
def test_default_password():
    print("测试功能：默认密码设置")
    result = subprocess.run([
        sys.executable, "-c", "from github_shell.utils.config import reset_config, get_developer_password; reset_config(); print(f'Password: {get_developer_password()}')"
    ], 
    capture_output=True, 
    text=True, 
    encoding='utf-8')
    
    print(f"输出: {result.stdout.strip()}")
    
    # 检查默认密码是否为wjr@2015
    if "wjr@2015" in result.stdout:
        print("✅ 默认密码设置正确")
        return True
    else:
        print("❌ 默认密码设置失败")
        return False

# 测试用户模式下无法修改核心配置
def test_user_mode_core_config_protection():
    print("\n测试功能：用户模式核心配置保护")
    # 使用三引号避免嵌套引号问题
    script = '''
from github_shell.utils.config import set_mode, set_config
set_mode('user')
result = set_config('developer_password', 'test123')
print(f'Result: {result}')
'''    
    result = subprocess.run([
        sys.executable, "-c", script
    ], 
    capture_output=True, 
    text=True, 
    encoding='utf-8')
    
    print(f"输出: {result.stdout.strip()}")
    
    # 检查是否返回False（表示无法修改）
    if "False" in result.stdout:
        print("✅ 用户模式无法修改核心配置，保护生效")
        return True
    else:
        print("❌ 用户模式可以修改核心配置，保护失效")
        return False

# 测试开发者模式下可以修改核心配置
def test_developer_mode_core_config_access():
    print("\n测试功能：开发者模式核心配置访问")
    # 使用三引号避免嵌套引号问题
    script = '''
from github_shell.utils.config import set_mode, set_config
set_mode('developer')
result = set_config('developer_password', 'test123')
print(f'Result: {result}')
'''    
    result = subprocess.run([
        sys.executable, "-c", script
    ], 
    capture_output=True, 
    text=True, 
    encoding='utf-8')
    
    print(f"输出: {result.stdout.strip()}")
    
    # 检查是否返回True（表示可以修改）
    if "True" in result.stdout:
        print("✅ 开发者模式可以修改核心配置，访问正常")
        return True
    else:
        print("❌ 开发者模式无法修改核心配置，访问异常")
        return False

# 测试用户模式下无法执行test命令
def test_user_mode_test_command_restriction():
    print("\n测试功能：用户模式test命令限制")
    # 直接使用根目录下的main.py文件
    result = subprocess.run([
        sys.executable, "main.py"
    ], 
    input="test test-lang\nexit\n", 
    text=True, 
    capture_output=True, 
    encoding='utf-8',
    errors='replace',
    cwd="c:\\Users\\ytwan\\Desktop\\github_shell")
    
    # 显示完整输出以调试
    print(f"完整输出: {result.stdout}")
    
    # 检查是否提示权限受限
    if "developer_commands_restricted" in result.stdout or "开发者模式" in result.stdout or "命令只能在开发者模式下使用" in result.stdout:
        print("✅ 用户模式无法执行test命令，限制生效")
        return True
    else:
        print("❌ 用户模式可以执行test命令，限制失效")
        return False

if __name__ == "__main__":
    print("🔍 开始测试用户模式源代码保护功能")
    print("=" * 50)
    
    # 运行所有测试
    tests = [
        test_default_password,
        test_user_mode_core_config_protection,
        test_developer_mode_core_config_access,
        test_user_mode_test_command_restriction
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"测试结果：{passed}/{total} 测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！用户模式源代码保护功能正常工作")
        sys.exit(0)
    else:
        print("❌ 部分测试失败！用户模式源代码保护功能存在问题")
        sys.exit(1)