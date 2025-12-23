#!/usr/bin/env python3

# 构建包的脚本
import subprocess
import sys

print("GitHub Shell 包构建工具")
print("=" * 50)

# 安装构建依赖
print("正在安装构建依赖...")
deps_result = subprocess.run([
    sys.executable, "-m", "pip", "install", "--upgrade", "build", "twine"
], capture_output=False, text=True)

if deps_result.returncode != 0:
    print("❌ 安装依赖失败")
    sys.exit(1)

# 构建包
print("\n正在构建包...")
build_result = subprocess.run([
    sys.executable, "-m", "build"
], capture_output=False, text=True)

if build_result.returncode == 0:
    print("\n✅ 包构建成功！")
    print("\n构建产物：")
    list_result = subprocess.run(["dir", "dist/"], shell=True, capture_output=True, text=True)
    print(list_result.stdout)
else:
    print("❌ 构建失败")
    sys.exit(1)
