# -*- coding: utf-8 -*-
"""
对比测试：验证无监控模式和带监控模式的差异

这个脚本会运行两种模式的测试，帮助你理解性能监控开销的影响
"""

import subprocess
import sys
import os

def run_test(data_size, rounds, no_profiling=False):
    """运行单次测试"""
    cmd = [
        sys.executable,
        'benchmarks/unified_profiler.py',
        '--data-size', str(data_size),
        '--rounds', str(rounds)
    ]
    
    if no_profiling:
        cmd.append('--no-profiling')
    
    print(f"\n{'='*70}")
    mode = "纯时间测量（无监控）" if no_profiling else "带性能分析（有监控）"
    print(f"运行模式: {mode}")
    print(f"命令: {' '.join(cmd)}")
    print(f"{'='*70}\n")
    
    result = subprocess.run(cmd, cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return result.returncode

def main():
    """主函数"""
    print("="*70)
    print("对比测试：无监控模式 vs 带监控模式")
    print("="*70)
    print("\n这个测试将运行两种模式，帮助你理解：")
    print("1. 无监控模式：更准确的加速比（推荐用于性能评估）")
    print("2. 带监控模式：可以识别热点函数（推荐用于优化指导）")
    print("\n测试配置：")
    
    # 测试参数
    data_size = 10000
    rounds = 3
    
    print(f"  数据规模: {data_size:,} 行")
    print(f"  测试轮数: {rounds} 轮")
    print()
    
    # 第一次测试：无监控模式
    print("\n" + "🚀"*35)
    print("第一阶段：无监控模式（纯时间测量）")
    print("🚀"*35)
    run_test(data_size, rounds, no_profiling=True)
    
    # 第二次测试：带监控模式
    print("\n" + "🔬"*35)
    print("第二阶段：带监控模式（性能分析）")
    print("🔬"*35)
    run_test(data_size, rounds, no_profiling=False)
    
    print("\n" + "="*70)
    print("对比测试完成！")
    print("="*70)
    print("\n请查看生成的报告，对比两种模式的加速比差异：")
    print("  - 无监控模式报告: performance_report_10K_*.md")
    print("  - 带监控模式报告: performance_report_10K_*.md")
    print("\n预期结果：")
    print("  - 无监控模式加速比: ~1.1-1.3x （更准确）")
    print("  - 带监控模式加速比: ~1.5-2.0x （受监控开销影响）")
    print("\n建议：")
    print("  - 用无监控模式评估真实性能")
    print("  - 用带监控模式找出优化目标")

if __name__ == "__main__":
    main()
