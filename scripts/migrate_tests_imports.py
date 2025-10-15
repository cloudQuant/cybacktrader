#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


def replace_in_file(filepath, replacements):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    for src, dst in replacements:
        content = content.replace(src, dst)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    if len(sys.argv) < 2:
        tests_root = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tests')
    else:
        tests_root = sys.argv[1]

    # Conservative textual replacements scoped to tests only
    replacements = [
        ('import backtrader as bt', 'import cybacktrader as bt'),
        ('from backtrader import ', 'from cybacktrader import '),
        ('import backtrader.indicators as ', 'import cybacktrader.indicators as '),
        ('import backtrader.analyzers as ', 'import cybacktrader.analyzers as '),
        ('import backtrader.observers as ', 'import cybacktrader.observers as '),
        ('import backtrader.signals as ', 'import cybacktrader.signals as '),
        ('import backtrader.sizers as ', 'import cybacktrader.sizers as '),
        ('import backtrader.feeds as ', 'import cybacktrader.feeds as '),
        ('import backtrader.plot as ', 'import cybacktrader.plot as '),
        ('import backtrader.utils', 'import cybacktrader.utils'),
        ('from backtrader.', 'from cybacktrader.'),
        (' import backtrader', ' import cybacktrader'),
        ('\nimport backtrader\n', '\nimport cybacktrader\n'),
    ]

    changed = 0
    for root, _, files in os.walk(tests_root):
        for name in files:
            if not name.endswith('.py'):
                continue
            fp = os.path.join(root, name)
            if replace_in_file(fp, replacements):
                changed += 1

    print(f"migrated files: {changed}")


if __name__ == '__main__':
    main()


