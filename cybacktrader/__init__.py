#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

"""
cybacktrader - Cython-accelerated backtrader

All imports use cybacktrader modules
"""

# Version
import warnings
try:
    from cybacktrader.version import __version__, __btversion__
except ImportError:
    warnings.warn("无法导入 cybacktrader.version: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

# Errors
try:
    from cybacktrader.errors import *
except ImportError:
    warnings.warn("无法导入 cybacktrader.errors: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)
from cybacktrader import errors as errors

# Utils - import from backtrader to avoid issues
try:
    from cybacktrader.utils import *
except ImportError:
    warnings.warn("无法导入 cybacktrader.utils: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

# Core line structures
try:
    from cybacktrader.linebuffer import *
except ImportError:
    warnings.warn("无法导入 cybacktrader.linebuffer: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

try:
    from cybacktrader.functions import *
except ImportError:
    warnings.warn("无法导入 cybacktrader.functions: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

# Trading objects
try:
    from cybacktrader.order import *
except ImportError:
    warnings.warn("无法导入 cybacktrader.order: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

try:
    from cybacktrader.comminfo import *
except ImportError:
    warnings.warn("无法导入 cybacktrader.comminfo: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

try:
    from cybacktrader.trade import *
except ImportError:
    warnings.warn("无法导入 cybacktrader.trade: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

try:
    from cybacktrader.position import *
except ImportError:
    warnings.warn("无法导入 cybacktrader.position: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

# Store
try:
    from cybacktrader.store import Store
except ImportError:
    warnings.warn("无法导入 cybacktrader.store: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

# Broker
try:
    from cybacktrader import broker as broker
except ImportError:
    warnings.warn("无法导入 cybacktrader.broker: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

try:
    from cybacktrader.broker import *
except ImportError:
    warnings.warn("无法导入 cybacktrader.broker: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

# Line series
try:
    from cybacktrader.lineseries import *
except ImportError:
    warnings.warn("无法导入 cybacktrader.lineseries: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

try:
    from cybacktrader.dataseries import *
except ImportError:
    warnings.warn("无法导入 cybacktrader.dataseries: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

try:
    from cybacktrader.feed import *
except ImportError:
    warnings.warn("无法导入 cybacktrader.feed: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

try:
    from cybacktrader.resamplerfilter import *
except ImportError:
    warnings.warn("无法导入 cybacktrader.resamplerfilter: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

# Iterators
try:
    from cybacktrader.lineiterator import *
except ImportError:
    warnings.warn("无法导入 cybacktrader.lineiterator: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

try:
    from cybacktrader.indicator import *
except ImportError:
    warnings.warn("无法导入 cybacktrader.indicator: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

try:
    from cybacktrader.analyzer import *
except ImportError:
    warnings.warn("无法导入 cybacktrader.analyzer: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

try:
    from cybacktrader.observer import *
except ImportError:
    warnings.warn("无法导入 cybacktrader.observer: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

try:
    from cybacktrader.sizer import *
except ImportError:
    warnings.warn("无法导入 cybacktrader.sizer: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

try:
    from cybacktrader.sizers import SizerFix  # old sizer for compatibility
except ImportError:
    warnings.warn("无法导入 cybacktrader.sizers: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

try:
    from cybacktrader.strategy import *
except ImportError:
    warnings.warn("无法导入 cybacktrader.strategy: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

try:
    from cybacktrader.writer import *
except ImportError:
    warnings.warn("无法导入 cybacktrader.writer: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

try:
    from cybacktrader.signal import *
except ImportError:
    warnings.warn("无法导入 cybacktrader.signal: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

# Cerebro
try:
    from cybacktrader.cerebro import *
except ImportError:
    warnings.warn("无法导入 cybacktrader.cerebro: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

try:
    from cybacktrader.timer import *
except ImportError:
    warnings.warn("无法导入 cybacktrader.timer: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

try:
    from cybacktrader.flt import *
except ImportError:
    warnings.warn("无法导入 cybacktrader.flt: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

# Submodules  
try:
    from cybacktrader import utils as utils
except ImportError:
    warnings.warn("无法导入 cybacktrader.utils: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

try:
    from cybacktrader import feeds as feeds
except ImportError:
    warnings.warn("无法导入 cybacktrader.feeds: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

# Indicators are loaded separately to avoid circular imports
# Users can import directly: from cybacktrader.indicators.sma import SMA
try:
    from cybacktrader import indicators as indicators
except ImportError:
    warnings.warn("无法导入 cybacktrader.indicators: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

try:
    from cybacktrader import indicators as ind
except ImportError:
    warnings.warn("无法导入 cybacktrader.indicators: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

try:
    from cybacktrader import observers as observers
except ImportError:
    warnings.warn("无法导入 cybacktrader.observers: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

try:
    from cybacktrader import observers as obs
except ImportError:
    warnings.warn("无法导入 cybacktrader.observers: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

try:
    from cybacktrader import analyzers as analyzers
except ImportError:
    warnings.warn("无法导入 cybacktrader.analyzers: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

try:
    from cybacktrader import commissions as commissions
except ImportError:
    warnings.warn("无法导入 cybacktrader.commissions: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

try:
    from cybacktrader import commissions as comms
except ImportError:
    warnings.warn("无法导入 cybacktrader.commissions: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

try:
    from cybacktrader import filters as filters
except ImportError:
    warnings.warn("无法导入 cybacktrader.filters: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

try:
    from cybacktrader import signals as signals
except ImportError:
    warnings.warn("无法导入 cybacktrader.signals: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

try:
    from cybacktrader import sizers as sizers
except ImportError:
    warnings.warn("无法导入 cybacktrader.sizers: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

try:
    from cybacktrader import stores as stores
except ImportError:
    warnings.warn("无法导入 cybacktrader.stores: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

try:
    from cybacktrader import brokers as brokers
except ImportError:
    warnings.warn("无法导入 cybacktrader.brokers: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

try:
    from cybacktrader import timer as timer
except ImportError:
    warnings.warn("无法导入 cybacktrader.timer: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

try:
    from cybacktrader import talib as talib
except ImportError:
    warnings.warn("无法导入 cybacktrader.talib: 请确保从已安装的包导入，而不是源码目录。", ImportWarning)

__all__ = ['__version__', '__btversion__', 'version', 'errors', 'mathsupport', 'utils', 'metabase', 'lineroot', 'linebuffer', 'functions', 'lineseries', 'dataseries', 'lineiterator', 'indicator', 'analyzer', 'observer', 'order', 'trade', 'position', 'comminfo', 'broker', 'feed', 'fillers', 'flt', 'resamplerfilter', 'tradingcal', 'cerebro', 'writer', 'signal', 'store', 'sizer', 'timer', 'talib', 'indicators', 'observers', 'analyzers', 'commissions', 'filters', 'signals', 'sizers', 'stores', 'brokers', 'timer', 'talib', 'utils', 'feeds', 'indicators', 'observers', 'analyzers', 'commissions', 'filters', 'signals', 'sizers', 'stores', 'brokers', 'timer', 'talib']
