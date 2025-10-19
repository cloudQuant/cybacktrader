#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Utils package - import from compiled Cython modules"""
import warnings
# Import from compiled py3 module
try:
    from cybacktrader.utils.py3 import *
except ImportError:
    warnings.warn("无法导入 cybacktrader.utils.py3: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

# Import date functions from dateintern module
try:
    from cybacktrader.utils.dateintern import num2date, date2num, time2num, num2time, num2dt
except ImportError:
    # Fallback if dateintern module is not available
    warnings.warn("无法导入 cybacktrader.utils.dateintern: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

# Import from other compiled modules
try:
    from cybacktrader.utils.autodict import *
except ImportError:
    warnings.warn("无法导入 cybacktrader.utils.autodict: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

try:
    from cybacktrader.utils.ordereddefaultdict import *
except ImportError:
    warnings.warn("无法导入 cybacktrader.utils.ordereddefaultdict: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

try:
    from cybacktrader.utils.dateintern import *
except ImportError:
    warnings.warn("无法导入 cybacktrader.utils.dateintern: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

try:
    from cybacktrader.utils.flushfile import *
except ImportError:
    warnings.warn("无法导入 cybacktrader.utils.flushfile: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

# fractal is imported separately to avoid circular imports
# from cybacktrader.utils.fractal import *
