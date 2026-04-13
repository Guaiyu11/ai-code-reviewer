#!/usr/bin/env python3
"""
Unindent - Remove indentation from text.
Usage: python unindent.py <file|text>
"""

import sys
import os
import re

def unindent_text(text):
    """Remove common leading indentation."""
    lines = text.split('\n')
    
    # Find minimum indentation (excluding empty lines)
    min_indent = float('inf')
    for line in lines:
        if line.strip():
            match = re.match(r'^(\s*)', line)
            if match:
                indent = len(match.group(1))
                min_indent = min(min_indent, indent)
    
    if min_indent == float('inf'):
        min_indent = 0
    
    # Remove indentation
    result = []
    for line in lines:
        if line.strip():
            result.append(line[min_indent:])
        else:
            result.append('')
    
    return '\n'.join(result)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python unindent.py <file|text>")
        sys.exit(1)
    
    target = sys.argv[1]
    
    if os.path.exists(target):
        with open(target, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        text = target
    
    print(unindent_text(text))
