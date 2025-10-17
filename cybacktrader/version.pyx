#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

# Cython深度性能优化标记
# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True

# backtrader版本号
__version__ = '0.1.0'

# backtrader版本号，元组格式
__btversion__ = tuple(int(x) for x in __version__.split('.'))
