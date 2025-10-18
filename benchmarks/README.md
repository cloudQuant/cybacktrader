# CyBacktrader基准测试和性能分析工具

本目录包含了CyBacktrader项目的基准测试和深度性能分析工具，用于评估优化效果和识别性能瓶颈。

## 🎯 推荐工具

### ⭐ 统一性能分析工具（推荐）
- **`unified_profiler.py`** - **最新的统一性能分析工具** ✅
  - ✅ **已修复所有已知问题** (v1.4.0)
  - 整合了函数级、行级、时间、内存等所有分析功能
  - **同时显示时间和内存数据** - 一次测试获得完整性能画像
  - **支持无监控模式** - 纯时间测量，更准确的加速比 🆕
  - 自动生成Markdown和HTML双格式报告
  - 支持多轮测试取平均值
  - **显示Top 100热点函数**，全面识别优化目标（已验证）
  - 报告自动保存到 `benchmarks/performance_reports/` 目录
  - 详细的优化建议和热点函数识别
  - **使用文档**: 见下方

## 文件说明

### 基准测试脚本
- **`ma_crossover_benchmark.py`** - 均线交叉策略基准测试（优化版）
  - 支持数据缓存机制，避免重复生成
  - 内存管理和详细统计信息
  - 命令行参数支持多种测试场景

### 性能分析脚本（旧版，建议使用unified_profiler.py）
- **`performance_profiler.py`** - 深度性能分析工具（旧版）
  - 支持函数级、行级、内存级性能分析
  - 自动生成详细的性能报告
  - 支持与原版backtrader对比
  - ⚠️ 建议使用 `unified_profiler.py` 替代

## 快速开始

### 1. 安装依赖

```bash
pip install pandas numpy psutil
pip install line_profiler  # 可选，用于行级分析
pip install backtrader     # 用于性能对比
```

### 2. 🚀 使用统一性能分析工具（**推荐使用 `unified_profiler.py`**，它整合了所有功能：

```bash
# 1. 纯时间测量（无监控，更准确的加速比）- 推荐用于性能评估
python benchmarks/unified_profiler.py --data-size 100000 --no-profiling --rounds 3

# 2. 带性能分析（有监控，可识别热点函数）- 推荐用于优化指导
python benchmarks/unified_profiler.py --data-size 100000 --rounds 3

# 3. 对比两种模式的差异
python benchmarks/compare_profiling_modes.py

# 4. 大规模测试（100万行数据）
python benchmarks/unified_profiler.py --data-size 1000000 --no-profiling --rounds 1

# 5. 内存对比
python benchmarks/unified_profiler.py --compare memory --rounds 3
```

**两种测试模式说明**：
- `--no-profiling`: 无监控模式
  - ✅ 纯时间测量，无cProfile/tracemalloc开销
  - ✅ 更准确的加速比（~1.1-1.3x）
  - ✅ 反映真实生产环境性能
  - ❌ 无法识别热点函数
  - 🎯 **用途**：性能评估、发布前基准测试

- 默认模式（带性能分析）：
  - ✅ 可识别Top 100热点函数
  - ✅ 详细的函数级性能数据
  - ✅ 函数对齐情况分析
  - ❌ 有监控开销，加速比虚高（~1.5-2.0x）
  - 🎯 **用途**：找出优化目标、开发中调优

**测试结果示例**：
```
✅ Backtrader 执行时间: 8.6673s
   内存使用: 11.66MB
   内存峰值: 7.27MB

✅ CyBacktrader 执行时间: 4.9197s
   内存使用: 11.89MB
   内存峰值: 8.33MB

📊 本轮加速比: 1.76x

性能对比摘要:
  加速比: 1.76x
  时间节省: 3.7477s (43.2%)
  内存节省: -0.23MB (-2.0%)

报告位置: benchmarks/performance_reports/
  - performance_report_*.md (包含Top 100热点函数 + 时间/内存数据)
  - performance_report_*.html (可视化报告)
```

### 3. 基本基准测试

```bash
# 运行小规模测试（推荐首次使用）
python benchmarks/ma_crossover_benchmark.py --data-sizes 10000 100000 --rounds 1

# 运行大规模测试（100万行数据）
python benchmarks/ma_crossover_benchmark.py --large-scale 1000000 --rounds 1

# 清理缓存并重新测试
python benchmarks/ma_crossover_benchmark.py --data-sizes 1000000 --cleanup-cache --rounds 1
```

### 4. 旧版性能分析（不推荐）

```bash
# 函数级性能分析（建议使用unified_profiler.py替代）
python benchmarks/performance_profiler.py --data-size 1000000 --profile-type function

# 行级性能分析（需安装line_profiler）
python benchmarks/performance_profiler.py --data-size 1000000 --profile-type line

# 内存性能分析（需安装memory_profiler）
python benchmarks/performance_profiler.py --data-size 1000000 --profile-type memory

# 与原版backtrader对比
python benchmarks/performance_profiler.py --data-size 1000000 --compare-backtrader
```

## 输出文件

### 统一性能分析工具输出
- **`benchmarks/performance_reports/`** 目录，包含：
  - `performance_report_*.md` - Markdown格式的详细报告（包含Top 100热点函数）
  - `performance_report_*.html` - HTML格式的可视化报告
  - `performance_data_*.json` - 完整的性能数据

### 基准测试输出
- **`benchmark_results.json`** - 详细的测试结果数据
- **`ma_crossover_benchmark_results.png`** - 性能对比图表

### 旧版性能分析输出
- **`performance_reports/`** 目录，包含：
  - `performance_report_*.txt` - 函数级性能分析报告
  - `line_profile_report_*.txt` - 行级性能分析报告
  - `memory_report_*.txt` - 内存性能分析报告
  - `summary_*.json` - 综合性能分析报告

## 脚本参数

### unified_profiler.py（推荐）

```bash
# 基本用法
python benchmarks/unified_profiler.py [选项]

选项：
  --data-size SIZE     测试数据规模 (默认: 100000)
  --data-file FILE     指定数据文件路径（可选）
  --type TYPE          分析类型: function/line (默认: function)
  --compare METRIC     对比指标: time/memory (默认: time)
  --rounds ROUNDS      测试轮数 (默认: 1)
  --output-dir DIR     报告输出目录 (默认: performance_reports)

示例：
  python benchmarks/unified_profiler.py --data-size 1000
  python benchmarks/unified_profiler.py --data-size 100000 --rounds 3
  python benchmarks/unified_profiler.py --compare memory --rounds 3
```

### ma_crossover_benchmark.py

```bash
# 基本用法
python benchmarks/ma_crossover_benchmark.py [选项]

选项：
  --data-sizes SIZES    测试的数据规模列表 (默认: [10000, 100000])
  --rounds ROUNDS       每规模运行轮数 (默认: 1)
  --no-cache           不使用数据缓存
  --cleanup-cache      清理旧缓存文件
  --large-scale SIZE   运行大规模测试（指定数据行数）
  --no-plot           不生成图表
```

### performance_profiler.py（旧版）

```bash
# 基本用法
python benchmarks/performance_profiler.py [选项]

选项：
  --data-size SIZE      测试数据规模 (默认: 1000000)
  --data-file FILE     指定数据文件路径
  --profile-type TYPE  分析类型: function/line/memory (默认: function)
  --top-n N            显示前N个最耗时函数 (默认: 20)
  --rounds ROUNDS      基准测试轮数 (默认: 1)
  --output-dir DIR     报告输出目录 (默认: performance_reports)
  --compare-backtrader 同时运行原版backtrader对比
```

## 使用建议

### 初次使用
1. 先运行小规模测试验证环境：`--data-sizes 10000`
2. 确认基本功能正常后，再进行大规模测试

### 性能分析
1. **函数级分析**：快速了解哪些函数最耗时
2. **行级分析**：精确定位热点代码行（需安装line_profiler）
3. **内存分析**：识别内存泄露和优化空间（需安装memory_profiler）

### 大规模测试
- 100万行数据通常需要几分钟到几十分钟
- 建议在有足够内存的机器上运行
- 使用`--rounds 1`减少测试时间

## 测试策略说明

### 均线交叉策略
- **快线周期**: 5日
- **慢线周期**: 20日
- **信号**: 金叉做多，死叉平多
- **资金**: 10万初始资金
- **佣金**: 0.1%

### 数据生成
- 使用随机游走模型生成OHLCV数据
- 包含真实的交易日历（跳过周末）
- 固定随机种子确保结果可重复

## 分析结果解读

### 函数级性能报告
```
Top 20最耗时函数:
         1000000 function calls in 15.234 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
   1000000   10.123    0.000   15.234    0.000 {method 'append' of 'list' objects}
```

- **ncalls**: 函数调用次数
- **tottime**: 函数本身执行时间
- **cumtime**: 函数+子函数执行时间
- **percall**: 平均每次调用时间

### 加速比计算
- 加速比 = 原版backtrader时间 / CyBacktrader时间
- 加速比 > 1 表示CyBacktrader更快

## 注意事项

1. **内存需求**: 100万行数据约需几百MB内存
2. **磁盘空间**: 数据文件和报告文件会占用磁盘空间
3. **运行时间**: 大规模测试可能需要较长时间
4. **依赖安装**: 根据需要安装可选依赖包

## 故障排除

### 常见问题
1. **ImportError**: 确保已正确安装所有依赖包
2. **内存不足**: 减少数据规模或增加系统内存
3. **权限错误**: 确保有读写权限

### 性能调优建议
1. 使用数据缓存避免重复生成
2. 合理设置测试轮数
3. 在专用机器上运行大规模测试

---

## 更新日志

- **v1.0**: 初始版本，支持基本基准测试
- **v1.1**: 添加数据缓存机制和内存管理
- **v1.2**: 添加深度性能分析工具
- **v1.3**: 支持命令行参数和多种分析类型

---

*CyBacktrader基准测试工具 - 为性能优化而生*

