#!/usr/bin/env python3
"""
Trim - Trim whitespace from files or text.
Usage: python trim.py <file> [--inplace] [--leading] [--trailing]
"""

import sys
import os

def trim_file(filepath, inplace=False, leading=True, trailing=True):
    """Trim whitespace from file."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        if leading and trailing:
            new_lines.append(line.strip() + '\n')
        elif leading:
            new_lines.append(line.lstrip())
        elif trailing:
            new_lines.append(line.rstrip() + '\n')
        else:
            new_lines.append(line)
    
    content = ''.join(new_lines)
    
    if inplace:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Trimmed: {filepath}")
    else:
        print(content)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python trim.py <file> [--inplace] [--leading] [--trailing]")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    
    leading = '--trailing' not in sys.argv
    trailing = '--leading' not in sys.argv
    inplace = '--inplace' in sys.argv
    
    trim_file(filepath, inplace, leading, trailing)
