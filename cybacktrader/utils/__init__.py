#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Utils package - import from compiled Cython modules"""

# Import from compiled py3 module
from cybacktrader.utils.py3 import *

# Import date functions from dateintern module
try:
    from cybacktrader.utils.dateintern import num2date, date2num, time2num, num2time, num2dt
except ImportError:
    # Fallback if dateintern module is not available
    pass

# Import from other compiled modules
try:
    from cybacktrader.utils.autodict import *
except ImportError:
    pass

try:
    from cybacktrader.utils.ordereddefaultdict import *
except ImportError:
    pass

try:
    from cybacktrader.utils.dateintern import *
except ImportError:
    pass

try:
    from cybacktrader.utils.flushfile import *
except ImportError:
    pass

# fractal is imported separately to avoid circular imports
# from cybacktrader.utils.fractal import *
