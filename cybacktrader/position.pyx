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

from copy import copy

# Cython imports for C-level optimization
cimport cython

# Internal C-level helper functions for performance
@cython.cdivision(True)
@cython.boundscheck(False)
cdef inline void _calc_position_delta(
    long oldsize,
    long delta,
    double old_price,
    double new_price,
    long* out_newsize,
    long* out_opened,
    long* out_closed,
    double* out_price
) noexcept nogil:
    """Fast C-level calculation of position updates
    
    Args:
        oldsize: current position size
        delta: size change (+ for buy, - for sell)
        old_price: current position price
        new_price: price of the transaction
        out_newsize: output - new position size
        out_opened: output - contracts opened
        out_closed: output - contracts closed
        out_price: output - new position price
    """
    cdef long newsize = oldsize + delta
    cdef long opened, closed
    cdef double result_price
    
    out_newsize[0] = newsize
    
    # Position closed to zero
    if newsize == 0:
        opened = 0
        closed = delta
        result_price = 0.0
    # Opening from zero
    elif oldsize == 0:
        opened = delta
        closed = 0
        result_price = new_price
    # Existing long position
    elif oldsize > 0:
        if delta > 0:  # Increased long
            opened = delta
            closed = 0
            result_price = (old_price * oldsize + delta * new_price) / newsize
        elif newsize > 0:  # Reduced long
            opened = 0
            closed = delta
            result_price = old_price
        else:  # Reversed to short
            opened = newsize
            closed = -oldsize
            result_price = new_price
    # Existing short position
    else:  # oldsize < 0
        if delta < 0:  # Increased short
            opened = delta
            closed = 0
            result_price = (old_price * oldsize + delta * new_price) / newsize
        elif newsize < 0:  # Reduced short
            opened = 0
            closed = delta
            result_price = old_price
        else:  # Reversed to long
            opened = newsize
            closed = -oldsize
            result_price = new_price
    
    out_opened[0] = opened
    out_closed[0] = closed
    out_price[0] = result_price

# Position类，保持和更新持仓的大小和价格，和其他的任何资产没有关系，它仅仅保存大小和价格
class Position(object):
    """
    Keeps and updates the size and price of a position. The object has no
    relationship to any asset. It only keeps size and price.

    Member Attributes:
      - size (int): current size of the position
      - price (float): current price of the position
    # position具有两个属性值，一个是size，代表当前持仓大小；一个是价格，代表当前持仓的价格。
    # position的实例可以通过len(position)来判断size是否是空的
    The Position instances can be tested using len(position) to see if size
    is not null

    """
    # 打印position的时候可以显示的信息
    def __str__(self):
        items = list()
        items.append('--- Position Begin')
        items.append('- Size: {}'.format(self.size))
        items.append('- Price: {}'.format(self.price))
        items.append('- Price orig: {}'.format(self.price_orig))
        items.append('- Closed: {}'.format(self.upclosed))
        items.append('- Opened: {}'.format(self.upopened))
        items.append('- Adjbase: {}'.format(self.adjbase))
        items.append('--- Position End')
        return '\n'.join(items)

    # 根据size和price的不同进行初始化 - Cython深度优化
    @cython.cdivision(True)
    def __init__(self, size=0, price=0.0):
        cdef long init_size = size
        cdef double init_price = price
        
        self.size = init_size
        if init_size:
            self.price = self.price_orig = init_price
        else:
            self.price = 0.0

        self.adjbase = None

        self.upopened = init_size
        self.upclosed = 0
        self.set(init_size, init_price)

        self.updt = None

    # 修改position的size和price - Cython深度优化
    @cython.final
    @cython.cdivision(True)
    def fix(self, size, price):
        cdef long oldsize, new_size
        cdef double new_price
        
        oldsize = self.size
        new_size = size
        new_price = price
        
        self.size = new_size
        self.price = new_price
        return self.size == oldsize
    # 设置position的size和price
    def set(self, size, price):
        # 如果现在的持仓大于0,并且理论上的size大于当前的size，就意味着要新开仓；
        # 如果理论上的size小于等于当前的持仓，那么开仓量是0和理论上size的最小量；
        # 平仓量等于当前持仓和当前持仓减去理论持仓量最小的一个值
        cdef long cur_size = self.size
        cdef long new_size = size
        cdef long upopened, upclosed
        cdef double price_d = price

        if cur_size > 0:
            if new_size > cur_size:
                upopened = new_size - cur_size  # new 10 - old 5 -> 5
                upclosed = 0
            else:
                # same side min(0, 3) -> 0 / reversal min(0, -3) -> -3
                upopened = 0 if new_size > 0 else new_size
                # same side min(10, 10 - 5) -> 5
                # reversal min(10, 10 - -5) -> min(10, 15) -> 10
                upclosed = cur_size if cur_size < (cur_size - new_size) else (cur_size - new_size)
        # 当前持仓小于0的时候，有类似的效果
        elif cur_size < 0:
            if new_size < cur_size:
                upopened = new_size - cur_size  # ex: -5 - -3 -> -2
                upclosed = 0
            else:
                # same side max(0, -5) -> 0 / reversal max(0, 5) -> 5
                upopened = 0 if new_size < 0 else new_size
                # same side max(-10, -10 - -5) -> max(-10, -5) -> -5
                # reversal max(-10, -10 - 5) -> max(-10, -15) -> -10
                upclosed = cur_size if cur_size > (cur_size - new_size) else (cur_size - new_size)
        # 如果当前持仓等于0，新开仓和平仓都等于0
        # todo 这里面直接使用0代替self.size可能可以提高效率
        else:  # self.size == 0
            upopened = cur_size
            upclosed = 0

        # 实际持仓大小
        self.size = new_size
        # 原始价格
        self.price_orig = self.price
        # 如果持仓大小大于0的话，当前价格就等于price，否则当前价格等于0
        if new_size:
            self.price = price_d
        else:
            self.price = 0.0

        self.upopened = upopened
        self.upclosed = upclosed

        return self.size, self.price, self.upopened, self.upclosed
    # 调用len(position)的时候，返回持仓的绝对值 - Cython深度优化
    @cython.final
    def __len__(self):
        cdef long size_val = self.size
        return abs(size_val)
    
    # 调用bool(position)判断当前size是否等于0 - Cython深度优化
    @cython.final
    def __bool__(self):
        return self.size != 0

    __nonzero__ = __bool__

    # 克隆持仓信息 - Cython深度优化
    @cython.final
    def clone(self):
        return Position(size=self.size, price=self.price)

    # 创建一个position实例，然后更新size和价格 - Cython深度优化
    @cython.final
    def pseudoupdate(self, size, price):
        return Position(self.size, self.price).update(size, price)

    # 更新size和price - 使用内部cdef函数优化
    def update(self, size, price, dt=None):
        """
        Updates the current position and returns the updated size, price and
        units used to open/close a position
        # 更新当前的持仓和返回更新后的大小、价格和需要开仓和平仓的头寸大小

        Args:
            size (int): amount to update the position size
                size < 0: A sell operation has taken place
                size > 0: A buy operation has taken place
            # 更新持仓大小的量，如果size小于0,将会发出一个卖操作，如果size大于0,将会发生一个买操作
            price (float):
                Must always be positive to ensure consistency
            # 价格，必须总是正数以保持持续性

        Returns:

            A tuple (non-named) containing
               size - new position size
                   Simply the sum of the existing size plus the "size" argument
               price - new position price
                   If a position is increased the new average price will be
                   returned
                   If a position is reduced the price of the remaining size
                   does not change
                   If a position is closed the price is nullified
                   If a position is reversed the price is the price given as
                   argument
               opened - amount of contracts from argument "size" that were used
                   to open/increase a position.
                   A position can be opened from 0 or can be a reversal.
                   If a reversal is performed then opened is less than "size",
                   because part of "size" will have been used to close the
                   existing position
               closed - amount of units from arguments "size" that were used to
                   close/reduce a position

            Both opened and closed carry the same sign as the "size" argument
            because they refer to a part of the "size" argument
            # 结果将会返回一个元组，包含下面的一些数据：
            # size 代表新的持仓大小，仅仅是已经有的持仓的大小加上新的持仓增量
            # price 代表新的持仓价格，根据持仓的不同，返回不同的价格
            # opened 代表需要新开的仓位
            # closed 代表需要平仓的仓位
        """
        # 更新持仓的时间
        self.datetime = dt  # record datetime update (datetime.datetime)
        # 原始的价格
        self.price_orig = self.price
        
        # 使用快速C级计算（需求6优化）
        cdef long oldsize = self.size
        cdef long delta = size
        cdef double price_d = price
        cdef long newsize, opened, closed
        cdef double new_price_result
        
        # 调用内部cdef函数进行快速计算
        _calc_position_delta(
            oldsize, delta, self.price, price_d,
            &newsize, &opened, &closed, &new_price_result
        )
        
        # 更新状态
        self.size = newsize
        self.price = new_price_result
        self.upopened = opened
        self.upclosed = closed

        return self.size, self.price, opened, closed
