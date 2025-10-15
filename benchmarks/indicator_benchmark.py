# -*- coding: utf-8 -*-

"""
Benchmark for comparing indicator performance between backtrader and cybacktrader
"""

import os
import time
import statistics
import datetime


def run_sma_test(module_name, rounds=5):
    """Run SMA indicator test"""
    mod = __import__(module_name)
    bt = mod
    
    # Get data file
    base_dir = os.path.dirname(os.path.dirname(__file__))
    datapath = os.path.join(base_dir, 'tests', 'datas', '2006-day-001.txt')
    
    class SMAStrategy(bt.Strategy):
        params = dict(period=30)
        
        def __init__(self):
            # Use SMA which internally uses Average
            self.sma = bt.indicators.SMA(self.data, period=self.p.period)
        
        def next(self):
            pass  # Just calculate, don't trade
    
    times = []
    for _ in range(rounds):
        data = bt.feeds.BacktraderCSVData(
            dataname=datapath,
            fromdate=datetime.datetime(2006, 1, 1),
            todate=datetime.datetime(2006, 12, 31),
        )
        
        cerebro = bt.Cerebro(runonce=True, preload=True)
        cerebro.adddata(data)
        cerebro.addstrategy(SMAStrategy, period=30)
        
        t0 = time.perf_counter()
        cerebro.run()
        times.append(time.perf_counter() - t0)
    
    return {
        'min': min(times),
        'max': max(times),
        'avg': statistics.mean(times),
        'raw': times
    }


if __name__ == "__main__":
    print("=" * 60)
    print("Indicator Performance Benchmark: SMA(30)")
    print("=" * 60)
    print()
    
    # Run benchmarks
    print("Running backtrader benchmark...")
    bt_result = run_sma_test("backtrader", rounds=5)
    
    print("Running cybacktrader benchmark...")
    cy_result = run_sma_test("cybacktrader", rounds=5)
    
    # Display results
    print()
    print("Results (seconds):")
    print("-" * 60)
    print(f"{'Module':<20} {'Min':<12} {'Avg':<12} {'Max':<12}")
    print("-" * 60)
    print(f"{'backtrader':<20} {bt_result['avg']:.6f}   {bt_result['avg']:.6f}   {bt_result['max']:.6f}")
    print(f"{'cybacktrader':<20} {cy_result['avg']:.6f}   {cy_result['avg']:.6f}   {cy_result['max']:.6f}")
    print("-" * 60)
    
    # Calculate speedup
    speedup = bt_result['avg'] / cy_result['avg']
    improvement = ((bt_result['avg'] - cy_result['avg']) / bt_result['avg']) * 100
    
    print()
    print(f"Speedup: {speedup:.2f}x")
    print(f"Improvement: {improvement:.1f}%")
    print()
    
    if speedup > 1.1:
        print("✓ cybacktrader is faster!")
    elif speedup < 0.9:
        print("✗ Performance regression detected")
    else:
        print("≈ Similar performance")

