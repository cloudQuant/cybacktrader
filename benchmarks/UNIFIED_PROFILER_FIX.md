# unified_profiler.py 修复说明

## 问题总结

运行 `unified_profiler.py` 时遇到两个关键错误：

### 1. `module 'cybacktrader' has no attribute 'Cerebro'`
**原因**: 脚本将项目根目录添加到 `sys.path` 的最前面，导致优先导入源码目录中未编译的 cybacktrader 模块，而不是已安装的完整包。

### 2. `Another profiling tool is already active`
**原因**: cProfile 和 tracemalloc 在第一轮测试后没有正确清理，导致后续轮次无法启动新的 profiler。

## 修复方案

### 修复 1: 确保使用已安装的包

**修改位置**: 第 38-41 行

```python
# 注释掉将项目根目录添加到 sys.path 的代码
# project_root = Path(__file__).parent.parent
# sys.path.insert(0, str(project_root))
```

这样可以确保 Python 优先使用 site-packages 中已编译安装的 cybacktrader 包。

### 修复 2: 添加 Cerebro 类检查

**修改位置**: 第 109-115 行

```python
elif module_name == 'cybacktrader':
    import cybacktrader as bt
    # 检查关键类是否存在
    if not hasattr(bt, 'Cerebro'):
        print(f"[失败] cybacktrader 模块不完整，缺少 Cerebro 类")
        print(f"       请先运行: pip install -e . 来安装 cybacktrader")
        return None
```

增加了导入验证，如果包不完整会给出清晰的错误提示。

### 修复 3: 完善 profiler 清理机制

**修改位置**: 第 171-241 行

主要改进：
1. 使用 try-finally 块确保 profiler 一定会被清理
2. 在每轮测试前完全禁用所有 profiler（包括 setprofile 和 settrace）
3. 检查并停止可能残留的 tracemalloc
4. 添加短暂延迟让系统完全清理资源
5. 在 finally 块中强制清理所有 profiler

```python
try:
    # 确保之前的profiler已经完全禁用
    import sys
    if hasattr(sys, 'getprofile') and sys.getprofile() is not None:
        sys.setprofile(None)
    if hasattr(sys, 'gettrace') and sys.gettrace() is not None:
        sys.settrace(None)
    
    # 停止可能残留的 tracemalloc
    if tracemalloc.is_tracing():
        tracemalloc.stop()
    
    # 强制垃圾回收
    gc.collect()
    time.sleep(0.1)  # 给系统一点时间完全清理
    
    # ... profiler 代码 ...
    
finally:
    # 确保清理
    if pr is not None:
        try:
            pr.disable()
        except:
            pass
    
    try:
        import sys
        sys.setprofile(None)
        sys.settrace(None)
    except:
        pass
    
    if tracemalloc.is_tracing():
        try:
            tracemalloc.stop()
        except:
            pass
    
    gc.collect()
```

## 测试结果

修复后的脚本成功运行：

```bash
$ python /home/yun/Documents/cybacktrader/benchmarks/unified_profiler.py --data-size 10000 --rounds 3

======================================================================
Backtrader vs CyBacktrader 统一性能分析工具
======================================================================
[配置] 配置信息:
   数据规模: 10,000 行
   分析类型: function
   对比指标: time
   测试轮数: 3
======================================================================

✅ 第 1/3 轮测试 - 成功
   Backtrader: 5.7622s, 内存: 11.53MB
   CyBacktrader: 1.7813s, 内存: 6.48MB
   加速比: 3.23x

✅ 第 2/3 轮测试 - 成功
   Backtrader: 5.7408s, 内存: 0.56MB
   CyBacktrader: 1.7637s, 内存: 0.00MB
   加速比: 3.25x

✅ 第 3/3 轮测试 - 成功
   Backtrader: 5.7241s, 内存: 0.00MB
   CyBacktrader: 1.7294s, 内存: 0.56MB
   加速比: 3.31x

======================================================================
性能对比摘要
======================================================================
Backtrader 平均时间:    5.7424s
CyBacktrader 平均时间:  1.7581s
加速比:                 3.27x
时间节省:               3.9842s (69.4%)
Backtrader 平均内存:    4.03MB
CyBacktrader 平均内存:  2.35MB
内存节省:               1.68MB (41.8%)
======================================================================

[成功] 所有报告已生成到目录: /home/yun/Documents/cybacktrader/benchmarks/performance_reports
```

## 关键要点

1. **永远不要将源码目录添加到 sys.path 前面**，除非你明确知道你在做什么
2. **使用 try-finally 确保资源清理**，特别是对于 profiler 这类全局状态
3. **多轮测试需要在每轮之间完全清理状态**，避免状态泄漏
4. **添加适当的验证检查**，在导入模块后验证关键类是否存在

## 使用方法

修复后，脚本可以正常使用：

```bash
# 基础测试（10万行数据，1轮）
python unified_profiler.py --data-size 100000

# 小规模多轮测试（1万行，3轮）
python unified_profiler.py --data-size 10000 --rounds 3

# 大规模测试（100万行，1轮）
python unified_profiler.py --data-size 1000000 --rounds 1

# 内存对比分析
python unified_profiler.py --data-size 50000 --compare memory --rounds 3
```

所有报告会自动生成到 `benchmarks/performance_reports/` 目录下，包括：
- Markdown 报告（详细的函数级对比）
- HTML 报告（美观的可视化报告）
- JSON 数据（原始数据，便于进一步分析）
