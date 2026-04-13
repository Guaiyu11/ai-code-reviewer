#!/usr/bin/env python3
"""
Sort Lines - Sort, dedupe, shuffle lines in text files.
Usage: python sort-lines.py <file> [--reverse] [--unique] [--shuffle] [--numeric] [--random-seed N]
"""

import sys
import os
import random

def sort_file(filepath, reverse=False, unique=False, shuffle=False, numeric=False):
    """Sort lines in a file."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.read().splitlines()
    
    if shuffle:
        random.shuffle(lines)
    else:
        if numeric:
            try:
                lines.sort(key=lambda x: float(x.strip()) if x.strip() else 0, reverse=reverse)
            except:
                lines.sort(reverse=reverse)
        else:
            lines.sort(reverse=reverse)
    
    if unique:
        seen = set()
        new_lines = []
        for line in lines:
            if line not in seen:
                seen.add(line)
                new_lines.append(line)
        lines = new_lines
    
    return lines

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python sort-lines.py <file> [--reverse] [--unique] [--shuffle] [--numeric]")
        print("\nExamples:")
        print("  python sort-lines.py words.txt --unique")
        print("  python sort-lines.py nums.txt --numeric --reverse")
        print("  python sort-lines.py data.txt --shuffle")
        sys.exit(1)
    
    filepath = sys.argv[1]
    reverse = '--reverse' in sys.argv
    unique = '--unique' in sys.argv
    shuffle = '--shuffle' in sys.argv
    numeric = '--numeric' in sys.argv
    
    if '--random-seed' in sys.argv:
        idx = sys.argv.index('--random-seed')
        random.seed(int(sys.argv[idx + 1]))
    
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    
    lines = sort_file(filepath, reverse, unique, shuffle, numeric)
    
    mode = []
    if reverse: mode.append('reverse')
    if unique: mode.append('unique')
    if shuffle: mode.append('shuffle')
    if numeric: mode.append('numeric')
    
    print(f"=== Sorted: {filepath} ===")
    print(f"Mode: {', '.join(mode) if mode else 'default'}")
    print(f"Lines: {len(lines)}\n")
    print('\n'.join(lines))
