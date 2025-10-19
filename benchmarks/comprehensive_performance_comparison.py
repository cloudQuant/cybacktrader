#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
全面性能对比测试
对比三种实现：backtrader(CPython), backtrader(PyPy), cybacktrader(CPython)
生成详细的性能报告和可视化图表
"""

import sys
import time
import statistics
import subprocess
import os
import json
from pathlib import Path

def get_python_version():
    """获取Python版本信息"""
    impl = sys.implementation.name
    version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    
    if impl == 'cpython':
        return f"CPython {version}", "CPython"
    elif impl == 'pypy':
        pypy_version = sys.pypy_version_info
        return f"PyPy {pypy_version.major}.{pypy_version.minor}.{pypy_version.micro}", "PyPy"
    else:
        return f"{impl} {version}", impl

def generate_test_data(n_rows=10000):
    """生成测试数据"""
    try:
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
        
        csv_file = 'performance_comparison_data.csv'
        df.to_csv(csv_file, index=False)
        print(f"✓ 数据已保存到: {csv_file}")
        return csv_file
    except ImportError as e:
        print(f"✗ 无法生成数据: {e}")
        # 尝试使用现有数据
        existing = ['compare_implementations_data.csv', '../tests/datas/2006-day-001.txt']
        for f in existing:
            if os.path.exists(f):
                print(f"✓ 使用现有数据: {f}")
                return f
        raise

def run_benchmark(module_name, csv_file, rounds=3):
    """运行单个基准测试"""
    try:
        if module_name == 'backtrader':
            import backtrader as bt
        else:
            import cybacktrader as bt
        
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
        
        times = []
        for i in range(rounds):
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
            times.append(elapsed)
            print(f"    第{i+1}轮: {elapsed:.4f}秒")
        
        return {
            'times': times,
            'avg': statistics.mean(times),
            'min': min(times),
            'max': max(times),
            'std': statistics.stdev(times) if len(times) > 1 else 0,
        }
    except Exception as e:
        print(f"    ✗ 测试失败: {e}")
        return None

def run_pypy_benchmark(csv_file, rounds=3):
    """使用PyPy运行backtrader测试"""
    pypy_script = f"""
import sys
import time
import statistics

def run_test():
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
        dataname='{csv_file}',
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
    rounds = {rounds}
    times = []
    for i in range(rounds):
        elapsed = run_test()
        times.append(elapsed)
        print(f"{{elapsed:.4f}}")
    
    print(f"AVG:{{statistics.mean(times):.4f}}")
    print(f"MIN:{{min(times):.4f}}")
    print(f"MAX:{{max(times):.4f}}")
    print(f"STD:{{statistics.stdev(times) if len(times) > 1 else 0:.4f}}")
"""
    
    pypy_test_file = 'pypy_benchmark_temp.py'
    with open(pypy_test_file, 'w') as f:
        f.write(pypy_script)
    
    try:
        # 检查PyPy虚拟环境
        pypy_venv = os.path.expanduser('~/pypy3-backtrader-env/bin/python')
        if os.path.exists(pypy_venv):
            pypy_cmd = pypy_venv
        else:
            pypy_cmd = 'pypy3'
        
        print(f"    使用: {pypy_cmd}")
        result = subprocess.run(
            [pypy_cmd, pypy_test_file],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode != 0:
            print(f"    ✗ PyPy运行失败: {result.stderr}")
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
                    print(f"    第{len(times)}轮: {t:.4f}秒")
                except ValueError:
                    continue
        
        stats['times'] = times
        return stats
        
    except Exception as e:
        print(f"    ✗ PyPy测试失败: {e}")
        return None
    finally:
        if os.path.exists(pypy_test_file):
            os.remove(pypy_test_file)

def create_performance_chart(results):
    """创建性能对比图表"""
    try:
        import matplotlib.pyplot as plt
        import matplotlib
        matplotlib.rcParams['font.sans-serif'] = ['Noto Sans CJK JP', 'DejaVu Sans']
        matplotlib.rcParams['axes.unicode_minus'] = False
        
        # 准备数据
        labels = []
        avg_times = []
        colors = []
        
        baseline = None
        
        for name, data in results.items():
            if data:
                labels.append(name)
                avg_times.append(data['avg'])
                if 'backtrader (CPython)' in name:
                    colors.append('#e74c3c')  # 红色
                    baseline = data['avg']
                elif 'PyPy' in name:
                    colors.append('#3498db')  # 蓝色
                else:
                    colors.append('#2ecc71')  # 绿色
        
        # 创建图表
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # 图1: 绝对时间对比
        bars1 = ax1.barh(labels, avg_times, color=colors, alpha=0.8)
        ax1.set_xlabel('平均运行时间 (秒)', fontsize=12)
        ax1.set_title('性能对比 - 绝对时间', fontsize=14, fontweight='bold')
        ax1.grid(axis='x', alpha=0.3)
        
        # 添加数值标签
        for i, (bar, time) in enumerate(zip(bars1, avg_times)):
            ax1.text(time + 0.01, bar.get_y() + bar.get_height()/2, 
                    f'{time:.3f}s', va='center', fontsize=10)
        
        # 图2: 相对性能（加速比）
        if baseline:
            speedups = [baseline / t for t in avg_times]
            bars2 = ax2.barh(labels, speedups, color=colors, alpha=0.8)
            ax2.set_xlabel('加速比 (相对于backtrader CPython)', fontsize=12)
            ax2.set_title('性能对比 - 加速比', fontsize=14, fontweight='bold')
            ax2.axvline(x=1.0, color='gray', linestyle='--', alpha=0.5, label='基准线')
            ax2.grid(axis='x', alpha=0.3)
            ax2.legend()
            
            # 添加加速比标签
            for i, (bar, speedup) in enumerate(zip(bars2, speedups)):
                ax2.text(speedup + 0.02, bar.get_y() + bar.get_height()/2, 
                        f'{speedup:.2f}x', va='center', fontsize=10, fontweight='bold')
        
        plt.tight_layout()
        
        # 保存图表
        output_file = 'performance_comparison.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"\n✓ 图表已保存: {output_file}")
        
        return output_file
        
    except ImportError as e:
        print(f"\n✗ 无法创建图表: {e}")
        print("提示: pip install matplotlib")
        return None

def main():
    print("="*70)
    print("全面性能对比测试")
    print("="*70)
    print()
    
    # 生成测试数据
    try:
        csv_file = generate_test_data(10000)
    except Exception as e:
        print(f"✗ 无法准备测试数据: {e}")
        return
    
    print()
    
    # 测试配置
    rounds = 3
    results = {}
    
    # 1. backtrader (CPython)
    print("1. 测试 backtrader (CPython)")
    print("-"*70)
    try:
        import backtrader
        print(f"  版本: {backtrader.__version__}")
        print(f"  Python: {get_python_version()[0]}")
        result = run_benchmark('backtrader', csv_file, rounds)
        if result:
            results['backtrader (CPython)'] = result
            print(f"  ✓ 平均时间: {result['avg']:.4f}秒")
    except ImportError:
        print("  ✗ backtrader未安装")
    
    print()
    
    # 2. cybacktrader (CPython)
    print("2. 测试 cybacktrader (CPython)")
    print("-"*70)
    try:
        import cybacktrader
        print(f"  版本: {cybacktrader.__version__}")
        print(f"  Python: {get_python_version()[0]}")
        result = run_benchmark('cybacktrader', csv_file, rounds)
        if result:
            results['cybacktrader (CPython)'] = result
            print(f"  ✓ 平均时间: {result['avg']:.4f}秒")
    except ImportError:
        print("  ✗ cybacktrader未安装")
    
    print()
    
    # 3. backtrader (PyPy)
    print("3. 测试 backtrader (PyPy)")
    print("-"*70)
    result = run_pypy_benchmark(csv_file, rounds)
    if result:
        results['backtrader (PyPy)'] = result
        print(f"  ✓ 平均时间: {result['avg']:.4f}秒")
        print(f"  注: 第1轮包含JIT预热时间")
    else:
        print("  ✗ PyPy测试失败或未安装")
    
    print()
    print("="*70)
    print("测试结果汇总")
    print("="*70)
    print()
    
    if not results:
        print("✗ 没有可用的测试结果")
        return
    
    # 计算基准
    baseline = results.get('backtrader (CPython)')
    if baseline:
        baseline_time = baseline['avg']
        print(f"基准: backtrader (CPython) = {baseline_time:.4f}秒")
        print()
        
        # 显示所有结果
        for name, data in results.items():
            speedup = baseline_time / data['avg']
            improvement = (speedup - 1) * 100
            print(f"{name}:")
            print(f"  平均时间: {data['avg']:.4f}秒")
            print(f"  加速比: {speedup:.2f}x")
            if improvement > 0:
                print(f"  提升: {improvement:.1f}% 🚀")
            else:
                print(f"  变化: {improvement:.1f}%")
            print()
    
    # 保存结果
    output_json = 'performance_comparison_results.json'
    with open(output_json, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"✓ 详细结果已保存: {output_json}")
    
    # 创建图表
    chart_file = create_performance_chart(results)
    
    print()
    print("="*70)
    print("测试完成！")
    print("="*70)

if __name__ == '__main__':
    main()
