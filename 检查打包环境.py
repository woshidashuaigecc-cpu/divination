#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
占卜起卦 - 打包前检查脚本
检查所有必需的工具和配置是否已正确安装
"""

import subprocess
import sys
import os
import shutil

def check_command(cmd, display_name):
    """检查命令是否可用"""
    try:
        result = subprocess.run([cmd, '--version'], 
                              capture_output=True, 
                              text=True,
                              timeout=5)
        if result.returncode == 0:
            print(f"✓ {display_name}: 已安装")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print(f"✗ {display_name}: 未找到")
    return False

def check_python_package(package_name):
    """检查 Python 包是否已安装"""
    try:
        __import__(package_name)
        print(f"✓ Python 包 {package_name}: 已安装")
        return True
    except ImportError:
        print(f"✗ Python 包 {package_name}: 未安装")
        return False

def main():
    print("=" * 50)
    print("  占卜起卦 - 打包环境检查")
    print("=" * 50)
    print()
    
    all_ok = True
    
    # 检查 Python
    print("【检查 Python】")
    if not check_command('python', 'Python'):
        print("  提示: 请安装 Python 3.9+")
        all_ok = False
    else:
        # 检查 Python 版本
        try:
            result = subprocess.run(['python', '--version'], 
                                  capture_output=True, 
                                  text=True)
            print(f"  版本: {result.stdout.strip()}")
        except:
            pass
    print()
    
    # 检查 Java
    print("【检查 Java】")
    if not check_command('java', 'Java JDK'):
        print("  提示: 请安装 Java JDK 11 或更高版本")
        print("  下载: https://www.oracle.com/java/technologies/downloads/")
        all_ok = False
    else:
        try:
            result = subprocess.run(['java', '--version'], 
                                  capture_output=True, 
                                  text=True)
            print(f"  {result.stderr.split(chr(10))[0]}")
        except:
            pass
    print()
    
    # 检查 Android SDK
    print("【检查 Android SDK】")
    android_sdk = os.environ.get('ANDROID_SDK_ROOT')
    if android_sdk:
        print(f"✓ Android SDK 路径: {android_sdk}")
    else:
        print("✗ ANDROID_SDK_ROOT 环境变量未设置")
        print("  提示: 请从 https://developer.android.com/studio 下载 Android Studio")
        all_ok = False
    print()
    
    # 检查 Python 包
    print("【检查 Python 包】")
    packages = ['kivy', 'buildozer', 'cython']
    missing_packages = []
    for pkg in packages:
        if not check_python_package(pkg):
            missing_packages.append(pkg)
    
    if missing_packages:
        print()
        print(f"  要安装缺失的包，运行:")
        print(f"  pip install {' '.join(missing_packages)}")
        all_ok = False
    print()
    
    # 总结
    print("=" * 50)
    if all_ok:
        print("✓ 所有检查通过！可以开始打包")
        print()
        print("下一步:")
        print("1. 运行: buildozer android debug")
        print("2. 等待编译完成")
        print("3. APK 将在 bin/ 文件夹中")
        return 0
    else:
        print("✗ 存在问题，请按照提示进行修复")
        print()
        print("常见问题:")
        print("- 确保已安装最新的 Visual C++ Build Tools")
        print("- 确保 JAVA_HOME 和 ANDROID_SDK_ROOT 环境变量正确")
        print("- 如需帮助，参见: 打包手机app说明.md")
        return 1

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n已取消")
        sys.exit(1)
