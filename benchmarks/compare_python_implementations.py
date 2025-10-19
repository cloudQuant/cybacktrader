#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python实现对比基准测试
对比CPython 3.13和PyPy运行backtrader的性能差异

目的：
1. 了解PyPy JIT编译能否显著提升backtrader性能
2. 评估性能瓶颈是在Python解释器层面还是算法层面
3. 为cybacktrader优化提供参考数据
"""

import sys
import time
import statistics
import subprocess
import os
from pathlib import Path

def generate_test_data(n_rows=10000):
    """生成测试数据"""
    import pandas as pd
    import numpy as np
    from datetime import datetime, timedelta
    
    print(f"生成{n_rows}行测试数据...")
    np.random.seed(42)
    
    start_date = datetime(2020, 1, 1)
    dates = [start_date + timedelta(days=i) for i in range(n_rows)]
    
    close_prices = 100 + np.cumsum(np.random.randn(n_rows) * 0.5)
    high_prices = close_prices + np.abs(np.random.randn(n_rows) * 0.5)
    low_prices = close_prices - np.abs(np.random.randn(n_rows) * 0.5)
    open_prices = close_prices + np.random.randn(n_rows) * 0.3
    volumes = np.random.randint(1000, 10000, n_rows)
    
    df = pd.DataFrame({
        'datetime': dates,
        'open': open_prices,
        'high': high_prices,
        'low': low_prices,
        'close': close_prices,
        'volume': volumes,
    })
    
    csv_file = 'compare_implementations_data.csv'
    df.to_csv(csv_file, index=False)
    print(f"数据已保存到: {csv_file}")
    return csv_file

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

def benchmark_single_run(csv_file, rounds=3):
    """单次基准测试"""
    times = []
    
    for i in range(rounds):
        elapsed = run_backtrader_test(csv_file)
        times.append(elapsed)
        print(f"  第{i+1}轮: {elapsed:.4f}秒")
    
    return {
        'times': times,
        'avg': statistics.mean(times),
        'min': min(times),
        'max': max(times),
        'std': statistics.stdev(times) if len(times) > 1 else 0,
    }

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

def check_pypy_available():
    """检查PyPy是否可用"""
    try:
        result = subprocess.run(['pypy3', '--version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if result.returncode == 0:
            return True, result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return False, None

def run_with_pypy(script_path, csv_file, rounds=3):
    """使用PyPy运行测试"""
    # 创建PyPy测试脚本
    pypy_script = """
import sys
import time
import statistics

def run_backtrader_test(csv_file):
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

if __name__ == '__main__':
    csv_file = sys.argv[1]
    rounds = int(sys.argv[2])
    
    times = []
    for i in range(rounds):
        elapsed = run_backtrader_test(csv_file)
        times.append(elapsed)
        print(f"{elapsed:.4f}")
    
    # 输出统计信息
    print(f"AVG:{statistics.mean(times):.4f}")
    print(f"MIN:{min(times):.4f}")
    print(f"MAX:{max(times):.4f}")
    print(f"STD:{statistics.stdev(times) if len(times) > 1 else 0:.4f}")
"""
    
    pypy_test_file = 'pypy_test_temp.py'
    with open(pypy_test_file, 'w') as f:
        f.write(pypy_script)
    
    try:
        print("使用PyPy运行测试...")
        result = subprocess.run(
            ['pypy3', pypy_test_file, csv_file, str(rounds)],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode != 0:
            print(f"PyPy运行失败: {result.stderr}")
            return None
        
        # 解析输出
        lines = result.stdout.strip().split('\n')
        times = []
        stats = {}
        
        for i, line in enumerate(lines):
            if line.startswith('AVG:'):
                stats['avg'] = float(line.split(':')[1])
            elif line.startswith('MIN:'):
                stats['min'] = float(line.split(':')[1])
            elif line.startswith('MAX:'):
                stats['max'] = float(line.split(':')[1])
            elif line.startswith('STD:'):
                stats['std'] = float(line.split(':')[1])
            else:
                try:
                    t = float(line)
                    times.append(t)
                    print(f"  第{len(times)}轮: {t:.4f}秒")
                except ValueError:
                    continue
        
        stats['times'] = times
        return stats
        
    except subprocess.TimeoutExpired:
        print("PyPy测试超时")
        return None
    finally:
        if os.path.exists(pypy_test_file):
            os.remove(pypy_test_file)

def main():
    print("="*70)
    print("Python实现性能对比基准测试")
    print("="*70)
    print()
    
    # 检查backtrader是否安装
    try:
        import backtrader
        print(f"✓ backtrader版本: {backtrader.__version__}")
    except ImportError:
        print("✗ backtrader未安装")
        print("请先安装: pip install backtrader")
        return
    
    # 生成测试数据
    csv_file = generate_test_data(10000)
    print()
    
    # 当前Python实现测试
    print(f"当前Python实现: {get_python_version()}")
    print("-"*70)
    
    current_impl = sys.implementation.name
    rounds = 3
    
    if current_impl == 'cpython':
        print(f"运行CPython基准测试 (共{rounds}轮)...")
        cpython_result = benchmark_single_run(csv_file, rounds)
        print(f"\nCPython结果:")
        print(f"  平均时间: {cpython_result['avg']:.4f}秒")
        print(f"  最小时间: {cpython_result['min']:.4f}秒")
        print(f"  最大时间: {cpython_result['max']:.4f}秒")
        print(f"  标准差: {cpython_result['std']:.4f}秒")
    else:
        print(f"运行{current_impl}基准测试 (共{rounds}轮)...")
        cpython_result = benchmark_single_run(csv_file, rounds)
        print(f"\n{current_impl}结果:")
        print(f"  平均时间: {cpython_result['avg']:.4f}秒")
    
    print()
    print("="*70)
    
    # 检查PyPy
    if current_impl != 'pypy':
        pypy_available, pypy_info = check_pypy_available()
        
        if pypy_available:
            print(f"✓ 检测到PyPy: {pypy_info}")
            print("-"*70)
            
            pypy_result = run_with_pypy(__file__, csv_file, rounds)
            
            if pypy_result:
                print(f"\nPyPy结果:")
                print(f"  平均时间: {pypy_result['avg']:.4f}秒")
                print(f"  最小时间: {pypy_result['min']:.4f}秒")
                print(f"  最大时间: {pypy_result['max']:.4f}秒")
                print(f"  标准差: {pypy_result['std']:.4f}秒")
                
                print()
                print("="*70)
                print("对比结果:")
                print("="*70)
                
                speedup = cpython_result['avg'] / pypy_result['avg']
                print(f"CPython平均时间: {cpython_result['avg']:.4f}秒")
                print(f"PyPy平均时间:    {pypy_result['avg']:.4f}秒")
                
                if speedup > 1:
                    print(f"PyPy加速比:      {speedup:.2f}x 🚀")
                    print(f"PyPy比CPython快 {(speedup-1)*100:.1f}%")
                else:
                    print(f"CPython加速比:   {1/speedup:.2f}x")
                    print(f"CPython比PyPy快 {(1/speedup-1)*100:.1f}%")
                
                print()
                print("分析:")
                if speedup > 2:
                    print("✓ PyPy显著快于CPython")
                    print("  → 说明性能瓶颈主要在Python解释器层面")
                    print("  → Cython优化可能无法获得很大收益")
                    print("  → 考虑使用PyPy作为运行时")
                elif speedup > 1.2:
                    print("✓ PyPy有一定优势")
                    print("  → Python解释器有优化空间")
                    print("  → Cython优化仍然有价值")
                elif speedup < 0.8:
                    print("✓ CPython更快")
                    print("  → 可能是NumPy/C扩展密集型")
                    print("  → Cython优化是正确的方向")
                else:
                    print("✓ 两者性能相近")
                    print("  → 瓶颈可能在算法或I/O")
                    print("  → 需要针对性优化")
        else:
            print("✗ 未检测到PyPy")
            print("提示: 可以安装PyPy进行对比测试")
            print("  Ubuntu/Debian: sudo apt-get install pypy3")
            print("  或访问: https://www.pypy.org/download.html")
    
    print()
    print("="*70)
    print("测试完成")
    print("="*70)

if __name__ == '__main__':
    main()
