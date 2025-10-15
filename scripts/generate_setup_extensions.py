#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
生成 setup.py 的 Extension 列表
只包含核心模块，跳过有外部依赖的模块
"""

import glob
from pathlib import Path

# 跳过这些模块（有特殊外部依赖或不需要编译）
SKIP_MODULES = {
    # 外部依赖相关
    'influxfeed',
    'pandafeed', 
    'quandl',
    'ccxtfeed',
    'ccxtbroker',
    'ccxtstore',
    'ctpbroker',
    'ctpdata',
    'ctpstore',
    'ibbroker',
    'ibdata',
    'ibstore',
    'oandabroker',
    'oanda',
    'oandastore',
    'vcbroker',
    'vcdata',
    'vchart',
    'vchartcsv',
    'vchartfile',
    'vcstore',
    'blaze',
    'pyfolio',
    
    # Plot 相关（matplotlib 依赖）
    'plot',
    'finance',
    'formatters',
    'locator',
    'multicursor',
    'scheme',
    
    # 其他
    'talib',  # 需要 TA-Lib
}


def should_compile(pyx_path):
    """判断是否应该编译此文件"""
    name = Path(pyx_path).stem
    
    # 检查是否在跳过列表中
    if name in SKIP_MODULES:
        return False
    
    # 检查路径中是否包含跳过的模块
    for skip_mod in SKIP_MODULES:
        if f'\\{skip_mod}\\' in pyx_path or f'/{skip_mod}/' in pyx_path:
            return False
        if pyx_path.endswith(f'\\{skip_mod}.pyx') or pyx_path.endswith(f'/{skip_mod}.pyx'):
            return False
    
    return True


def main():
    pyx_files = glob.glob('cybacktrader/**/*.pyx', recursive=True)
    
    # 过滤文件
    compile_list = [f for f in pyx_files if should_compile(f)]
    skip_list = [f for f in pyx_files if not should_compile(f)]
    
    print(f"Total .pyx files: {len(pyx_files)}")
    print(f"Will compile: {len(compile_list)}")
    print(f"Will skip: {len(skip_list)}")
    print()
    
    # 生成 Extension 代码
    print("# Copy this to setup.py:")
    print("ext_modules = [")
    
    for pyx in sorted(compile_list):
        module_path = pyx.replace('\\', '/').replace('.pyx', '').replace('/', '.')
        print(f'    Extension("{module_path}", ["{pyx.replace(chr(92), "/")}"]),')
    
    print("]")
    
    if skip_list:
        print("\n# Skipped modules:")
        for skip in sorted(skip_list):
            print(f"#   {skip}")


if __name__ == '__main__':
    main()





