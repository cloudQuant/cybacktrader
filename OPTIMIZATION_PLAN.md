# Cybacktrader 性能优化计划

## 项目概况

- **总 .pyx 文件数**：162个
- **当前性能**：相对 backtrader 提升 10-15%
- **优化目标**：提升 2-10 倍性能

## 架构分析

### 核心模块层次（按setup.py编译顺序）

```
Level 1 (基础层):
  - version, errors, mathsupport
  - utils: py3, date, autodict, ordereddefaultdict, dateintern, flushfile, fractal

Level 2 (元类层):
  - metabase, lineroot

Level 3 (核心数据结构):
  - linebuffer  ⭐ 热点
  - functions

Level 4 (数据系列):
  - lineseries  ⭐ 热点
  - dataseries
  - lineiterator

Level 5 (交易组件):
  - order, trade, position
  - comminfo      ⭐ 热点
  - indicator     ⭐ 热点
  - analyzer
  - observer

Level 6 (执行层):
  - feed
  - broker        ⭐ 热点
  - strategy      ⭐ 热点
  - signal
  - store, sizer, writer, timer, fillers, flt, resamplerfilter, tradingcal

Level 7 (引擎层):
  - cerebro       ⭐ 热点

Level 8 (子模块):
  - indicators/*, analyzers/*, brokers/*, feeds/*, etc.
```

## 优化优先级矩阵

### 🔥 最高优先级（P0）- 热点代码

这些模块在每次 tick 都会被调用，优化效果最明显：

| 模块 | 大小 | 重要性 | 调用频率 | 优化潜力 | 优先级 |
|------|------|--------|----------|----------|--------|
| **linebuffer.pyx** | 36KB | ⭐⭐⭐⭐⭐ | 极高 | 极高 | **P0-1** |
| **indicator.pyx** | 中 | ⭐⭐⭐⭐⭐ | 极高 | 极高 | **P0-2** |
| **lineseries.pyx** | 37KB | ⭐⭐⭐⭐⭐ | 极高 | 高 | **P0-3** |
| **strategy.pyx** | 86KB | ⭐⭐⭐⭐ | 高 | 高 | **P0-4** |

**优化重点**：
- linebuffer: 数据访问优化，使用内存视图
- indicator: 向量化计算，减少 Python 对象操作
- lineseries: 优化数据系列操作
- strategy: 优化 _next 循环

### ⚡ 高优先级（P1）- 核心逻辑

| 模块 | 大小 | 重要性 | 调用频率 | 优化潜力 | 优先级 |
|------|------|--------|----------|----------|--------|
| **cerebro.pyx** | 84KB | ⭐⭐⭐⭐⭐ | 中 | 中高 | **P1-1** |
| **broker.pyx** | 中 | ⭐⭐⭐⭐ | 高 | 中高 | **P1-2** |
| **order.pyx** | 29KB | ⭐⭐⭐⭐ | 中 | 中 | **P1-3** |
| **comminfo.pyx** | 20KB | ⭐⭐⭐ | 中 | 中 | **P1-4** |

### 📊 中优先级（P2）- 常用模块

| 模块 | 优先级 |
|------|--------|
| **indicators/sma.pyx** | P2-1 |
| **indicators/ema.pyx** | P2-2 |
| **indicators/crossover.pyx** | P2-3 |
| **functions.pyx** | P2-4 |
| **metabase.pyx** | P2-5 |

### 🔧 低优先级（P3）- 辅助模块

- utils 模块
- analyzers 模块
- observers 模块
- 其他 indicators

## 优化技术清单

### 1. 类型声明优化

```cython
# 之前（纯 Python）
def get_value(self):
    return self.value

# 之后（Cython 优化）
cdef double get_value(self):
    return self.value
```

### 2. 循环优化

```cython
# 之前
for i in range(len(data)):
    result[i] = data[i] * 2

# 之后
cdef int i
cdef double[:] data_view = data
cdef double[:] result_view = result
for i in range(data_view.shape[0]):
    result_view[i] = data_view[i] * 2.0
```

### 3. 使用 C 数学库

```cython
from libc.math cimport sqrt, fabs, pow
cdef double result = sqrt(fabs(value))
```

### 4. 减少 Python 对象操作

```cython
# 之前
def process(self):
    d = {}
    d['key'] = self.calculate()
    return d

# 之后
cdef class Result:
    cdef public double value
    
cdef Result process(self):
    cdef Result r = Result()
    r.value = self.calculate()
    return r
```

### 5. 使用内存视图

```cython
cdef double[:] prices  # 内存视图，直接访问内存
prices[i]              # 快速访问
```

## 优化执行计划

### 第一阶段：核心热点优化（预计提升 50-100%）

1. **linebuffer.pyx** (第1周)
   - [ ] 添加类型声明
   - [ ] 使用内存视图优化数据访问
   - [ ] 优化 __getitem__ 和 __setitem__
   - [ ] 测试并验证

2. **indicator.pyx** (第1-2周)
   - [ ] 优化指标计算循环
   - [ ] 添加 cdef 方法
   - [ ] 减少 Python 对象创建
   - [ ] 测试并验证

3. **lineseries.pyx** (第2周)
   - [ ] 优化数据系列操作
   - [ ] 使用静态类型
   - [ ] 优化内存访问
   - [ ] 测试并验证

4. **strategy.pyx** (第2-3周)
   - [ ] 优化 _next 方法
   - [ ] 优化订单处理循环
   - [ ] 添加类型声明
   - [ ] 测试并验证

**里程碑 1**：运行基准测试，验证性能提升

### 第二阶段：核心逻辑优化（预计再提升 20-50%）

5. **cerebro.pyx** (第3-4周)
   - [ ] 优化主循环
   - [ ] 减少函数调用开销
   - [ ] 优化数据预加载
   - [ ] 测试并验证

6. **broker.pyx** (第4周)
   - [ ] 优化订单匹配
   - [ ] 优化持仓计算
   - [ ] 添加类型声明
   - [ ] 测试并验证

7. **order.pyx** (第4周)
   - [ ] 优化订单状态管理
   - [ ] 使用 C 结构体
   - [ ] 测试并验证

8. **comminfo.pyx** (第4周)
   - [ ] 优化佣金计算
   - [ ] 内联关键函数
   - [ ] 测试并验证

**里程碑 2**：运行基准测试，验证累计性能提升

### 第三阶段：常用模块优化（预计再提升 10-20%）

9. **indicators/sma.pyx** (第5周)
10. **indicators/ema.pyx** (第5周)
11. **indicators/crossover.pyx** (第5周)
12. **functions.pyx** (第5周)
13. **metabase.pyx** (第5-6周)

**里程碑 3**：运行基准测试，验证总体性能提升

### 第四阶段：其他模块优化（预计再提升 5-10%）

14. utils 模块
15. analyzers 模块
16. observers 模块
17. 其他 indicators

**最终里程碑**：运行完整基准测试，生成性能报告

## 优化验证流程

每优化一个文件后：

```bash
# 1. 重新编译安装
pip install -U .

# 2. 运行测试套件
pytest tests -n 8

# 3. 如果所有测试通过，运行基准测试
python benchmarks/ma_crossover_benchmark.py

# 4. 记录性能数据
# 5. 提交代码
```

## 性能目标

| 阶段 | 目标加速比 | 累计加速比 |
|------|-----------|-----------|
| 基线 | 1.13x | 1.13x |
| 第一阶段 | 1.5-2.0x | 1.7-2.3x |
| 第二阶段 | 1.2-1.5x | 2.0-3.4x |
| 第三阶段 | 1.1-1.2x | 2.2-4.1x |
| 第四阶段 | 1.05-1.1x | 2.3-4.5x |

**最终目标**：相对原始 backtrader **2-5倍性能提升**

## 优化技巧和注意事项

### ✅ DO（推荐）

1. **优先优化热点代码**：使用 profiler 找出瓶颈
2. **添加类型声明**：所有循环变量都声明类型
3. **使用内存视图**：访问大数组时使用 `double[:]`
4. **减少函数调用**：内联小函数，使用 `cdef inline`
5. **使用 C 标准库**：math, stdlib 等
6. **保持测试通过**：每次优化后必须运行测试

### ❌ DON'T（避免）

1. **不要过早优化**：先测量，再优化
2. **不要破坏 API**：保持对外接口不变
3. **不要跳过测试**：确保功能正确性
4. **不要优化冷代码**：只优化真正的热点
5. **不要牺牲可读性**：注释清楚优化的目的

## 工具和资源

### 性能分析工具

```bash
# Cython 注解（查看 Python 交互）
cython -a filename.pyx

# Python profiler
python -m cProfile script.py

# Line profiler
kernprof -l -v script.py
```

### 参考资源

- Cython 文档：https://cython.readthedocs.io/
- Cython 最佳实践
- NumPy 内存视图文档

## 进度跟踪

- [ ] 第一阶段：核心热点优化
  - [ ] linebuffer.pyx
  - [ ] indicator.pyx
  - [ ] lineseries.pyx
  - [ ] strategy.pyx
- [ ] 第二阶段：核心逻辑优化
- [ ] 第三阶段：常用模块优化
- [ ] 第四阶段：其他模块优化
- [ ] 最终验证和文档

---

**开始日期**：2025-10-16  
**预计完成**：6-8周  
**当前状态**：准备开始第一阶段

