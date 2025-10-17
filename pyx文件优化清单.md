# PYX 文件优化清单

**总数**：162个文件  
**策略**：保守优化（只添加基本编译器指令+关键类型声明）

---

## ✅ 已完成优化（P0模块）

1. ✅ cybacktrader/linebuffer.pyx - 深度优化
2. ✅ cybacktrader/indicator.pyx - 保守优化
3. ✅ cybacktrader/lineseries.pyx - 保守优化
4. ✅ cybacktrader/strategy.pyx - 修复typo+保守优化

---

## 📋 待优化文件列表（按setup.py编译顺序）

### Level 1: 基础模块（6个）

5. cybacktrader/version.pyx
6. cybacktrader/errors.pyx
7. cybacktrader/mathsupport.pyx
8. cybacktrader/utils/py3.pyx
9. cybacktrader/utils/date.pyx
10. cybacktrader/utils/autodict.pyx

### Level 2: 元类和根（2个）

11. cybacktrader/metabase.pyx
12. cybacktrader/lineroot.pyx

### Level 3: 核心函数（1个）

13. cybacktrader/functions.pyx

### Level 4: 数据系列（2个）

14. cybacktrader/dataseries.pyx
15. cybacktrader/lineiterator.pyx

### Level 5: 交易组件（6个）

16. cybacktrader/order.pyx
17. cybacktrader/trade.pyx
18. cybacktrader/position.pyx
19. cybacktrader/comminfo.pyx
20. cybacktrader/analyzer.pyx
21. cybacktrader/observer.pyx

### Level 6: 执行层（11个）

22. cybacktrader/feed.pyx
23. cybacktrader/broker.pyx
24. cybacktrader/signal.pyx
25. cybacktrader/store.pyx
26. cybacktrader/sizer.pyx
27. cybacktrader/writer.pyx
28. cybacktrader/timer.pyx
29. cybacktrader/fillers.pyx
30. cybacktrader/flt.pyx
31. cybacktrader/resamplerfilter.pyx
32. cybacktrader/tradingcal.pyx

### Level 7: 引擎（1个）

33. cybacktrader/cerebro.pyx

### Level 8: 子模块（~130个）

**Analyzers** (14个已优化timereturn，剩余13个)
**Brokers** (6个)
**Feeds** (15个)
**Filters** (8个)
**Indicators** (70+个)
**Observers** (7个)
**Plot** (7个)
**Sizers** (2个)
**Stores** (6个)
**Utils** (剩余部分)

---

## 优化策略

### 基本优化模板

```python
# 在文件开头添加（紧跟#!/usr/bin/env python之后）
# Cython性能优化标记
# cython: language_level=3
```

### 如果有明显循环

```python
# 添加循环变量类型声明
cdef int i
for i in range(start, end):
    # ...
```

### 不做的事

- ❌ 不添加 boundscheck=False
- ❌ 不添加 wraparound=False
- ❌ 不做深度重构
- ❌ 不破坏API

---

## 执行计划

1. 按Level顺序逐个文件优化
2. 每优化一个，立即测试：
   ```bash
   pip install -U .
   pytest tests -n 8
   ```
3. 如果测试失败，回滚该文件
4. 继续下一个文件

---

**当前进度**：4/162 (2.5%)  
**目标**：100% (162/162)

