#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup script for cybacktrader with Cython compilation support
"""

from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize
import numpy as np
import os

# Compiler directives - enable safety checks for debugging
compiler_directives = {
    'language_level': '3',
    'boundscheck': True,   # Enable bounds checking for safety
    'wraparound': True,    # Enable negative indexing
    'cdivision': False,    # Use Python division semantics for safety
    'initializedcheck': True,
    'nonecheck': True,
    'embedsignature': True,
    'profile': False,
}

# C++ compiler settings
import sys
from setuptools.extension import Extension as _Extension

class Extension(_Extension):
    def __init__(self, *args, **kwargs):
        _Extension.__init__(self, *args, **kwargs)
        # Let Cython decide the language (will generate .c files by default)
        # No extra compiler flags for now

# Compile modules in dependency order
import glob
from pathlib import Path

# Try to compile all modules - don't skip any
# External dependencies will be handled with try/except in the code
# Skip mabase to keep it as pure Python (metaclass issues with Cython)
SKIP_MODULES = {'mabase'}

def should_compile(pyx_path):
    """Check if module should be compiled"""
    name = Path(pyx_path).stem
    if name in SKIP_MODULES:
        return False
    for skip_mod in SKIP_MODULES:
        if f'{skip_mod}' in str(pyx_path):
            return False
    return True

# Define compilation order based on dependencies
# Level 1: No internal dependencies
LEVEL_1 = [
    'cybacktrader/version.pyx',
    'cybacktrader/errors.pyx',
    'cybacktrader/mathsupport.pyx',
    'cybacktrader/utils/py3.pyx',
    'cybacktrader/utils/date.pyx',
    'cybacktrader/utils/autodict.pyx',
    'cybacktrader/utils/ordereddefaultdict.pyx',
    'cybacktrader/utils/dateintern.pyx',
    'cybacktrader/utils/flushfile.pyx',
    'cybacktrader/utils/fractal.pyx',
]

# Level 2: Depends on level 1
LEVEL_2 = [
    'cybacktrader/metabase.pyx',
    'cybacktrader/lineroot.pyx',
]

# Level 3: Core line structures
LEVEL_3 = [
    'cybacktrader/linebuffer.pyx',
    'cybacktrader/functions.pyx',
]

# Level 4: Depends on linebuffer
LEVEL_4 = [
    'cybacktrader/lineseries.pyx',
    'cybacktrader/dataseries.pyx',
    'cybacktrader/lineiterator.pyx',
]

# Level 5: Trading and analysis
LEVEL_5 = [
    'cybacktrader/order.pyx',
    'cybacktrader/trade.pyx',
    'cybacktrader/position.pyx',
    'cybacktrader/comminfo.pyx',
    'cybacktrader/indicator.pyx',
    'cybacktrader/analyzer.pyx',
    'cybacktrader/observer.pyx',
]

# Level 6: Execution
LEVEL_6 = [
    'cybacktrader/feed.pyx',
    'cybacktrader/broker.pyx',
    'cybacktrader/strategy.pyx',
    'cybacktrader/signal.pyx',
    'cybacktrader/store.pyx',
    'cybacktrader/sizer.pyx',
    'cybacktrader/writer.pyx',
    'cybacktrader/timer.pyx',
    'cybacktrader/fillers.pyx',
    'cybacktrader/flt.pyx',
    'cybacktrader/resamplerfilter.pyx',
    'cybacktrader/tradingcal.pyx',
]

# Level 7: Cerebro (depends on almost everything)
LEVEL_7 = [
    'cybacktrader/cerebro.pyx',
]

# Level 8: Sub-modules (depend on base modules)
LEVEL_8 = glob.glob('cybacktrader/**/*.pyx', recursive=True)

# Build ordered extension list
ordered_pyx = []
for level in [LEVEL_1, LEVEL_2, LEVEL_3, LEVEL_4, LEVEL_5, LEVEL_6, LEVEL_7]:
    ordered_pyx.extend(level)

# Add remaining modules from LEVEL_8
for pyx in LEVEL_8:
    pyx_normalized = pyx.replace('\\', '/')
    if pyx_normalized not in ordered_pyx and should_compile(pyx):
        ordered_pyx.append(pyx_normalized)

# Create extensions
ext_modules = []
for pyx_file in ordered_pyx:
    if not should_compile(pyx_file):
        continue
    module_path = pyx_file.replace('\\', '/').replace('.pyx', '').replace('/', '.')
    ext_modules.append(Extension(module_path, [pyx_file]))

print(f"\n[INFO] 将按顺序编译 {len(ext_modules)} 个模块")
print(f"[INFO] 跳过 {len(SKIP_MODULES)} 个有问题的模块")

setup(
    name='cybacktrader',
    version='0.1.0',
    description='Cython-accelerated, drop-in compatible interface for backtrader',
    long_description=open('README.md', encoding='utf-8').read() if os.path.exists('README.md') else '',
    long_description_content_type='text/markdown',
    author='cybacktrader maintainers',
    python_requires='>=3.8',
    packages=find_packages(include=['cybacktrader', 'cybacktrader.*']),
    install_requires=[
        # Core dependencies
    ],
    extras_require={
        'dev': [
            'cython>=3.0',
            'numpy',
            'pytest',
            'pytest-cov',
        ],
        'plotting': [
            'matplotlib',
        ],
    },
    ext_modules=cythonize(
        ext_modules,
        compiler_directives=compiler_directives,
        language_level='3',
        annotate=True,  # Generate HTML annotation files for optimization review
    ) if ext_modules else [],
    include_dirs=[np.get_include()] if ext_modules else [],
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Cython',
        'Topic :: Office/Business :: Financial',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

