#!/usr/bin/env python3
"""
File Tree - Display directory tree structure.
Usage: python filetree.py [path] [--depth N] [--exclude PATTERN]
"""

import sys
import os

def tree(path, prefix='', max_depth=None, current_depth=0, exclude=None):
    """Generate tree structure."""
    if max_depth is not None and current_depth > max_depth:
        return []
    
    lines = []
    
    try:
        entries = sorted(os.listdir(path), key=lambda x: (not os.path.isdir(os.path.join(path, x)), x))
    except PermissionError:
        return lines
    
    for i, entry in enumerate(entries):
        if exclude and exclude in entry:
            continue
        
        full = os.path.join(path, entry)
        is_last = i == len(entries) - 1
        
        connector = '└── ' if is_last else '├── '
        
        if prefix:
            display_prefix = prefix + connector
        else:
            display_prefix = ''
        
        lines.append(display_prefix + entry)
        
        if os.path.isdir(full):
            extension = '    ' if is_last else '│   '
            lines.extend(tree(full, prefix + extension, max_depth, current_depth + 1, exclude))
    
    return lines

if __name__ == '__main__':
    path = '.'
    max_depth = None
    exclude = None
    
    for i, arg in enumerate(sys.argv[1:], 1):
        if not arg.startswith('--'):
            path = arg
        elif arg == '--depth' and i < len(sys.argv) - 1:
            max_depth = int(sys.argv[i])
        elif arg == '--exclude' and i < len(sys.argv) - 1:
            exclude = sys.argv[i]
    
    if not os.path.exists(path):
        print(f"Error: Path not found: {path}")
        sys.exit(1)
    
    lines = tree(path, max_depth=max_depth, exclude=exclude)
    print(path)
    for line in lines:
        print(line)
    
    print(f"\n{len(lines)} items")
