#!/usr/bin/env python3
"""
Indent - Add indentation to text.
Usage: python indent.py <file|text> [--spaces N] [--tabs]
"""

import sys
import os

def indent_text(text, spaces=4, use_tabs=False):
    """Add indentation."""
    indent = '\t' if use_tabs else ' ' * spaces
    
    lines = text.split('\n')
    return '\n'.join(indent + line for line in lines)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python indent.py <file|text> [--spaces N] [--tabs]")
        sys.exit(1)
    
    target = sys.argv[1]
    spaces = 4
    use_tabs = '--tabs' in sys.argv
    
    for i, arg in enumerate(sys.argv):
        if arg == '--spaces' and i + 1 < len(sys.argv):
            spaces = int(sys.argv[i + 1])
    
    if os.path.exists(target):
        with open(target, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        text = target
    
    print(indent_text(text, spaces, use_tabs))
