# 贡献指南

感谢您对 cybacktrader 的关注！我们欢迎各种形式的贡献。

## 如何贡献

### 报告问题

如果您发现 bug 或有功能建议：

1. 查看 [Issues](https://github.com/yourusername/cybacktrader/issues) 确认问题未被报告
2. 创建新 Issue，提供详细信息：
   - 问题描述
   - 复现步骤
   - 预期行为 vs 实际行为
   - 环境信息（OS、Python 版本等）

### 提交代码

#### 1. Fork 和 Clone

```bash
# Fork 仓库（在 GitHub 上点击 Fork）
git clone https://github.com/your-username/cybacktrader.git
cd cybacktrader
```

#### 2. 创建分支

```bash
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/your-bug-fix
```

#### 3. 设置开发环境

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装开发依赖
pip install -e .[dev]
```

#### 4. 进行修改

遵循以下原则：

- **保持兼容性**: 确保 API 与 backtrader 100% 兼容
- **添加测试**: 为新功能或修复添加测试
- **文档更新**: 更新相关文档
- **代码风格**: 遵循 PEP 8

#### 5. 运行测试

```bash
# 运行所有测试
pytest tests/

# 运行特定测试
pytest tests/original_tests/test_order.py -v

# 运行性能测试
python benchmarks/baseline_benchmark.py
```

#### 6. 提交代码

```bash
git add .
git commit -m "描述性的提交信息"
git push origin your-branch-name
```

#### 7. 创建 Pull Request

1. 在 GitHub 上创建 Pull Request
2. 描述您的更改
3. 链接相关的 Issues
4. 等待审核

## Cython 优化指南

### 选择优化目标

优先考虑：

1. **热点函数**: 使用 profiler 识别
2. **数值计算**: 循环、数组操作
3. **频繁调用**: 每次回测调用数千次的函数

### Cython 化步骤

#### 步骤 1: 复制 Python 文件

```bash
# 示例：优化 example.py
cp backtrader/example.py cybacktrader/example.pyx
```

#### 步骤 2: 添加 Cython 指令

```cython
# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True
# cython: initializedcheck=False
# cython: nonecheck=False
```

#### 步骤 3: 添加类型声明

```cython
# Python 原代码
def calculate(x, y):
    result = 0
    for i in range(len(x)):
        result += x[i] * y[i]
    return result

# Cython 优化后
cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef double calculate(double[::1] x, double[::1] y):
    cdef:
        double result = 0.0
        Py_ssize_t i, n = x.shape[0]
    
    for i in range(n):
        result += x[i] * y[i]
    
    return result
```

#### 步骤 4: 更新 setup.py

```python
ext_modules = [
    Extension("cybacktrader.example", ["cybacktrader/example.pyx"]),
]
```

#### 步骤 5: 编译和测试

```bash
# 编译
python setup.py build_ext --inplace

# 测试
python -c "from cybacktrader import example; print(example.calculate([1,2,3], [4,5,6]))"

# 运行完整测试
pytest tests/
```

#### 步骤 6: 性能验证

```python
import time
import backtrader.example as bt_example
import cybacktrader.example as cy_example

# 测试数据
data = list(range(10000))

# backtrader 版本
t0 = time.perf_counter()
bt_example.calculate(data, data)
bt_time = time.perf_counter() - t0

# cybacktrader 版本
t0 = time.perf_counter()
cy_example.calculate(data, data)
cy_time = time.perf_counter() - t0

print(f"加速比: {bt_time / cy_time:.2f}x")
```

### Cython 最佳实践

#### 1. 使用类型化内存视图

```cython
# ✅ 推荐
cpdef process_array(double[::1] data):
    cdef Py_ssize_t i
    cdef double total = 0.0
    for i in range(data.shape[0]):
        total += data[i]
    return total

# ❌ 避免
def process_list(data):
    total = 0
    for x in data:
        total += x
    return total
```

#### 2. 声明所有变量类型

```cython
cdef:
    int i, j, k
    double result
    Py_ssize_t n
```

#### 3. 使用 cpdef 支持 Python 调用

```cython
# cpdef 生成 C 和 Python 接口
cpdef double my_function(double x):
    return x * 2.0
```

#### 4. 避免 Python 对象

```cython
# ✅ 使用 C 类型
cdef double x = 1.0

# ❌ 避免 Python 对象
x = 1.0  # Python float
```

#### 5. 使用 C 库函数

```cython
from libc.math cimport sqrt, sin, cos, pow

cpdef double distance(double x1, double y1, double x2, double y2):
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)
```

### 兼容性检查清单

- [ ] API 签名不变
- [ ] 返回值类型一致
- [ ] 错误处理保持一致
- [ ] 所有测试通过
- [ ] 性能有提升
- [ ] 文档已更新

## 代码风格

### Python 代码

遵循 PEP 8：

```python
# ✅ 好的风格
def calculate_sma(data, period=20):
    """计算简单移动平均"""
    return sum(data[-period:]) / period

# ❌ 避免
def calcSMA(d,p=20):
    return sum(d[-p:])/p
```

### Cython 代码

```cython
# ✅ 清晰的类型声明
cpdef double calculate_average(double[::1] values):
    """
    Calculate average of values
    
    Args:
        values: Array of doubles
        
    Returns:
        Average as double
    """
    cdef:
        double total = 0.0
        Py_ssize_t i, n = values.shape[0]
    
    for i in range(n):
        total += values[i]
    
    return total / n
```

### 文档字符串

```python
def my_function(arg1, arg2):
    """
    简短描述
    
    详细描述（可选）
    
    Args:
        arg1 (type): 参数1的描述
        arg2 (type): 参数2的描述
        
    Returns:
        type: 返回值描述
        
    Raises:
        ValueError: 何时抛出异常
        
    Example:
        >>> my_function(1, 2)
        3
    """
    return arg1 + arg2
```

## 测试指南

### 编写测试

```python
import pytest
import cybacktrader as bt

def test_strategy_execution():
    """测试策略执行"""
    cerebro = bt.Cerebro()
    # ... 设置
    results = cerebro.run()
    assert len(results) > 0

def test_indicator_calculation():
    """测试指标计算"""
    data = [1, 2, 3, 4, 5]
    sma = bt.indicators.SMA(data, period=3)
    assert sma[0] == 4.0  # (3+4+5)/3
```

### 性能测试

```python
import pytest

@pytest.mark.benchmark
def test_performance(benchmark):
    """性能基准测试"""
    def run_backtest():
        cerebro = bt.Cerebro()
        # ... 设置
        cerebro.run()
    
    benchmark(run_backtest)
```

## 发布流程

### 版本号

遵循语义化版本 (SemVer)：

- MAJOR.MINOR.PATCH
- 0.1.0 -> 0.1.1 (bug 修复)
- 0.1.0 -> 0.2.0 (新功能)
- 0.9.0 -> 1.0.0 (重大变更)

### 发布检查清单

- [ ] 所有测试通过
- [ ] 文档已更新
- [ ] CHANGELOG.md 已更新
- [ ] 版本号已更新
- [ ] 创建 Git tag
- [ ] 构建分发包
- [ ] 上传到 PyPI

## 获取帮助

- 📧 邮件列表: [cybacktrader@example.com](mailto:cybacktrader@example.com)
- 💬 Discord: [链接]
- 📖 文档: [链接]
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/cybacktrader/issues)

## 行为准则

请保持：

- 尊重和包容
- 建设性反馈
- 专业态度
- 乐于助人

## 致谢

感谢所有贡献者！您的努力让 cybacktrader 变得更好。

## 许可证

贡献的代码将遵循项目的 [许可证](./LICENSE)。

