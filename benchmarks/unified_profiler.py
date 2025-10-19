#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Backtrader vs CyBacktrader 统一性能分析工具

功能：
1. 支持函数级和代码行级性能对比
2. 支持时间和内存对比
3. 支持多轮测试取平均值
4. 生成HTML和Markdown详细报告

使用示例：
    # 函数级时间对比（默认）
    python unified_profiler.py --data-size 100000
    
    # 代码行级时间对比
    python unified_profiler.py --type line --rounds 3
    
    # 函数级内存对比
    python unified_profiler.py --compare memory --rounds 5
"""

import os
import sys
import time
import cProfile
import pstats
import io
import argparse
import json
import tracemalloc
import psutil
from pathlib import Path
from datetime import datetime
import gc

# 注意：不要将项目根目录添加到 sys.path，以确保使用已安装的 cybacktrader 包
# 而不是源码目录中的未编译版本
# project_root = Path(__file__).parent.parent
# sys.path.insert(0, str(project_root))

# 尝试导入line_profiler
try:
    from line_profiler import LineProfiler
    LINE_PROFILER_AVAILABLE = True
except ImportError:
    LINE_PROFILER_AVAILABLE = False


def create_test_dataset(n_rows=100000, data_file=None):
    """创建测试数据集"""
    print(f"[图表] 创建 {n_rows:,} 行测试数据...")
    
    import pandas as pd
    import numpy as np
    from datetime import datetime as dt, timedelta
    
    np.random.seed(42)
    
    start_date = dt(2000, 1, 1)
    dates = []
    current_date = start_date
    
    while len(dates) < n_rows:
        if current_date.weekday() < 5:
            dates.append(current_date)
        current_date += timedelta(days=1)
    
    initial_price = 100.0
    returns = np.random.normal(0.0001, 0.02, n_rows)
    close_prices = np.empty(n_rows)
    close_prices[0] = initial_price
    
    for i in range(1, n_rows):
        close_prices[i] = close_prices[i-1] * (1 + returns[i])
    
    open_prices = close_prices * (1 + np.random.uniform(-0.005, 0.005, n_rows))
    price_range = np.random.uniform(0, 0.01, n_rows)
    high_prices = np.maximum(open_prices, close_prices) * (1 + price_range)
    low_prices = np.minimum(open_prices, close_prices) * (1 - price_range)
    volume = np.random.exponential(5000000, n_rows).astype(int) + 1000000
    
    df = pd.DataFrame({
        'datetime': [d.strftime('%Y-%m-%d') for d in dates],
        'open': open_prices,
        'high': high_prices,
        'low': low_prices,
        'close': close_prices,
        'volume': volume,
        'openinterest': 0
    })
    
    if data_file is None:
        data_file = f"test_data_{n_rows}.csv"
    
    os.makedirs(os.path.dirname(data_file) if os.path.dirname(data_file) else '.', exist_ok=True)
    df.to_csv(data_file, index=False)
    print(f"[成功] 数据已保存: {data_file}")
    
    return data_file


def run_strategy_with_profiling(module_name, data_file, profile_type='function', compare_metric='time'):
    """运行策略并进行性能分析"""
    
    try:
        if module_name == 'backtrader':
            import backtrader as bt
        elif module_name == 'cybacktrader':
            import cybacktrader as bt
            # 检查关键类是否存在
            if not hasattr(bt, 'Cerebro'):
                print(f"[失败] cybacktrader 模块不完整，缺少 Cerebro 类")
                print(f"       请先运行: pip install -e . 来安装 cybacktrader")
                return None
        else:
            raise ValueError(f"未知模块: {module_name}")
    except ImportError as e:
        print(f"[失败] 无法导入 {module_name}: {e}")
        return None
    
    def run_strategy():
        cerebro = bt.Cerebro(runonce=True, preload=True, maxcpus=1)
        
        class GenericCSV(bt.feeds.GenericCSVData):
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
        
        data = GenericCSV(dataname=data_file)
        cerebro.adddata(data)
        
        class MACrossStrategy(bt.Strategy):
            params = (('fast_period', 5), ('slow_period', 20))
            
            def __init__(self):
                self.fast_ma = bt.indicators.SMA(self.data.close, period=self.p.fast_period)
                self.slow_ma = bt.indicators.SMA(self.data.close, period=self.p.slow_period)
                self.crossover = bt.indicators.CrossOver(self.fast_ma, self.slow_ma)
            
            def next(self):
                if not self.position:
                    if self.crossover > 0:
                        self.buy()
                else:
                    if self.crossover < 0:
                        self.close()
        
        cerebro.addstrategy(MACrossStrategy)
        cerebro.broker.setcash(100000.0)
        cerebro.broker.setcommission(commission=0.001)
        
        cerebro.run()
    
    result = {
        'module': module_name,
        'profile_type': profile_type,
        'compare_metric': compare_metric,
        'success': False
    }
    
    try:
        if compare_metric == 'time':
            if profile_type == 'function':
                # 函数级时间分析（同时收集内存数据）
                pr = None
                
                try:
                    # 确保之前的profiler已经完全禁用
                    import sys
                    if hasattr(sys, 'getprofile') and sys.getprofile() is not None:
                        sys.setprofile(None)
                    if hasattr(sys, 'gettrace') and sys.gettrace() is not None:
                        sys.settrace(None)
                    
                    # 停止可能残留的 tracemalloc
                    if tracemalloc.is_tracing():
                        tracemalloc.stop()
                    
                    # 强制垃圾回收
                    gc.collect()
                    time.sleep(0.1)  # 给系统一点时间完全清理
                    
                    # 同时启动内存监控
                    process = psutil.Process(os.getpid())
                    memory_before = process.memory_info().rss / 1024 / 1024
                    tracemalloc.start()
                    
                    # 创建新的 profiler
                    pr = cProfile.Profile()
                    pr.enable()
                    
                    start_time = time.time()
                    run_strategy()
                    execution_time = time.time() - start_time
                    
                    pr.disable()
                    
                    # 获取内存数据
                    current, peak = tracemalloc.get_traced_memory()
                    tracemalloc.stop()
                    memory_after = process.memory_info().rss / 1024 / 1024
                    
                    stats = pstats.Stats(pr)
                    stats.sort_stats('cumulative')
                    
                    result['execution_time'] = execution_time
                    result['stats'] = stats
                    result['memory_used_mb'] = memory_after - memory_before
                    result['memory_peak_mb'] = peak / 1024 / 1024
                    result['success'] = True
                    
                finally:
                    # 确保清理
                    if pr is not None:
                        try:
                            pr.disable()
                        except:
                            pass
                    
                    try:
                        import sys
                        sys.setprofile(None)
                        sys.settrace(None)
                    except:
                        pass
                    
                    if tracemalloc.is_tracing():
                        try:
                            tracemalloc.stop()
                        except:
                            pass
                    
                    gc.collect()
                
            elif profile_type == 'line' and LINE_PROFILER_AVAILABLE:
                lp = LineProfiler()
                lp.add_function(run_strategy)
                
                start_time = time.time()
                lp.runcall(run_strategy)
                execution_time = time.time() - start_time
                
                s = io.StringIO()
                lp.print_stats(stream=s)
                line_stats = s.getvalue()
                
                result['execution_time'] = execution_time
                result['line_stats'] = line_stats
                result['success'] = True
                
        elif compare_metric == 'memory':
            process = psutil.Process(os.getpid())
            gc.collect()
            
            memory_before = process.memory_info().rss / 1024 / 1024
            tracemalloc.start()
            
            start_time = time.time()
            run_strategy()
            execution_time = time.time() - start_time
            
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            memory_after = process.memory_info().rss / 1024 / 1024
            
            result['execution_time'] = execution_time
            result['memory_used_mb'] = memory_after - memory_before
            result['memory_peak_mb'] = peak / 1024 / 1024
            result['success'] = True
            
            gc.collect()
    
    except Exception as e:
        print(f"[失败] {module_name} 执行失败: {e}")
    
    return result


def extract_function_stats(stats):
    """从pstats中提取函数统计信息"""
    if stats is None:
        return {}
    
    function_data = {}
    
    for func, (cc, nc, tt, ct, callers) in stats.stats.items():
        filename, line, func_name = func
        
        # 只过滤掉系统内置函数，保留所有用户代码
        if any(x in filename for x in ['<frozen', '<built-in>']):
            continue
        
        # 过滤掉标准库和第三方库（除了backtrader/cybacktrader）
        if 'site-packages' in filename and not any(x in filename for x in ['backtrader', 'cybacktrader']):
            continue
        
        key = f"{func_name}::{filename}::{line}"
        
        function_data[key] = {
            'function': func_name,
            'filename': filename,
            'line': line,
            'ncalls': nc,
            'tottime': tt,
            'cumtime': ct,
            'percall_tot': tt / nc if nc > 0 else 0,
            'percall_cum': ct / nc if nc > 0 else 0,
        }
    
    return function_data


def generate_markdown_report(comparison, output_file):
    """生成Markdown报告"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Backtrader vs CyBacktrader 性能对比报告\n\n")
        f.write(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**分析类型**: {comparison['profile_type']} 级别\n")
        f.write(f"**对比指标**: {comparison['compare_metric']}\n")
        f.write(f"**测试轮数**: {comparison['rounds']}\n\n")
        
        # 总体性能对比
        f.write("## [图表] 总体性能对比\n\n")
        
        bt_avg = comparison['backtrader']['avg_time']
        cy_avg = comparison['cybacktrader']['avg_time']
        speedup = comparison['comparison']['speedup']
        improvement = comparison['comparison']['improvement_percent']
        
        f.write("| 指标 | Backtrader | CyBacktrader | 改进 |\n")
        f.write("|------|------------|--------------|------|\n")
        f.write(f"| 平均执行时间 | {bt_avg:.4f}s | {cy_avg:.4f}s | {speedup:.2f}x |\n")
        f.write(f"| 时间节省 | - | - | {bt_avg - cy_avg:.4f}s ({improvement:.1f}%) |\n")
        
        # 显示内存信息（如果有）
        if 'avg_memory' in comparison['backtrader'] and 'avg_memory' in comparison['cybacktrader']:
            bt_mem = comparison['backtrader']['avg_memory']
            cy_mem = comparison['cybacktrader']['avg_memory']
            mem_saved = comparison['comparison']['memory_saved']
            mem_improvement = comparison['comparison']['memory_improvement']
            
            f.write(f"| 平均内存使用 | {bt_mem:.2f}MB | {cy_mem:.2f}MB | {mem_saved:.2f}MB ({mem_improvement:.1f}%) |\n")
            f.write(f"| 内存峰值 | {comparison['backtrader']['avg_peak']:.2f}MB | {comparison['cybacktrader']['avg_peak']:.2f}MB | - |\n")
        
        f.write("\n")
        
        # 多轮测试详情
        if comparison['rounds'] > 1:
            f.write("## [提升] 多轮测试详情\n\n")
            f.write("| 轮次 | Backtrader (s) | CyBacktrader (s) | 加速比 |\n")
            f.write("|------|----------------|------------------|--------|\n")
            
            bt_times = comparison['backtrader']['all_times']
            cy_times = comparison['cybacktrader']['all_times']
            
            for i, (bt_t, cy_t) in enumerate(zip(bt_times, cy_times), 1):
                round_speedup = bt_t / cy_t if cy_t > 0 else 0
                f.write(f"| {i} | {bt_t:.4f} | {cy_t:.4f} | {round_speedup:.2f}x |\n")
            
            f.write("\n")
        
        # 函数级对比
        if 'function_comparison' in comparison:
            func_comp = comparison['function_comparison']
            
            f.write("##  需要优化的热点函数 (Top 100)\n\n")
            f.write("以下函数在CyBacktrader中仍然耗时较多，建议进一步优化：\n\n")
            f.write("| 排名 | 函数名 | BT累积时间(s) | CY累积时间(s) | 改进(%) | 时间节省(s) | 文件 |\n")
            f.write("|------|--------|---------------|---------------|---------|-------------|------|\n")
            
            # 按backtrader累积时间排序，显示Top 100
            # 不过滤，直接排序后取前100
            hotspots = sorted(func_comp, key=lambda x: x['bt_cumtime'], reverse=True)
            
            for idx, item in enumerate(hotspots[:100], 1):
                func_name = item['function'][:50]
                filename = item['filename']
                
                improvement_str = f"{item['improvement']:+.1f}%"
                if item['improvement'] > 0:
                    improvement_str = f"[成功] {improvement_str}"
                elif item['improvement'] < -10:
                    improvement_str = f"[警告]️ {improvement_str}"
                
                f.write(f"| {idx} | `{func_name}` | {item['bt_cumtime']:.4f} | {item['cy_cumtime']:.4f} | {improvement_str} | {item['time_saved']:.4f} | {filename} |\n")
            
            # 改进最大的函数
            f.write("\n## [成功] 改进最显著的函数 (Top 20)\n\n")
            improved = [c for c in func_comp if c['improvement'] > 0 and c['bt_cumtime'] > 0.001]
            improved.sort(key=lambda x: x['time_saved'], reverse=True)
            
            if improved:
                f.write("| 排名 | 函数名 | BT累积时间(s) | CY累积时间(s) | 改进(%) | 时间节省(s) | 文件 |\n")
                f.write("|------|--------|---------------|---------------|---------|-------------|------|\n")
                
                for idx, item in enumerate(improved[:20], 1):
                    func_name = item['function'][:50]
                    filename = item['filename']
                    f.write(f"| {idx} | `{func_name}` | {item['bt_cumtime']:.4f} | {item['cy_cumtime']:.4f} | [成功] {item['improvement']:+.1f}% | {item['time_saved']:.4f} | {filename} |\n")
            
            # 性能下降的函数
            regressed = [c for c in func_comp if c['improvement'] < -5 and c['cy_cumtime'] > 0.001]
            if regressed:
                regressed.sort(key=lambda x: x['improvement'])
                
                f.write("\n## [警告]️ 需要关注的函数（性能下降）\n\n")
                f.write("| 排名 | 函数名 | BT累积时间(s) | CY累积时间(s) | 变化(%) | 额外耗时(s) | 文件 |\n")
                f.write("|------|--------|---------------|---------------|---------|-------------|------|\n")
                
                for idx, item in enumerate(regressed[:10], 1):
                    func_name = item['function'][:50]
                    filename = item['filename']
                    f.write(f"| {idx} | `{func_name}` | {item['bt_cumtime']:.4f} | {item['cy_cumtime']:.4f} | [警告]️ {item['improvement']:+.1f}% | {-item['time_saved']:.4f} | {filename} |\n")

        # 函数对齐情况
        if 'function_alignment' in comparison:
            f.write("\n##  函数对齐情况\n\n")
            f.write("| 函数名 | 文件 | BT存在 | CY存在 | BT累积时间(s) | CY累积时间(s) |\n")
            f.write("|--------|------|--------|--------|----------------|----------------|\n")
            aligned = comparison['function_alignment']
            # 重点按 BT 时间排序，显示前 200 条
            aligned = sorted(aligned, key=lambda x: x['bt_cumtime'], reverse=True)[:200]
            for item in aligned:
                f.write(f"| `{item['function']}` | {item['filename']} | {'[成功]' if item['in_bt'] else '[失败]'} | {'[成功]' if item['in_cy'] else '[失败]'} | {item['bt_cumtime']:.4f} | {item['cy_cumtime']:.4f} |\n")
        
        # 优化建议
        f.write("\n## [提示] 优化建议\n\n")
        
        if 'function_comparison' in comparison:
            f.write("### 高优先级优化目标\n\n")
            hotspots = [c for c in comparison['function_comparison'] if c['cy_cumtime'] > 0.001]
            hotspots.sort(key=lambda x: x['cy_cumtime'], reverse=True)
            
            for idx, item in enumerate(hotspots[:10], 1):
                func_name = item['function']
                filename = os.path.basename(item['filename'])
                
                f.write(f"{idx}. **`{func_name}`** (文件: `{filename}`)\n")
                f.write(f"   - 当前耗时: {item['cy_cumtime']:.4f}s\n")
                f.write(f"   - 改进空间: {item['improvement']:+.1f}%\n")
                
                if 'next' in func_name.lower():
                    f.write(f"   - 建议: 使用 `cdef` 声明，添加类型注解，考虑使用 `nogil`\n")
                elif any(x in func_name.lower() for x in ['__getitem__', '__setitem__', 'get', 'set']):
                    f.write(f"   - 建议: 优化数组访问，使用内存视图(memoryview)\n")
                elif 'sma' in func_name.lower() or 'indicator' in func_name.lower():
                    f.write(f"   - 建议: 使用Cython优化循环，使用C数学函数\n")
                else:
                    f.write(f"   - 建议: 分析函数逻辑，添加Cython类型声明\n")
                
                f.write("\n")
        
        f.write("### 通用优化策略\n\n")
        f.write("1. **使用 `cdef class`**: 将Python类转换为Cython扩展类型\n")
        f.write("2. **类型声明**: 为变量、参数和返回值添加C类型声明\n")
        f.write("3. **内存视图**: 使用typed memoryviews处理NumPy数组\n")
        f.write("4. **释放GIL**: 在纯计算代码块使用 `with nogil`\n")
        f.write("5. **C函数**: 使用 `libc.math` 中的C数学函数\n")
        f.write("6. **内联函数**: 对小型频繁调用的函数使用 `cdef inline`\n")
    
    print(f"[成功] Markdown报告已生成: {output_file}")


def generate_html_report(comparison, output_file):
    """生成HTML报告"""
    
    bt_avg = comparison['backtrader']['avg_time']
    cy_avg = comparison['cybacktrader']['avg_time']
    speedup = comparison['comparison']['speedup']
    improvement = comparison['comparison']['improvement_percent']
    
    # 构建函数表格HTML
    function_table_html = ""
    if 'function_comparison' in comparison:
        func_comp = comparison['function_comparison']
        # 按backtrader累积时间排序，显示Top 100
        hotspots = sorted(func_comp, key=lambda x: x['bt_cumtime'], reverse=True)
        
        function_table_html = "<h2> 需要优化的热点函数 (Top 100)</h2><table><thead><tr><th>排名</th><th>函数名</th><th>BT累积时间(s)</th><th>CY累积时间(s)</th><th>改进(%)</th><th>时间节省(s)</th><th>文件</th></tr></thead><tbody>"
        
        for idx, item in enumerate(hotspots[:100], 1):
            func_name = item['function'][:50]
            filename = item['filename']
            improvement_class = "positive" if item['improvement'] > 0 else "negative"
            
            function_table_html += f"<tr><td>{idx}</td><td><code>{func_name}</code></td><td>{item['bt_cumtime']:.4f}</td><td>{item['cy_cumtime']:.4f}</td><td class='{improvement_class}'>{item['improvement']:+.1f}%</td><td>{item['time_saved']:.4f}</td><td>{filename}</td></tr>"
        
        function_table_html += "</tbody></table>"
    
    # 构建多轮测试表格
    rounds_table_html = ""
    if comparison['rounds'] > 1:
        bt_times = comparison['backtrader']['all_times']
        cy_times = comparison['cybacktrader']['all_times']
        
        rounds_table_html = "<h2>[提升] 多轮测试详情</h2><table><thead><tr><th>轮次</th><th>Backtrader (s)</th><th>CyBacktrader (s)</th><th>加速比</th></tr></thead><tbody>"
        
        for i, (bt_t, cy_t) in enumerate(zip(bt_times, cy_times), 1):
            round_speedup = bt_t / cy_t if cy_t > 0 else 0
            rounds_table_html += f"<tr><td>{i}</td><td>{bt_t:.4f}</td><td>{cy_t:.4f}</td><td>{round_speedup:.2f}x</td></tr>"
        
        rounds_table_html += "</tbody></table>"
    
    # 内存卡片（如果有）
    memory_cards_html = ""
    if 'avg_memory' in comparison['backtrader'] and 'avg_memory' in comparison['cybacktrader']:
        memory_cards_html = f"""
                    <div class="stat-card">
                        <h3>Backtrader 平均内存</h3>
                        <div class="value">{comparison['backtrader']['avg_memory']:.2f}MB</div>
                        <div class="subvalue">峰值 {comparison['backtrader']['avg_peak']:.2f}MB</div>
                    </div>
                    <div class="stat-card">
                        <h3>CyBacktrader 平均内存</h3>
                        <div class="value">{comparison['cybacktrader']['avg_memory']:.2f}MB</div>
                        <div class="subvalue">峰值 {comparison['cybacktrader']['avg_peak']:.2f}MB</div>
                    </div>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Backtrader vs CyBacktrader 性能对比报告</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; border-radius: 10px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); overflow: hidden; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; text-align: center; }}
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .header p {{ font-size: 1.1em; opacity: 0.9; }}
        .content {{ padding: 40px; }}
        .section {{ margin-bottom: 40px; }}
        .section h2 {{ color: #667eea; font-size: 1.8em; margin-bottom: 20px; padding-bottom: 10px; border-bottom: 3px solid #667eea; }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .stat-card {{ background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); padding: 25px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: transform 0.3s; }}
        .stat-card:hover {{ transform: translateY(-5px); }}
        .stat-card h3 {{ font-size: 0.9em; color: #666; margin-bottom: 10px; text-transform: uppercase; }}
        .stat-card .value {{ font-size: 2em; font-weight: bold; color: #667eea; }}
        .stat-card .subvalue {{ font-size: 0.9em; color: #888; margin-top: 5px; }}
        .speedup-card {{ background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; }}
        .speedup-card h3, .speedup-card .value {{ color: white; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        th {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px; text-align: left; font-weight: 600; }}
        td {{ padding: 12px 15px; border-bottom: 1px solid #eee; }}
        tr:hover {{ background: #f5f5f5; }}
        code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-family: 'Courier New', monospace; }}
        .positive {{ color: #10b981; font-weight: bold; }}
        .negative {{ color: #ef4444; font-weight: bold; }}
        .footer {{ background: #f8f9fa; padding: 20px; text-align: center; color: #666; border-top: 1px solid #eee; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>[快速] 性能对比报告</h1>
            <p>Backtrader vs CyBacktrader</p>
            <p style="font-size: 0.9em; margin-top: 10px;">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="content">
            <div class="section">
                <h2>[图表] 总体性能对比</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <h3>Backtrader 平均时间</h3>
                        <div class="value">{bt_avg:.4f}s</div>
                    </div>
                <div class="stats-grid">
                    {memory_cards_html}
                </div>
                    <div class="stat-card">
                        <h3>CyBacktrader 平均时间</h3>
                        <div class="value">{cy_avg:.4f}s</div>
                    </div>
                    <div class="stat-card speedup-card">
                        <h3>加速比</h3>
                        <div class="value">{speedup:.2f}x</div>
                        <div class="subvalue">性能提升 {improvement:.1f}%</div>
                    </div>
                    <div class="stat-card">
                        <h3>时间节省</h3>
                        <div class="value">{bt_avg - cy_avg:.4f}s</div>
                        <div class="subvalue">每次运行</div>
                    </div>
                </div>
                
                <p><strong>分析类型:</strong> {comparison['profile_type']} 级别</p>
                <p><strong>对比指标:</strong> {comparison['compare_metric']}</p>
                <p><strong>测试轮数:</strong> {comparison['rounds']}</p>
            </div>
            
            {rounds_table_html}
            
            <div class="section">
                {function_table_html}
            </div>
            
            <div class="section">
                <h2>[提示] 优化建议</h2>
                <ul style="line-height: 2;">
                    <li><strong>使用 cdef class:</strong> 将Python类转换为Cython扩展类型</li>
                    <li><strong>类型声明:</strong> 为变量、参数和返回值添加C类型声明</li>
                    <li><strong>内存视图:</strong> 使用typed memoryviews处理NumPy数组</li>
                    <li><strong>释放GIL:</strong> 在纯计算代码块使用 with nogil</li>
                    <li><strong>C函数:</strong> 使用 libc.math 中的C数学函数</li>
                    <li><strong>内联函数:</strong> 对小型频繁调用的函数使用 cdef inline</li>
                </ul>
            </div>
        </div>
        
        <div class="footer">
            <p>CyBacktrader 性能分析工具 | 生成于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"[成功] HTML报告已生成: {output_file}")


def compare_results(bt_results, cy_results, rounds):
    """对比分析结果"""
    
    comparison = {
        'rounds': rounds,
        'profile_type': bt_results[0]['profile_type'],
        'compare_metric': bt_results[0]['compare_metric'],
        'backtrader': {},
        'cybacktrader': {},
        'comparison': {}
    }
    
    bt_times = [r['execution_time'] for r in bt_results if r['success']]
    cy_times = [r['execution_time'] for r in cy_results if r['success']]
    
    if not bt_times or not cy_times:
        print("[失败] 没有成功的测试结果")
        return None
    
    bt_avg_time = sum(bt_times) / len(bt_times)
    cy_avg_time = sum(cy_times) / len(cy_times)
    
    comparison['backtrader']['avg_time'] = bt_avg_time
    comparison['backtrader']['all_times'] = bt_times
    comparison['cybacktrader']['avg_time'] = cy_avg_time
    comparison['cybacktrader']['all_times'] = cy_times
    
    comparison['comparison']['speedup'] = bt_avg_time / cy_avg_time if cy_avg_time > 0 else 0
    comparison['comparison']['time_saved'] = bt_avg_time - cy_avg_time
    comparison['comparison']['improvement_percent'] = ((bt_avg_time - cy_avg_time) / bt_avg_time * 100) if bt_avg_time > 0 else 0
    
    # 收集内存数据（如果有）
    bt_memory = [r.get('memory_used_mb', 0) for r in bt_results if r['success'] and 'memory_used_mb' in r]
    cy_memory = [r.get('memory_used_mb', 0) for r in cy_results if r['success'] and 'memory_used_mb' in r]
    bt_peak = [r.get('memory_peak_mb', 0) for r in bt_results if r['success'] and 'memory_peak_mb' in r]
    cy_peak = [r.get('memory_peak_mb', 0) for r in cy_results if r['success'] and 'memory_peak_mb' in r]
    
    if bt_memory and cy_memory:
        comparison['backtrader']['avg_memory'] = sum(bt_memory) / len(bt_memory)
        comparison['backtrader']['avg_peak'] = sum(bt_peak) / len(bt_peak) if bt_peak else 0
        comparison['cybacktrader']['avg_memory'] = sum(cy_memory) / len(cy_memory)
        comparison['cybacktrader']['avg_peak'] = sum(cy_peak) / len(cy_peak) if cy_peak else 0
        
        comparison['comparison']['memory_saved'] = comparison['backtrader']['avg_memory'] - comparison['cybacktrader']['avg_memory']
        comparison['comparison']['memory_improvement'] = (comparison['comparison']['memory_saved'] / comparison['backtrader']['avg_memory'] * 100) if comparison['backtrader']['avg_memory'] > 0 else 0
    
    if comparison['compare_metric'] == 'time' and comparison['profile_type'] == 'function':
        bt_func_data = extract_function_stats(bt_results[-1].get('stats'))
        cy_func_data = extract_function_stats(cy_results[-1].get('stats'))
        
        all_keys = set(bt_func_data.keys()) | set(cy_func_data.keys())
        
        func_comparison = []
        function_alignment = []
        
        for key in all_keys:
            bt_info = bt_func_data.get(key, {})
            cy_info = cy_func_data.get(key, {})
            
            if '::' in key:
                parts = key.split('::')
                func_name = parts[0]
                filename = parts[1] if len(parts) > 1 else ''
            else:
                func_name = key
                filename = ''
            
            bt_cumtime = bt_info.get('cumtime', 0)
            cy_cumtime = cy_info.get('cumtime', 0)
            
            if cy_cumtime > 0 and bt_cumtime > 0:
                improvement = ((bt_cumtime - cy_cumtime) / bt_cumtime) * 100
            elif bt_cumtime > 0 and cy_cumtime == 0:
                improvement = 100
            elif bt_cumtime == 0 and cy_cumtime > 0:
                improvement = -100
            else:
                improvement = 0
            
            func_comparison.append({
                'function': func_name,
                'filename': filename,
                'bt_cumtime': bt_cumtime,
                'cy_cumtime': cy_cumtime,
                'bt_tottime': bt_info.get('tottime', 0),
                'cy_tottime': cy_info.get('tottime', 0),
                'bt_ncalls': bt_info.get('ncalls', 0),
                'cy_ncalls': cy_info.get('ncalls', 0),
                'improvement': improvement,
                'time_saved': bt_cumtime - cy_cumtime,
            })
            
            function_alignment.append({
                'function': func_name,
                'filename': filename,
                'in_bt': key in bt_func_data,
                'in_cy': key in cy_func_data,
                'bt_cumtime': bt_cumtime,
                'cy_cumtime': cy_cumtime,
            })
        
        func_comparison.sort(key=lambda x: x['bt_cumtime'], reverse=True)
        comparison['function_comparison'] = func_comparison
        comparison['function_alignment'] = function_alignment
    
    elif comparison['compare_metric'] == 'memory':
        bt_memory = [r.get('memory_used_mb', 0) for r in bt_results if r['success']]
        cy_memory = [r.get('memory_used_mb', 0) for r in cy_results if r['success']]
        bt_peak = [r.get('memory_peak_mb', 0) for r in bt_results if r['success']]
        cy_peak = [r.get('memory_peak_mb', 0) for r in cy_results if r['success']]
        
        comparison['backtrader']['avg_memory'] = sum(bt_memory) / len(bt_memory) if bt_memory else 0
        comparison['backtrader']['avg_peak'] = sum(bt_peak) / len(bt_peak) if bt_peak else 0
        comparison['cybacktrader']['avg_memory'] = sum(cy_memory) / len(cy_memory) if cy_memory else 0
        comparison['cybacktrader']['avg_peak'] = sum(cy_peak) / len(cy_peak) if cy_peak else 0
        
        comparison['comparison']['memory_saved'] = comparison['backtrader']['avg_memory'] - comparison['cybacktrader']['avg_memory']
        comparison['comparison']['memory_improvement'] = (comparison['comparison']['memory_saved'] / comparison['backtrader']['avg_memory'] * 100) if comparison['backtrader']['avg_memory'] > 0 else 0
    
    return comparison


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='Backtrader vs CyBacktrader 统一性能分析工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 函数级时间对比（默认）
  python unified_profiler.py --data-size 100000
  
  # 代码行级时间对比，运行3轮
  python unified_profiler.py --type line --rounds 3
  
  # 函数级内存对比，运行5轮
  python unified_profiler.py --compare memory --rounds 5
  
  # 完整参数示例
  python unified_profiler.py --data-size 100000 --type function --compare time --rounds 3 --output-dir reports
        """
    )
    
    parser.add_argument('--data-size', type=int, default=100000,
                       help='测试数据规模，默认：100000')
    parser.add_argument('--data-file', type=str,
                       help='指定数据文件路径（可选）')
    parser.add_argument('--type', choices=['function', 'line'], default='function',
                       help='分析类型：function=函数级，line=代码行级，默认：function')
    parser.add_argument('--compare', choices=['time', 'memory'], default='time',
                       help='对比指标：time=时间，memory=内存，默认：time')
    parser.add_argument('--rounds', type=int, default=1,
                       help='测试轮数，默认：1')
    parser.add_argument('--output-dir', type=str, default=None,
                       help='报告输出目录，默认：benchmarks/performance_reports')
    
    args = parser.parse_args()
    
    # 设置默认输出目录为benchmarks下
    if args.output_dir is None:
        benchmarks_dir = os.path.dirname(os.path.abspath(__file__))
        args.output_dir = os.path.join(benchmarks_dir, 'performance_reports')
    
    # 验证参数
    if args.type == 'line' and not LINE_PROFILER_AVAILABLE:
        print("[失败] 行级分析需要安装 line_profiler")
        print("   安装命令: pip install line_profiler")
        return 1
    
    print("="*70)
    print("Backtrader vs CyBacktrader 统一性能分析工具")
    print("="*70)
    print(f"[配置] 配置信息:")
    print(f"   数据规模: {args.data_size:,} 行")
    print(f"   分析类型: {args.type}")
    print(f"   对比指标: {args.compare}")
    print(f"   测试轮数: {args.rounds}")
    print(f"   输出目录: {args.output_dir}")
    print("="*70)
    
    # 创建输出目录
    os.makedirs(args.output_dir, exist_ok=True)
    
    # 准备数据文件
    if args.data_file and os.path.exists(args.data_file):
        data_file = args.data_file
        print(f"\n[成功] 使用现有数据文件: {data_file}")
    else:
        data_file = args.data_file if args.data_file else f"test_data_{args.data_size}.csv"
        if not os.path.exists(data_file):
            data_file = create_test_dataset(args.data_size, data_file)
        else:
            print(f"\n[成功] 使用现有数据文件: {data_file}")
    
    # 运行多轮测试
    print(f"\n{'='*70}")
    print(f"开始性能分析...")
    print(f"{'='*70}\n")
    
    bt_results = []
    cy_results = []
    
    for round_num in range(args.rounds):
        print(f"{'='*70}")
        print(f"第 {round_num + 1}/{args.rounds} 轮测试")
        print(f"{'='*70}")
        
        # 测试 Backtrader
        print(f"\n[分析] 分析 Backtrader...")
        bt_result = run_strategy_with_profiling('backtrader', data_file, args.type, args.compare)
        
        if bt_result and bt_result['success']:
            bt_results.append(bt_result)
            print(f"[成功] Backtrader 执行时间: {bt_result['execution_time']:.4f}s")
            if 'memory_used_mb' in bt_result:
                print(f"   内存使用: {bt_result.get('memory_used_mb', 0):.2f}MB")
                print(f"   内存峰值: {bt_result.get('memory_peak_mb', 0):.2f}MB")
        else:
            print(f"[失败] Backtrader 测试失败")
        
        # 测试 CyBacktrader
        print(f"\n[分析] 分析 CyBacktrader...")
        cy_result = run_strategy_with_profiling('cybacktrader', data_file, args.type, args.compare)
        
        if cy_result and cy_result['success']:
            cy_results.append(cy_result)
            print(f"[成功] CyBacktrader 执行时间: {cy_result['execution_time']:.4f}s")
            if 'memory_used_mb' in cy_result:
                print(f"   内存使用: {cy_result.get('memory_used_mb', 0):.2f}MB")
                print(f"   内存峰值: {cy_result.get('memory_peak_mb', 0):.2f}MB")
        else:
            print(f"[失败] CyBacktrader 测试失败")
        
        # 显示本轮对比
        if bt_result and cy_result and bt_result['success'] and cy_result['success']:
            round_speedup = bt_result['execution_time'] / cy_result['execution_time']
            print(f"\n[图表] 本轮加速比: {round_speedup:.2f}x")
        
        print()
    
    # 检查是否有成功的测试
    if not bt_results or not cy_results:
        print("\n[失败] 没有成功的测试结果，无法生成报告")
        return 1
    
    # 对比分析
    print(f"\n{'='*70}")
    print("生成对比报告...")
    print(f"{'='*70}\n")
    
    comparison = compare_results(bt_results, cy_results, args.rounds)
    
    if comparison is None:
        print("[失败] 对比分析失败")
        return 1
    
    # 生成报告（文件名包含数据规模）
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    # 优先从数据文件名中解析规模，例如 test_data_1000000.csv
    ds = 0
    try:
        base = os.path.basename(str(locals().get('data_file', '')))
        if base.startswith('test_data_') and base.endswith('.csv'):
            numpart = base[len('test_data_'):-4]
            if numpart.isdigit():
                ds = int(numpart)
    except Exception:
        ds = 0
    # 回退到 --data-size
    if not ds:
        try:
            ds = int(getattr(args, 'data_size', 0) or 0)
        except Exception:
            ds = 0
    if ds >= 1_000_000:
        size_suffix = f"{ds // 1_000_000}M"
    elif ds >= 1_000:
        size_suffix = f"{ds // 1_000}K"
    elif ds > 0:
        size_suffix = f"{ds}"
    else:
        size_suffix = "unknown"

    markdown_file = os.path.join(args.output_dir, f'performance_report_{size_suffix}_{timestamp}.md')
    generate_markdown_report(comparison, markdown_file)
    
    html_file = os.path.join(args.output_dir, f'performance_report_{size_suffix}_{timestamp}.html')
    generate_html_report(comparison, html_file)
    
    # 保存JSON数据
    json_file = os.path.join(args.output_dir, f'performance_data_{size_suffix}_{timestamp}.json')
    
    # 准备JSON数据（移除不能序列化的对象）
    json_data = {
        'timestamp': datetime.now().isoformat(),
        'config': {
            'data_size': args.data_size,
            'profile_type': args.type,
            'compare_metric': args.compare,
            'rounds': args.rounds,
        },
        'summary': {
            'backtrader_avg_time': comparison['backtrader']['avg_time'],
            'cybacktrader_avg_time': comparison['cybacktrader']['avg_time'],
            'speedup': comparison['comparison']['speedup'],
            'improvement_percent': comparison['comparison']['improvement_percent'],
        }
    }
    
    if 'function_comparison' in comparison:
        json_data['function_comparison'] = comparison['function_comparison']
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    print(f"[成功] JSON数据已保存: {json_file}")
    
    # 打印摘要
    print(f"\n{'='*70}")
    print("性能对比摘要")
    print(f"{'='*70}")
    print(f"Backtrader 平均时间:    {comparison['backtrader']['avg_time']:.4f}s")
    print(f"CyBacktrader 平均时间:  {comparison['cybacktrader']['avg_time']:.4f}s")
    print(f"加速比:                 {comparison['comparison']['speedup']:.2f}x")
    print(f"时间节省:               {comparison['comparison']['time_saved']:.4f}s ({comparison['comparison']['improvement_percent']:.1f}%)")
    
    if 'avg_memory' in comparison['backtrader'] and 'avg_memory' in comparison['cybacktrader']:
        print(f"Backtrader 平均内存:    {comparison['backtrader']['avg_memory']:.2f}MB")
        print(f"CyBacktrader 平均内存:  {comparison['cybacktrader']['avg_memory']:.2f}MB")
        print(f"内存节省:               {comparison['comparison']['memory_saved']:.2f}MB ({comparison['comparison']['memory_improvement']:.1f}%)")
    
    print(f"{'='*70}")
    
    print(f"\n[成功] 所有报告已生成到目录: {args.output_dir}")
    print(f"    Markdown报告: {markdown_file}")
    print(f"    HTML报告: {html_file}")
    print(f"   [图表] JSON数据: {json_file}")
    
    # 清理测试数据文件（如果是自动生成的）
    if not args.data_file and os.path.exists(data_file):
        try:
            os.remove(data_file)
            print(f"\n️  已清理测试数据文件: {data_file}")
        except:
            pass
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
