#!/usr/bin/env python3
"""
配置管理和模式切换测试脚本
用于验证配置管理功能和开发者模式/用户模式的切换
"""

from github_shell.utils.config import (
    reset_config, get_developer_password, set_mode,
    set_config, get_mode, get_config
)

def test_config_management():
    """测试配置管理功能"""
    print("\n=== 测试配置管理功能 ===")
    
    # 测试1: 默认密码设置
    print("\n1. 测试默认密码设置：")
    set_mode("developer")  # 切换到开发者模式
    reset_config()  # 重置配置
    password = get_developer_password()
    print(f"默认密码: '{password}'")
    assert password == "wjr@2015", f"默认密码错误，应为 'wjr@2015'，实际为 '{password}'"
    print("✅ 默认密码设置正确")
    
    # 测试2: 配置项获取
    print("\n2. 测试配置项获取：")
    mode = get_config("mode")
    print(f"当前模式: {mode}")
    assert mode == "user", f"模式获取错误，应为 'user'，实际为 '{mode}'"
    print("✅ 配置项获取正确")
    
    # 测试3: 配置项设置
    print("\n3. 测试配置项设置：")
    set_mode("developer")  # 切换到开发者模式
    result = set_config("language", "chinese")
    print(f"设置语言返回: {result}")
    assert result is True, "配置项设置失败"
    language = get_config("language")
    print(f"设置后语言: {language}")
    assert language == "chinese", f"语言设置错误，应为 'chinese'，实际为 '{language}'"
    print("✅ 配置项设置正确")

def test_mode_switching():
    """测试模式切换功能"""
    print("\n=== 测试模式切换功能 ===")
    
    # 测试1: 切换到开发者模式
    print("\n1. 测试切换到开发者模式：")
    result = set_mode("developer")
    print(f"切换到开发者模式返回: {result}")
    assert result is True, "切换到开发者模式失败"
    mode = get_mode()
    print(f"当前模式: {mode}")
    assert mode == "developer", f"模式切换错误，应为 'developer'，实际为 '{mode}'"
    print("✅ 切换到开发者模式成功")
    
    # 测试2: 切换到用户模式
    print("\n2. 测试切换到用户模式：")
    result = set_mode("user")
    print(f"切换到用户模式返回: {result}")
    assert result is True, "切换到用户模式失败"
    mode = get_mode()
    print(f"当前模式: {mode}")
    assert mode == "user", f"模式切换错误，应为 'user'，实际为 '{mode}'"
    print("✅ 切换到用户模式成功")
    
    # 测试3: 无效模式切换
    print("\n3. 测试无效模式切换：")
    result = set_mode("invalid_mode")
    print(f"无效模式切换返回: {result}")
    assert result is False, "无效模式切换应该失败"
    print("✅ 无效模式切换处理正确")

def test_core_config_protection():
    """测试核心配置保护功能"""
    print("\n=== 测试核心配置保护功能 ===")
    
    # 测试1: 用户模式无法修改核心配置
    print("\n1. 测试用户模式核心配置保护：")
    set_mode("user")  # 切换到用户模式
    result = set_config("developer_password", "test123")
    print(f"用户模式修改核心配置返回: {result}")
    assert result is False, "用户模式应该无法修改核心配置"
    print("✅ 用户模式无法修改核心配置，保护生效")
    
    # 测试2: 开发者模式可以修改核心配置
    print("\n2. 测试开发者模式核心配置访问：")
    set_mode("developer")  # 切换到开发者模式
    result = set_config("developer_password", "test123")
    print(f"开发者模式修改核心配置返回: {result}")
    assert result is True, "开发者模式应该可以修改核心配置"
    password = get_developer_password()
    print(f"修改后密码: '{password}'")
    assert password == "test123", f"核心配置修改错误，应为 'test123'，实际为 '{password}'"
    print("✅ 开发者模式可以修改核心配置，访问正常")
    
    # 恢复默认密码
    reset_config()

def main():
    """主测试函数"""
    print("🚀 配置管理和模式切换测试")
    
    test_config_management()
    test_mode_switching()
    test_core_config_protection()
    
    print("\n✅ 所有测试完成！")

if __name__ == "__main__":
    main()