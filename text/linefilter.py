#!/usr/bin/env python3
"""
Line Filter - Filter lines by pattern, grep-like with extra features.
Usage: python linefilter.py <file> <pattern> [--invert] [--count] [--before N] [--after N]
"""

import sys
import os
import re

def filter_lines(filepath, pattern, invert=False, before=0, after=0):
    """Filter lines matching pattern."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    matches = []
    match_indices = []
    
    regex = re.compile(pattern)
    
    for i, line in enumerate(lines):
        found = bool(regex.search(line))
        if invert:
            found = not found
        if found:
            match_indices.append(i)
    
    for i in match_indices:
        start = max(0, i - before)
        end = min(len(lines), i + after + 1)
        matches.append((i + 1, lines[start:end]))  # line num, context lines
    
    return matches

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python linefilter.py <file> <pattern> [--invert] [--count] [--before N] [--after N]")
        sys.exit(1)
    
    filepath = sys.argv[1]
    pattern = sys.argv[2]
    
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    
    invert = '--invert' in sys.argv
    before = 0
    after = 0
    
    for i, arg in enumerate(sys.argv):
        if arg == '--before' and i + 1 < len(sys.argv):
            before = int(sys.argv[i + 1])
        elif arg == '--after' and i + 1 < len(sys.argv):
            after = int(sys.argv[i + 1])
    
    if '--count' in sys.argv:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        regex = re.compile(pattern)
        count = sum(1 for line in content.split('\n') if bool(regex.search(line)))
        print(f"{count} matches")
        sys.exit(0)
    
    matches = filter_lines(filepath, pattern, invert, before, after)
    
    print(f"=== {len(matches)} matches ===\n")
    
    shown = set()
    for linenum, context in matches:
        for i, line in enumerate(context):
            global_i = linenum - before + i
            if global_i not in shown:
                marker = '>' if global_i == linenum else ' '
                print(f"{marker} {global_i:5d}: {line.rstrip()}")
                shown.add(global_i)
    
    if not matches:
        sys.exit(1)
