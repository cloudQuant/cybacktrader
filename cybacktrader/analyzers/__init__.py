#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

# Import from compiled Cython analyzer modules
# Import in order to avoid circular dependencies

# Base analyzers without external dependencies
try:
    from cybacktrader.analyzers.timereturn import *
except ImportError:
    pass

try:
    from cybacktrader.analyzers.tradeanalyzer import *
except ImportError:
    pass

try:
    from cybacktrader.analyzers.sqn import *
except ImportError:
    pass

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

try:
    from cybacktrader.analyzers.total_value import *
except ImportError:
    pass

try:
    from cybacktrader.analyzers.transactions import *
except ImportError:
    pass

try:
    from cybacktrader.analyzers.vwr import *
except ImportError:
    pass

try:
    from cybacktrader.analyzers.periodstats import *
except ImportError:
    pass

try:
    from cybacktrader.analyzers.calmar import *
except ImportError:
    pass

# Skip logreturnsrolling, positions, pyfolio, sharpe_ratio_stats, leverage
# to avoid potential circular imports or external dependencies
# They can be imported directly when needed
