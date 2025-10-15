#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
监控编译进度
"""

import time
from pathlib import Path


def check_status():
    """检查当前编译状态"""
    pyx_files = list(Path('cybacktrader').rglob('*.pyx'))
    pyd_files = list(Path('cybacktrader').rglob('*.pyd'))
    
    total = len(pyx_files)
    compiled = len(pyd_files)
    rate = (compiled / total * 100) if total > 0 else 0
    
    return total, compiled, rate


def main():
    print("监控编译进度（每10秒刷新一次）...")
    print("按 Ctrl+C 停止")
    print()
    
    prev_count = 0
    
    try:
        while True:
            total, compiled, rate = check_status()
            
            if compiled != prev_count:
                print(f"[{time.strftime('%H:%M:%S')}] 已编译: {compiled}/{total} ({rate:.1f}%) [+{compiled - prev_count}]")
                prev_count = compiled
            
            if compiled >= total:
                print("\n[完成] 所有模块编译完成！")
                break
            
            time.sleep(10)
    
    except KeyboardInterrupt:
        print(f"\n[停止] 当前进度: {compiled}/{total} ({rate:.1f}%)")


if __name__ == '__main__':
    main()


