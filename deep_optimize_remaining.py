#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
深度优化P1剩余文件 - 添加aggressive Cython编译指令
对计算密集型文件进行最大化性能优化
"""
import os
import re
from pathlib import Path

# 深度优化模板
AGGRESSIVE_DIRECTIVES = """# Cython深度性能优化标记
# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True
# cython: initializedcheck=False
# cython: infer_types=True"""

# 保守优化模板
CONSERVATIVE_DIRECTIVES = """# Cython性能优化标记（保守设置）
# cython: language_level=3
# cython: infer_types=True"""


def upgrade_to_aggressive(filepath):
    """将保守优化升级为深度优化"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已经是深度优化
    if 'boundscheck=False' in content:
        print(f"  [SKIP] Already aggressive: {filepath.name}")
        return False
    
    # 查找并替换优化指令
    patterns = [
        # 匹配保守设置
        r'# Cython性能优化标记\（保守设置\）\n# cython: language_level=3\n# cython: infer_types=True',
        # 匹配基本设置
        r'# Cython性能优化标记\n# cython: language_level=3\n# cython: infer_types=True',
        # 匹配简单设置
        r'# Cython性能优化标记\n# cython: language_level=3(?:\n)?',
    ]
    
    new_content = content
    replaced = False
    for pattern in patterns:
        if re.search(pattern, content):
            new_content = re.sub(pattern, AGGRESSIVE_DIRECTIVES, content)
            replaced = True
            break
    
    if not replaced:
        print(f"  [WARN] Pattern not found in: {filepath.name}")
        return False
    
    # 写回文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  [UPGRADED] {filepath.name}")
    return True


def add_cdef_optimizations(filepath):
    """为关键循环添加cdef声明"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找once方法中的循环，添加cdef int i
    pattern = r'(def once\(self[^)]*\):.*?)(for i in range\()'
    
    def add_cdef(match):
        method_def = match.group(1)
        for_loop = match.group(2)
        
        # 检查是否已有cdef
        if 'cdef int i' in method_def or 'cdef Py_ssize_t i' in method_def:
            return match.group(0)
        
        # 在for循环前添加cdef
        indent = '        '  # 假设是8空格缩进
        return method_def + f'{indent}cdef int i\n{indent}' + for_loop
    
    new_content = re.sub(pattern, add_cdef, content, flags=re.DOTALL)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False


def deep_optimize_file(filepath, add_cdef=False):
    """深度优化单个文件"""
    upgraded = upgrade_to_aggressive(filepath)
    
    if add_cdef and upgraded:
        if add_cdef_optimizations(filepath):
            print(f"    + Added cdef optimizations")
    
    return upgraded


def main():
    print("=" * 70)
    print("Deep Optimization for Remaining P1 Files")
    print("=" * 70)
    
    # 需要升级为深度优化的文件
    files_to_upgrade = [
        # 核心基类
        Path("cybacktrader/analyzer.pyx"),
        
        # 高频使用的indicators（从保守升级到深度）
        Path("cybacktrader/indicators/basicops.pyx"),
        Path("cybacktrader/indicators/crossover.pyx"),
        Path("cybacktrader/indicators/deviation.pyx"),
        Path("cybacktrader/indicators/envelope.pyx"),
        Path("cybacktrader/indicators/oscillator.pyx"),
        Path("cybacktrader/indicators/percentchange.pyx"),
        Path("cybacktrader/indicators/percentrank.pyx"),
        
        # 技术指标深度优化
        Path("cybacktrader/indicators/directionalmove.pyx"),
        Path("cybacktrader/indicators/hadelta.pyx"),
        Path("cybacktrader/indicators/heikinashi.pyx"),
        Path("cybacktrader/indicators/pivotpoint.pyx"),
        Path("cybacktrader/indicators/psar.pyx"),
        
        # 分析器优化
        Path("cybacktrader/analyzers/returns.pyx"),
        Path("cybacktrader/analyzers/drawdown.pyx"),
        Path("cybacktrader/analyzers/sharpe.pyx"),
        Path("cybacktrader/analyzers/timereturn.pyx"),
    ]
    
    print("\n[INFO] Upgrading files to aggressive optimization...")
    count = 0
    for filepath in files_to_upgrade:
        if filepath.exists():
            # 对有循环的文件添加cdef
            add_cdef = 'indicators' in str(filepath)
            if deep_optimize_file(filepath, add_cdef=add_cdef):
                count += 1
        else:
            print(f"  [NOT FOUND] {filepath}")
    
    print(f"\n[DONE] Upgraded {count} files to aggressive optimization")
    
    # 处理mabase.py - 元类文件保持Python不转换
    print("\n[INFO] Checking mabase.py...")
    mabase_py = Path("cybacktrader/indicators/mabase.py")
    if mabase_py.exists():
        print("  [INFO] mabase.py contains metaclass - keeping as .py for compatibility")
    
    print("\n" + "=" * 70)
    print(f"[SUCCESS] Deep optimization complete! Total: {count} files")
    print("=" * 70)
    print("\nNext steps:")
    print("  1. pip install -U .")
    print("  2. pytest tests -n 8")
    print("  3. python benchmarks/ma_crossover_benchmark.py")


if __name__ == "__main__":
    main()
