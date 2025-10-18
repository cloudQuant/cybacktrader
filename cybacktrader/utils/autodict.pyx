#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

# Cython深度性能优化标记（完整版）
# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: nonecheck=False
# cython: initializedcheck=False
# cython: infer_types=True

from collections import OrderedDict, defaultdict

# from .py3 import values as py3lvalues
from cybacktrader.utils.py3 import values as py3lvalues  #修改相对引用为绝对引用

# Cython imports
cimport cython

@cython.boundscheck(False)
cpdef inline object Tree():
    """创建递归默认字典"""
    # 不知道定义这个函数有什么用，其他地方没有用到过，忽略
    # 可以考虑删除
    return defaultdict(Tree)

class AutoDictList(dict):
    # 继承字典，当访问缺失的的key的时候，将会自动生成一个key值，对应的value值是一个空的列表
    # 这个新创建的类仅仅用在了collections.defaultdict(AutoDictList)这一行代码中。
    
    @cython.boundscheck(False)
    def __missing__(self, key):
        value = list()
        self[key] = value
        return value

class DotDict(dict):
    # If the attribut is not found in the usual places try the dict itself
    # 这个类仅仅用于了下面一行代码,当访问属性的时候，如果没有这个属性，将会调用__getattr__
    # _obj.dnames = DotDict([(d._name, d) for d in _obj.datas if getattr(d, '_name', '')])
    
    @cython.boundscheck(False)
    def __getattr__(self, key):
        if key.startswith('__'):
            return super(DotDict, self).__getattr__(key)
        return self[key]

# 这个函数用途稍微广泛一些，主要在tradeanalyzer和ibstore里面调用了，是对python字典的扩展
# 相比于python内置的dict，额外增加了一个属性：_closed,增加了函数_close,_open,__missing__,__getattr__,重写了__setattr__
class AutoDict(dict):
    # 初始化默认属性 _closed设置成False
    _closed = False
    
    # _close方法 - Cython优化
    @cython.boundscheck(False)
    def _close(self):
        # 类的属性修改为True
        self._closed = True
        # 对于字典中的值，如果这些值是AutoDict或者AutoOrderedDict的实例，就调用_close方法设置属性_closed为True
        for key, val in self.items():
            if isinstance(val, (AutoDict, AutoOrderedDict)):
                val._close()
    
    # _open方法，设置_closed属性为False
    @cython.boundscheck(False)
    def _open(self):
        self._closed = False
    
    # __missing__方法处理当key不存在的情况
    @cython.boundscheck(False)
    def __missing__(self, key):
        if self._closed:
            raise KeyError

        value = self[key] = AutoDict()
        return value
    
    # __getattr__ - Cython优化
    @cython.boundscheck(False)
    def __getattr__(self, key):
        # 简化逻辑，移除永远为False的条件
        return self[key]
    
    # __setattr__ - Cython优化
    @cython.boundscheck(False)
    def __setattr__(self, key, value):
        # 简化逻辑，移除永远为False的条件
        self[key] = value

# 创建的一个新的有序的字典，增加了一些函数，和AutoDict有些类似
class AutoOrderedDict(OrderedDict):
    _closed = False

    # _close方法 - Cython优化
    @cython.boundscheck(False)
    def _close(self):
        self._closed = True
        for key, val in self.items():
            if isinstance(val, (AutoDict, AutoOrderedDict)):
                val._close()

    # _open方法 - Cython优化
    @cython.boundscheck(False)
    def _open(self):
        self._closed = False

    # __missing__方法 - Cython优化
    @cython.boundscheck(False)
    def __missing__(self, key):
        if self._closed:
            raise KeyError

        value = self[key] = AutoOrderedDict()
        return value
    
    # __getattr__和__setattr__这两个函数相比于AutoDict的正常了很多
    @cython.boundscheck(False)
    def __getattr__(self, key):
        if key.startswith('_'):
            raise AttributeError

        return self[key]

    @cython.boundscheck(False)
    def __setattr__(self, key, value):
        if key.startswith('_'):
            self.__dict__[key] = value
            return

        self[key] = value
    # 定义的数学操作，暂时还没明白是什么意思，但是看起来只有__iadd__和__isub__是正常的
    # Define math operations
    def __iadd__(self, other):
        if type(self) != type(other):
            return type(other)() + other

        return self + other

    def __isub__(self, other):
        if type(self) != type(other):
            return type(other)() - other

        return self - other

    def __imul__(self, other):
        if type(self) != type(other):
            return type(other)() * other

        return self + other

    def __idiv__(self, other):
        if type(self) != type(other):
            return type(other)() // other

        return self + other

    def __itruediv__(self, other):
        if type(self) != type(other):
            return type(other)() / other

        return self + other

    def lvalues(self):
        return py3lvalues(self)

if __name__ == "__main__":
    aod = AutoOrderedDict()
    print("aod",dir(aod))
    od = OrderedDict()
    print("od",dir(od))
    