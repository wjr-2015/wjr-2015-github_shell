#!/usr/bin/env python3
"""
GitHub Simulation Shell 发布脚本
用于版本管理和GitHub发布
"""

import os
import sys
import subprocess
import re
from datetime import datetime


def run_command(cmd, shell=False):
    """运行命令并返回结果"""
    cmd_str = ' '.join(cmd) if isinstance(cmd, list) else cmd
    print(f"执行命令: {cmd_str}")
    try:
        result = subprocess.run(
            cmd, 
            shell=shell, 
            text=True, 
            capture_output=True,
            timeout=30  # 添加超时机制，防止命令无限期运行
        )
        if result.returncode != 0:
            error_msg = f"命令执行失败 (返回码: {result.returncode}): {cmd_str}"
            if result.stdout.strip():
                error_msg += f"\n标准输出: {result.stdout.strip()}"
            if result.stderr.strip():
                error_msg += f"\n标准错误: {result.stderr.strip()}"
            print(error_msg)
            return False, result
        return True, result
    except subprocess.TimeoutExpired:
        print(f"命令执行超时: {cmd_str}")
        return False, None
    except FileNotFoundError:
        print(f"命令未找到: {cmd_str}")
        return False, None
    except Exception as e:
        print(f"命令执行异常: {cmd_str}")
        print(f"异常信息: {e}")
        return False, None


def get_current_version():
    """获取当前版本号，支持预发布版本"""
    with open("setup.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # 支持预发布版本格式，如 1.0.0a1, 1.0.0b2, 1.0.0rc3
    match = re.search(r"version=(\s*['"])([\d.]+(?:(?:a|b|rc)\d+)?)(['"]", content)
    if match:
        return match.group(2)
    return None


def increment_version(current_version, increment_type="patch"):
    """递增版本号，支持预发布版本
    
    Args:
        current_version: 当前版本号
        increment_type: 递增类型 (major, minor, patch, pre)
    
    Returns:
        str: 递增后的版本号
    """
    # 解析版本号
    version_pattern = re.compile(r"(\d+)\.(\d+)\.(\d+)([a|b|rc]\d+)?")
    match = version_pattern.match(current_version)
    
    if not match:
        print(f"无法解析版本号: {current_version}")
        return None
    
    major = int(match.group(1))
    minor = int(match.group(2))
    patch = int(match.group(3))
    pre_release = match.group(4) or ""
    
    if increment_type == "pre":
        # 递增预发布版本
        if pre_release:
            # 已有预发布版本，递增数字
            pre_type = pre_release[0]
            pre_num = int(pre_release[1:])
            new_pre_release = f"{pre_type}{pre_num + 1}"
            return f"{major}.{minor}.{patch}{new_pre_release}"
        else:
            # 没有预发布版本，添加alpha1
            return f"{major}.{minor}.{patch}a1"
    elif increment_type == "major":
        # 递增主版本号
        return f"{major + 1}.0.0"
    elif increment_type == "minor":
        # 递增次版本号
        return f"{major}.{minor + 1}.0"
    elif increment_type == "patch":
        # 递增补丁版本号
        return f"{major}.{minor}.{patch + 1}"
    
    return None


def update_version(version):
    """更新版本号"""
    updated_files = []
    
    try:
        # 更新setup.py
        with open("setup.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        new_content = re.sub(r"version=(\s*['"])([\d.]+)(['"]", f"version=\1{version}\3", content)
        
        with open("setup.py", "w", encoding="utf-8") as f:
            f.write(new_content)
        updated_files.append("setup.py")
    except Exception as e:
        print(f"更新setup.py失败: {e}")
        return False
    
    try:
        # 更新__init__.py
        with open("github_shell/__init__.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        new_content = re.sub(r"__version__ = (\s*['"])([\d.]+(?:(?:a|b|rc)\d+)?)['"]", f"__version__ = \1{version}\2", content)
        
        with open("github_shell/__init__.py", "w", encoding="utf-8") as f:
            f.write(new_content)
        updated_files.append("github_shell/__init__.py")
    except Exception as e:
        print(f"更新__init__.py失败: {e}")
        return False
    
    try:
        # 更新config.py
        with open("github_shell/utils/config.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        new_content = re.sub(r'"version":\s*['"]([\d.]+(?:(?:a|b|rc)\d+)?)['"]', f'"version": "{version}"', content)
        
        with open("github_shell/utils/config.py", "w", encoding="utf-8") as f:
            f.write(new_content)
        updated_files.append("github_shell/utils/config.py")
    except Exception as e:
        print(f"更新config.py失败: {e}")
        return False
    
    print(f"✅ 已更新以下文件的版本号为 {version}:")
    for file in updated_files:
        print(f"  - {file}")
    return True


def create_git_tag(version):
    """创建Git标签"""
    tag_name = f"v{version}"
    success, result = run_command(["git", "tag", "-a", tag_name, "-m", f"Release version {version}"])
    if not success:
        return False
    
    success, result = run_command(["git", "push", "origin", tag_name])
    return success


def check_git_status():
    """检查Git状态"""
    success, result = run_command(["git", "status"])
    if not success:
        return False
    
    if "nothing to commit, working tree clean" in result.stdout:
        return True
    else:
        print("⚠️  Git工作树不干净，请先提交所有更改")
        return False


def push_to_github():
    """推送到GitHub"""
    # 拉取最新代码
    success, result = run_command(["git", "pull"])
    if not success:
        return False
    
    # 推送代码
    success, result = run_command(["git", "push"])
    return success


def get_release_notes(version):
    """获取发布说明"""
    notes = input("请输入发布说明 (Ctrl+D结束输入):\n").strip()
    if not notes:
        # 默认发布说明
        notes = f"Release version {version}\n\n更新内容:\n- 自动生成的发布说明"
    return notes


def update_changelog(version, release_notes):
    """更新CHANGELOG.md"""
    try:
        # 读取CHANGELOG.md
        with open("CHANGELOG.md", "r", encoding="utf-8") as f:
            content = f.read()
        
        # 获取当前日期
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # 准备新的版本条目
        new_version_entry = f"## [{version}] - {current_date}\n{release_notes}\n\n"
        
        # 替换[Unreleased]部分
        if "## [Unreleased]" in content:
            # 有未发布的更改
            new_content = re.sub(r"## \[Unreleased\]\n\n", f"## [Unreleased]\n\n{new_version_entry}", content)
        else:
            # 没有未发布的更改，直接在最前面添加
            new_content = f"## [Unreleased]\n\n{new_version_entry}{content}"
        
        # 写入更新后的内容
        with open("CHANGELOG.md", "w", encoding="utf-8") as f:
            f.write(new_content)
        
        print(f"✅ 已更新CHANGELOG.md，添加了版本 {version} 的发布说明")
        return True
    except Exception as e:
        print(f"更新CHANGELOG.md失败: {e}")
        return False


def main():
    """主函数"""
    print("GitHub Simulation Shell 发布工具")
    print("=" * 50)
    
    # 检查是否在开发者模式
    from github_shell.utils.config import get_mode
    if get_mode() != "developer":
        print("❌ 此命令仅在开发者模式下可用")
        print("请先切换到开发者模式: mode developer")
        sys.exit(1)
    
    # 检查Git状态
    if not check_git_status():
        sys.exit(1)
    
    # 获取当前版本
    current_version = get_current_version()
    if not current_version:
        print("无法获取当前版本号")
        sys.exit(1)
    
    print(f"当前版本: {current_version}")
    
    # 版本递增选项
    print("\n版本递增选项:")
    print("1. 手动输入版本号")
    print("2. 递增主版本号 (major) - 1.0.0 -> 2.0.0")
    print("3. 递增次版本号 (minor) - 1.0.0 -> 1.1.0")
    print("4. 递增补丁版本号 (patch) - 1.0.0 -> 1.0.1")
    print("5. 递增预发布版本 (pre) - 1.0.0 -> 1.0.0a1 或 1.0.0a1 -> 1.0.0a2")
    
    choice = input("请选择版本递增方式 (1-5, 默认: 1): ").strip()
    
    new_version = None
    if choice == "2":
        new_version = increment_version(current_version, "major")
    elif choice == "3":
        new_version = increment_version(current_version, "minor")
    elif choice == "4":
        new_version = increment_version(current_version, "patch")
    elif choice == "5":
        new_version = increment_version(current_version, "pre")
    
    # 如果自动递增失败或者用户选择手动输入，让用户手动输入
    if not new_version or choice == "1":
        new_version = input(f"输入新版本号 (默认: {current_version}): ").strip()
        if not new_version:
            new_version = current_version
    
    # 更新版本
    if update_version(new_version):
        print(f"✅ 版本已更新为 {new_version}")
    else:
        print("❌ 版本更新失败")
        sys.exit(1)
    
    # 获取发布说明
    release_notes = get_release_notes(new_version)
    
    # 更新CHANGELOG.md
    if not update_changelog(new_version, release_notes):
        sys.exit(1)
    
    # 提交更改
    success, result = run_command(["git", "add", "."])
    if not success:
        sys.exit(1)
    
    success, result = run_command([f"git", "commit", "-m", f"Release version {new_version}"])
    if not success:
        sys.exit(1)
    
    # 推送到GitHub
    if push_to_github():
        print("✅ 代码已推送到GitHub")
    else:
        print("❌ 代码推送失败")
        sys.exit(1)
    
    # 创建Git标签
    if create_git_tag(new_version):
        print(f"✅ 已创建标签 v{new_version}")
    else:
        print("❌ 标签创建失败")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print(f"🎉 发布成功！")
    print(f"版本: {new_version}")
    print(f"发布说明:\n{release_notes}")
    print("=" * 50)


if __name__ == "__main__":
    main()