#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

# Cython性能优化标记
# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True

from ..utils.py3 import range

from cybacktrader.indicators.mabase import MovingAverageBase
from cybacktrader.indicators.basicops import WeightedAverage

# 加权平均均线
class WeightedMovingAverage(MovingAverageBase):
    '''
    A Moving Average which gives an arithmetic weighting to values with the
    newest having the more weight

    Formula:
      - weights = range(1, period + 1)
      - coef = 2 / (period * (period + 1))
      - movav = coef * Sum(weight[i] * data[period - i] for i in range(period))

    See also:
      - http://en.wikipedia.org/wiki/Moving_average#Weighted_moving_average
    '''
    alias = ('WMA', 'MovingAverageWeighted',)
    lines = ('wma',)

    def __init__(self):
        coef = 2.0 / (self.p.period * (self.p.period + 1.0))
        weights = tuple(float(x) for x in range(1, self.p.period + 1))

        # Before super to ensure mixins (right-hand side in subclassing)
        # can see the assignment operation and operate on the line
        self.lines[0] = WeightedAverage(
            self.data, period=self.p.period,
            coef=coef, weights=weights)

        super(WeightedMovingAverage, self).__init__()
