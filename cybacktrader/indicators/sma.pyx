#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

# Cython深度性能优化标记
# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True
# cython: initializedcheck=False
# cython: infer_types=True
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True

from cybacktrader.indicators.mabase import MovingAverageBase
from cybacktrader.indicators.basicops import Average

# 移动平均线指标
class MovingAverageSimple(MovingAverageBase):
    """
    Non-weighted average of the last n periods

    Formula:
      - movav = Sum(data, period) / period

    See also:
      - http://en.wikipedia.org/wiki/Moving_average#Simple_moving_average
    """
    alias = ('SMA', 'SimpleMovingAverage',)
    lines = ('sma',)

    def __init__(self):
        # Before super to ensure mixins (right-hand side in subclassing)
        # can see the assignment operation and operate on the line
        self.lines[0] = Average(self.data, period=self.p.period)

        super(MovingAverageSimple, self).__init__()
