#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
批量优化P1文件 - 添加Cython编译指令
"""
import os
import re
from pathlib import Path

# P1文件路径
INDICATORS_DIR = Path("cybacktrader/indicators")
ANALYZERS_DIR = Path("cybacktrader/analyzers")

# 优化模板 - 保守设置
CONSERVATIVE_DIRECTIVES = """# Cython性能优化标记（保守设置）
# cython: language_level=3
# cython: infer_types=True"""

# 深度优化模板 - 用于计算密集型文件
AGGRESSIVE_DIRECTIVES = """# Cython深度性能优化标记
# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True
# cython: initializedcheck=False
# cython: infer_types=True"""


def process_file(filepath, aggressive=False):
    """处理单个文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已经优化过
    if 'cython: infer_types' in content:
        print(f"  [SKIP] Already optimized: {filepath.name}")
        return False
    
    # 查找现有的Cython标记
    pattern = r'(#!/usr/bin/env python\n# -\*- coding: utf-8.*?\n\n)(# Cython.*?\n# cython: language_level=3\n)'
    
    directives = AGGRESSIVE_DIRECTIVES if aggressive else CONSERVATIVE_DIRECTIVES
    
    # 替换现有标记
    new_content = re.sub(pattern, r'\1' + directives + '\n', content, flags=re.DOTALL)
    
    # 如果没有找到标记，在文件开头添加
    if new_content == content:
        lines = content.split('\n')
        # 找到编码行
        insert_pos = 2  # 默认在第3行
        for i, line in enumerate(lines[:5]):
            if 'coding:' in line or '-*-' in line:
                insert_pos = i + 2
                break
        
        lines.insert(insert_pos, '')
        lines.insert(insert_pos + 1, directives)
        new_content = '\n'.join(lines)
    
    # 写回文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  [OK] Optimized: {filepath.name}")
    return True


def batch_optimize_indicators():
    """批量优化indicators"""
    print("\n[INFO] Batch optimizing indicators/...")
    files = list(INDICATORS_DIR.glob("*.pyx"))
    files.extend(list(INDICATORS_DIR.glob("contrib/*.pyx")))
    
    # 计算密集型文件使用深度优化
    aggressive_files = {
        'sma.pyx', 'ema.pyx', 'wma.pyx', 'dema.pyx', 'tema.pyx',
        'rsi.pyx', 'macd.pyx', 'atr.pyx', 'bollinger.pyx',
        'stochastic.pyx', 'cci.pyx', 'momentum.pyx'
    }
    
    count = 0
    for filepath in sorted(files):
        is_aggressive = filepath.name in aggressive_files
        if process_file(filepath, aggressive=is_aggressive):
            count += 1
    
    print(f"[DONE] indicators optimized: {count}/{len(files)} files")
    return count


def batch_optimize_analyzers():
    """批量优化analyzers"""
    print("\n[INFO] Batch optimizing analyzers/...")
    
    if not ANALYZERS_DIR.exists():
        print("  [WARN] analyzers directory not found")
        return 0
    
    files = list(ANALYZERS_DIR.glob("*.pyx"))
    count = 0
    for filepath in sorted(files):
        # analyzers使用保守优化
        if process_file(filepath, aggressive=False):
            count += 1
    
    print(f"[DONE] analyzers optimized: {count}/{len(files)} files")
    return count


if __name__ == "__main__":
    print("=" * 70)
    print("Batch Optimize P1 Files (indicators + analyzers)")
    print("=" * 70)
    
    total = 0
    total += batch_optimize_indicators()
    total += batch_optimize_analyzers()
    
    print("\n" + "=" * 70)
    print(f"[SUCCESS] Batch optimization complete! Total: {total} files")
    print("=" * 70)
    print("\n下一步：")
    print("  1. pip install -U .")
    print("  2. pytest tests -n 8")
