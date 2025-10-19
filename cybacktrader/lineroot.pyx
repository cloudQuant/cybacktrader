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

"""

.module:: lineroot

Definition of the base class LineRoot and base classes LineSingle/LineMultiple
to define interfaces and hierarchy for the real operational classes

.moduleauthor:: Daniel Rodriguez

"""

import operator
from cybacktrader import metabase
from cybacktrader.utils.py3 import with_metaclass
# from utils.py3 import range, with_metaclass
# import metabase

# Cython imports for C-level optimization
cimport cython

class MetaLineRoot(metabase.MetaParams):
    """
    Once the object is created (effectively pre-init) the "owner" of this
    class is sought
    # 当这个类在创建之前(pre-init之前)，会寻找这个类的一个父类，并保存到_owner属性上
    """

    def donew(cls, *args, **kwargs):
        _obj, args, kwargs = super(MetaLineRoot, cls).donew(*args, **kwargs)

        # Find the owner and store it
        # Check if owner is explicitly passed (for Cython compatibility)
        owner = kwargs.pop('_owner', None)
        if owner is None:
            # Fallback to findowner
            # startlevel = 4 ... to skip intermediate call stacks
            ownerskip = kwargs.pop('_ownerskip', None)
            # findowner用于寻找_obj的父类，属于_obj._OwnerCls或者LineMultiple的实例，同时这个父类还不能是ownerskip
            owner = metabase.findowner(_obj,
                                             _obj._OwnerCls or LineMultiple,
                                             skip=ownerskip)
        else:
            # Still pop _ownerskip if it was passed
            kwargs.pop('_ownerskip', None)
        
        _obj._owner = owner

        # Parameter values have now been set before __init__
        return _obj, args, kwargs

class LineRoot(with_metaclass(MetaLineRoot, object)):
    """
    Defines a common base and interfaces for Single and Multiple
    LineXXX instances

        Period management
        Iteration management
        Operation (dual/single operand) Management
        Rich Comparison operator definition
    为line实例定义一个共同的基类和接口，主要用于周期管理、迭代管理、操作管理和丰富的对比操作。
    需要额外注意的是，with_metaclass(MetaLineRoot,object)创建了一个类：temporary_class,这个类继承了MetaLineRoot和object，LineRoot继承的是temporary_class
    到这里的继承关系如下：LineRoot-->MetaLineRoot-->MetaParams-->MetaBase-->type
    """
    # 初始化的时候类的属性
    _OwnerCls = None    # 默认的父类实例是None
    _minperiod = 1      # 最小周期是1
    _opstage = 1        # 操作状态默认是1

    # 指标类型、策略类型和观察类型的值分别是0,1,2
    IndType, StratType, ObsType = range(3)

    # 转变操作状态为1 - Cython深度优化
    @cython.final
    def _stage1(self):
        self._opstage = 1

    # 转变操作状态为2 - Cython深度优化
    @cython.final
    def _stage2(self):
        self._opstage = 2

    # 根据line的操作状态决定调用哪种操作算法 - Cython深度优化
    def _operation(self, other, operation, r=False, intify=False):
        cdef int opstage = self._opstage
        if opstage == 1:
            return self._operation_stage1(
                other, operation, r=r, intify=intify)

        return self._operation_stage2(other, operation, r=r)
    
    # 自身的操作 - Cython深度优化
    def _operationown(self, operation):
        cdef int opstage = self._opstage
        if opstage == 1:
            return self._operationown_stage1(operation)

        return self._operationown_stage2(operation)

    # 改变lines去实施最小缓存计划
    def qbuffer(self, int savemem=0):
        """Change the lines to implement a minimum size qbuffer scheme"""
        raise NotImplementedError

    # 需要达到的最小缓存
    def minbuffer(self, int size):
        """Receive notification of how large the buffer must at least be"""
        raise NotImplementedError

    # 可以用于在策略中设置最小的周期，可以不用等待指标产生具体的值就开始运行
    def setminperiod(self, minperiod):
        """
        Direct minperiod manipulation. It could be used for example
        by a strategy
        to not wait for all indicators to produce a value
        
        """
        self._minperiod = minperiod

    # 更新最小周期，最小周期可能在其他地方已经计算产生，跟现有的最小周期对比，选择一个最大的作为最小周期 - Cython优化
    def updateminperiod(self, minperiod):
        """
        Update the minperiod if needed. The minperiod will have been
        calculated elsewhere
        and has to take over if greater that self's
        """
        cdef int current_min = self._minperiod
        cdef int new_min = minperiod
        self._minperiod = max(current_min, new_min)

    # 添加最小周期
    def addminperiod(self, minperiod):
        """
        Add a minperiod to own ... to be defined by subclasses
        """
        raise NotImplementedError

    # 增加最小周期
    def incminperiod(self, minperiod):
        """
        Increment the minperiod with no considerations
        """
        raise NotImplementedError

    # 在最小周期内迭代的时候将会调用这个函数
    def prenext(self):
        """
        It will be called during the "minperiod" phase of an iteration.
        """
        pass
    
    # 在最小周期迭代结束的时候，即将开始next的时候调用一次
    def nextstart(self):
        """
        It will be called when the minperiod phase is over for the 1st
        post-minperiod value. Only called once and defaults to automatically
        calling next
        """
        self.next()

    # 最小周期迭代结束后，开始调用next
    def next(self):
        """
        Called to calculate values when the minperiod is over
        """
        pass

    # 在最小周期迭代的时候调用preonce
    def preonce(self, int start, int end):
        """
        It will be called during the "minperiod" phase of a "once" iteration
        """
        pass

    # 在最小周期结束的时候运行一次，调用once
    def oncestart(self, int start, int end):
        """
        It will be called when the minperiod phase is over for the 1st
        post-minperiod value

        Only called once and defaults to automatically calling once
        
        """
        self.once(start, end)

    # 当最小周期迭代结束的时候调用用于计算结果
    def once(self, int start, int end):
        """
        Called to calculate values at "once" when the minperiod is over
        
        """
        pass

    # Arithmetic operators
    # 一些算术操作
    def _makeoperation(self, other, operation, r=False, _ownerskip=None):
        raise NotImplementedError

    # 做自身操作
    def _makeoperationown(self, operation, _ownerskip=None):
        raise NotImplementedError

    # 自身操作阶段1
    def _operationown_stage1(self, operation):
        """
        Operation with single operand which is "self"
        """
        return self._makeoperationown(operation, _ownerskip=self)
    
    # 自身操作阶段2
    def _operationown_stage2(self, operation):
        return operation(self[0])

    # 右操作
    def _roperation(self, other, operation, intify=False):
        """
        Relies on self._operation to and passes "r" True to define a
        reverse operation
        """
        return self._operation(other, operation, r=True, intify=intify)

    # 阶段1操作，判断other是不是包含多个line,如果有多个line，就取出第一个line,然后进行操作
    def _operation_stage1(self, other, operation, r=False, intify=False):
        """
        Two operands' operation. Scanning of other happens to understand
        if other must be directly an operand or rather a subitem thereof
        """
        if isinstance(other, LineMultiple):
            other = other.lines[0]

        return self._makeoperation(other, operation, r, self)

    # 阶段2操作，如果other是一个line，就取出当前值，然后进行操作
    def _operation_stage2(self, other, operation, r=False):
        """
        Rich Comparison operators. Scans other and returns either an
        operation with other directly or a subitem from other
        """
        if isinstance(other, LineRoot):
            other = other[0]

        # operation(float, other) ... expecting other to be a float
        if r:
            return operation(other, self[0])

        return operation(self[0], other)

    
    # 加
    def __add__(self, other):
        return self._operation(other, operator.__add__)

    # 右加
    def __radd__(self, other):
        return self._roperation(other, operator.__add__)

    # 减
    def __sub__(self, other):
        return self._operation(other, operator.__sub__)

    # 右减
    def __rsub__(self, other):
        return self._roperation(other, operator.__sub__)

    # 乘
    def __mul__(self, other):
        return self._operation(other, operator.__mul__)

    # 右乘
    def __rmul__(self, other):
        return self._roperation(other, operator.__mul__)

    # 除
    def __div__(self, other):
        return self._operation(other, operator.__div__)

    # 右除
    def __rdiv__(self, other):
        return self._roperation(other, operator.__div__)

    # 向下取整数
    def __floordiv__(self, other):
        return self._operation(other, operator.__floordiv__)

    # 右向下取整
    def __rfloordiv__(self, other):
        return self._roperation(other, operator.__floordiv__)

    # 真除法
    def __truediv__(self, other):
        return self._operation(other, operator.__truediv__)

    # 右真除法
    def __rtruediv__(self, other):
        return self._roperation(other, operator.__truediv__)

    # 幂
    def __pow__(self, other):
        return self._operation(other, operator.__pow__)

    # 右幂
    def __rpow__(self, other):
        return self._roperation(other, operator.__pow__)

    # 绝对值
    def __abs__(self):
        return self._operationown(operator.__abs__)

    # 取负的结果
    def __neg__(self):
        return self._operationown(operator.__neg__)

    # a<b
    def __lt__(self, other):
        return self._operation(other, operator.__lt__)

    # a>b
    def __gt__(self, other):
        return self._operation(other, operator.__gt__)

    # a<=b
    def __le__(self, other):
        return self._operation(other, operator.__le__)

    # a>=b
    def __ge__(self, other):
        return self._operation(other, operator.__ge__)

    # a = b
    def __eq__(self, other):
        return self._operation(other, operator.__eq__)

    # a!=b
    def __ne__(self, other):
        return self._operation(other, operator.__ne__)

    #  a!=0
    def __nonzero__(self):
        return self._operationown(bool)

    __bool__ = __nonzero__

    # Python 3 forces explicit implementation of hash if
    # the class has redefined __eq__
    __hash__ = object.__hash__

class LineMultiple(LineRoot):
    """
    Base class for LineXXX instances that hold more than one line
    LineMultiple-->LineRoot-->MetaLineRoot-->MetaParams-->MetaBase-->type
    # 这个类继承自LineRoot，用于操作line多余1条的类
    """
    # 重置
    def reset(self):
        self._stage1()
        self.lines.reset()

    # 对每一条line设置为操作状态1 - Cython优化
    def _stage1(self):
        super(LineMultiple, self)._stage1()
        cdef object line
        for line in self.lines:
            line._stage1()

    # 对每一条line设置为操作状态2 - Cython优化
    def _stage2(self):
        super(LineMultiple, self)._stage2()
        cdef object line
        for line in self.lines:
            line._stage2()
    # # 对每一条line增加一个最小周期 - Cython优化
    def addminperiod(self, minperiod):
        """
        The passed minperiod is fed to the lines
        """
        # pass it down to the lines
        cdef object line
        for line in self.lines:
            line.addminperiod(minperiod)

    # 对每一条line增加最小周期，但是这个在LineRoot里面好没有实施 - Cython优化
    def incminperiod(self, minperiod):
        """
        The passed minperiod is fed to the lines
        """
        # pass it down to the lines
        cdef object line
        for line in self.lines:
            line.incminperiod(minperiod)

    # 多条line操作的时候是对第一条line进行操作
    def _makeoperation(self, other, operation, r=False, _ownerskip=None):
        return self.lines[0]._makeoperation(other, operation, r, _ownerskip)

    # 多条line操作的时候是对第一条line的自身进行操作
    def _makeoperationown(self, operation, _ownerskip=None):
        return self.lines[0]._makeoperationown(operation, _ownerskip)

    # 对多条line设置qbuffer - Cython优化
    def qbuffer(self, int savemem=0):
        cdef object line
        for line in self.lines:
            line.qbuffer(savemem=1)

    # 对多条line设置最小的缓存量 - Cython优化
    def minbuffer(self, int size):
        cdef object line
        for line in self.lines:
            line.minbuffer(size)

class LineSingle(LineRoot):
    """
    Base class for LineXXX instances that hold a single line
    LineSingle-->LineRoot-->MetaLineRoot-->MetaParams-->MetaBase-->type
    # 这个类继承自LineRoot，用于操作line是一条的类
    """
    # 增加minperiod，增加的时候需要减去初始化设置的时候self._minperiod=1的设置 - Cython优化
    def addminperiod(self, minperiod):
        """
        Add the minperiod (substracting the overlapping 1 minimum period)
        """
        cdef int mp = minperiod
        self._minperiod += mp - 1
    # 增加minperiod,不考虑初始的self._minperiod的值 - Cython优化
    def incminperiod(self, minperiod):
        """
        Increment the minperiod with no considerations
        """
        cdef int mp = minperiod
        self._minperiod += mp

