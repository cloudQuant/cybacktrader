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

from cybacktrader.indicator import Indicator

# 内联C函数：释放GIL执行核心循环
cdef inline void _compute_momentum(double[:] dst, double[:] cur, double[:] base, int start, int end, int period) noexcept nogil:
    cdef int i
    for i in range(start, end):
        dst[i] = cur[i] - base[i - period]

cdef inline void _compute_momosc(double[:] dst, double[:] cur, double[:] base, int start, int end, int period) noexcept nogil:
    cdef int i
    for i in range(start, end):
        dst[i] = 100.0 * cur[i] / base[i - period]

cdef inline void _compute_roc(double[:] dst, double[:] cur, double[:] base, int start, int end, int period) noexcept nogil:
    cdef int i
    cdef double denom
    for i in range(start, end):
        denom = base[i - period]
        dst[i] = (cur[i] - denom) / denom if denom != 0.0 else 0.0

# 动量指标，动量震荡指标，ROC指标，ROC指标乘以100
class Momentum(Indicator):
    '''
    Measures the change in price by calculating the difference between the
    current price and the price from a given period ago

    Formula:
      - momentum = data - data_period

    See:
      - http://en.wikipedia.org/wiki/Momentum_(technical_analysis)
    '''
    lines = ('momentum',)
    params = (('period', 12),)
    plotinfo = dict(plothlines=[0.0])

    def __init__(self):
        self.l.momentum = self.data - self.data(-self.p.period)
        super(Momentum, self).__init__()

    def once(self, int start, int end):
        # Cython深度优化：momentum = data - data_period
        cdef int i, period
        cdef double[:] dst = self.lines.momentum.array
        cdef double[:] cur = self.data.array
        cdef double[:] base = self.data.array
        cdef int s = start
        cdef int e = end
        period = self.p.period
        with nogil:
            _compute_momentum(dst, cur, base, s, e, period)

class MomentumOscillator(Indicator):
    '''
    Measures the ratio of change in prices over a period

    Formula:
      - mosc = 100 * (data / data_period)

    See:
      - http://ta.mql4.com/indicators/oscillators/momentum
    '''
    alias = ('MomentumOsc',)

    # Named output lines
    lines = ('momosc',)

    # Accepted parameters (and defaults) -
    params = (('period', 12),
              ('band', 100.0))

    def _plotlabel(self):
        plabels = [self.p.period]
        return plabels

    def _plotinit(self):
        self.plotinfo.plothlines = [self.p.band]

    def __init__(self):
        self.l.momosc = 100.0 * (self.data / self.data(-self.p.period))
        super(MomentumOscillator, self).__init__()

    def once(self, int start, int end):
        # Cython深度优化：momosc = 100 * data / data_period
        cdef int i, period
        cdef double[:] dst = self.lines.momosc.array
        cdef double[:] cur = self.data.array
        cdef double[:] base = self.data.array
        cdef int s = start
        cdef int e = end
        period = self.p.period
        with nogil:
            _compute_momosc(dst, cur, base, s, e, period)

class RateOfChange(Indicator):
    '''
    Measures the ratio of change in prices over a period

    Formula:
      - roc = (data - data_period) / data_period

    See:
      - http://en.wikipedia.org/wiki/Momentum_(technical_analysis)
    '''
    alias = ('ROC',)

    # Named output lines
    lines = ('roc',)

    # Accepted parameters (and defaults) -
    params = (('period', 12),)

    def __init__(self):
        dperiod = self.data(-self.p.period)
        self.l.roc = (self.data - dperiod) / dperiod
        super(RateOfChange, self).__init__()

    def once(self, int start, int end):
        # Cython深度优化：roc = (data - data_period) / data_period
        cdef int i, period
        cdef double[:] dst = self.lines.roc.array
        cdef double[:] cur = self.data.array
        cdef double[:] base = self.data.array
        cdef double denom
        cdef int s = start
        cdef int e = end
        period = self.p.period
        with nogil:
            _compute_roc(dst, cur, base, s, e, period)

class RateOfChange100(Indicator):
    '''
    Measures the ratio of change in prices over a period with base 100

    This is for example how ROC is defined in stockcharts

    Formula:
      - roc = 100 * (data - data_period) / data_period

    See:
      - http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:rate_of_change_roc_and_momentum

    '''
    alias = ('ROC100',)

    # Named output lines
    lines = ('roc100',)

    # Accepted parameters (and defaults)
    params = (('period', 12),)

    def __init__(self):
        self.l.roc100 = 100.0 * RateOfChange(self.data, period=self.p.period)
        super(RateOfChange100, self).__init__()
