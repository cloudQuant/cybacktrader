#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
为有外部依赖的模块添加条件导入
使它们可以编译成功（即使外部包未安装）
"""

import re
from pathlib import Path


# 需要修复的模块和它们的外部依赖
EXTERNAL_DEPS = {
    'influxfeed': ['influxdb'],
    'blaze': ['blaze', 'odo'],
    'pandafeed': ['pandas'],
    'quandl': ['quandl'],
    'pyfolio': ['pyfolio'],
    'ccxtfeed': ['ccxt'],
    'ccxtbroker': ['ccxt'],
    'ccxtstore': ['ccxt'],
    'ctpbroker': ['vnpy', 'ctp'],
    'ctpdata': ['vnpy', 'ctp'],
    'ctpstore': ['vnpy', 'ctp'],
    'ibbroker': ['ibpy', 'ib'],
    'ibdata': ['ibpy', 'ib'],
    'ibstore': ['ibpy', 'ib'],
    'oandabroker': ['oandav20'],
    'oanda': ['oandav20'],
    'oandastore': ['oandav20'],
    'vcbroker': ['visionchart'],
    'vcdata': ['visionchart'],
    'vchart': ['visionchart'],
    'vchartcsv': ['visionchart'],
    'vchartfile': ['visionchart'],
    'vcstore': ['visionchart'],
}


def add_safe_imports(file_path):
    """为文件添加安全的条件导入"""
    
    if not Path(file_path).exists():
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 为常见的外部依赖添加条件导入
    external_imports = [
        ('from influxdb import', 'influxdb', 'InfluxDBClient'),
        ('import ccxt', 'ccxt', None),
        ('import pandas as pd', 'pandas', 'pd'),
        ('import quandl', 'quandl', None),
        ('import pyfolio', 'pyfolio', None),
        ('from oandapyV20', 'oandapyV20', None),
        ('import blaze', 'blaze', None),
    ]
    
    for import_stmt, package, alias in external_imports:
        if import_stmt in content and f'try:\n    {import_stmt}' not in content:
            # 添加 try/except
            safe_import = f'''try:
    {import_stmt}
except ImportError:
    {alias or package} = None  # {package} not available'''
            
            content = content.replace(import_stmt, safe_import)
    
    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    
    return False


def main():
    print("=" * 70)
    print("为外部依赖模块添加安全导入")
    print("=" * 70)
    print()
    
    cybacktrader_dir = Path('cybacktrader')
    fixed = []
    
    # 修复所有有外部依赖的模块
    for module_name, deps in EXTERNAL_DEPS.items():
        # 查找对应的 .pyx 文件
        pyx_files = list(cybacktrader_dir.rglob(f'{module_name}.pyx'))
        
        for pyx_file in pyx_files:
            if add_safe_imports(pyx_file):
                print(f"[OK] 修复: {pyx_file.relative_to(cybacktrader_dir)}")
                fixed.append(str(pyx_file))
    
    print()
    print("=" * 70)
    print(f"[成功] 修复了 {len(fixed)} 个文件")
    print("=" * 70)
    print()
    print("现在重新编译:")
    print("  python setup.py build_ext --inplace")


if __name__ == '__main__':
    main()

