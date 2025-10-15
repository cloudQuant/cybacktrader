#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

# Import from compiled Cython analyzer modules
# Import in order to avoid circular dependencies

# Base analyzers without external dependencies
from cybacktrader.analyzers.timereturn import *
from cybacktrader.analyzers.tradeanalyzer import *
from cybacktrader.analyzers.sqn import *

# Import analyzers that may have dependencies
try:
    from cybacktrader.analyzers.annualreturn import *
except ImportError:
    pass

try:
    from cybacktrader.analyzers.drawdown import *
except ImportError:
    pass

try:
    from cybacktrader.analyzers.returns import *
except ImportError:
    pass

try:
    from cybacktrader.analyzers.sharpe import *
except ImportError:
    pass

# Skip calmar, leverage, logreturnsrolling, periodstats, positions, pyfolio, 
# sharpe_ratio_stats, total_value, transactions, vwr to avoid circular imports
# They can be imported directly when needed
