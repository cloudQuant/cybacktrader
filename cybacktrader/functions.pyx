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

import functools
import math

from cybacktrader.linebuffer import LineActions
from cybacktrader.utils.py3 import cmp

# C级比较函数：避免在热点循环中调用Python层cmp
cdef inline int cmp_double(double a, double b) nogil:
    if a < b:
        return -1
    elif a > b:
        return 1
    else:
        return 0

# Generate a List equivalent which uses "is" for contains
# 创建一个新的List类,改写了__contains__方法,如果list中有一个元素的哈希值等于other的哈希值，那么就返回True
class List(list):
    def __contains__(self, other):
        return any(x.__hash__() == other.__hash__() for x in self)

# 创建一个类，把其中的元素进行序列化
class Logic(LineActions):
    def __init__(self, *args):
        super(Logic, self).__init__()
        self.args = [self.arrayize(arg) for arg in args]

# 避免两个line想除的时候有值是0，如果分母是0,除以得到的值是0
class DivByZero(Logic):
    """This operation is a Lines object and fills it values by executing a
    division on the numerator / denominator arguments and avoiding a division
    by zero exception by checking the denominator

    Params:
      - a: numerator (numeric or iterable object ... mostly a Lines object)
      - b: denominator (numeric or iterable object ... mostly a Lines object)
      - zero (def: 0.0): value to apply if division by zero would be raised

    """
    def __init__(self, a, b, zero=0.0):
        super(DivByZero, self).__init__(a, b)
        self.a = a
        self.b = b
        self.zero = zero

    def next(self):
        b = self.b[0]
        self[0] = self.a[0] / b if b else self.zero

    def once(self, start, end):
        # Cython深度优化：除法保护
        cdef int i, s = start, e = end
        cdef double b, zero_val = self.zero
        cdef double[:] dst = self.array
        cdef double[:] srca = self.a.array
        cdef double[:] srcb = self.b.array

        with nogil:
            for i in range(s, e):
                b = srcb[i]
                dst[i] = srca[i] / b if b != 0.0 else zero_val

# 考虑分母分子都可能是0的两个line的想除操作
class DivZeroByZero(Logic):
    """This operation is a Lines object and fills it values by executing a
    division on the numerator / denominator arguments and avoiding a division
    by zero exception or an indetermination by checking the
    denominator/numerator pair

    Params:
      - a: numerator (numeric or iterable object ... mostly a Lines object)
      - b: denominator (numeric or iterable object ... mostly a Lines object)
      - single (def: +inf): value to apply if division is x / 0
      - dual (def: 0.0): value to apply if division is 0 / 0
    """
    def __init__(self, a, b, single=float('inf'), dual=0.0):
        super(DivZeroByZero, self).__init__(a, b)
        self.a = a
        self.b = b
        self.single = single
        self.dual = dual

    def next(self):
        b = self.b[0]
        a = self.a[0]
        if b == 0.0:
            self[0] = self.dual if a == 0.0 else self.single
        else:
            self[0] = self.a[0] / b

    def once(self, start, end):
        # Cython深度优化：双零除法保护
        cdef int i, s = start, e = end
        cdef double a, b
        cdef double single = self.single
        cdef double dual = self.dual
        cdef double[:] dst = self.array
        cdef double[:] srca = self.a.array
        cdef double[:] srcb = self.b.array

        with nogil:
            for i in range(s, e):
                b = srcb[i]
                a = srca[i]
                if b == 0.0:
                    dst[i] = dual if a == 0.0 else single
                else:
                    dst[i] = a / b

# 对比a和b,a和b很可能是line
class Cmp(Logic):
    def __init__(self, a, b):
        super(Cmp, self).__init__(a, b)
        self.a = self.args[0]
        self.b = self.args[1]

    def next(self):
        self[0] = cmp(self.a[0], self.b[0])

    def once(self, start, end):
        # Cython优化：比较操作
        cdef int i, s = start, e = end
        cdef double[:] dst = self.array
        cdef double[:] srca = self.a.array
        cdef double[:] srcb = self.b.array

        with nogil:
            for i in range(s, e):
                dst[i] = cmp_double(srca[i], srcb[i])

# 对比两个line,a和b，a<b的时候，返回r1相应的值，a=b的时候，返回r2相应的值，a>b的时候，返回r3相应的值
# todo 在backtrader量化交流群中有一个朋友指出了这个问题
class CmpEx(Logic):
    def __init__(self, a, b, r1, r2, r3):
        super(CmpEx, self).__init__(a, b, r1, r2, r3)
        self.a = self.args[0]
        self.b = self.args[1]
        self.r1 = self.args[2]
        self.r2 = self.args[3]
        self.r3 = self.args[4]

    def next(self):
        # self[0] = cmp(self.a[0], self.b[0])
        if self.a[0]<self.b[0]:
            self[0] = self.r1[0]
        elif self.a[0]>self.b[0]:
            self[0] = self.r3[0]
        else:
            self[0] = self.r2[0]

    def once(self, start, end):
        # Cython优化：扩展比较
        cdef int i, s = start, e = end
        cdef double ai, bi
        cdef double[:] dst = self.array
        cdef double[:] srca = self.a.array
        cdef double[:] srcb = self.b.array
        cdef double[:] r1 = self.r1.array
        cdef double[:] r2 = self.r2.array
        cdef double[:] r3 = self.r3.array

        with nogil:
            for i in range(s, e):
                ai = srca[i]
                bi = srcb[i]

                if ai < bi:
                    dst[i] = r1[i]
                elif ai > bi:
                    dst[i] = r3[i]
                else:
                    dst[i] = r2[i]

# if判断，对于cond满足的时候，返回a相应的值，不满足的时候，返回b相应的值
class If(Logic):
    def __init__(self, cond, a, b):
        super(If, self).__init__(a, b)
        self.a = self.args[0]
        self.b = self.args[1]
        self.cond = self.arrayize(cond)

    def next(self):
        self[0] = self.a[0] if self.cond[0] else self.b[0]

    def once(self, start, end):
        # Cython优化：IF条件
        cdef int i
        cdef object dst = self.array
        cdef object srca = self.a.array
        cdef object srcb = self.b.array
        cdef object cond = self.cond.array

        for i in range(start, end):
            dst[i] = srca[i] if cond[i] else srcb[i]

# 一个逻辑应用到多个元素上
class MultiLogic(Logic):
    def next(self):
        self[0] = self.flogic([arg[0] for arg in self.args])

    def once(self, start, end):
        # Cython优化：多逻辑
        cdef int i
        dst = self.array
        arrays = [arg.array for arg in self.args]
        flogic = self.flogic

        for i in range(start, end):
            dst[i] = flogic([arr[i] for arr in arrays])

# 主要是调用了functools.partial生成偏函数，functools.reduce,对一个sequence迭代使用function
class MultiLogicReduce(MultiLogic):
    def __init__(self, *args, **kwargs):
        super(MultiLogicReduce, self).__init__(*args)
        if 'initializer' not in kwargs:
            self.flogic = functools.partial(functools.reduce, self.flogic)
        else:
            self.flogic = functools.partial(functools.reduce, self.flogic,
                                            initializer=kwargs['initializer'])

# 继承类，对flogic进行处理
class Reduce(MultiLogicReduce):
    def __init__(self, flogic, *args, **kwargs):
        self.flogic = flogic
        super(Reduce, self).__init__(*args, **kwargs)

# The _xxxlogic functions are defined at module scope to make them
# pickable and therefore compatible with multiprocessing

# 判断x和y是不是都是True
def _andlogic(x, y):
    return bool(x and y)

# 判断是否是所有的元素都是True的
class And(MultiLogicReduce):
    flogic = staticmethod(_andlogic)

# 判断x或者y中有没有一个是真的
def _orlogic(x, y):
    return bool(x or y)

# 判断序列中是否有一个是真的
class Or(MultiLogicReduce):
    flogic = staticmethod(_orlogic)

# 求最大值
class Max(MultiLogic):
    flogic = max

# 求最小值
class Min(MultiLogic):
    flogic = min

# 求和
class Sum(MultiLogic):
    flogic = math.fsum

# 是否有一个
class Any(MultiLogic):
    flogic = any

# 是否所有的
class All(MultiLogic):
    flogic = all
