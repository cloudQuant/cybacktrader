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

import math
from libc.math cimport sqrt, pow as c_pow

# 看了一下，这几个函数主要用于计算一些指标使用，在主体中没有用到，注释一下，稍后回来看是否需要用cython改进，暂时没有改进的必要。
# 但是这几个函数其实可以考虑使用numpy改进一下，numpy提供了具体的函数用于计算均值，计算标准差

# 这个计算的是平均值，带了一个参数bessel，用于确定计算平均值的时候分母的值是否减去一。分子使用math.fsum用于计算和
def average(x, bessel=False):
    """
    Args:
      x: iterable with len

      oneless: (default ``False``) reduces the length of the array for the
                division.

    Returns:
      A float with the average of the elements of x
    """
    return math.fsum(x) / (len(x) - bessel)

# 用于计算方差 - Cython优化
def variance(x, avgx=None):
    """
    Args:
      x: iterable with len

    Returns:
      A list with the variance for each element of x
    """
    cdef double avg
    cdef double y
    if avgx is None:
        avg = average(x)
    else:
        avg = avgx
    return [c_pow(y - avg, 2.0) for y in x]

# 这个函数用于计算一个可迭代对象x的标准差。
def standarddev(x, avgx=None, bessel=False):
    """
    Args:
      x: iterable with len

      bessel: (default ``False``) to be passed to the average to divide by
      ``N - 1`` (Bessel's correction)

    Returns:
      A float with the standard deviation of the elements of x
    """
    return math.sqrt(average(variance(x, avgx), bessel=bessel))
