#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

# Lazy import mechanism to avoid circular imports
# Indicators are imported on-demand when accessed

# Import MovAv for attribute access but don't pre-register indicators
# to avoid circular import issues during module initialization
from .mabase import MovAv  # noqa: F401

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
    'Highest': 'basicops',
    'Lowest': 'basicops',
    'SumN': 'basicops',
    
    # Moving Average Base
    'MovingAverage': 'mabase',
    'MovingAverageBase': 'mabase',
    'MovAv': 'mabase',
    'Average': 'basicops',
    
    # Moving Averages
    'SMA': 'sma',
    'SimpleMovingAverage': 'sma',
    'EMA': 'ema',
    'ExponentialMovingAverage': 'ema',
    'DEMA': 'dema',
    'DoubleExponentialMovingAverage': 'dema',
    'TEMA': 'dema',
    'TripleExponentialMovingAverage': 'dema',
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
    
    # Crossover
    'CrossOver': 'crossover',
    'CrossUp': 'crossover',
    'CrossDown': 'crossover',
    
    # Oscillators and Indicators
    'RSI': 'rsi',
    'RelativeStrengthIndex': 'rsi',
    'RSI_Safe': 'rsi',
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
    'MomentumOscillator': 'momentum',
    'RMI': 'rmi',
    'TRIX': 'trix',
    'Trix': 'trix',
    'TSI': 'tsi',
    'WilliamsR': 'williams',
    'WilliamsAD': 'williams',
    'AroonUp': 'aroon',
    'AroonDown': 'aroon',
    'AroonIndicator': 'aroon',
    'AroonUpDown': 'aroon',
    'AroonUpDownOscillator': 'aroon',
    'AroonOscillator': 'aroon',
    'DPO': 'dpo',
    'DetrendedPriceOscillator': 'dpo',
    'DirectionalMovement': 'directionalmove',
    'DM': 'directionalmove',
    'UpMove': 'directionalmove',
    'DownMove': 'directionalmove',
    'DMA': 'dma',
    'KST': 'kst',
    'LRSI': 'lrsi',
    'UltimateOscillator': 'ultimateoscillator',
    'Vortex': 'vortex',
    'ZLIND': 'zlind',
    'ZeroLagIndicator': 'zlind',
    'ZLIndicator': 'zlind',
    'ZLInd': 'zlind',
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
    
    # Envelope (base and specific types)
    'Envelope': 'envelope',
    'SMAEnvelope': 'envelope',
    'EMAEnvelope': 'envelope',
    'WMAEnvelope': 'envelope',
    'DEMAEnvelope': 'envelope',
    'TEMAEnvelope': 'envelope',
    'KAMAEnvelope': 'envelope',
    'SMMAEnvelope': 'envelope',
    
    # Oscillators (base and specific types)
    'Oscillator': 'oscillator',
    'SMAOscillator': 'oscillator',
    'SMAOsc': 'oscillator',
    'EMAOscillator': 'oscillator',
    'EMAOsc': 'oscillator',
    'WMAOscillator': 'oscillator',
    'WMAOsc': 'oscillator',
    'DEMAOscillator': 'oscillator',
    'DEMAOsc': 'oscillator',
    'TEMAOscillator': 'oscillator',
    'TEMAOsc': 'oscillator',
    'KAMAOscillator': 'oscillator',
    'KAMAOsc': 'oscillator',
    'SMMAOscillator': 'oscillator',
    'SMMAOsc': 'oscillator',
    'PrettyGoodOscillator': 'prettygoodoscillator',
    'PGO': 'prettygoodoscillator',
    'PriceOscillator': 'priceoscillator',
    'PriceOsc': 'priceoscillator',
    'PercentagePriceOscillator': 'priceoscillator',
    'PPO': 'priceoscillator',
    'PercentagePriceOscillatorShort': 'priceoscillator',
    'PPOShort': 'priceoscillator',
    'PercentChange': 'percentchange',
    'PctChange': 'percentchange',
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
    
    # Handle dynamically generated Oscillator variants (e.g., SMAOsc, KAMAOscillator)
    if name.endswith('Oscillator') or name.endswith('Osc'):
        # Extract the base moving average name
        if name.endswith('Oscillator'):
            base_name = name[:-10]  # Remove 'Oscillator'
        else:
            base_name = name[:-3]  # Remove 'Osc'
        
        # Try to create the oscillator variant dynamically
        try:
            # First ensure the moving average is loaded
            from cybacktrader.indicators.mabase import MovAv, MovingAverage
            import cybacktrader.indicators.oscillator as osc_mod
            import sys
            
            # Try to get the base moving average (this triggers registration)
            movav_class = None
            try:
                movav_class = getattr(MovAv, base_name)
            except AttributeError:
                # Try to find in registered moving averages
                for ma in MovingAverage._movavs:
                    if (ma.__name__ == base_name or
                        base_name in getattr(ma, 'alias', [])):
                        movav_class = ma
                        break
            
            if movav_class is not None:
                # Create the oscillator class dynamically
                newclsname = movav_class.__name__ + 'Oscillator'
                
                # Check if already exists in module
                if hasattr(osc_mod, newclsname) or hasattr(osc_mod, name):
                    return getattr(osc_mod, name if hasattr(osc_mod, name) else newclsname)
                
                # Create new class
                newclsdct = {
                    '__doc__': f'Oscillation of a {movav_class.__name__} around its data',
                    '__module__': osc_mod.OscillatorMixIn.__module__,
                    '_notregister': True,
                }
                newcls = type(str(newclsname), (movav_class, osc_mod.OscillatorMixIn), newclsdct)
                setattr(osc_mod, newclsname, newcls)
                # Also set the short alias
                short_name = movav_class.__name__ + 'Osc'
                setattr(osc_mod, short_name, newcls)
                return newcls
        except (ImportError, AttributeError) as e:
            pass
    
    # Handle dynamically generated Envelope variants (e.g., SMAEnvelope, KAMAEnvelope) 
    if name.endswith('Envelope'):
        base_name = name[:-8]  # Remove 'Envelope'
        
        # Try to create the envelope variant dynamically
        try:
            from cybacktrader.indicators.mabase import MovAv, MovingAverage
            import cybacktrader.indicators.envelope as env_mod
            import sys
            
            # Try to get the base moving average (this triggers registration)
            movav_class = None
            try:
                movav_class = getattr(MovAv, base_name)
            except AttributeError:
                # Try to find in registered moving averages
                for ma in MovingAverage._movavs:
                    if (ma.__name__ == base_name or
                        base_name in getattr(ma, 'alias', [])):
                        movav_class = ma
                        break
            
            if movav_class is not None:
                # Create the envelope class dynamically
                newclsname = movav_class.__name__ + 'Envelope'
                
                # Check if already exists in module
                if hasattr(env_mod, newclsname) or hasattr(env_mod, name):
                    return getattr(env_mod, name if hasattr(env_mod, name) else newclsname)
                
                # Create new class
                movname = movav_class.__name__
                try:
                    linename = movav_class.lines._getlinealias(0)
                except:
                    linename = movname
                    
                newclsdct = {
                    '__doc__': f'{movname} and envelope bands separated "perc" from it',
                    '__module__': env_mod.EnvelopeMixIn.__module__,
                    '_notregister': True,
                }
                newcls = type(str(newclsname), (movav_class, env_mod.EnvelopeMixIn), newclsdct)
                setattr(env_mod, newclsname, newcls)
                return newcls
        except (ImportError, AttributeError):
            pass
    
    raise AttributeError(f"module 'cybacktrader.indicators' has no attribute '{name}'")
