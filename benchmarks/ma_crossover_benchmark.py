# -*- coding: utf-8 -*-

"""
均线交叉策略基准测试
对比 backtrader 和 cybacktrader 在不同数据规模下的性能
"""

import os
import sys
import time
import datetime
import statistics
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

# 设置中文字体
rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
rcParams['axes.unicode_minus'] = False


def generate_ohlcv_data(n_rows, start_date=None):
    """
    生成n行的OHLCV数据
    
    参数:
        n_rows: 数据行数
        start_date: 起始日期，默认为2000-01-01
    
    返回:
        pandas DataFrame，包含日期、开盘价、最高价、最低价、收盘价、成交量
    """
    if start_date is None:
        start_date = datetime.datetime(2000, 1, 1)
    
    # 生成日期序列（使用交易日，跳过周末）
    # 为了避免日期溢出，我们循环重复使用一段时间内的日期
    dates = []
    current_date = start_date
    day_count = 0
    
    while len(dates) < n_rows:
        # 跳过周末
        if current_date.weekday() < 5:  # 0-4 是周一到周五
            dates.append(current_date)
        current_date += datetime.timedelta(days=1)
        day_count += 1
        
        # 如果日期太远，重新开始（从起始日期循环）
        # 但索引值不同，以保持数据的唯一性
        if day_count > 5000:  # 约20年的交易日
            current_date = start_date
            day_count = 0
    
    # 生成价格数据：使用随机游走模拟真实价格走势
    np.random.seed(42)  # 固定随机种子以确保可重复性
    
    # 初始价格
    initial_price = 100.0
    
    # 生成收益率序列（带有趋势和波动）
    returns = np.random.normal(0.0001, 0.02, n_rows)  # 平均收益率0.01%，波动率2%
    
    # 计算收盘价
    close = initial_price * np.exp(np.cumsum(returns))
    
    # 生成开盘价、最高价、最低价（基于收盘价）
    # 开盘价：收盘价的微小变化
    open_price = close * (1 + np.random.uniform(-0.005, 0.005, n_rows))
    
    # 最高价：开盘价和收盘价的最大值，再加上一个随机波动
    high = np.maximum(open_price, close) * (1 + np.random.uniform(0, 0.01, n_rows))
    
    # 最低价：开盘价和收盘价的最小值，再减去一个随机波动
    low = np.minimum(open_price, close) * (1 - np.random.uniform(0, 0.01, n_rows))
    
    # 生成成交量
    volume = np.random.randint(1000000, 10000000, n_rows)
    
    # 创建DataFrame
    df = pd.DataFrame({
        'datetime': dates,
        'open': open_price,
        'high': high,
        'low': low,
        'close': close,
        'volume': volume,
        'openinterest': 0  # backtrader需要这个字段
    })
    
    return df


def save_data_to_csv(df, filename):
    """将DataFrame保存为CSV文件"""
    # 格式化日期
    df_copy = df.copy()
    
    # 确保 datetime 列是 datetime 类型
    if not pd.api.types.is_datetime64_any_dtype(df_copy['datetime']):
        df_copy['datetime'] = pd.to_datetime(df_copy['datetime'])
    
    df_copy['datetime'] = df_copy['datetime'].dt.strftime('%Y-%m-%d')
    
    # 保存为CSV（不包含索引）
    df_copy.to_csv(filename, index=False)
    
    return filename


def create_data_feed(module, csv_file, df):
    """创建数据源"""
    bt = module
    
    # 使用通用CSV数据源
    class GenericCSV(bt.feeds.GenericCSVData):
        """通用CSV数据源"""
        params = (
            ('dtformat', '%Y-%m-%d'),
            ('datetime', 0),
            ('open', 1),
            ('high', 2),
            ('low', 3),
            ('close', 4),
            ('volume', 5),
            ('openinterest', 6),
        )
    
    return GenericCSV(dataname=csv_file)


class MACrossoverStrategy:
    """均线交叉策略基类"""
    
    @staticmethod
    def create_strategy(bt_module):
        """创建策略类"""
        bt = bt_module
        
        class Strategy(bt.Strategy):
            """
            5日均线金叉20日均线做多，死叉平多策略
            """
            params = (
                ('fast_period', 5),   # 快线周期
                ('slow_period', 20),  # 慢线周期
            )
            
            def __init__(self):
                # 创建均线指标
                self.fast_ma = bt.indicators.SMA(self.data.close, period=self.p.fast_period)
                self.slow_ma = bt.indicators.SMA(self.data.close, period=self.p.slow_period)
                
                # 创建交叉信号
                self.crossover = bt.indicators.CrossOver(self.fast_ma, self.slow_ma)
            
            def next(self):
                # 如果没有持仓
                if not self.position:
                    # 金叉（快线上穿慢线）：做多
                    if self.crossover > 0:
                        self.buy()
                else:
                    # 死叉（快线下穿慢线）：平多
                    if self.crossover < 0:
                        self.close()
        
        return Strategy


def run_benchmark(module_name, df, csv_file, rounds=3):
    """
    运行基准测试
    
    参数:
        module_name: 模块名称 ('backtrader' 或 'cybacktrader')
        df: pandas DataFrame数据
        csv_file: CSV文件路径
        rounds: 运行轮数
    
    返回:
        字典，包含运行时间统计
    """
    mod = __import__(module_name)
    bt = mod
    
    times = []
    
    for _ in range(rounds):
        # 创建Cerebro引擎
        cerebro = bt.Cerebro(runonce=True, preload=True)
        
        # 添加数据
        data = create_data_feed(bt, csv_file, df)
        cerebro.adddata(data)
        
        # 添加策略
        Strategy = MACrossoverStrategy.create_strategy(bt)
        cerebro.addstrategy(Strategy)
        
        # 设置初始资金
        cerebro.broker.setcash(100000.0)
        
        # 设置佣金
        cerebro.broker.setcommission(commission=0.001)
        
        # 运行并计时
        t0 = time.perf_counter()
        cerebro.run()
        elapsed = time.perf_counter() - t0
        times.append(elapsed)
    
    return {
        'min': min(times),
        'max': max(times),
        'avg': statistics.mean(times),
        'median': statistics.median(times),
        'std': statistics.stdev(times) if len(times) > 1 else 0,
        'raw': times
    }


def format_number(n):
    """格式化数字，如 10000 -> '1万', 1000000 -> '100万'"""
    if n >= 100000000:
        return f"{n // 100000000}亿"
    elif n >= 10000:
        return f"{n // 10000}万"
    else:
        return str(n)


def run_comparison(data_sizes, rounds=3):
    """
    运行性能对比测试
    
    参数:
        data_sizes: 数据规模列表
        rounds: 每个规模运行的轮数
    
    返回:
        结果字典
    """
    results = {
        'backtrader': {},
        'cybacktrader': {}
    }
    
    print("=" * 80)
    print("均线交叉策略基准测试")
    print("策略：5日均线金叉20日均线做多，死叉平多")
    print("=" * 80)
    print()
    
    for n_rows in data_sizes:
        print(f"生成 {format_number(n_rows)} 行数据...")
        df = generate_ohlcv_data(n_rows)
        
        # 保存为临时CSV文件
        csv_file = f'temp_data_{n_rows}.csv'
        save_data_to_csv(df, csv_file)
        
        print(f"运行 backtrader 基准测试（{format_number(n_rows)} 行数据）...")
        try:
            bt_result = run_benchmark('backtrader', df, csv_file, rounds=rounds)
            results['backtrader'][n_rows] = bt_result
            print(f"  平均耗时: {bt_result['avg']:.4f} 秒")
        except Exception as e:
            print(f"  错误: {e}")
            results['backtrader'][n_rows] = None
        
        print(f"运行 cybacktrader 基准测试（{format_number(n_rows)} 行数据）...")
        try:
            cy_result = run_benchmark('cybacktrader', df, csv_file, rounds=rounds)
            results['cybacktrader'][n_rows] = cy_result
            print(f"  平均耗时: {cy_result['avg']:.4f} 秒")
        except Exception as e:
            print(f"  错误: {e}")
            results['cybacktrader'][n_rows] = None
        
        # 删除临时CSV文件
        try:
            os.remove(csv_file)
        except:
            pass
        
        # 计算加速比
        if results['backtrader'][n_rows] and results['cybacktrader'][n_rows]:
            speedup = bt_result['avg'] / cy_result['avg']
            print(f"  加速比: {speedup:.2f}x")
        
        print()
    
    return results


def plot_results(results, data_sizes):
    """
    绘制性能对比图
    
    参数:
        results: 测试结果字典
        data_sizes: 数据规模列表
    """
    # 提取数据
    bt_times = [results['backtrader'][n]['avg'] if results['backtrader'][n] else None 
                for n in data_sizes]
    cy_times = [results['cybacktrader'][n]['avg'] if results['cybacktrader'][n] else None 
                for n in data_sizes]
    
    # 过滤掉None值
    valid_indices = [i for i in range(len(data_sizes)) 
                     if bt_times[i] is not None and cy_times[i] is not None]
    
    if not valid_indices:
        print("没有有效的测试结果可以绘图")
        return
    
    valid_sizes = [data_sizes[i] for i in valid_indices]
    valid_bt_times = [bt_times[i] for i in valid_indices]
    valid_cy_times = [cy_times[i] for i in valid_indices]
    
    # 创建图表
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # 图1：运行时间对比
    x_labels = [format_number(n) for n in valid_sizes]
    x_pos = np.arange(len(x_labels))
    
    width = 0.35
    ax1.bar(x_pos - width/2, valid_bt_times, width, label='backtrader', alpha=0.8)
    ax1.bar(x_pos + width/2, valid_cy_times, width, label='cybacktrader', alpha=0.8)
    
    ax1.set_xlabel('数据行数', fontsize=12)
    ax1.set_ylabel('运行时间（秒）', fontsize=12)
    ax1.set_title('backtrader vs cybacktrader 运行时间对比', fontsize=14, fontweight='bold')
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(x_labels)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 图2：加速比
    speedups = [bt / cy for bt, cy in zip(valid_bt_times, valid_cy_times)]
    
    ax2.plot(x_pos, speedups, marker='o', linewidth=2, markersize=8, color='green')
    ax2.axhline(y=1, color='r', linestyle='--', alpha=0.5, label='1x基准线')
    
    ax2.set_xlabel('数据行数', fontsize=12)
    ax2.set_ylabel('加速比（倍）', fontsize=12)
    ax2.set_title('cybacktrader 相对于 backtrader 的加速比', fontsize=14, fontweight='bold')
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(x_labels)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 在数据点上标注数值
    for i, (x, y) in enumerate(zip(x_pos, speedups)):
        ax2.annotate(f'{y:.2f}x', xy=(x, y), xytext=(0, 10), 
                    textcoords='offset points', ha='center', fontsize=10)
    
    plt.tight_layout()
    
    # 保存图表
    output_dir = os.path.dirname(__file__)
    output_path = os.path.join(output_dir, 'ma_crossover_benchmark_results.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"图表已保存到: {output_path}")
    
    # 显示图表
    plt.show()


def print_summary(results, data_sizes):
    """打印结果摘要"""
    print()
    print("=" * 80)
    print("测试结果摘要")
    print("=" * 80)
    print()
    
    print(f"{'数据规模':<15} {'backtrader(秒)':<20} {'cybacktrader(秒)':<20} {'加速比':<10}")
    print("-" * 80)
    
    for n_rows in data_sizes:
        bt_result = results['backtrader'].get(n_rows)
        cy_result = results['cybacktrader'].get(n_rows)
        
        if bt_result and cy_result:
            bt_time = bt_result['avg']
            cy_time = cy_result['avg']
            speedup = bt_time / cy_time
            
            print(f"{format_number(n_rows):<15} {bt_time:<20.4f} {cy_time:<20.4f} {speedup:<10.2f}x")
        else:
            print(f"{format_number(n_rows):<15} {'N/A':<20} {'N/A':<20} {'N/A':<10}")
    
    print("-" * 80)
    print()


if __name__ == "__main__":
    # 定义测试的数据规模
    # 注意：可以通过修改这个列表来调整测试规模
    data_sizes = [
        10000,      # 1万行
        100000,     # 10万行
        # 1000000,    # 100万行（可选，耗时较长）
        # 10000000,   # 1千万行（可选，耗时很长）
        # 100000000,  # 1亿行（可选，耗时很长且需要大量内存）
    ]
    
    # 运行基准测试
    rounds = 1  # 每个规模运行1轮
    results = run_comparison(data_sizes, rounds=rounds)
    
    # 打印结果摘要
    print_summary(results, data_sizes)
    
    # 绘制对比图
    plot_results(results, data_sizes)
    
    print()
    print("基准测试完成！")

