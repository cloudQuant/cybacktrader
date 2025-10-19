#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
诊断脚本 - 检查runonce模式是否真正被使用
"""
import cybacktrader as bt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class TestStrategy(bt.Strategy):
    params = (
        ('fast_period', 5),
        ('slow_period', 20),
    )

    def __init__(self):
        self.fast_ma = bt.indicators.SMA(self.data.close, period=self.params.fast_period)
        self.slow_ma = bt.indicators.SMA(self.data.close, period=self.params.slow_period)
        self.crossover = bt.indicators.CrossOver(self.fast_ma, self.slow_ma)
        
        # 计数器
        self.next_calls = 0
        self.once_calls = 0

    def next(self):
        self.next_calls += 1
        if not self.position:
            if self.crossover > 0:
                self.buy()
        else:
            if self.crossover < 0:
                self.close()
    
    def stop(self):
        print(f"\n策略统计：")
        print(f"  next()调用次数: {self.next_calls}")

# 生成测试数据
print("生成测试数据...")
n_bars = 10000
dates = [datetime(2020, 1, 1) + timedelta(days=i) for i in range(n_bars)]
np.random.seed(42)
close_prices = 100 + np.cumsum(np.random.randn(n_bars) * 0.5)
high_prices = close_prices + np.abs(np.random.randn(n_bars) * 0.5)
low_prices = close_prices - np.abs(np.random.randn(n_bars) * 0.5)
open_prices = close_prices + np.random.randn(n_bars) * 0.3
volumes = np.random.randint(1000, 10000, n_bars)

df = pd.DataFrame({
    'datetime': dates,
    'open': open_prices,
    'high': high_prices,
    'low': low_prices,
    'close': close_prices,
    'volume': volumes,
})

datafile = 'temp_diagnose_data.csv'
df.to_csv(datafile, index=False)

# 测试不同模式
for mode_name, runonce, preload in [
    ("模式1: runonce=True, preload=True", True, True),
    ("模式2: runonce=False, preload=True", False, True),
    ("模式3: runonce=False, preload=False", False, False),
]:
    print(f"\n{'='*60}")
    print(f"测试 {mode_name}")
    print(f"{'='*60}")
    
    cerebro = bt.Cerebro(runonce=runonce, preload=preload, maxcpus=1)
    
    data = bt.feeds.GenericCSVData(
        dataname=datafile,
        dtformat='%Y-%m-%d',
        datetime=0,
        open=1,
        high=2,
        low=3,
        close=4,
        volume=5,
        openinterest=-1,
    )
    
    cerebro.adddata(data)
    cerebro.addstrategy(TestStrategy)
    cerebro.broker.setcash(100000.0)
    cerebro.broker.setcommission(commission=0.001)
    
    # 检查内部状态
    print(f"\n启动前的Cerebro状态：")
    print(f"  cerebro.p.runonce = {cerebro.p.runonce}")
    print(f"  cerebro.p.preload = {cerebro.p.preload}")
    
    import time
    t0 = time.perf_counter()
    result = cerebro.run()
    elapsed = time.perf_counter() - t0
    
    print(f"\n启动后的Cerebro状态：")
    print(f"  cerebro._dorunonce = {cerebro._dorunonce}")
    print(f"  cerebro._dopreload = {cerebro._dopreload}")
    print(f"\n运行时间: {elapsed:.4f}秒")

print(f"\n{'='*60}")
print("诊断完成")
print(f"{'='*60}")
