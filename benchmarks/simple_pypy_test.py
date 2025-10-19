#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简化的PyPy性能测试 - 不依赖pandas
直接使用现有的CSV文件进行测试
"""

import sys
import time
import statistics

def get_python_version():
    """获取Python版本信息"""
    impl = sys.implementation.name
    version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    
    if impl == 'cpython':
        return f"CPython {version}"
    elif impl == 'pypy':
        pypy_version = sys.pypy_version_info
        return f"PyPy {pypy_version.major}.{pypy_version.minor}.{pypy_version.micro} (Python {version})"
    else:
        return f"{impl} {version}"

def run_backtrader_test(csv_file):
    """运行backtrader测试"""
    import backtrader as bt
    
    class TestStrategy(bt.Strategy):
        params = (
            ('fast_period', 5),
            ('slow_period', 20),
        )
        
        def __init__(self):
            self.fast_ma = bt.indicators.SMA(self.data.close, period=self.params.fast_period)
            self.slow_ma = bt.indicators.SMA(self.data.close, period=self.params.slow_period)
            self.crossover = bt.indicators.CrossOver(self.fast_ma, self.slow_ma)
        
        def next(self):
            if not self.position:
                if self.crossover > 0:
                    self.buy()
            else:
                if self.crossover < 0:
                    self.close()
    
    cerebro = bt.Cerebro(runonce=True, preload=True)
    
    data = bt.feeds.GenericCSVData(
        dataname=csv_file,
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
    
    t0 = time.perf_counter()
    cerebro.run()
    elapsed = time.perf_counter() - t0
    
    return elapsed

def main():
    print("="*70)
    print("PyPy性能测试（简化版）")
    print("="*70)
    print()
    
    # 检查backtrader
    try:
        import backtrader
        print(f"✓ backtrader版本: {backtrader.__version__}")
    except ImportError:
        print("✗ backtrader未安装")
        return
    
    # 当前Python实现
    print(f"✓ Python实现: {get_python_version()}")
    print()
    
    # 查找测试数据文件
    import os
    import glob
    
    # 尝试多个可能的位置
    possible_files = [
        'compare_implementations_data.csv',
        '../tests/datas/2006-day-001.txt',
        'data_cache/*.csv',
    ]
    
    csv_file = None
    for pattern in possible_files:
        files = glob.glob(pattern)
        if files:
            csv_file = files[0]
            break
    
    if not csv_file:
        print("✗ 未找到测试数据文件")
        print("请先运行: python compare_python_implementations.py")
        print("或使用现有的测试数据")
        return
    
    print(f"使用数据文件: {csv_file}")
    print()
    
    # 运行测试
    rounds = 3
    print(f"运行基准测试 (共{rounds}轮)...")
    print("-"*70)
    
    times = []
    for i in range(rounds):
        elapsed = run_backtrader_test(csv_file)
        times.append(elapsed)
        print(f"  第{i+1}轮: {elapsed:.4f}秒")
    
    print()
    print("="*70)
    print("测试结果:")
    print("="*70)
    print(f"平均时间: {statistics.mean(times):.4f}秒")
    print(f"最小时间: {min(times):.4f}秒")
    print(f"最大时间: {max(times):.4f}秒")
    print(f"标准差:   {statistics.stdev(times) if len(times) > 1 else 0:.4f}秒")
    print()
    
    # 如果是PyPy，给出对比建议
    if sys.implementation.name == 'pypy':
        print("提示: 请使用CPython运行相同测试进行对比")
        print("  python compare_python_implementations.py")
    else:
        print("提示: 请使用PyPy运行相同测试进行对比")
        print("  pypy3 simple_pypy_test.py")
    
    print()
    print("="*70)

if __name__ == '__main__':
    main()
