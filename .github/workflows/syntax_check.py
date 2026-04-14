#!/usr/bin/env python3
"""GitHub Actions: Syntax check all Python files."""
import sys
from pathlib import Path

errors = []
total = 0
for f in Path('.').rglob('*.py'):
    if '.git' in str(f):
        continue
    total += 1
    try:
        with open(f, encoding='utf-8', errors='ignore') as fp:
            compile(fp.read(), str(f), 'exec')
    except SyntaxError as e:
        errors.append(f'{f}:{e.lineno}: {e.msg}')

if errors:
    for e in errors:
        print(e)
    print(f'\n{len(errors)} syntax error(s) found')
    sys.exit(1)
else:
    print(f'Syntax OK: {total} files checked')
