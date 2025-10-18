# Cython深度优化技术指南

## 一、优化技术清单（按优先级排序）

### 1. 类级别优化（最高优先级）
```cython
# ❌ 错误：普通Python类
class MyClass:
    def __init__(self):
        self.value = 0

# ✅ 正确：Cython扩展类型
cdef class MyClass:
    cdef double value
    
    def __init__(self):
        self.value = 0.0
```

### 2. 方法级别优化
```cython
# ❌ 错误：所有方法都是def
def calculate(self, x):
    return x * 2

# ✅ 正确：使用cdef/cpdef
cpdef double calculate(self, double x):
    return self._fast_calc(x)

cdef inline double _fast_calc(self, double x) nogil:
    return x * 2.0
```

### 3. 变量类型声明
```cython
# ❌ 错误：无类型声明
def process_array(data):
    total = 0
    for i in range(len(data)):
        total += data[i]
    return total

# ✅ 正确：完整类型声明
cpdef double process_array(double[:] data):
    cdef double total = 0.0
    cdef int i, n = data.shape[0]
    
    for i in range(n):
        total += data[i]
    return total
```

### 4. NumPy数组优化（使用内存视图）
```cython
# ❌ 错误：直接使用NumPy数组
def process_numpy(np.ndarray arr):
    for i in range(len(arr)):
        arr[i] *= 2

# ✅ 正确：使用typed memoryview
def process_numpy(double[:] arr):
    cdef int i
    with nogil:
        for i in range(arr.shape[0]):
            arr[i] *= 2.0
```

### 5. 数学运算优化
```cython
# 导入C数学库
from libc.math cimport sqrt, pow, sin, cos, log, exp, fabs, isnan, isinf
from libc.stdlib cimport malloc, free, abs

# ❌ 错误：使用Python数学函数
import math
result = math.sqrt(x)

# ✅ 正确：使用C数学函数
cdef double result = sqrt(x)
```

### 6. GIL释放（并行优化）
```cython
# ✅ 在纯计算代码中释放GIL
cdef double compute_intensive(double[:] data) nogil:
    cdef int i
    cdef double result = 0.0
    
    for i in range(data.shape[0]):
        result += data[i] * data[i]
    
    return sqrt(result)

# 使用with nogil块
def parallel_process(double[:, :] matrix):
    cdef int i, j
    cdef double total = 0.0
    
    with nogil:
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                total += matrix[i, j]
    
    return total
```

## 二、cybacktrader特定优化策略

### 1. LineBuffer优化
```cython
cdef class LineBuffer:
    cdef double* _data       # C数组
    cdef int _idx           # 当前索引
    cdef int _size          # 缓冲区大小
    cdef int _lenmark       # 长度标记
    
    cdef inline double get_value(self, int ago) nogil:
        """获取历史值，ago=0为当前值"""
        return self._data[self._idx - ago]
    
    cdef inline void set_value(self, double value) nogil:
        """设置当前值"""
        self._data[self._idx] = value
```

### 2. Indicator优化
```cython
cdef class Indicator:
    cdef double[:] _lines    # 使用内存视图
    cdef int _period
    cdef bint _valid
    
    cpdef void next(self):
        """每个bar调用一次"""
        self._calculate_value()
    
    cdef inline void _calculate_value(self) nogil:
        """核心计算逻辑"""
        pass
```

### 3. Strategy优化
```cython
cdef class Strategy:
    cdef list _indicators
    cdef object _broker
    cdef double _cash
    
    cpdef void next(self):
        """策略主逻辑"""
        if self._should_buy():
            self._place_order(1)
    
    cdef bint _should_buy(self) nogil:
        """买入条件判断"""
        return True
```

## 三、编译指令最佳实践

### 完整编译指令模板
```cython
# 基础优化（安全）
# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True

# 高级优化（需要谨慎）
# cython: nonecheck=False         # 关闭None检查
# cython: initializedcheck=False  # 关闭初始化检查
# cython: overflowcheck=False     # 关闭溢出检查

# 类型推断
# cython: infer_types=True        # 自动类型推断

# 优化选项
# cython: optimize.unpack_method_calls=True
# cython: optimize.use_switch=True
```

## 四、性能测试基准

### 优化前后对比测试
```python
# 测试脚本 benchmark_optimization.py
import time
import numpy as np

def benchmark_indicator(indicator_class, data, iterations=1000):
    """测试指标性能"""
    start = time.perf_counter()
    
    indicator = indicator_class(period=20)
    for _ in range(iterations):
        for value in data:
            indicator.calculate(value)
    
    elapsed = time.perf_counter() - start
    return elapsed

# 生成测试数据
data = np.random.randn(1000)

# 测试优化前
time_before = benchmark_indicator(OldIndicator, data)

# 测试优化后
time_after = benchmark_indicator(NewIndicator, data)

# 计算提升
speedup = time_before / time_after
print(f"性能提升: {speedup:.2f}x")
print(f"内存使用降低: {memory_before / memory_after:.2f}x")
```

## 五、常见问题和解决方案

### 1. 类型转换问题
```cython
# 问题：Python对象到C类型转换
# 解决：显式类型转换
cdef double value = <double>python_obj
```

### 2. None值处理
```cython
# 问题：None值导致段错误
# 解决：添加检查
if obj is not None:
    cdef double val = (<MyClass>obj).value
```

### 3. 数组边界问题
```cython
# 问题：数组越界
# 解决：添加边界检查或确保索引有效
if 0 <= index < array_size:
    value = array[index]
```

### 4. GIL相关问题
```cython
# 问题：nogil块中不能使用Python对象
# 解决：在nogil块外处理Python对象
cdef double[:] data = python_array  # 转换为内存视图
with nogil:
    # 现在可以安全操作data
    pass
```

## 六、优化检查清单

### 每个文件必须检查：
- [ ] 所有类改为`cdef class`
- [ ] 热点方法改为`cdef`或`cpdef`
- [ ] 循环变量声明C类型
- [ ] 使用内存视图处理数组
- [ ] 数学运算使用C库函数
- [ ] 适当位置释放GIL
- [ ] 添加完整编译指令
- [ ] 测试编译成功
- [ ] 运行测试通过
- [ ] 性能基准测试

## 七、优化工作流

```bash
# 1. 优化单个文件
vim cybacktrader/indicators/sma.pyx

# 2. 测试编译
pip install -U .

# 3. 运行测试
pytest tests/test_indicators.py -v

# 4. 性能测试
python benchmarks/test_sma_performance.py

# 5. 提交更改
git add cybacktrader/indicators/sma.pyx
git commit -m "Optimize SMA indicator with Cython"
```

## 八、预期性能提升

根据不同模块的特点，预期性能提升如下：

| 模块类型 | 预期提升 | 关键优化点 |
|---------|---------|-----------|
| 数据缓冲 | 5-10x | C数组、内存视图 |
| 指标计算 | 8-15x | 类型声明、C数学函数 |
| 策略执行 | 3-5x | 方法内联、GIL释放 |
| 数据加载 | 2-3x | 缓冲I/O、批处理 |
| 整体回测 | 5-10x | 综合优化效果 |

## 九、注意事项

1. **保持API兼容性**：优化不应改变公共接口
2. **逐步优化**：先优化热点代码，再优化其他部分
3. **充分测试**：每次优化后必须运行完整测试套件
4. **性能监控**：建立基准测试，监控优化效果
5. **文档更新**：记录优化决策和性能数据
