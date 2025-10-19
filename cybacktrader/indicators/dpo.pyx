#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

# Cython性能优化标记（保守设置）
# cython: language_level=3
# cython: infer_types=True
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True

# Python 2/3 compatibility imports

from cybacktrader.indicator import Indicator
from cybacktrader.indicators.mabase import MovAv

# 去除趋势后的价格波动
class DetrendedPriceOscillator(Indicator):
    '''
    Defined by Joe DiNapoli in his book *"Trading with DiNapoli levels"*

    It measures the price variations against a Moving Average (the trend)
    and therefore removes the "trend" factor from the price.

    Formula:
      - movav = MovingAverage(close, period)
      - dpo = close - movav(shifted period / 2 + 1)

    See:
      - http://en.wikipedia.org/wiki/Detrended_price_oscillator
    '''
    # Named alias for invocation
    alias = ('DPO',)

    # Named output lines
    lines = ('dpo',)

    # Accepted parameters (and defaults) -
    # MovAvg also parameter to allow experimentation
    params = (('period', 20), ('movav', MovAv.Simple))

    # Emphasize central 0.0 line in plot
    plotinfo = dict(plothlines=[0.0])

    # Indicator information after the name (in brackets)
    def _plotlabel(self):
        plabels = [self.p.period]
        plabels += [self.p.movav] * self.p.notdefault('movav')
        return plabels

    def __init__(self):
        # Create the Moving Average
        ma = self.p.movav(self.data, period=self.p.period)

        # Calculate value (look back period/2 + 1 in MA) and bind to 'dpo' line
        self.lines.dpo = self.data - ma(-self.p.period // 2 + 1)
        # 保存引用以便 once 中使用高效数组访问
        self._ma_ref = ma

        super(DetrendedPriceOscillator, self).__init__()

    def once(self, int start, int end):
        # Cython深度优化：使用 typed memoryviews 与 C 循环
        cdef int i
        cdef int shift = self.p.period // 2 - 1  # 对应 ma(-period//2 + 1)
        cdef double[:] dst = self.lines.dpo.array
        cdef double[:] src = self.data.array
        cdef double[:] ma_arr = self._ma_ref.array

        for i in range(start, end):
            dst[i] = src[i] - ma_arr[i - shift]
