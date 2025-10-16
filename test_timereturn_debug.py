#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

import sys
sys.path.insert(0, 'tests/original_tests')

import testcommon
import cybacktrader as bt
import cybacktrader.indicators as btind

class RunStrategy(bt.Strategy):
    params = (
        ('printdata', False),
        ('printops', False),
        ('stocklike', False),
    )
    
    def __init__(self):
        self.sma = btind.SMA(self.data, period=15)
        self.cross = btind.CrossOver(self.data.close, self.sma, plot=True)

    def start(self):
        print(f"Strategy.start() - broker value: {self.broker.getvalue()}")

    def next(self):
        pass

chkdatas = 1

datas = [testcommon.getdata(i) for i in range(chkdatas)]
cerebros = testcommon.runtest(
    datas,
    RunStrategy,
    printdata=False,
    stocklike=False,
    printops=False,
    plot=False,
    analyzer=(bt.analyzers.TimeReturn, dict(timeframe=bt.TimeFrame.Years))
)

print("\n=== Checking results ===")
for cerebro in cerebros:
    strat = cerebro.runstrats[0][0]
    analyzer = strat.analyzers[0]
    analysis = analyzer.get_analysis()
    print(f"Analysis: {analysis}")
    print(f"First value: {str(analysis[next(iter(analysis.keys()))])}")
    print(f"Expected: 0.2794999999999983")
    
    # Debug analyzer internals
    print(f"\nAnalyzer debug:")
    print(f"  _value_start: {analyzer._value_start}")
    print(f"  _lastvalue: {analyzer._lastvalue}")
    print(f"  _value: {analyzer._value}")
    print(f"  _fundmode: {analyzer._fundmode}")

