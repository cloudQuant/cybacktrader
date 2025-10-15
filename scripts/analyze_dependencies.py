#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
分析 cybacktrader 模块依赖关系
确定正确的编译顺序
"""

import re
from pathlib import Path
from collections import defaultdict, deque


def extract_imports(pyx_file):
    """提取文件中的 cybacktrader 导入"""
    try:
        with open(pyx_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return []
    
    imports = []
    
    # from cybacktrader.xxx import
    for match in re.finditer(r'from cybacktrader\.(\S+) import', content):
        imports.append(match.group(1))
    
    # from cybacktrader import xxx
    for match in re.finditer(r'from cybacktrader import (\w+)', content):
        imports.append(match.group(1))
    
    return list(set(imports))


def build_dependency_graph(base_dir='cybacktrader'):
    """构建依赖图"""
    base_path = Path(base_dir)
    dependencies = {}  # module -> [depends_on]
    
    for pyx_file in base_path.rglob('*.pyx'):
        # 模块名
        rel_path = pyx_file.relative_to(base_path)
        module_name = str(rel_path).replace('\\', '.').replace('/', '.').replace('.pyx', '')
        
        # 提取依赖
        imports = extract_imports(pyx_file)
        dependencies[module_name] = imports
    
    return dependencies


def topological_sort(dependencies):
    """
    拓扑排序确定编译顺序
    
    Returns:
        levels: [[level0_modules], [level1_modules], ...]
    """
    # 计算入度
    in_degree = defaultdict(int)
    all_modules = set(dependencies.keys())
    
    for module, deps in dependencies.items():
        for dep in deps:
            # 只考虑内部依赖
            dep_module = dep.split('.')[0]  # 取第一层
            if dep_module in all_modules or any(m.startswith(dep_module + '.') for m in all_modules):
                in_degree[module] += 1
    
    # 初始化：入度为0的模块
    levels = []
    current_level = [m for m in all_modules if in_degree[m] == 0]
    levels.append(sorted(current_level))
    
    processed = set(current_level)
    
    # 逐层处理
    while len(processed) < len(all_modules):
        next_level = []
        for module in all_modules:
            if module in processed:
                continue
            # 检查依赖是否都已处理
            deps = dependencies.get(module, [])
            deps_ready = all(
                any(d in processed or d.startswith(p) for p in processed)
                for d in deps if d
            )
            if deps_ready:
                next_level.append(module)
        
        if not next_level:
            # 有循环依赖或孤立节点
            remaining = sorted(all_modules - processed)
            levels.append(remaining)
            break
        
        levels.append(sorted(next_level))
        processed.update(next_level)
    
    return levels


def main():
    print("=" * 70)
    print("cybacktrader 依赖关系分析")
    print("=" * 70)
    print()
    
    dependencies = build_dependency_graph()
    print(f"总模块数: {len(dependencies)}")
    print()
    
    # 显示一些依赖关系示例
    print("依赖关系示例:")
    print("-" * 70)
    for module in sorted(dependencies.keys())[:10]:
        deps = dependencies[module]
        if deps:
            print(f"{module}")
            for dep in deps[:3]:
                print(f"  ← {dep}")
            if len(deps) > 3:
                print(f"  ← ... 还有 {len(deps) - 3} 个")
    
    print()
    print("=" * 70)
    print("推荐编译顺序（按层级）")
    print("=" * 70)
    
    levels = topological_sort(dependencies)
    
    for i, level in enumerate(levels):
        print(f"\n第 {i+1} 层 ({len(level)} 个模块):")
        print("-" * 70)
        for module in level[:15]:
            print(f"  {module}")
        if len(level) > 15:
            print(f"  ... 还有 {len(level) - 15} 个")
    
    print()
    print("=" * 70)
    print("编译建议")
    print("=" * 70)
    print()
    print("1. 先编译第 1 层（无依赖或只依赖外部）")
    print("2. 逐层编译后续层级")
    print("3. 如果某层编译失败，跳过继续下一层")
    print()
    print("提示：大部分模块应该在第 1 层（因为主要依赖已编译的根模块）")


if __name__ == '__main__':
    main()



