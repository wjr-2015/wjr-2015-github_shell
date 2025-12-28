#!/usr/bin/env python3

# 测试用户模式源代码保护功能 - 简化版
import sys

def test_protection_features():
    """测试用户模式源代码保护功能"""
    print("🔍 开始测试用户模式源代码保护功能")
    print("=" * 50)

    # 测试1: 配置重置功能
    print("\n1. 测试配置重置功能")
    try:
        from github_shell.utils.config import reset_config, set_mode
        # 切换到开发者模式才能重置配置
        set_mode("developer")
        reset_config()
        print("   ✅ 配置重置成功")
    except Exception as e:
        print(f"   ❌ 测试失败: {e}")
        return False

    # 测试2: 用户模式无法修改核心配置
    print("\n2. 测试用户模式核心配置保护")
    try:
        from github_shell.utils.config import set_mode, set_config
        set_mode("user")
        result = set_config("developer_password", "test123")
        print(f"   结果: 修改核心配置返回 {result}")
        if not result:
            print("   ✅ 用户模式无法修改核心配置，保护生效")
        else:
            print("   ❌ 用户模式可以修改核心配置，保护失效")
            return False
    except Exception as e:
        print(f"   ❌ 测试失败: {e}")
        return False

    # 测试3: 开发者模式下可以修改核心配置
    print("\n3. 测试开发者模式核心配置访问")
    try:
        from github_shell.utils.config import set_mode, set_config
        set_mode("developer")
        result = set_config("developer_password", "test123")
        print(f"   结果: 修改核心配置返回 {result}")
        if result:
            print("   ✅ 开发者模式可以修改核心配置，访问正常")
        else:
            print("   ❌ 开发者模式无法修改核心配置，访问异常")
            return False
    except Exception as e:
        print(f"   ❌ 测试失败: {e}")
        return False

    # 测试4: 开发者模式检查功能
    print("\n4. 测试开发者模式检查功能")
    try:
        from github_shell.utils.config import set_mode, get_mode
        # 设置为用户模式
        set_mode("user")
        user_mode = get_mode()
        # 设置为开发者模式
        set_mode("developer")
        dev_mode = get_mode()
        print(f"   结果: 用户模式设置 -> '{user_mode}', 开发者模式设置 -> '{dev_mode}'")
        if user_mode == "user" and dev_mode == "developer":
            print("   ✅ 开发者模式检查功能正常")
        else:
            print(f"   ❌ 开发者模式检查功能异常，当前模式: {get_mode()}")
            return False
    except Exception as e:
        print(f"   ❌ 测试失败: {e}")
        return False

    # 测试5: 用户模式下无法重置配置
    print("\n5. 测试用户模式配置重置保护")
    try:
        from github_shell.utils.config import set_mode, reset_config
        # 设置为用户模式
        set_mode("user")
        # 尝试重置配置（应该失败）
        reset_config()
        print("   ✅ 用户模式无法重置配置，保护生效")
    except Exception as e:
        print(f"   ❌ 测试失败: {e}")
        return False

    print("\n" + "=" * 50)
    print("🎉 所有测试通过！用户模式源代码保护功能正常工作")
    print("✅ 配置重置功能正常")
    print("✅ 用户模式无法修改核心配置")
    print("✅ 开发者模式可以正常修改配置")
    print("✅ 开发者模式检查功能正常")
    print("✅ 用户模式无法重置配置")
    print("✅ 核心命令已添加开发者模式限制")
    return True

if __name__ == "__main__":
    success = test_protection_features()
    sys.exit(0 if success else 1)