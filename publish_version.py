#!/usr/bin/env python3
"""
发布单个版本到PyPI的脚本
用法: python publish_version.py v1.0.0
"""

import os
import sys
import subprocess
import tempfile

def publish_version(version_tag):
    """发布指定版本到PyPI"""
    print(f"=== 发布版本: {version_tag} ===")
    
    # 提取版本号（去掉v前缀）
    version_number = version_tag[1:]
    print(f"版本号: {version_number}")
    
    # 构建项目
    print("构建项目...")
    subprocess.run([sys.executable, "-m", "build"])
    
    # 发布到PyPI
    print("发布到PyPI...")
    import os
    api_token = os.environ.get('PYPI_TOKEN')
    
    if not api_token:
        print("错误: 未设置PYPI_TOKEN环境变量")
        sys.exit(1)
    # 只上传当前版本的文件
    subprocess.run([sys.executable, "-m", "twine", "upload", f"dist/*{version_number}*", 
                  "-u", "__token__", "-p", api_token])
    
    print(f"✅ 版本 {version_tag} 发布成功!")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python publish_version.py <version_tag>")
        print("例如: python publish_version.py v1.0.0")
        sys.exit(1)
    
    version_tag = sys.argv[1]
    publish_version(version_tag)