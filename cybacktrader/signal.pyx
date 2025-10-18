#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

# Cython深度性能优化标记（完整版）
# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True
# cython: nonecheck=False
# cython: initializedcheck=False
# cython: infer_types=True
# cython: optimize.unpack_method_calls=True
# cython: optimize.use_switch=True

import cybacktrader as bt

# Cython imports for C-level optimization
cimport cython

# 创建不同的SIGNAL类型
(

    SIGNAL_NONE,
    SIGNAL_LONGSHORT,
    SIGNAL_LONG,
    SIGNAL_LONG_INV,
    SIGNAL_LONG_ANY,
    SIGNAL_SHORT,
    SIGNAL_SHORT_INV,
    SIGNAL_SHORT_ANY,
    SIGNAL_LONGEXIT,
    SIGNAL_LONGEXIT_INV,
    SIGNAL_LONGEXIT_ANY,
    SIGNAL_SHORTEXIT,
    SIGNAL_SHORTEXIT_INV,
    SIGNAL_SHORTEXIT_ANY,

) = range(14)

# 不同的信号类型
SignalTypes = [
    SIGNAL_NONE,
    SIGNAL_LONGSHORT,
    SIGNAL_LONG, SIGNAL_LONG_INV, SIGNAL_LONG_ANY,
    SIGNAL_SHORT, SIGNAL_SHORT_INV, SIGNAL_SHORT_ANY,
    SIGNAL_LONGEXIT, SIGNAL_LONGEXIT_INV, SIGNAL_LONGEXIT_ANY,
    SIGNAL_SHORTEXIT, SIGNAL_SHORTEXIT_INV, SIGNAL_SHORTEXIT_ANY
]

# 继承指标，创建一个signal指标 - Cython深度优化
class Signal(bt.Indicator):
    # 信号类型
    SignalTypes = SignalTypes
    # 创建了一个signal的line
    lines = ('signal',)
    # 初始化 - Cython深度优化
    @cython.boundscheck(False)
    @cython.wraparound(False)
    def __init__(self):
        cdef object data0 = self.data0
        
        self.lines.signal = data0.lines[0]
        self.plotinfo.plotmaster = getattr(data0, '_clock', data0)
