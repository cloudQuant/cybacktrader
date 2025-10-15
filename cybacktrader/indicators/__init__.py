#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

# Lazy import mechanism to avoid circular imports
# Indicators are imported on-demand when accessed

_indicator_modules = {
    # Basic
    'PeriodN': 'basicops',
    'And': 'basicops',
    'Or': 'basicops',
    'If': 'basicops',
    'Any': 'basicops',
    'All': 'basicops',
    'Cmp': 'basicops',
    'Max': 'basicops',
    'Min': 'basicops',
    'Sum': 'basicops',
    'Reduce': 'basicops',
    
    # Moving Average Base
    'MovingAverage': 'mabase',
    'MovingAverageBase': 'mabase',
    'MovAv': 'mabase',
    'Average': 'mabase',
    
    # Moving Averages
    'SMA': 'sma',
    'SimpleMovingAverage': 'sma',
    'EMA': 'ema',
    'ExponentialMovingAverage': 'ema',
    'DEMA': 'dema',
    'DoubleExponentialMovingAverage': 'dema',
    'WMA': 'wma',
    'WeightedMovingAverage': 'wma',
    'SMMA': 'smma',
    'SmoothedMovingAverage': 'smma',
    'ZLEMA': 'zlema',
    'ZeroLagExponentialMovingAverage': 'zlema',
    'HMA': 'hma',
    'HullMovingAverage': 'hma',
    'KAMA': 'kama',
    'KaufmanAdaptiveMovingAverage': 'kama',
    'TEMA': 'dema',  # Assuming TEMA is in dema module
    
    # Crossover
    'CrossOver': 'crossover',
    'CrossUp': 'crossover',
    'CrossDown': 'crossover',
    
    # Oscillators and Indicators
    'RSI': 'rsi',
    'RelativeStrengthIndex': 'rsi',
    'Stochastic': 'stochastic',
    'StochasticFull': 'stochastic',
    'StochasticFast': 'stochastic',
    'CCI': 'cci',
    'CommodityChannelIndex': 'cci',
    'ATR': 'atr',
    'AverageTrueRange': 'atr',
    'Momentum': 'momentum',
    'RateOfChange': 'momentum',
    'ROC': 'momentum',
    'RMI': 'rmi',
    'TRIX': 'trix',
    'TSI': 'tsi',
    'WilliamsR': 'williams',
    'WilliamsAD': 'williams',
    'AroonUp': 'aroon',
    'AroonDown': 'aroon',
    'AroonIndicator': 'aroon',
    'AroonOscillator': 'aroon',
    'DPO': 'dpo',
    'DetrendedPriceOscillator': 'dpo',
    'DirectionalMovement': 'directionalmove',
    'DM': 'directionalmove',
    'DMA': 'dma',
    'KST': 'kst',
    'LRSI': 'lrsi',
    'UltimateOscillator': 'ultimateoscillator',
    'Vortex': 'vortex',
    'ZLIND': 'zlind',
    'PSAR': 'psar',
    'ParabolicSAR': 'psar',
    'Ichimoku': 'ichimoku',
    'HeikinAshi': 'heikinashi',
    'AwesomeOscillator': 'awesomeoscillator',
    'AO': 'awesomeoscillator',
    
    # MACD
    'MACD': 'macd',
    'MACDHisto': 'macd',
    
    # Bollinger
    'BollingerBands': 'bollinger',
    'BBands': 'bollinger',
    
    # Envelope
    'Envelope': 'envelope',
    'SMAEnvelope': 'envelope',
    'EMAEnvelope': 'envelope',
    'WMAEnvelope': 'envelope',
    'DEMAEnvelope': 'envelope',
    'TEMAEnvelope': 'envelope',
    'KAMAEnvelope': 'envelope',
    'SMMAEnvelope': 'envelope',
    
    # Oscillators
    'Oscillator': 'oscillator',
    'PrettyGoodOscillator': 'prettygoodoscillator',
    'PGO': 'prettygoodoscillator',
    'PriceOscillator': 'priceoscillator',
    'PercentChange': 'percentchange',
    'PercentRank': 'percentrank',
    'PivotPoint': 'pivotpoint',
    
    # Special
    'DV2': 'dv2',
    'HADelta': 'hadelta',
    'Hurst': 'hurst',
    'OLS': 'ols',
    
    # Composite indicators
    'AccelerationDecelerationOscillator': 'accdecoscillator',
    'AccDec': 'accdecoscillator',
    
    # Deviation
    'StandardDeviation': 'deviation',
    'StdDev': 'deviation',
}

_loaded_modules = {}

def __getattr__(name):
    """Lazy load indicators on demand to avoid circular imports"""
    if name in _indicator_modules:
        module_name = _indicator_modules[name]
        
        # Load the module if not already loaded
        if module_name not in _loaded_modules:
            try:
                mod = __import__(f'cybacktrader.indicators.{module_name}', fromlist=[name])
                _loaded_modules[module_name] = mod
            except ImportError as e:
                raise AttributeError(f"Cannot import indicator '{name}' from module '{module_name}': {e}")
        
        # Get the attribute from the loaded module
        mod = _loaded_modules[module_name]
        if hasattr(mod, name):
            return getattr(mod, name)
        
        # Try to find it in the module's exports
        for attr_name in dir(mod):
            attr = getattr(mod, attr_name)
            if hasattr(attr, '__name__') and attr.__name__ == name:
                return attr
    
    raise AttributeError(f"module 'cybacktrader.indicators' has no attribute '{name}'")
