#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
性能分析脚本 - 用于找出cybacktrader的真正性能瓶颈
"""
import sys
import cProfile
import pstats
from io import StringIO
import cybacktrader as bt
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import os

class TestStrategy(bt.Strategy):
    params = (
        ('fast_period', 5),
        ('slow_period', 20),
    )

    def __init__(self):
        # 快速移动平均线
        self.fast_ma = bt.indicators.SMA(self.data.close, period=self.params.fast_period)
        # 慢速移动平均线
        self.slow_ma = bt.indicators.SMA(self.data.close, period=self.params.slow_period)
        # 交叉信号
        self.crossover = bt.indicators.CrossOver(self.fast_ma, self.slow_ma)

    def next(self):
        if not self.position:
            if self.crossover > 0:
                self.buy()
        else:
            if self.crossover < 0:
                self.close()

def generate_test_data(num_bars=10000):
    """生成测试数据"""
    print(f'生成{num_bars}条测试数据...')
    
    start_date = datetime(2020, 1, 1)
    dates = [start_date + timedelta(minutes=i) for i in range(num_bars)]
    
    # 生成OHLCV数据
    np.random.seed(42)
    close_prices = 100 + np.cumsum(np.random.randn(num_bars) * 0.5)
    high_prices = close_prices + np.abs(np.random.randn(num_bars) * 0.5)
    low_prices = close_prices - np.abs(np.random.randn(num_bars) * 0.5)
    open_prices = close_prices + np.random.randn(num_bars) * 0.3
    volumes = np.random.randint(1000, 10000, num_bars)
    
    df = pd.DataFrame({
        'datetime': dates,
        'open': open_prices,
        'high': high_prices,
        'low': low_prices,
        'close': close_prices,
        'volume': volumes,
    })
    
    datafile = 'temp_profile_data.csv'
    df.to_csv(datafile, index=False)
    print(f'数据已保存到: {datafile}')
    return datafile

def run_test():
    """运行测试并进行性能分析"""
    # 生成测试数据
    datafile = generate_test_data(10000)
    
    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy)
    
    data = bt.feeds.GenericCSVData(
        dataname=datafile,
        dtformat='%Y-%m-%d %H:%M:%S',
        datetime=0,
        open=1,
        high=2,
        low=3,
        close=4,
        volume=5,
        openinterest=-1,
    )
    
    cerebro.adddata(data)
    cerebro.broker.setcash(100000.0)
    cerebro.broker.setcommission(commission=0.001)
    
    print('开始运行...')
    cerebro.run()
    print('运行完成')

if __name__ == '__main__':
    # 创建性能分析器
    profiler = cProfile.Profile()
    
    # 运行并分析
    profiler.enable()
    run_test()
    profiler.disable()
    
    # 生成报告
    s = StringIO()
    ps = pstats.Stats(profiler, stream=s)
    ps.strip_dirs()
    ps.sort_stats('cumulative')
    
    print('\n' + '='*80)
    print('Top 50 函数按累计时间排序:')
    print('='*80)
    ps.print_stats(50)
    
    # 保存到文件
    with open('profile_report.txt', 'w', encoding='utf-8') as f:
        ps = pstats.Stats(profiler, stream=f)
        ps.strip_dirs()
        ps.sort_stats('cumulative')
        ps.print_stats(100)
    
    print('\n详细报告已保存到: profile_report.txt')
