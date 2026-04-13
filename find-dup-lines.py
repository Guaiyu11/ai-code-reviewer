#!/usr/bin/env python3
"""
Find Duplicate Lines - Find duplicate lines in files.
Usage: python find-dup-lines.py <file>
"""

import sys
import os
from collections import Counter

def find_dup_lines(filepath):
    """Find duplicate lines in file."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    # Count non-empty lines
    non_empty = [l.strip() for l in lines if l.strip()]
    counter = Counter(non_empty)
    
    dups = [(count, line) for line, count in counter.items() if count > 1]
    dups.sort(reverse=True)
    
    return dups

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python find-dup-lines.py <file>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    
    dups = find_dup_lines(filepath)
    
    print(f"=== Duplicate Lines: {filepath} ===\n")
    
    if not dups:
        print("No duplicate lines found")
    else:
        print(f"Found {len(dups)} duplicate lines:\n")
        for count, line in dups[:30]:
            print(f"[{count}x] {line[:100]}")
