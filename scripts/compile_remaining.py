#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
编译剩余的 .pyx 模块
"""

from setuptools import setup, Extension
from Cython.Build import cythonize
import glob

compiler_directives = {
    'language_level': '3',
    'boundscheck': False,
    'wraparound': False,
    'cdivision': True,
}

# 手动添加需要编译但还未编译的模块
remaining_modules = [
    "cybacktrader.version",
    "cybacktrader.errors",
    "cybacktrader.signal",
    "cybacktrader.store",
    "cybacktrader.resamplerfilter",
    "cybacktrader.cerebro",
    "cybacktrader.flt",
    "cybacktrader.fillers",
    "cybacktrader.tradingcal",
    "cybacktrader.metabase",
]

ext_modules = []
for mod in remaining_modules:
    pyx_file = mod.replace('.', '/') + '.pyx'
    ext_modules.append(Extension(mod, [pyx_file]))

print(f"编译 {len(ext_modules)} 个剩余模块...")
for ext in ext_modules:
    print(f"  {ext.name}")

setup(
    name='cybacktrader-remaining',
    ext_modules=cythonize(ext_modules, compiler_directives=compiler_directives),
)

