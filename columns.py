#!/usr/bin/env python3
"""
Columns - Display text in columns.
Usage: python columns.py <items...> [--cols N] [--sep SEP]
"""

import sys

def to_columns(items, cols=3, sep='  '):
    """Display items in columns."""
    rows = (len(items) + cols - 1) // cols
    col_width = max(len(str(i)) for i in items) + 2
    
    lines = []
    for r in range(rows):
        row_items = []
        for c in range(cols):
            idx = r + c * rows
            if idx < len(items):
                item = str(items[idx]).ljust(col_width)
                row_items.append(item)
        lines.append(sep.join(row_items))
    
    return '\n'.join(lines)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python columns.py <items...> [--cols N] [--sep SEP]")
        sys.exit(1)
    
    cols = 3
    sep = '  '
    
    args = []
    for i, arg in enumerate(sys.argv[1:], 1):
        if arg == '--cols' and i < len(sys.argv) - 1:
            cols = int(sys.argv[i + 1])
        elif arg == '--sep' and i < len(sys.argv) - 1:
            sep = sys.argv[i + 1]
        elif not arg.startswith('--'):
            args.append(arg)
    
    print(to_columns(args, cols, sep))
