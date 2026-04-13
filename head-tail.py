#!/usr/bin/env python3
"""
Head/Tail - Show first or last N lines of file.
Usage: python head-tail.py <file> [--head N] [--tail N]
"""

import sys
import os

def head(filepath, n=10):
    """Show first n lines."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for i, line in enumerate(f):
            if i >= n:
                break
            print(line, end='')

def tail(filepath, n=10):
    """Show last n lines."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    for line in lines[-n:]:
        print(line, end='')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python head-tail.py <file> [--head N] [--tail N]")
        sys.exit(1)
    
    filepath = sys.argv[1]
    n = 10
    
    for i, arg in enumerate(sys.argv):
        if arg == '--head' and i + 1 < len(sys.argv):
            n = int(sys.argv[i + 1])
            head(filepath, n)
            return
        elif arg == '--tail' and i + 1 < len(sys.argv):
            n = int(sys.argv[i + 1])
            tail(filepath, n)
            return
    
    # Default: head
    head(filepath, n)
