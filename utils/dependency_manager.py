#!/usr/bin/env python3
"""
依赖管理模块
用于自动检测和安装缺失的依赖库
"""

import subprocess
import sys

def check_and_install_dependencies():
    """检查并安装缺失的依赖库
    
    Returns:
        bool: 是否成功安装所有依赖
    """
    print("🔍 检查依赖库...")
    
    # 定义所需的依赖库
    required_dependencies = [
        "requests>=2.25.0"
    ]
    
    missing_dependencies = []
    
    # 检查每个依赖库
    for dep in required_dependencies:
        # 提取库名（忽略版本要求）
        lib_name = dep.split('>=')[0].split('<=')[0].split('==')[0].strip()
        
        try:
            # 尝试导入库
            __import__(lib_name)
            print(f"✅ {lib_name} 已安装")
        except ImportError:
            # 库未安装，添加到缺失列表
            missing_dependencies.append(dep)
            print(f"❌ {lib_name} 未安装")
    
    # 如果有缺失的依赖，尝试安装
    if missing_dependencies:
        print(f"\n📦 发现 {len(missing_dependencies)} 个缺失依赖，尝试安装...")
        
        try:
            # 使用pip安装所有缺失的依赖
            subprocess.check_call([
                sys.executable, "-m", "pip", "install"
            ] + missing_dependencies, 
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)
            print("✅ 所有依赖安装成功！")
            return True
        except subprocess.CalledProcessError:
            print("❌ 依赖安装失败，请手动安装：")
            for dep in missing_dependencies:
                print(f"  pip install {dep}")
            return False
    
    print("✅ 所有依赖已安装")
    return True

def check_module(module_name):
    """检查单个模块是否存在
    
    Args:
        module_name: 模块名称
        
    Returns:
        bool: 模块是否存在
    """
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False

def install_module(module_name):
    """安装单个模块
    
    Args:
        module_name: 模块名称
        
    Returns:
        bool: 是否安装成功
    """
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", module_name
        ], 
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False
