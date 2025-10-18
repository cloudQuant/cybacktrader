#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

# Cython性能优化标记（保守设置）
# cython: language_level=3
# cython: infer_types=True
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True

from cybacktrader.indicator import Indicator

__all__ = ['PercentChange', 'PctChange']

# 变动百分比
class PercentChange(Indicator):
    '''
      Measures the perccentage change of the current value with respect to that
      of period bars ago
    '''
    alias = ('PctChange',)
    lines = ('pctchange',)

    # Fancy plotting name
    plotlines = dict(pctchange=dict(_name='%change'))

    # update value to standard for Moving Averages
    params = (('period', 30),)

    def __init__(self):
        # 深度优化：保持表达式接口但优化 once 路径
        self.lines.pctchange = self.data / self.data(-self.p.period) - 1.0
        super(PercentChange, self).__init__()

    def once(self, start, end):
        # Cython深度优化：基于 C 循环计算 pctchange
        cdef int i, period
        cdef double[:] dst = self.lines.pctchange.array
        cdef double[:] cur = self.data.array
        cdef double[:] prev = self.data.array  # 复用同一数组，但用偏移访问
        cdef double denom
        period = self.p.period

        for i in range(start, end):
            denom = prev[i - period]
            dst[i] = (cur[i] / denom - 1.0) if denom != 0.0 else 0.0
