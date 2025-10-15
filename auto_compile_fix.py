#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
自动编译和修复循环
按照当前需求.md的要求实现
"""

import subprocess
import time
import os
import re
from pathlib import Path


LOG_FILE = "compile_auto.log"


def clear_log():
    """清除旧日志"""
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    print(f"[清除] 旧日志已删除: {LOG_FILE}")


def start_compilation():
    """启动后台编译"""
    clear_log()
    
    print("[启动] 开始编译...")
    print(f"[日志] {LOG_FILE}")
    
    # 启动后台编译进程
    with open(LOG_FILE, 'w', encoding='utf-8') as log:
        process = subprocess.Popen(
            ['python', 'setup.py', 'build_ext', '--inplace'],
            stdout=log,
            stderr=subprocess.STDOUT,
            text=True
        )
    
    return process


def analyze_log():
    """
    分析日志，查找错误
    
    Returns:
        (has_errors, error_info, is_complete)
    """
    if not os.path.exists(LOG_FILE):
        return False, [], False
    
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return False, [], False
    
    errors = []
    
    # 检查是否有编译错误
    if 'Error compiling Cython file' in content:
        # 提取错误信息
        error_pattern = r'cybacktrader[/\\](\S+\.pyx):(\d+):(\d+): (.+)'
        for match in re.finditer(error_pattern, content):
            file_path, line, col, msg = match.groups()
            errors.append({
                'file': file_path,
                'line': int(line),
                'col': int(col),
                'message': msg
            })
    
    # 检查是否完成
    is_complete = 'copying' in content or 'running build_ext' in content
    if 'CompileError' in content:
        is_complete = False
    
    return len(errors) > 0, errors, is_complete


def check_compilation_success():
    """检查编译是否全部成功"""
    pyx_count = len(list(Path('cybacktrader').rglob('*.pyx')))
    pyd_count = len(list(Path('cybacktrader').rglob('*.pyd')))
    
    # 考虑跳过的模块
    from setup import SKIP_MODULES
    skip_count = len(SKIP_MODULES)
    
    target_count = pyx_count - skip_count
    
    print(f"[进度] 已编译: {pyd_count}/{target_count} (目标: {pyx_count} - {skip_count} 跳过)")
    
    return pyd_count >= target_count


def fix_errors(errors):
    """
    自动修复错误
    
    Returns:
        fixed_count: 修复的错误数量
    """
    fixed = 0
    
    for error in errors[:5]:  # 每次最多修复5个
        file_path = error['file']
        message = error['message']
        
        print(f"[修复] {file_path}: {message}")
        
        # 根据错误类型修复
        if 'undeclared name not builtin' in message:
            # 提取未声明的名称
            match = re.search(r'undeclared name not builtin: (\w+)', message)
            if match:
                undeclared_name = match.group(1)
                
                # 尝试修复
                if fix_undeclared_name(file_path, undeclared_name):
                    fixed += 1
    
    return fixed


def fix_undeclared_name(file_path, name):
    """修复未声明的名称"""
    full_path = Path('cybacktrader') / file_path
    
    if not full_path.exists():
        return False
    
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # pyecharts 相关
    if name in ['Kline', 'Line', 'Bar', 'Grid', 'EffectScatter']:
        if 'from pyecharts.charts import' not in content:
            content = re.sub(
                r'(from __future__ import.*?\n)',
                f'\\1\ntry:\n    from pyecharts.charts import Kline, Line, Bar, Grid, EffectScatter\n    from pyecharts import options as opts\nexcept ImportError:\n    Kline = Line = Bar = Grid = EffectScatter = opts = None\n',
                content
            )
    
    # pd, sm 等
    elif name == 'pd':
        if 'import pandas as pd' not in content:
            content = re.sub(
                r'(from cybacktrader import.*?\n)',
                '\\1try:\n    import pandas as pd\nexcept ImportError:\n    pd = None\n',
                content
            )
    
    elif name == 'sm':
        if 'import statsmodels' not in content:
            content = re.sub(
                r'(from cybacktrader import.*?\n)',
                '\\1try:\n    import statsmodels.api as sm\nexcept ImportError:\n    sm = None\n',
                content
            )
    
    elif name == 'coint':
        if 'from statsmodels.tsa.stattools import coint' not in content:
            content = re.sub(
                r'(from cybacktrader import.*?\n)',
                '\\1try:\n    from statsmodels.tsa.stattools import coint\nexcept ImportError:\n    coint = None\n',
                content
            )
    
    if content != original:
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ 已修复: 添加 {name} 导入")
        return True
    
    return False


def main():
    """主循环"""
    print("=" * 70)
    print("自动编译和修复循环")
    print("=" * 70)
    print()
    
    iteration = 0
    max_iterations = 20  # 最多迭代20次
    
    while iteration < max_iterations:
        iteration += 1
        print(f"\n{'='*70}")
        print(f"第 {iteration} 轮编译")
        print(f"{'='*70}\n")
        
        # 启动编译
        process = start_compilation()
        
        # 每30秒检查一次
        for check_round in range(20):  # 最多检查10分钟
            time.sleep(30)
            
            print(f"[检查] {check_round + 1}/20 (30秒间隔)")
            
            has_errors, errors, is_complete = analyze_log()
            
            if has_errors:
                print(f"[发现] {len(errors)} 个错误")
                # 终止编译进程
                process.terminate()
                try:
                    process.wait(timeout=10)
                except:
                    process.kill()
                
                # 修复错误
                fixed = fix_errors(errors)
                print(f"[修复] 修复了 {fixed} 个错误")
                
                if fixed > 0:
                    print("[继续] 重新编译...")
                    break
                else:
                    print("[停止] 无法自动修复，需要手动处理")
                    return
            
            # 检查是否完成
            if process.poll() is not None:
                # 进程已结束
                print("[完成] 编译进程已结束")
                
                if check_compilation_success():
                    print("\n" + "="*70)
                    print("✅ 所有模块编译成功！")
                    print("="*70)
                    return
                else:
                    # 检查是否还有错误
                    if has_errors:
                        break  # 继续下一轮
                    else:
                        print("[信息] 编译完成，检查结果...")
                        time.sleep(5)
                        return
        
        if iteration >= max_iterations:
            print("\n[停止] 达到最大迭代次数")
            break
    
    print("\n最终状态:")
    pyx_count = len(list(Path('cybacktrader').rglob('*.pyx')))
    pyd_count = len(list(Path('cybacktrader').rglob('*.pyd')))
    print(f"已编译: {pyd_count}/{pyx_count}")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[用户中断] 停止编译")

