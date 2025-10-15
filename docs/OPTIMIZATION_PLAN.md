# cybacktrader 优化实施计划

## 概述

本文档详细说明了将 backtrader 核心模块 Cython 化的具体实施计划。

## 优化优先级

基于性能分析，按以下优先级进行优化：

### Priority A: 核心数据路径 (估计 3-5x 加速)

这些模块是回测过程中最频繁调用的，优化收益最大。

#### 1. lineroot.py (基础依赖)

**复杂度**: 中等
**预期收益**: 1.5x
**依赖**: metabase.py (保持 Python)

**关键优化点**:
- 算术运算符方法（`__add__`, `__sub__`, `__mul__` 等）
- `_operation` 和 `_operationown` 方法
- 类型检查和条件分支

**Cython 策略**:
```cython
# 使用 cpdef 支持 Python 调用
cpdef _operation_stage2(self, other, operation, bint r=False):
    cdef double other_val
    if isinstance(other, LineRoot):
        other_val = <double>other[0]
    else:
        other_val = <double>other
    
    if r:
        return operation(other_val, <double>self[0])
    return operation(<double>self[0], other_val)
```

#### 2. linebuffer.py (最高优先级)

**复杂度**: 高
**预期收益**: 2-3x
**热点**: `__getitem__`, `__setitem__`, `forward`, `backwards`

**文件大小**: ~900 行
**关键优化点**:
- 数组索引访问（`__getitem__`, `__setitem__`）
- 缓冲区管理（`forward`, `backwards`, `rewind`）
- 双端队列操作（`deque`）

**Cython 策略**:
```cython
from cpython cimport array
from libc.stdlib cimport malloc, free

cdef class LineBuffer:
    cdef:
        array.array _array
        Py_ssize_t _idx
        Py_ssize_t _lenmark
        int mode
        list bindings
    
    @cython.boundscheck(False)
    @cython.wraparound(False)
    cpdef double __getitem__(self, Py_ssize_t ago):
        cdef Py_ssize_t idx = self._idx - ago
        return self._array.data.as_doubles[idx]
```

**实施步骤**:
1. 创建 `linebuffer.pxd` 声明文件
2. 将 `array.array` 转换为 Cython 类型化数组
3. 优化 `__getitem__`/`__setitem__` 使用内存视图
4. 保留 `deque` 逻辑但使用 C 类型
5. 逐步测试每个方法

#### 3. lineiterator.py

**复杂度**: 高
**预期收益**: 1.8x
**依赖**: linebuffer, lineseries

**关键优化点**:
- 迭代器协议（`__next__`）
- `prenext`, `next`, `preonce`, `once` 调用链
- Line 访问和更新

**Cython 策略**:
```cython
cdef class LineIterator(LineMultiple):
    cdef:
        list _lineiterators
        Py_ssize_t _clock
        bint _stalled
    
    cpdef prenext(self):
        # 内联快速路径
        pass
    
    cpdef next(self):
        # 内联快速路径
        pass
```

#### 4. lineseries.py

**复杂度**: 中等
**预期收益**: 1.5x

**关键优化点**:
- `__getitem__` 转发到 lines
- Lines 集合管理
- 属性访问

### Priority B: 指标计算 (估计额外 2-3x 加速)

#### 5. indicator.py

**复杂度**: 高
**预期收益**: 2x
**依赖**: lineiterator

**关键优化点**:
- `next()` 方法调用
- `once()` 批量计算
- 指标链式计算

#### 6. 常用指标模块

按使用频率优化：

1. **indicators/sma.py** (Simple Moving Average)
   - 最常用，优先级最高
   - 简单算法，容易优化
   - 预期: 3-5x

2. **indicators/ema.py** (Exponential Moving Average)
   - 常用，递归计算
   - 预期: 2-3x

3. **indicators/rsi.py** (Relative Strength Index)
   - 常用，多步计算
   - 预期: 2-3x

4. **indicators/macd.py** (MACD)
   - 常用，组合指标
   - 预期: 2x

**SMA Cython 示例**:
```cython
# cython: boundscheck=False
# cython: wraparound=False

from libc.math cimport fabs

cdef class SMA:
    cdef:
        double[::1] _data
        Py_ssize_t _period
        double _sum
        
    @cython.boundscheck(False)
    @cython.wraparound(False)
    cpdef double next(self):
        cdef:
            Py_ssize_t i
            double val_add, val_del
            double result
        
        val_add = self._data[0]
        val_del = self._data[-self._period]
        
        self._sum = self._sum - val_del + val_add
        result = self._sum / self._period
        
        return result
```

### Priority C: 引擎和调度 (估计额外 1.5-2x 加速)

#### 7. cerebro.py

**复杂度**: 非常高
**预期收益**: 1.5x
**依赖**: 几乎所有模块

**关键优化点**:
- `_runonce()` 批量运行循环
- `_runnext()` 单步运行循环
- 策略/指标/数据的调度

**注意**: 由于高度依赖其他模块，应最后优化

#### 8. broker.py

**复杂度**: 高
**预期收益**: 1.3x

**关键优化点**:
- 订单撮合逻辑
- 持仓计算
- 现金管理

#### 9. order.py

**复杂度**: 中等
**预期收益**: 1.2x

**关键优化点**:
- 订单状态管理
- 价格计算

## 实施策略

### 渐进式转换方法

1. **混合模式**: Python 和 Cython 模块共存
   - Cython 模块优先导入
   - Python 版本作为回退
   - 保证兼容性

2. **保留 .pxd 接口文件**
   - 定义 C 级别接口
   - 允许模块间高效调用
   - 示例: `linebuffer.pxd`

3. **单元测试驱动**
   - 每个模块转换后运行完整测试
   - 性能回归测试
   - 功能等价性验证

### 依赖管理

```
metabase.py (Python)
    ↓
lineroot.pyx (Cython)
    ↓
linebuffer.pyx (Cython)
    ↓
lineseries.pyx (Cython)
    ↓
lineiterator.pyx (Cython)
    ↓
indicator.pyx (Cython)
    ↓
indicators/*.pyx (Cython)
```

**建议顺序**:
1. mathsupport ✅
2. lineroot
3. linebuffer
4. lineseries
5. lineiterator
6. indicator
7. 常用指标 (SMA, EMA, RSI, MACD)
8. cerebro, broker, order

## 技术细节

### Cython 编译选项

```python
compiler_directives = {
    'language_level': '3',
    'boundscheck': False,      # 禁用边界检查
    'wraparound': False,       # 禁用负索引
    'cdivision': True,         # C 除法
    'initializedcheck': False, # 禁用初始化检查
    'nonecheck': False,        # 禁用 None 检查
    'embedsignature': True,    # 嵌入签名
}
```

### 类型声明最佳实践

```cython
# 整数类型
cdef Py_ssize_t i, j, n
cdef int count
cdef long long big_int

# 浮点类型
cdef double value
cdef float small_value

# 数组/列表
cdef double[::1] array_1d       # 1D memoryview
cdef double[:, ::1] array_2d     # 2D memoryview
cdef list python_list

# 布尔
cdef bint flag

# 对象
cdef object obj
```

### 性能测试框架

```python
# benchmarks/module_benchmark.py

import time
import statistics

def benchmark_module(bt_module, cy_module, test_func, rounds=100):
    """
    对比 backtrader 和 cybacktrader 模块性能
    """
    # backtrader
    bt_times = []
    for _ in range(rounds):
        t0 = time.perf_counter()
        test_func(bt_module)
        bt_times.append(time.perf_counter() - t0)
    
    # cybacktrader
    cy_times = []
    for _ in range(rounds):
        t0 = time.perf_counter()
        test_func(cy_module)
        cy_times.append(time.perf_counter() - t0)
    
    bt_avg = statistics.mean(bt_times)
    cy_avg = statistics.mean(cy_times)
    speedup = bt_avg / cy_avg
    
    return {
        'backtrader': bt_avg,
        'cybacktrader': cy_avg,
        'speedup': speedup
    }
```

## 风险和挑战

### 技术风险

1. **元类兼容性**
   - backtrader 大量使用元类
   - Cython 对元类支持有限
   - **缓解**: 保持元类为 Python，只优化热点方法

2. **动态特性**
   - Python 的动态特性（如 `setattr`, `getattr`）
   - Cython 静态类型限制
   - **缓解**: 使用 `object` 类型保持灵活性

3. **内存管理**
   - C 级别的内存管理
   - 潜在内存泄漏
   - **缓解**: 使用 Python 对象生命周期，避免手动 malloc/free

### 兼容性风险

1. **API 变化**
   - 必须保持 100% API 兼容
   - **缓解**: 完整的测试套件

2. **行为差异**
   - 浮点数精度
   - 边界情况处理
   - **缓解**: 详细的单元测试和对比测试

## 里程碑

### Phase 1: 基础设施 (已完成 ✅)
- [x] 项目结构
- [x] 构建系统
- [x] 兼容层
- [x] mathsupport Cython 化

### Phase 2: 核心 Line 模块 (3个月)
- [ ] lineroot.pyx
- [ ] linebuffer.pyx
- [ ] lineseries.pyx
- [ ] lineiterator.pyx
- 目标: 3-5x 加速

### Phase 3: 指标系统 (3个月)
- [ ] indicator.pyx
- [ ] SMA, EMA, RSI, MACD
- [ ] 其他常用指标
- 目标: 累计 5-8x 加速

### Phase 4: 引擎优化 (3个月)
- [ ] cerebro.pyx
- [ ] broker.pyx
- [ ] order.pyx
- 目标: 累计 10x+ 加速

### Phase 5: 优化和发布 (3个月)
- [ ] 性能调优
- [ ] 内存优化
- [ ] 完整文档
- [ ] 生产发布

## 参考资源

- [Cython 文档](https://cython.readthedocs.io/)
- [Cython 最佳实践](https://cython.readthedocs.io/en/latest/src/userguide/numpy_tutorial.html)
- [backtrader 源码](https://github.com/mementum/backtrader)
- [性能分析工具](https://docs.python.org/3/library/profile.html)

