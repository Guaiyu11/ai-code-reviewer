#!/usr/bin/env python3
"""
Diff Tool - Compare two files or directories side by side.
Usage: python diff-tool.py <file1> <file2> [--unified] [--context N]
"""

import sys
import os
import difflib

def read_file(path):
    """Read file content."""
    if not os.path.exists(path):
        return None, f"File not found: {path}"
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read().splitlines(), None
    except Exception as e:
        return None, str(e)

def unified_diff(a_name, a_lines, b_name, b_lines, context=3):
    """Generate unified diff output."""
    return list(difflib.unified_diff(
        a_lines, b_lines,
        fromfile=a_name,
        tofile=b_name,
        n=context
    ))

def side_by_side(a_name, a_lines, b_name, b_lines):
    """Generate side-by-side comparison."""
    # Pad shorter list
    max_lines = max(len(a_lines), len(b_lines))
    a_lines.extend([''] * (max_lines - len(a_lines)))
    b_lines.extend([''] * (max_lines - len(b_lines)))
    
    width = 80
    half = width // 2 - 3
    
    lines = []
    lines.append(f"{'FILE A':^{half}}|{'FILE B':^{half}}")
    lines.append('-' * width)
    
    changes = 0
    for i, (a, b) in enumerate(zip(a_lines, b_lines), 1):
        if a != b:
            changes += 1
            marker = '*'
        else:
            marker = ' '
        
        a_display = (a[:half] + '..') if len(a) > half else a
        b_display = (b[:half] + '..') if len(b) > half else b
        lines.append(f"{marker} {a_display:<{half}}| {b_display:<{half}}")
    
    return lines, changes

def inline_diff(a_lines, b_lines):
    """Show diff with inline markers."""
    differ = difflib.Differ()
    diff = list(differ.compare(a_lines, b_lines))
    
    added = sum(1 for d in diff if d.startswith('+'))
    removed = sum(1 for d in diff if d.startswith('-'))
    
    return diff, added, removed

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python diff-tool.py <file1> <file2> [--unified] [--side] [--inline]")
        print("\nExamples:")
        print("  python diff-tool.py old.txt new.txt")
        print("  python diff-tool.py old.txt new.txt --unified")
        print("  python diff-tool.py old.txt new.txt --inline")
        sys.exit(1)
    
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    
    mode = 'side'
    for arg in sys.argv:
        if arg == '--unified':
            mode = 'unified'
        elif arg == '--side':
            mode = 'side'
        elif arg == '--inline':
            mode = 'inline'
    
    a_lines, err = read_file(file1)
    if err:
        print(f"Error reading {file1}: {err}")
        sys.exit(1)
    
    b_lines, err = read_file(file2)
    if err:
        print(f"Error reading {file2}: {err}")
        sys.exit(1)
    
    print(f"=== Diff: {file1} vs {file2} ===\n")
    
    if mode == 'side':
        lines, changes = side_by_side(file1, a_lines, file2, b_lines)
        print('\n'.join(lines))
        print(f"\n{changes} line(s) changed")
    
    elif mode == 'unified':
        diff = unified_diff(file1, a_lines, file2, b_lines)
        if diff:
            print('\n'.join(diff))
        else:
            print("Files are identical")
    
    elif mode == 'inline':
        diff, added, removed = inline_diff(a_lines, b_lines)
        print(f"Changes: +{added} -{removed}")
        print()
        for line in diff[:100]:
            if line.startswith('+'):
                print(f'\033[92m{line}\033[0m')
            elif line.startswith('-'):
                print(f'\033[91m{line}\033[0m')
            elif line.startswith('?'):
                print(f'\033[94m{line}\033[0m')
            else:
                print(line)
