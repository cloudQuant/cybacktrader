#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

from ..utils.py3 import with_metaclass

from cybacktrader import Indicator

# 移动平均类，用于设置指标的名字
class MovingAverage(object):
    '''MovingAverage (alias MovAv)

    A placeholder to gather all Moving Average Types in a single place.

    Instantiating a SimpleMovingAverage can be achieved as follows::

      sma = MovingAverage.Simple(self.data, period)

    Or using the shorter aliases::

      sma = MovAv.SMA(self.data, period)

    or with the full (forwards and backwards) names:

      sma = MovAv.SimpleMovingAverage(self.data, period)

      sma = MovAv.MovingAverageSimple(self.data, period)

    '''
    # 移动平均类的保存
    _movavs = []

    @classmethod
    def register(cls, regcls):
        # 如果指标中没有_notregister或者_notregister的值是False，就继续运行，进行注册，否则直接返回
        if getattr(regcls, '_notregister', False):
            return
        # 把需要计算的指标类添加进去
        cls._movavs.append(regcls)
        # 类的名称，并且把类名称设置成cls的属性，属性值为具体的类
        clsname = regcls.__name__
        setattr(cls, clsname, regcls)

        # 具体指标的别名，如果指标开头是MovingAverage,那么，用后面的值作为别名，如果结尾是MovingAverage，用前面的值作为别名
        # 如果取得的别名不是空字符串，那么就把别名也设置成属性，该属性的值为这个类
        clsalias = ''
        if clsname.endswith('MovingAverage'):
            clsalias = clsname.split('MovingAverage')[0]
        elif clsname.startswith('MovingAverage'):
            clsalias = clsname.split('MovingAverage')[1]

        if clsalias:
            setattr(cls, clsalias, regcls)

# Metaclass for lazy loading of MovAv attributes
class MetaMovAv(type):
    # Mapping of attribute names to modules for lazy loading
    _attr_to_module = {
        'SMA': 'sma',
        'SimpleMovingAverage': 'sma',
        'Simple': 'sma',
        'MovingAverageSimple': 'sma',
        'EMA': 'ema',
        'ExponentialMovingAverage': 'ema',
        'Exponential': 'ema',
        'MovingAverageExponential': 'ema',
        'SMMA': 'smma',
        'SmoothedMovingAverage': 'smma',
        'Smoothed': 'smma',
        'MovingAverageSmoothed': 'smma',
        'WilderMA': 'smma',
        'MovingAverageWilder': 'smma',
        'WMA': 'wma',
        'WeightedMovingAverage': 'wma',
        'Weighted': 'wma',
        'MovingAverageWeighted': 'wma',
        'DEMA': 'dema',
        'DoubleExponentialMovingAverage': 'dema',
        'TEMA': 'dema',
        'TripleExponentialMovingAverage': 'dema',
        'KAMA': 'kama',
        'AdaptiveMovingAverage': 'kama',
        'Adaptive': 'kama',
        'ZLEMA': 'zlema',
        'ZeroLagExponentialMovingAverage': 'zlema',
        'HMA': 'hma',
        'HullMovingAverage': 'hma',
        'Hull': 'hma',
    }
    
    def __getattribute__(cls, name):
        # Try normal attribute access first
        try:
            return type.__getattribute__(cls, name)
        except AttributeError:
            # Check if we have a mapping for lazy loading
            attr_to_module = type.__getattribute__(cls, '_attr_to_module')
            if name in attr_to_module:
                module_name = attr_to_module[name]
                try:
                    # Import the module to trigger registration
                    __import__(f'cybacktrader.indicators.{module_name}', 
                              fromlist=['__name__'])
                    # After import, try to get the attribute again
                    return type.__getattribute__(cls, name)
                except (ImportError, AttributeError):
                    pass
            
            # If still not found, raise AttributeError
            raise AttributeError(f"type object '{cls.__name__}' has no attribute '{name}'")

# 移动平均的别名
class MovAv(MovingAverage, metaclass=MetaMovAv):
    pass  # alias

# 移动平均的基类
class MetaMovAvBase(Indicator.__class__):
    # Register any MovingAverage with the placeholder to allow the automatic
    # creation of envelopes and oscillators
    # 创建移动平均值的类
    def __new__(meta, name, bases, dct):
        # Create the class
        cls = super(MetaMovAvBase, meta).__new__(meta, name, bases, dct)

        MovingAverage.register(cls)

        # return the class
        return cls

# 移动平均的基类，增加参数和画图的设置
class MovingAverageBase(with_metaclass(MetaMovAvBase, Indicator)):
    # 参数
    params = (('period', 30),)
    # 默认画到主图上
    plotinfo = dict(subplot=False)
