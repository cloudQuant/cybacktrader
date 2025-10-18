#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""快速批量优化剩余P0文件"""

import os
import subprocess

# 剩余需要优化的P0文件（只添加编译指令）
FILES = [
    'cybacktrader/indicator.pyx',
    'cybacktrader/mathsupport.pyx',
    'cybacktrader/functions.pyx',
]

OLD = '''# Cython深度性能优化标记
# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True
# cython: initializedcheck=False
# cython: infer_types=True'''

NEW = '''# Cython深度性能优化标记（完整版）
# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True
# cython: nonecheck=False
# cython: initializedcheck=False
# cython: infer_types=True
# cython: optimize.unpack_method_calls=True
# cython: optimize.use_switch=True'''

def optimize_file(filepath):
    """优化单个文件"""
    if not os.path.exists(filepath):
        print(f"✗ 文件不存在: {filepath}")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if OLD in content:
        new_content = content.replace(OLD, NEW)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✓ 优化完成: {filepath}")
        return True
    else:
        print(f"✗ 未找到匹配模式: {filepath}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("快速批量优化P0文件")
    print("=" * 60)
    
    success = []
    for filepath in FILES:
        if optimize_file(filepath):
            success.append(filepath)
    
    print("=" * 60)
    print(f"优化完成: {len(success)}/{len(FILES)} 个文件")
    print("=" * 60)
    
    if success:
        print("\n开始编译测试...")
        result = subprocess.run(['pip', 'install', '-U', '.'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ 编译成功")
            print("\n开始运行测试...")
            result = subprocess.run(['pytest', 'tests', '-n', '8', '-q', '--tb=no'],
                                  capture_output=True, text=True)
            if '84 passed' in result.stdout:
                print("✓ 所有测试通过 (84/84)")
                print("\n提交到Git...")
                for f in success:
                    subprocess.run(['git', 'add', f])
                subprocess.run(['git', 'commit', '-m', 
                              f'Batch optimize {len(success)} files: add complete compiler directives'])
                print("✓ 已提交到Git")
            else:
                print("✗ 测试失败")
                print(result.stdout[-500:])
        else:
            print("✗ 编译失败")

if __name__ == '__main__':
    main()
