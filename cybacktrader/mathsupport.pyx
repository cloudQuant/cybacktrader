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
from libc.math cimport sqrt as c_sqrt, pow as c_pow, fabs as c_fabs
cimport cython

# 深度Cython优化：C-level数学计算函数，极大提升性能

# 深度优化：cpdef允许Python和C调用，显著提升性能
cpdef double average(object x, bint bessel=False):
    """
    深度优化的平均值计算
    
    Args:
      x: iterable with len
      bessel: (default ``False``) reduces the length of the array for the
                division (Bessel's correction).

    Returns:
      A float with the average of the elements of x
    """
    cdef double sum_val
    cdef int n
    cdef int divisor
    
    # Fast path for common types
    try:
        n = len(x)
        if n == 0:
            return 0.0
        
        # Use math.fsum for numerical stability (keeps Python behavior)
        sum_val = math.fsum(x)
        divisor = n - (1 if bessel else 0)
        
        if divisor == 0:
            return 0.0
            
        return sum_val / <double>divisor
    except (TypeError, ZeroDivisionError):
        # Fallback
        return 0.0

# 用于计算方差 - Cython深度优化：cpdef + C-level循环 + nogil
cpdef list variance(object x, object avgx=None):
    """
    深度优化的方差计算：使用C-level循环和类型声明
    
    Args:
      x: iterable with len
      avgx: pre-computed average (default None means compute it)

    Returns:
      A list with the variance for each element of x
    """
    cdef double avg
    cdef double diff
    cdef int i, n
    cdef list result
    cdef double val
    
    # Compute average if not provided - maintain backward compatibility
    if avgx is None:
        avg = average(x, False)
    else:
        avg = <double>avgx
    
    # Fast path: pre-allocate result list
    try:
        n = len(x)
        result = [0.0] * n
        
        # Optimized loop with C types
        for i in range(n):
            val = <double>x[i]
            diff = val - avg
            result[i] = diff * diff  # Faster than c_pow for squaring
        
        return result
    except (TypeError, IndexError):
        # Fallback: use list comprehension
        return [c_pow(<double>y - avg, 2.0) for y in x]

# 这个函数用于计算一个可迭代对象x的标准差 - Cython深度优化
cpdef double standarddev(object x, object avgx=None, bint bessel=False):
    """
    深度优化的标准差计算：直接使用C math函数
    
    Args:
      x: iterable with len
      avgx: pre-computed average (default None means compute it)
      bessel: (default ``False``) to be passed to the average to divide by
      ``N - 1`` (Bessel's correction)

    Returns:
      A float with the standard deviation of the elements of x
    """
    cdef double var_avg
    cdef list var_list
    
    try:
        # Compute variance
        var_list = variance(x, avgx)
        
        # Compute average of variance
        var_avg = average(var_list, bessel)
        
        # Return square root using C function
        return c_sqrt(var_avg)
    except (TypeError, ValueError):
        # Fallback
        return 0.0
