#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
fast_strptime性能测试脚本
对比Python标准库的strptime和我们优化的fast_strptime
目标：10-20倍性能提升
"""

import time
import datetime
import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 导入我们的快速解析器
from cybacktrader.utils.fast_strptime import (
    fast_strptime_date,
    fast_strptime_datetime,
    fast_strptime_datetime_micro,
    fast_strptime_iso,
    strptime as fast_strptime_compat
)

def benchmark_function(name, func, test_data, iterations=100000):
    """基准测试函数"""
    print(f"\n测试 {name} ({iterations:,}次调用)")
    
    start = time.time()
    for data in test_data * (iterations // len(test_data)):
        func(*data)
    elapsed = time.time() - start
    
    print(f"  总耗时: {elapsed:.4f}秒")
    print(f"  平均每次: {elapsed/iterations*1000000:.2f}微秒")
    print(f"  每秒调用: {iterations/elapsed:,.0f}次")
    
    return elapsed

def main():
    """主测试函数"""
    print("="*70)
    print("fast_strptime 性能基准测试")
    print("="*70)
    print(f"Python版本: {sys.version}")
    print(f"测试时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    iterations = 100000
    
    # ========================================================================
    # 测试1: 日期解析 YYYY-MM-DD
    # ========================================================================
    print("\n" + "="*70)
    print("测试1: 日期解析 (YYYY-MM-DD)")
    print("="*70)
    
    test_dates = [
        ("2023-01-15",),
        ("2023-06-30",),
        ("2024-12-31",),
    ]
    
    # Python标准库
    python_time = benchmark_function(
        "Python datetime.strptime",
        lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'),
        test_dates,
        iterations
    )
    
    # 我们的快速解析器
    fast_time = benchmark_function(
        "fast_strptime_date",
        fast_strptime_date,
        test_dates,
        iterations
    )
    
    speedup = python_time / fast_time
    print(f"\n  ⚡ 加速比: {speedup:.2f}x")
    print(f"  ⚡ 性能提升: {(speedup-1)*100:.1f}%")
    
    # ========================================================================
    # 测试2: 日期时间解析 YYYY-MM-DD HH:MM:SS
    # ========================================================================
    print("\n" + "="*70)
    print("测试2: 日期时间解析 (YYYY-MM-DD HH:MM:SS)")
    print("="*70)
    
    test_datetimes = [
        ("2023-01-15 09:30:00",),
        ("2023-06-30 14:45:30",),
        ("2024-12-31 23:59:59",),
    ]
    
    # Python标准库
    python_time = benchmark_function(
        "Python datetime.strptime",
        lambda s: datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S'),
        test_datetimes,
        iterations
    )
    
    # 我们的快速解析器
    fast_time = benchmark_function(
        "fast_strptime_datetime",
        fast_strptime_datetime,
        test_datetimes,
        iterations
    )
    
    speedup = python_time / fast_time
    print(f"\n  ⚡ 加速比: {speedup:.2f}x")
    print(f"  ⚡ 性能提升: {(speedup-1)*100:.1f}%")
    
    # ========================================================================
    # 测试3: 日期时间解析（带微秒） YYYY-MM-DD HH:MM:SS.ffffff
    # ========================================================================
    print("\n" + "="*70)
    print("测试3: 日期时间解析（带微秒） (YYYY-MM-DD HH:MM:SS.ffffff)")
    print("="*70)
    
    test_datetimes_micro = [
        ("2023-01-15 09:30:00.123456",),
        ("2023-06-30 14:45:30.654321",),
        ("2024-12-31 23:59:59.999999",),
    ]
    
    # Python标准库
    python_time = benchmark_function(
        "Python datetime.strptime",
        lambda s: datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S.%f'),
        test_datetimes_micro,
        iterations
    )
    
    # 我们的快速解析器
    fast_time = benchmark_function(
        "fast_strptime_datetime_micro",
        fast_strptime_datetime_micro,
        test_datetimes_micro,
        iterations
    )
    
    speedup = python_time / fast_time
    print(f"\n  ⚡ 加速比: {speedup:.2f}x")
    print(f"  ⚡ 性能提升: {(speedup-1)*100:.1f}%")
    
    # ========================================================================
    # 测试4: ISO 8601格式 YYYY-MM-DDTHH:MM:SS
    # ========================================================================
    print("\n" + "="*70)
    print("测试4: ISO 8601格式 (YYYY-MM-DDTHH:MM:SS)")
    print("="*70)
    
    test_iso = [
        ("2023-01-15T09:30:00",),
        ("2023-06-30T14:45:30",),
        ("2024-12-31T23:59:59",),
    ]
    
    # Python标准库
    python_time = benchmark_function(
        "Python datetime.strptime",
        lambda s: datetime.datetime.strptime(s, '%Y-%m-%dT%H:%M:%S'),
        test_iso,
        iterations
    )
    
    # 我们的快速解析器
    fast_time = benchmark_function(
        "fast_strptime_iso",
        fast_strptime_iso,
        test_iso,
        iterations
    )
    
    speedup = python_time / fast_time
    print(f"\n  ⚡ 加速比: {speedup:.2f}x")
    print(f"  ⚡ 性能提升: {(speedup-1)*100:.1f}%")
    
    # ========================================================================
    # 测试5: 兼容接口测试
    # ========================================================================
    print("\n" + "="*70)
    print("测试5: 兼容接口 (strptime兼容)")
    print("="*70)
    
    test_compat = [
        ("2023-01-15 09:30:00", '%Y-%m-%d %H:%M:%S'),
        ("2023-06-30 14:45:30", '%Y-%m-%d %H:%M:%S'),
        ("2024-12-31 23:59:59", '%Y-%m-%d %H:%M:%S'),
    ]
    
    # Python标准库
    python_time = benchmark_function(
        "Python datetime.strptime",
        lambda s, fmt: datetime.datetime.strptime(s, fmt),
        test_compat,
        iterations
    )
    
    # 我们的快速解析器
    fast_time = benchmark_function(
        "fast_strptime (兼容接口)",
        fast_strptime_compat,
        test_compat,
        iterations
    )
    
    speedup = python_time / fast_time
    print(f"\n  ⚡ 加速比: {speedup:.2f}x")
    print(f"  ⚡ 性能提升: {(speedup-1)*100:.1f}%")
    
    # ========================================================================
    # 总结
    # ========================================================================
    print("\n" + "="*70)
    print("测试完成！")
    print("="*70)
    print("\n优化技术:")
    print("  ✅ C级别字符解析（直接ASCII码计算）")
    print("  ✅ nogil并行（释放GIL锁）")
    print("  ✅ 内联函数（零函数调用开销）")
    print("  ✅ 边界检查禁用")
    print("  ✅ 避免Python对象创建")
    print("\n预期效果:")
    print("  🎯 目标: 10-20倍性能提升")
    print("  🚀 适用场景: CSV数据加载、大量日期解析")
    print("\n应用位置:")
    print("  📁 cybacktrader/feeds/csvgeneric.pyx")
    print("  📁 cybacktrader/btrun/btrun.pyx")
    print("  📁 其他所有使用datetime.strptime的地方")

if __name__ == "__main__":
    main()

