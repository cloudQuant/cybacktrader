# PyPy3 安装和配置指南

## 问题说明

在Ubuntu/Debian系统上，PyPy3的pip默认是禁用的，需要手动安装。

## 解决方案

### 方法1：安装pypy3-pip（推荐）

```bash
# 安装PyPy3的pip
sudo apt-get update
sudo apt-get install pypy3-pip

# 验证安装
pypy3 -m pip --version
```

### 方法2：使用get-pip.py

如果apt-get安装失败，可以手动安装pip：

```bash
# 下载get-pip.py
wget https://bootstrap.pypa.io/get-pip.py

# 使用PyPy3安装pip
pypy3 get-pip.py

# 清理
rm get-pip.py

# 验证
pypy3 -m pip --version
```

### 方法3：使用虚拟环境（最佳实践）

```bash
# 安装pypy3-venv
sudo apt-get install pypy3-venv

# 创建PyPy虚拟环境
pypy3 -m venv ~/pypy3-env

# 激活虚拟环境
source ~/pypy3-env/bin/activate

# 现在pip应该可用了
pip --version

# 升级pip
pip install --upgrade pip
```

## 安装backtrader

### 在系统PyPy3中安装

```bash
# 方法1完成后
pypy3 -m pip install backtrader

# 或者从本地安装
pypy3 -m pip install /home/yun/Documents/backtrader
```

### 在虚拟环境中安装（推荐）

```bash
# 激活虚拟环境
source ~/pypy3-env/bin/activate

# 安装依赖
pip install numpy pandas

# 安装backtrader
pip install backtrader

# 或从本地安装
pip install /home/yun/Documents/backtrader
```

## 运行性能对比测试

### 使用系统PyPy3

```bash
cd /home/yun/Documents/cybacktrader/benchmarks
pypy3 compare_python_implementations.py
```

### 使用虚拟环境

```bash
# 激活虚拟环境
source ~/pypy3-env/bin/activate

# 运行测试
cd /home/yun/Documents/cybacktrader/benchmarks
python compare_python_implementations.py

# 退出虚拟环境
deactivate
```

## 完整安装流程（推荐）

```bash
# 1. 安装必要的包
sudo apt-get update
sudo apt-get install pypy3 pypy3-pip pypy3-venv

# 2. 创建虚拟环境
pypy3 -m venv ~/pypy3-backtrader-env

# 3. 激活虚拟环境
source ~/pypy3-backtrader-env/bin/activate

# 4. 升级pip
pip install --upgrade pip

# 5. 安装依赖
pip install numpy pandas

# 6. 安装backtrader
pip install backtrader
# 或从本地安装
# pip install /home/yun/Documents/backtrader

# 7. 验证安装
python -c "import backtrader; print(backtrader.__version__)"

# 8. 运行性能测试
cd /home/yun/Documents/cybacktrader/benchmarks
python compare_python_implementations.py

# 9. 完成后退出虚拟环境
deactivate
```

## 常见问题

### Q1: pypy3-pip安装失败

**解决：** 使用get-pip.py方法

```bash
wget https://bootstrap.pypa.io/get-pip.py
pypy3 get-pip.py --user
rm get-pip.py
```

### Q2: NumPy在PyPy上安装很慢

**原因：** PyPy需要编译NumPy，可能需要10-30分钟

**解决：** 耐心等待，或使用预编译版本

```bash
# 使用conda的PyPy（如果可用）
conda install -c conda-forge pypy

# 或者跳过NumPy测试
# 修改测试脚本，不生成数据，使用现有CSV
```

### Q3: backtrader在PyPy上运行出错

**可能原因：**
- 某些C扩展不兼容PyPy
- NumPy版本问题

**解决：**
```bash
# 尝试安装兼容版本
pip install numpy==1.24.0
pip install backtrader
```

### Q4: 虚拟环境激活失败

**检查：**
```bash
# 确认虚拟环境创建成功
ls -la ~/pypy3-env/bin/

# 如果没有activate，重新创建
rm -rf ~/pypy3-env
pypy3 -m venv ~/pypy3-env
```

## 性能测试注意事项

### 首次运行

PyPy使用JIT编译，首次运行会比较慢：

```bash
# 建议运行多轮让JIT预热
# 测试脚本默认3轮，第2-3轮性能更准确
```

### 内存使用

PyPy通常使用更多内存：

```bash
# 如果内存不足，减少数据规模
# 修改脚本中的 n_rows=10000 为更小的值
```

## 预期结果

### 如果一切正常

```
Python实现性能对比基准测试
======================================================================
✓ backtrader版本: 1.9.76.123
生成10000行测试数据...

当前Python实现: PyPy 7.3.x (Python 3.x)
----------------------------------------------------------------------
运行PyPy基准测试 (共3轮)...
  第1轮: 0.xxxx秒
  第2轮: 0.xxxx秒
  第3轮: 0.xxxx秒

PyPy结果:
  平均时间: 0.xxxx秒
  ...

对比结果:
CPython平均时间: 0.4832秒
PyPy平均时间:    0.xxxx秒
PyPy加速比:      x.xxxx 🚀
```

## 快速命令参考

```bash
# 安装PyPy环境
sudo apt-get install pypy3 pypy3-pip pypy3-venv

# 创建虚拟环境
pypy3 -m venv ~/pypy3-env

# 激活
source ~/pypy3-env/bin/activate

# 安装backtrader
pip install backtrader

# 运行测试
cd /home/yun/Documents/cybacktrader/benchmarks
python compare_python_implementations.py

# 退出
deactivate
```

---

**更新时间：** 2025年10月19日  
**适用系统：** Ubuntu/Debian  
**PyPy版本：** 3.x
