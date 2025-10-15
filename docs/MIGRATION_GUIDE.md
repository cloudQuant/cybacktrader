# cybacktrader 迁移指南

## 快速迁移

### 1. 最简单的迁移

只需将导入语句从 `backtrader` 改为 `cybacktrader`：

```python
# 原代码
import backtrader as bt

# 新代码 - 只需修改这一行
import cybacktrader as bt

# 其余代码完全不变
cerebro = bt.Cerebro()
# ... 您的策略代码
```

### 2. 子模块导入

```python
# 原代码
from backtrader import indicators as ind
from backtrader.analyzers import SharpeRatio

# 新代码
from cybacktrader import indicators as ind
from cybacktrader.analyzers import SharpeRatio
```

### 3. 批量迁移测试文件

使用提供的迁移脚本：

```bash
python scripts/migrate_tests_imports.py [测试目录路径]
```

该脚本会自动替换所有 `backtrader` 导入为 `cybacktrader`。

## 兼容性说明

### 完全兼容的特性

- ✅ 所有策略接口（Strategy）
- ✅ 所有指标（Indicators）
- ✅ 所有分析器（Analyzers）
- ✅ 所有数据源（Feeds）
- ✅ 订单管理（Orders）
- ✅ 回测引擎（Cerebro）
- ✅ 绘图功能（Plotting）

### 当前优化状态

#### 已优化模块（Cython 编译）

- ✅ `mathsupport` - 数学支持函数（已优化）

#### 计划优化模块

**优先级 A - 核心数据路径**
- 📋 `lineroot` - Line 基类
- 📋 `linebuffer` - Line 缓冲区
- 📋 `lineiterator` - Line 迭代器
- 📋 `lineseries` - Line 序列

**优先级 B - 计算密集模块**
- 📋 `indicator` - 指标基类
- 📋 `indicators/*` - 各种技术指标

**优先级 C - 调度与撮合**
- 📋 `cerebro` - 回测引擎
- 📋 `broker` - 经纪商模拟
- 📋 `order` - 订单处理

## 性能优化建议

### 1. 使用编译后的模块

确保安装时编译 Cython 扩展：

```bash
pip install -e .[dev]
python setup.py build_ext --inplace
```

### 2. 优化策略代码

虽然 `cybacktrader` 提供了底层优化，您的策略代码也可以优化：

```python
# 避免在 next() 中重复计算
class MyStrategy(bt.Strategy):
    def __init__(self):
        # 在初始化时计算指标，而不是在 next() 中
        self.sma = bt.indicators.SMA(self.data.close, period=20)
    
    def next(self):
        # 直接使用预计算的指标
        if self.data.close[0] > self.sma[0]:
            self.buy()
```

### 3. 使用 runonce 模式

```python
cerebro = bt.Cerebro(runonce=True, preload=True)
# runonce=True 使用矢量化运算，速度更快
```

## 性能基准

### 测试环境

- CPU: [您的CPU型号]
- Python: 3.13.5
- 数据集: 2006-day-001.txt (251 天数据)
- 策略: 简单 SMA(30) 策略

### 当前性能

| 模块 | 平均时间 | 改进 |
|------|---------|------|
| backtrader | ~19.3ms | 基准 |
| cybacktrader (兼容层) | ~16.7ms | 1.15x |
| cybacktrader (优化后) | TBD | 目标 10x+ |

## 故障排查

### ImportError: No module named 'cybacktrader'

确保已正确安装：

```bash
pip install -e .
```

### 编译错误

确保已安装 Cython 和编译工具：

```bash
# Windows
pip install Cython
# 需要 Visual Studio Build Tools

# Linux
pip install Cython
sudo apt-get install build-essential
```

### 性能没有提升

1. 确保 Cython 模块已编译：
   ```bash
   python setup.py build_ext --inplace
   ```

2. 检查是否使用了编译的版本：
   ```python
   import cybacktrader.mathsupport as ms
   print(ms.__file__)  # 应该以 .pyd (Windows) 或 .so (Linux) 结尾
   ```

## 回滚到 backtrader

如果遇到问题，可以轻松回滚：

```python
# 只需改回原来的导入
import backtrader as bt
# 所有代码保持不变
```

## 贡献优化

如果您想贡献 Cython 优化：

1. Fork 仓库
2. 创建优化分支
3. 添加性能测试
4. 确保所有测试通过
5. 提交 Pull Request

详见 [CONTRIBUTING.md](./CONTRIBUTING.md)

