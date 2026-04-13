#!/usr/bin/env python3
"""
String Replace - Find and replace strings in files.
Usage: python str-replace.py <file> <find> <replace> [--preview]
"""

import sys
import os
import re

def replace_in_file(filepath, find, replace, regex=False, preview=False):
    """Replace string in file."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    if regex:
        new_content = re.sub(find, replace, content)
    else:
        new_content = content.replace(find, replace)
    
    count = content.count(find) if not regex else len(re.findall(find, content))
    
    if preview or count == 0:
        print(f"Found {count} occurrence(s)")
        if preview:
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                if find in line:
                    print(f"  Line {i}: {line.rstrip()}")
    else:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Replaced {count} occurrence(s) in {filepath}")

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python str-replace.py <file> <find> <replace> [--regex] [--preview]")
        sys.exit(1)
    
    filepath = sys.argv[1]
    find = sys.argv[2]
    replace = sys.argv[3]
    regex = '--regex' in sys.argv
    preview = '--preview' in sys.argv
    
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    
    replace_in_file(filepath, find, replace, regex, preview)
