#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
检查 cybacktrader 的编译状态
显示哪些 .pyx 文件已编译，哪些还未编译
"""

import os
from pathlib import Path
from collections import defaultdict


def check_compilation_status(base_dir='cybacktrader'):
    """
    检查编译状态
    
    Returns:
        compiled: 已编译的文件列表
        not_compiled: 未编译的文件列表
    """
    base_path = Path(base_dir)
    
    compiled = []
    not_compiled = []
    
    # 遍历所有 .pyx 文件
    for pyx_file in base_path.rglob('*.pyx'):
        # 构造对应的 .pyd 文件名
        pyd_name = pyx_file.stem + '.cp313-win_amd64.pyd'
        pyd_file = pyx_file.parent / pyd_name
        
        rel_path = pyx_file.relative_to(base_path)
        
        if pyd_file.exists():
            compiled.append(str(rel_path))
        else:
            not_compiled.append(str(rel_path))
    
    return compiled, not_compiled


def group_by_directory(file_list):
    """按目录分组文件"""
    groups = defaultdict(list)
    
    for file_path in file_list:
        if '\\' in file_path or '/' in file_path:
            # 有子目录
            parts = file_path.replace('\\', '/').split('/')
            dir_name = parts[0]
            groups[dir_name].append(file_path)
        else:
            # 根目录
            groups['[root]'].append(file_path)
    
    return groups


def main():
    print("=" * 70)
    print("cybacktrader 编译状态检查")
    print("=" * 70)
    print()
    
    compiled, not_compiled = check_compilation_status()
    
    total = len(compiled) + len(not_compiled)
    compile_rate = (len(compiled) / total * 100) if total > 0 else 0
    
    print(f"总计 .pyx 文件: {total}")
    print(f"已编译: {len(compiled)} 个 ({compile_rate:.1f}%)")
    print(f"未编译: {len(not_compiled)} 个")
    print()
    
    # 按目录分组显示
    print("=" * 70)
    print("已编译模块（按目录）")
    print("=" * 70)
    
    compiled_groups = group_by_directory(compiled)
    for dir_name in sorted(compiled_groups.keys()):
        files = compiled_groups[dir_name]
        print(f"\n{dir_name}/ ({len(files)} 个):")
        for f in sorted(files)[:5]:  # 只显示前5个
            print(f"  ✓ {Path(f).name}")
        if len(files) > 5:
            print(f"  ... 还有 {len(files) - 5} 个")
    
    print()
    print("=" * 70)
    print("未编译模块（按目录）")
    print("=" * 70)
    
    not_compiled_groups = group_by_directory(not_compiled)
    for dir_name in sorted(not_compiled_groups.keys()):
        files = not_compiled_groups[dir_name]
        print(f"\n{dir_name}/ ({len(files)} 个):")
        for f in sorted(files):
            print(f"  ✗ {Path(f).name}")
    
    print()
    print("=" * 70)
    print("统计摘要")
    print("=" * 70)
    
    # 按目录统计
    all_groups = {}
    for dir_name in set(list(compiled_groups.keys()) + list(not_compiled_groups.keys())):
        c_count = len(compiled_groups.get(dir_name, []))
        nc_count = len(not_compiled_groups.get(dir_name, []))
        total_count = c_count + nc_count
        rate = (c_count / total_count * 100) if total_count > 0 else 0
        all_groups[dir_name] = (c_count, nc_count, total_count, rate)
    
    print(f"\n{'目录':<20} {'已编译':>8} {'未编译':>8} {'总计':>8} {'完成率':>8}")
    print("-" * 70)
    for dir_name in sorted(all_groups.keys()):
        c, nc, t, rate = all_groups[dir_name]
        print(f"{dir_name:<20} {c:>8} {nc:>8} {t:>8} {rate:>7.1f}%")
    
    print("-" * 70)
    print(f"{'总计':<20} {len(compiled):>8} {len(not_compiled):>8} {total:>8} {compile_rate:>7.1f}%")
    print()
    
    if not_compiled:
        print("\n未编译的文件列表（用于调试）:")
        print("-" * 70)
        for f in sorted(not_compiled)[:20]:  # 只显示前20个
            print(f"  {f}")
        if len(not_compiled) > 20:
            print(f"  ... 还有 {len(not_compiled) - 20} 个")


if __name__ == '__main__':
    main()

