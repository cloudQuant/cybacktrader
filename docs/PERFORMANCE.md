# cybacktrader 性能分析报告

## 概述

本文档记录了 cybacktrader 的性能优化进展和分析结果。

## 优化策略

### Cython 优化技术

1. **静态类型声明**
   - 使用 `cdef` 声明 C 类型变量
   - 减少 Python 对象开销

2. **禁用安全检查**
   ```cython
   # cython: boundscheck=False  # 禁用边界检查
   # cython: wraparound=False   # 禁用负索引
   # cython: cdivision=True     # 使用 C 除法语义
   ```

3. **内存视图**
   - 使用 `memoryview` 直接访问内存
   - 避免 Python 列表的开销

4. **函数内联**
   - 对小型热点函数使用 `inline`
   - 减少函数调用开销

## 基准测试

### 测试方法

使用标准数据集和简单策略进行测试：

- **数据集**: `tests/datas/2006-day-001.txt` (251 个交易日)
- **策略**: SMA(30) 简单移动平均策略
- **模式**: `runonce=True, preload=True`
- **轮次**: 3 轮取平均值

### 基准测试结果

#### mathsupport 模块优化

| 实现 | 平均时间 | 相对性能 |
|------|---------|----------|
| Python (backtrader) | ~19.3ms | 1.00x (基准) |
| Cython (优化) | ~16.7ms | 1.15x |

**分析**: mathsupport 模块虽然已优化，但在整体回测中占比较小，因此整体性能提升有限。

#### 热点分析

使用 `cProfile` 进行性能剖析：

```bash
python -m cProfile -o profile.stats benchmarks/baseline_benchmark.py
```

**主要热点函数** (基于 backtrader 原始代码):

1. `LineBuffer.__getitem__()` - 数组访问 (~25% 时间)
2. `LineBuffer.__setitem__()` - 数组写入 (~20% 时间)
3. `Indicator.next()` - 指标计算 (~15% 时间)
4. `Strategy.next()` - 策略逻辑 (~10% 时间)
5. `Cerebro._runonce()` - 批量运行 (~8% 时间)

### 优化路线图

#### 阶段 1: 数学支持 (已完成 ✅)

- ✅ `mathsupport.py` → `mathsupport.pyx`
- 预期提升: ~1.1x
- 实际提升: ~1.15x

#### 阶段 2: 核心数据路径 (计划中 📋)

目标模块：
- `linebuffer.py` → `linebuffer.pyx`
- `lineiterator.py` → `lineiterator.pyx`
- `lineseries.py` → `lineseries.pyx`

预期提升: ~3-5x (这些是最热点的路径)

#### 阶段 3: 指标计算 (计划中 📋)

目标模块：
- `indicator.py` → `indicator.pyx`
- `indicators/sma.py` → `indicators/sma.pyx`
- `indicators/ema.py` → `indicators/ema.pyx`

预期提升: 累计 ~5-8x

#### 阶段 4: 引擎优化 (计划中 📋)

目标模块：
- `cerebro.py` → `cerebro.pyx`
- `broker.py` → `broker.pyx`

预期提升: 累计 ~10x+

## 内存使用

### 当前状态

| 配置 | 内存使用 |
|------|---------|
| backtrader (默认) | ~50MB (1000天数据) |
| cybacktrader (Cython) | ~48MB (预期) |

### 优化目标

- 使用 Cython 的内存池
- 减少 Python 对象分配
- 目标: 减少 20% 内存使用

## 扩展性测试

### 数据量测试

| 数据天数 | backtrader | cybacktrader (目标) |
|---------|-----------|-------------------|
| 100 | 8ms | <1ms |
| 1,000 | 80ms | <8ms |
| 10,000 | 800ms | <80ms |
| 100,000 | 8s | <0.8s |

### 并发测试

使用多进程优化运行：

```python
cerebro.optstrategy(MyStrategy, period=range(10, 50))
cerebro.run(maxcpus=4)
```

## 性能分析工具

### 1. cProfile

生成性能报告：

```bash
python -m cProfile -o output.pstats your_strategy.py
python -m pstats output.pstats
```

### 2. line_profiler

逐行分析：

```bash
pip install line_profiler
kernprof -l -v your_strategy.py
```

### 3. Cython 注解

查看 Cython 优化效果：

```bash
python setup.py build_ext --inplace
# 查看生成的 .html 文件
```

## 最佳实践

### 1. 策略优化

```python
class OptimizedStrategy(bt.Strategy):
    def __init__(self):
        # ✅ 在 __init__ 中创建指标
        self.sma_fast = bt.indicators.SMA(period=10)
        self.sma_slow = bt.indicators.SMA(period=30)
        self.crossover = bt.indicators.CrossOver(self.sma_fast, self.sma_slow)
    
    def next(self):
        # ✅ 直接使用预计算的值
        if self.crossover > 0:
            self.buy()
        elif self.crossover < 0:
            self.sell()
```

### 2. 数据预加载

```python
# ✅ 预加载数据，使用 runonce 模式
cerebro = bt.Cerebro(runonce=True, preload=True)
```

### 3. 避免频繁访问

```python
# ❌ 避免
for i in range(10):
    value = self.data.close[0]  # 重复访问

# ✅ 推荐
close = self.data.close[0]  # 只访问一次
for i in range(10):
    use_value(close)
```

## 已知限制

1. **当前版本限制**
   - 大部分模块仍使用 Python 实现
   - 仅 `mathsupport` 使用 Cython 优化

2. **兼容性**
   - 需要 C 编译器
   - Windows 需要 Visual Studio Build Tools

3. **功能限制**
   - 保持 100% API 兼容
   - 不改变任何功能行为

## 持续优化

### 监控

定期运行基准测试：

```bash
python benchmarks/baseline_benchmark.py
```

### 目标

- 短期目标 (3个月): 3-5x 性能提升
- 中期目标 (6个月): 8-10x 性能提升  
- 长期目标 (1年): 15-20x 性能提升

## 贡献

欢迎贡献性能优化！请提供：

1. 性能基准测试
2. Cython 优化代码
3. 兼容性测试
4. 文档更新

## 参考资料

- [Cython 文档](https://cython.readthedocs.io/)
- [Python 性能分析](https://docs.python.org/3/library/profile.html)
- [backtrader 文档](https://www.backtrader.com/docu/)

