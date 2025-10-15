#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
分析未编译成功的 .pyx 文件
详细罗列并分类
"""

from pathlib import Path
from collections import defaultdict


def get_uncompiled_modules():
    """
    获取所有未编译成功的模块
    
    Returns:
        list: 未编译的 .pyx 文件路径列表
    """
    cybacktrader_dir = Path('cybacktrader')
    uncompiled = []
    
    for pyx_file in cybacktrader_dir.rglob('*.pyx'):
        # 检查对应的 .pyd 文件是否存在
        pyd_file = pyx_file.parent / (pyx_file.stem + '.cp313-win_amd64.pyd')
        
        if not pyd_file.exists():
            uncompiled.append(pyx_file)
    
    return uncompiled


def categorize_modules(modules):
    """按目录分类模块"""
    categories = defaultdict(list)
    
    for module in modules:
        rel_path = module.relative_to('cybacktrader')
        parts = str(rel_path).split('\\')
        
        if len(parts) > 1:
            category = parts[0]  # 子目录名
        else:
            category = '[root]'  # 根目录
        
        categories[category].append(rel_path)
    
    return categories


def analyze_module_content(pyx_file):
    """分析模块内容，找出可能的问题"""
    try:
        with open(pyx_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return []
    
    issues = []
    
    # 检查外部依赖
    external_imports = {
        'influxdb': 'InfluxDB数据库',
        'ccxt': 'CCXT加密货币交易',
        'oandapyV20': 'OANDA外汇',
        'blaze': 'Blaze数据处理',
        'odo': 'Odo数据转换',
        'pyfolio': 'PyFolio分析',
        'quandl': 'Quandl数据源',
        'vnpy': 'VNPy/CTP期货',
        'ctp': 'CTP期货',
        'ib.ext': 'Interactive Brokers',
        'ib.opt': 'Interactive Brokers',
        'visionchart': 'VisionChart',
    }
    
    for lib, desc in external_imports.items():
        if f'import {lib}' in content or f'from {lib}' in content:
            issues.append(f"依赖外部库: {lib} ({desc})")
    
    # 检查 frompackages
    if 'frompackages' in content:
        issues.append("使用了frompackages机制（Cython不支持）")
    
    return issues


def main():
    print("=" * 80)
    print("未编译成功的 .pyx 文件分析报告")
    print("=" * 80)
    print()
    
    # 获取所有未编译的模块
    uncompiled = get_uncompiled_modules()
    
    # 统计
    total_pyx = len(list(Path('cybacktrader').rglob('*.pyx')))
    compiled = total_pyx - len(uncompiled)
    
    print(f"总计 .pyx 文件: {total_pyx} 个")
    print(f"已编译成功: {compiled} 个 ({compiled/total_pyx*100:.1f}%)")
    print(f"未编译成功: {len(uncompiled)} 个 ({len(uncompiled)/total_pyx*100:.1f}%)")
    print()
    
    if not uncompiled:
        print("恭喜！所有模块都已编译成功！")
        return
    
    # 按类别分组
    categories = categorize_modules(uncompiled)
    
    print("=" * 80)
    print("未编译模块详细列表（按目录分类）")
    print("=" * 80)
    print()
    
    total_listed = 0
    for category in sorted(categories.keys()):
        modules = categories[category]
        print(f"\n【{category.upper()}】 目录 - {len(modules)} 个模块")
        print("-" * 80)
        
        for i, rel_path in enumerate(sorted(modules), 1):
            full_path = Path('cybacktrader') / rel_path
            total_listed += 1
            
            print(f"\n{total_listed}. {rel_path}")
            
            # 分析原因
            issues = analyze_module_content(full_path)
            if issues:
                print("   原因:")
                for issue in issues:
                    print(f"     - {issue}")
            else:
                print("   原因: 未知（需要查看编译日志）")
    
    print("\n" + "=" * 80)
    print("统计摘要")
    print("=" * 80)
    print()
    print(f"{'目录':<20} {'未编译数量':>10}")
    print("-" * 80)
    for category in sorted(categories.keys()):
        print(f"{category:<20} {len(categories[category]):>10}")
    print("-" * 80)
    print(f"{'总计':<20} {len(uncompiled):>10}")
    print()
    
    print("=" * 80)
    print("下一步建议")
    print("=" * 80)
    print()
    
    # 分析需要安装的包
    all_deps = set()
    for pyx in uncompiled:
        issues = analyze_module_content(pyx)
        for issue in issues:
            if '依赖外部库' in issue:
                # 提取库名
                lib = issue.split(':')[1].split('(')[0].strip()
                all_deps.add(lib)
    
    if all_deps:
        print("需要安装的外部包:")
        for dep in sorted(all_deps):
            print(f"  - {dep}")
        print()
        print("安装命令:")
        # 将包名映射到pip包名
        pip_names = {
            'ib.ext': 'ibapi',
            'ib.opt': 'ibapi',
            'oandapyV20': 'oandapyV20',
            'vnpy': 'vnpy',
            'ctp': 'vnpy',
            'visionchart': '# visionchart（可能需要手动安装）',
        }
        
        pip_packages = []
        for dep in sorted(all_deps):
            pip_name = pip_names.get(dep, dep)
            if not pip_name.startswith('#'):
                pip_packages.append(pip_name)
        
        if pip_packages:
            print(f"  pip install {' '.join(pip_packages)}")
    
    print()
    print("然后重新编译:")
    print("  python setup.py build_ext --inplace")
    print()


if __name__ == '__main__':
    main()

