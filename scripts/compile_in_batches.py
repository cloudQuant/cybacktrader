#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
分批编译 .pyx 文件，跳过有错误的继续编译其他的
"""

from setuptools import setup, Extension
from Cython.Build import cythonize
import glob
from pathlib import Path

compiler_directives = {
    'language_level': '3',
}

# 已知会失败的模块（有特殊依赖）
KNOWN_FAILURES = {
    'influxfeed', 'vchartcsv', 'atr',  # 有未声明的名称
}

def get_compilable_modules():
    """获取所有可编译的模块"""
    extensions = []
    
    for pyx_file in glob.glob('cybacktrader/**/*.pyx', recursive=True):
        # 检查是否已有 .pyd
        pyd_file = pyx_file.replace('.pyx', '.cp313-win_amd64.pyd')
        if Path(pyd_file).exists():
            continue  # 已编译，跳过
        
        # 检查是否在失败列表
        name = Path(pyx_file).stem
        if name in KNOWN_FAILURES:
            continue
        
        module_path = pyx_file.replace('\\', '/').replace('.pyx', '').replace('/', '.')
        extensions.append(Extension(module_path, [pyx_file.replace('\\', '/')]))
    
    return extensions

ext_modules = get_compilable_modules()

print(f"\n[INFO] 将编译 {len(ext_modules)} 个剩余模块")
print("前20个:")
for ext in ext_modules[:20]:
    print(f"  {ext.name}")

if ext_modules:
    setup(
        name='cybacktrader-batch',
        ext_modules=cythonize(ext_modules, compiler_directives=compiler_directives, force=False),
    )
else:
    print("\n[INFO] 所有模块已编译完成!")

