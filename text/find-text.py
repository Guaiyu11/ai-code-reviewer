#!/usr/bin/env python3
"""
Find Text - Find text in files recursively.
Usage: python find-text.py <directory> <text> [--ext py|js|html]
"""

import sys
import os
import re

def find_text(path, text, extensions=None):
    """Find text in files."""
    results = []
    
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv', '.git']]
        
        for f in files:
            if f.startswith('.'):
                continue
            
            ext = os.path.splitext(f)[1].lower()
            if extensions and ext not in extensions:
                continue
            
            filepath = os.path.join(root, f)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                    for i, line in enumerate(file, 1):
                        if text.lower() in line.lower():
                            results.append((filepath, i, line.strip()))
            except:
                pass
    
    return results

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python find-text.py <directory> <text> [--ext py|js|html]")
        sys.exit(1)
    
    path = sys.argv[1]
    text = sys.argv[2]
    extensions = None
    
    for i, arg in enumerate(sys.argv):
        if arg == '--ext' and i + 1 < len(sys.argv):
            ext = sys.argv[i + 1].lower()
            if not ext.startswith('.'):
                ext = '.' + ext
            extensions = {ext}
    
    results = find_text(path, text, extensions)
    
    print(f"=== Search: '{text}' in {path} ===\n")
    print(f"Found: {len(results)} matches\n")
    
    for filepath, line_num, line in results[:50]:
        relpath = os.path.relpath(filepath, path)
        print(f"{relpath}:{line_num}: {line[:100]}")
