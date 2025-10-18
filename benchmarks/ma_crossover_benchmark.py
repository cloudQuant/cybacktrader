# -*- coding: utf-8 -*-

"""
均线交叉策略基准测试 - 优化版
对比 backtrader 和 cybacktrader 在不同数据规模下的性能

优化内容：
1. 添加数据缓存机制，避免重复生成
2. 改进数据生成算法，提升效率
3. 优化内存使用，减少内存泄露风险
4. 添加详细的性能统计信息
"""

import os
import sys
import time
import datetime
import statistics
import pickle
import hashlib
import gc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
rcParams['axes.unicode_minus'] = False


def get_data_hash(n_rows, seed=42):
    """生成数据缓存的哈希值"""
    content = f"{n_rows}_{seed}"
    return hashlib.md5(content.encode()).hexdigest()


def load_cached_data(n_rows, cache_dir=None):
    """从缓存加载数据"""
    if cache_dir is None:
        cache_dir = os.path.join(os.path.dirname(__file__), 'data_cache')

    os.makedirs(cache_dir, exist_ok=True)

    data_hash = get_data_hash(n_rows)
    cache_file = os.path.join(cache_dir, f'ohlcv_data_{n_rows}_{data_hash}.pkl')

    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'rb') as f:
                data = pickle.load(f)
            print(f"从缓存加载 {n_rows} 行数据: {cache_file}")
            return data
        except Exception as e:
            print(f"缓存文件损坏，重新生成: {e}")
            return None

    return None


def save_cached_data(df, n_rows, cache_dir=None):
    """保存数据到缓存"""
    if cache_dir is None:
        cache_dir = os.path.join(os.path.dirname(__file__), 'data_cache')

    os.makedirs(cache_dir, exist_ok=True)

    data_hash = get_data_hash(n_rows)
    cache_file = os.path.join(cache_dir, f'ohlcv_data_{n_rows}_{data_hash}.pkl')

    try:
        with open(cache_file, 'wb') as f:
            pickle.dump(df, f)
        print(f"保存数据到缓存: {cache_file}")
    except Exception as e:
        print(f"保存缓存失败: {e}")


def generate_ohlcv_data(n_rows, start_date=None, use_cache=True):
    """
    生成或从缓存加载n行的OHLCV数据 - 优化版

    参数:
        n_rows: 数据行数
        start_date: 起始日期，默认为2000-01-01
        use_cache: 是否使用缓存

    返回:
        pandas DataFrame，包含日期、开盘价、最高价、最低价、收盘价、成交量
    """
    # 尝试从缓存加载
    if use_cache:
        cached_data = load_cached_data(n_rows)
        if cached_data is not None:
            return cached_data

    print(f"生成 {n_rows} 行OHLCV数据...")

    if start_date is None:
        start_date = datetime.datetime(2000, 1, 1)

    # 优化：预分配内存，提高效率
    dates = []
    current_date = start_date

    # 生成交易日日期序列（跳过周末）
    while len(dates) < n_rows:
        if current_date.weekday() < 5:  # 周一到周五
            dates.append(current_date)
        current_date += datetime.timedelta(days=1)

    # 固定随机种子以确保可重复性
    np.random.seed(42)

    # 优化：使用向量化操作，提高性能
    # 生成收益率序列（带有轻微趋势和波动）
    returns = np.random.normal(0.0001, 0.02, n_rows)

    # 计算收盘价（使用更稳定的累积乘积）
    initial_price = 100.0
    close_prices = np.empty(n_rows, dtype=np.float64)
    close_prices[0] = initial_price

    # 使用更高效的循环计算累积价格
    for i in range(1, n_rows):
        close_prices[i] = close_prices[i-1] * (1 + returns[i])

    # 生成开盘价（基于收盘价的小幅变化）
    open_prices = close_prices * (1 + np.random.uniform(-0.005, 0.005, n_rows))

    # 生成最高价和最低价
    price_range = np.random.uniform(0, 0.01, n_rows)
    high_prices = np.maximum(open_prices, close_prices) * (1 + price_range)
    low_prices = np.minimum(open_prices, close_prices) * (1 - price_range)

    # 生成成交量（更真实的成交量分布）
    volume_base = np.random.exponential(5000000, n_rows).astype(int) + 1000000
    volume = np.clip(volume_base, 1000000, 50000000)

    # 创建DataFrame（一次性构建，提高效率）
    df = pd.DataFrame({
        'datetime': dates,
        'open': open_prices,
        'high': high_prices,
        'low': low_prices,
        'close': close_prices,
        'volume': volume,
        'openinterest': 0  # backtrader需要这个字段
    })

    # 保存到缓存（如果启用）
    if use_cache:
        save_cached_data(df, n_rows)

    return df


def save_data_to_csv(df, filename):
    """将DataFrame保存为CSV文件 - 优化版"""
    try:
        # 格式化日期（直接修改原DataFrame，避免拷贝）
        df_copy = df.copy()

        # 确保 datetime 列是 datetime 类型
        if not pd.api.types.is_datetime64_any_dtype(df_copy['datetime']):
            df_copy['datetime'] = pd.to_datetime(df_copy['datetime'])

        df_copy['datetime'] = df_copy['datetime'].dt.strftime('%Y-%m-%d')

        # 保存为CSV（不包含索引，使用更快的引擎）
        df_copy.to_csv(filename, index=False, engine='c')

        return filename
    except Exception as e:
        print(f"保存CSV文件失败: {e}")
        return None


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


def run_benchmark(module_name, df, csv_file, rounds=3, memory_cleanup=True):
    """
    运行基准测试 - 优化版

    参数:
        module_name: 模块名称 ('backtrader' 或 'cybacktrader')
        df: pandas DataFrame数据
        csv_file: CSV文件路径
        rounds: 运行轮数
        memory_cleanup: 是否进行内存清理

    返回:
        字典，包含运行时间统计和内存使用信息
    """
    import psutil
    import os

    try:
        mod = __import__(module_name)
        bt = mod
    except ImportError as e:
        print(f"无法导入模块 {module_name}: {e}")
        return None

    times = []
    memory_usages = []

    for round_num in range(rounds):
        # 获取进程信息
        process = psutil.Process(os.getpid())
        memory_before = process.memory_info().rss / 1024 / 1024  # MB

        # 创建Cerebro引擎（优化参数）
        cerebro = bt.Cerebro(runonce=True, preload=True, maxcpus=1)

        try:
            # 添加数据
            data = create_data_feed(bt, csv_file, df)
            cerebro.adddata(data)

            # 添加策略
            Strategy = MACrossoverStrategy.create_strategy(bt)
            cerebro.addstrategy(Strategy)

            # 设置初始资金和佣金
            cerebro.broker.setcash(100000.0)
            cerebro.broker.setcommission(commission=0.001)

            # 强制垃圾回收
            if memory_cleanup:
                gc.collect()

            # 运行并计时
            t0 = time.perf_counter()
            cerebro.run()
            elapsed = time.perf_counter() - t0

            times.append(elapsed)

            # 计算内存使用
            memory_after = process.memory_info().rss / 1024 / 1024  # MB
            memory_used = memory_after - memory_before
            memory_usages.append(memory_used)

            print(f"  第{round_num+1}轮: {elapsed:.4f}s, 内存增量: {memory_used:.1f}MB")

        except Exception as e:
            print(f"  第{round_num+1}轮运行出错: {e}")
            times.append(float('inf'))
            memory_usages.append(0)
            continue

        finally:
            # 清理引用，帮助垃圾回收
            if 'cerebro' in locals():
                del cerebro
            if 'data' in locals():
                del data
            if 'Strategy' in locals():
                del Strategy

    # 计算统计信息
    valid_times = [t for t in times if t != float('inf')]

    if not valid_times:
        return None

    result = {
        'min': min(valid_times),
        'max': max(valid_times),
        'avg': statistics.mean(valid_times),
        'median': statistics.median(valid_times),
        'std': statistics.stdev(valid_times) if len(valid_times) > 1 else 0,
        'raw': times,
        'memory_avg': statistics.mean(memory_usages) if memory_usages else 0,
        'memory_max': max(memory_usages) if memory_usages else 0,
        'rounds_completed': len(valid_times)
    }

    return result


def format_number(n):
    """格式化数字，如 10000 -> '1万', 1000000 -> '100万'"""
    if n >= 100000000:
        return f"{n // 100000000}亿"
    elif n >= 10000:
        return f"{n // 10000}万"
    else:
        return str(n)


def run_comparison(data_sizes, rounds=3, use_cache=True, cleanup_cache=False):
    """
    运行性能对比测试 - 优化版

    参数:
        data_sizes: 数据规模列表
        rounds: 每个规模运行的轮数
        use_cache: 是否使用数据缓存
        cleanup_cache: 是否清理旧缓存文件

    返回:
        结果字典，包含详细的性能统计信息
    """
    results = {
        'backtrader': {},
        'cybacktrader': {},
        'data_generation_time': {},
        'total_time': 0
    }

    total_start_time = time.time()

    print("=" * 80)
    print("均线交叉策略基准测试 - 优化版")
    print("策略：5日均线金叉20日均线做多，死叉平多")
    print("优化特性：数据缓存、内存管理、详细统计")
    print("=" * 80)
    print()

    # 清理旧缓存（可选）
    if cleanup_cache:
        cache_dir = os.path.join(os.path.dirname(__file__), 'data_cache')
        if os.path.exists(cache_dir):
            import shutil
            shutil.rmtree(cache_dir)
            print("已清理旧缓存文件")
        print()

    for n_rows in data_sizes:
        print(f"处理 {format_number(n_rows)} 行数据...")

        # 生成或加载数据
        data_start_time = time.time()
        df = generate_ohlcv_data(n_rows, use_cache=use_cache)
        data_gen_time = time.time() - data_start_time

        results['data_generation_time'][n_rows] = data_gen_time
        print(f"  数据准备耗时: {data_gen_time:.2f} 秒")

        # 保存为CSV文件（临时）
        csv_file = f'temp_data_{n_rows}_{int(time.time())}.csv'
        if save_data_to_csv(df, csv_file):
            print(f"  CSV文件已创建: {csv_file}")

            # 测试 backtrader
            print(f"  运行 backtrader 基准测试...")
            bt_result = run_benchmark('backtrader', df, csv_file, rounds=rounds)
            results['backtrader'][n_rows] = bt_result

            if bt_result:
                print(f"    平均耗时: {bt_result['avg']:.4f} 秒")
                print(f"    内存使用: {bt_result['memory_avg']:.1f} MB")
            else:
                print("    运行失败")

            # 测试 cybacktrader
            print(f"  运行 cybacktrader 基准测试...")
            cy_result = run_benchmark('cybacktrader', df, csv_file, rounds=rounds)
            results['cybacktrader'][n_rows] = cy_result

            if cy_result:
                print(f"    平均耗时: {cy_result['avg']:.4f} 秒")
                print(f"    内存使用: {cy_result['memory_avg']:.1f} MB")
            else:
                print("    运行失败")

            # 计算加速比
            if bt_result and cy_result and bt_result['avg'] > 0 and cy_result['avg'] > 0:
                speedup = bt_result['avg'] / cy_result['avg']
                print(f"  加速比: {speedup:.2f}x")

                # 添加加速比到结果中
                if 'speedup' not in results:
                    results['speedup'] = {}
                results['speedup'][n_rows] = speedup
            else:
                print("  无法计算加速比")

        else:
            print("  CSV文件创建失败，跳过此规模测试")
            results['backtrader'][n_rows] = None
            results['cybacktrader'][n_rows] = None

        # 清理临时文件
        try:
            if os.path.exists(csv_file):
                os.remove(csv_file)
        except:
            pass

        # 强制垃圾回收
        gc.collect()

        print()

    # 计算总耗时
    results['total_time'] = time.time() - total_start_time

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
    """打印结果摘要 - 优化版"""
    print()
    print("=" * 100)
    print("测试结果摘要")
    print("=" * 100)
    print()

    # 打印表头
    header = f"{'数据规模':<12} {'backtrader(秒)':<15} {'cybacktrader(秒)':<15} {'加速比':<10} {'内存使用(MB)':<15} {'数据生成(秒)':<12}"
    print(header)
    print("-" * 100)

    total_bt_time = 0
    total_cy_time = 0
    valid_tests = 0

    for n_rows in data_sizes:
        bt_result = results['backtrader'].get(n_rows)
        cy_result = results['cybacktrader'].get(n_rows)
        data_gen_time = results['data_generation_time'].get(n_rows, 0)

        if bt_result and cy_result:
            bt_time = bt_result['avg']
            cy_time = cy_result['avg']
            speedup = bt_time / cy_time if cy_time > 0 else 0
            memory_usage = f"{bt_result['memory_avg']:.1f}/{cy_result['memory_avg']:.1f}"

            total_bt_time += bt_time
            total_cy_time += cy_time
            valid_tests += 1

            print(f"{format_number(n_rows):<12} {bt_time:<15.4f} {cy_time:<15.4f} {speedup:<10.2f}x {memory_usage:<15} {data_gen_time:<12.2f}")
        else:
            print(f"{format_number(n_rows):<12} {'N/A':<15} {'N/A':<15} {'N/A':<10} {'N/A':<15} {data_gen_time:<12.2f}")

    print("-" * 100)

    # 打印总体统计
    if valid_tests > 0:
        avg_speedup = total_bt_time / total_cy_time if total_cy_time > 0 else 0
        print(f"总体加速比: {avg_speedup:.2f}x (基于{valid_tests}个有效测试)")
        print(f"总测试耗时: {results['total_time']:.2f} 秒")

    print()


def run_large_scale_test(n_rows=1000000, rounds=1, use_cache=True):
    """
    运行大规模数据测试（专为100万行数据优化）

    参数:
        n_rows: 数据行数，默认100万
        rounds: 运行轮数
        use_cache: 是否使用缓存
    """
    print(f"开始大规模测试：{format_number(n_rows)} 行数据")
    print("=" * 80)

    # 运行测试
    results = run_comparison([n_rows], rounds=rounds, use_cache=use_cache)

    # 打印详细结果
    print_summary(results, [n_rows])

    return results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='均线交叉策略基准测试')
    parser.add_argument('--data-sizes', nargs='+', type=int,
                       default=[10000, 100000],
                       help='测试的数据规模列表，默认：[10000, 100000]')
    parser.add_argument('--rounds', type=int, default=1,
                       help='每个规模运行的轮数，默认：1')
    parser.add_argument('--no-cache', action='store_true',
                       help='不使用数据缓存')
    parser.add_argument('--cleanup-cache', action='store_true',
                       help='清理旧缓存文件')
    parser.add_argument('--large-scale', type=int,
                       help='运行大规模测试，指定数据行数，默认：1000000')
    parser.add_argument('--no-plot', action='store_true',
                       help='不生成图表')

    args = parser.parse_args()

    # 如果指定大规模测试
    if args.large_scale:
        results = run_large_scale_test(args.large_scale, args.rounds,
                                    use_cache=not args.no_cache)
    else:
        # 普通基准测试
        data_sizes = args.data_sizes

        print(f"测试数据规模: {[format_number(n) for n in data_sizes]}")
        print(f"每规模运行轮数: {args.rounds}")

        # 运行基准测试
        results = run_comparison(data_sizes, rounds=args.rounds,
                               use_cache=not args.no_cache,
                               cleanup_cache=args.cleanup_cache)

        # 打印结果摘要
        print_summary(results, data_sizes)

        # 绘制对比图（如果启用）
        if not args.no_plot:
            try:
                plot_results(results, data_sizes)
            except Exception as e:
                print(f"图表生成失败: {e}")

    print("基准测试完成！")

    # 保存详细结果到文件
    import json
    result_file = os.path.join(os.path.dirname(__file__), 'benchmark_results.json')
    try:
        # 转换numpy类型为可序列化类型
        def convert_for_json(obj):
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, dict):
                return {k: convert_for_json(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_for_json(i) for i in obj]
            else:
                return obj

        serializable_results = convert_for_json(results)
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(serializable_results, f, indent=2, ensure_ascii=False)
        print(f"详细结果已保存到: {result_file}")
    except Exception as e:
        print(f"保存结果失败: {e}")

