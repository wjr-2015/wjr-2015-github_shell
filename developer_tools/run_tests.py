#!/usr/bin/env python3

# 运行测试的脚本
import subprocess
import sys

print("GitHub Shell 测试运行工具")
print("=" * 50)

# 运行测试
print("正在运行测试...")
result = subprocess.run([
    sys.executable, "-m", "pytest", "github_shell/tests/", "-v"
], capture_output=False, text=True)

if result.returncode == 0:
    print("✅ 所有测试通过")
else:
    print("❌ 测试失败")
    sys.exit(1)
