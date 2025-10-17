#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

# Cython性能优化标记
# cython: language_level=3

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

# backtrader版本号
__version__ = '0.1.0'

# backtrader版本号，元组格式
__btversion__ = tuple(int(x) for x in __version__.split('.'))
