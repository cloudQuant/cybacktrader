#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

# Import from compiled Cython feed modules
# Import basic feeds without external dependencies
try:
    from cybacktrader.feeds.btcsv import *
except ImportError:
    pass

try:
    from cybacktrader.feeds.csvgeneric import *
except ImportError:
    pass

try:
    from cybacktrader.feeds.chainer import *
except ImportError:
    pass

try:
    from cybacktrader.feeds.rollover import *
except ImportError:
    pass

# Skip influxfeed, pandafeed, ccxtfeed, yahoo, etc as they may have external dependencies
