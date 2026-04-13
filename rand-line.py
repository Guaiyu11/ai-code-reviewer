#!/usr/bin/env python3
"""
Rand Line - Pick random line from file.
Usage: python rand-line.py <file>
"""

import sys
import os
import random

def pick_random_line(filepath):
    """Pick random line from file."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = [l.rstrip() for l in f if l.strip()]
    
    if not lines:
        return None
    
    return random.choice(lines)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python rand-line.py <file>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    
    line = pick_random_line(filepath)
    if line:
        print(line)
