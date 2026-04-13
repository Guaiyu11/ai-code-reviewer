#!/usr/bin/env python3
"""
Wrap - Wrap text to specified width.
Usage: python wrap.py <width> [--file FILE]
"""

import sys

def wrap_text(text, width=80):
    """Wrap text to specified width."""
    words = text.split()
    lines = []
    current = ''
    
    for word in words:
        if len(current) + len(word) + 1 <= width:
            current += (' ' if current else '') + word
        else:
            if current:
                lines.append(current)
            current = word
    
    if current:
        lines.append(current)
    
    return '\n'.join(lines)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python wrap.py <width> [--file FILE]")
        sys.exit(1)
    
    width = int(sys.argv[1])
    
    if '--file' in sys.argv:
        idx = sys.argv.index('--file')
        filepath = sys.argv[idx + 1]
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        text = sys.stdin.read()
    
    print(wrap_text(text, width))
