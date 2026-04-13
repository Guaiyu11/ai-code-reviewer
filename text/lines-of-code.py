#!/usr/bin/env python3
"""
Lines of Code - Count lines of code in project.
Usage: python lines-of-code.py <directory> [--ext py|js|all]
"""

import sys
import os

EXTENSIONS = {
    'py': ['.py'],
    'js': ['.js', '.jsx'],
    'ts': ['.ts', '.tsx'],
    'java': ['.java'],
    'cpp': ['.cpp', '.cc', '.cxx', '.h', '.hpp'],
    'go': ['.go'],
    'rs': ['.rs'],
    'rb': ['.rb'],
    'php': ['.php'],
    'c': ['.c', '.h'],
}

def count_lines(filepath):
    """Count non-empty, non-comment lines."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    code_lines = 0
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith('#') and not stripped.startswith('//'):
            code_lines += 1
    return code_lines

def count_dir(path, extensions):
    """Count lines in directory."""
    total = 0
    files = 0
    results = {}
    
    for root, dirs, filenames in os.walk(path):
        # Skip hidden and common non-source dirs
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv', 'build', 'dist']]
        
        for f in filenames:
            if f.startswith('.'):
                continue
            ext = os.path.splitext(f)[1]
            if ext in extensions:
                filepath = os.path.join(root, f)
                try:
                    lines = count_lines(filepath)
                    total += lines
                    files += 1
                    results[filepath] = lines
                except:
                    pass
    
    return total, files, results

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python lines-of-code.py <directory> [--ext py|js|ts|java|cpp|go|rs|all]")
        sys.exit(1)
    
    path = sys.argv[1]
    ext = 'all'
    
    for i, arg in enumerate(sys.argv):
        if arg == '--ext' and i + 1 < len(sys.argv):
            ext = sys.argv[i + 1].lower()
    
    if ext == 'all':
        extensions = set()
        for exts in EXTENSIONS.values():
            extensions.update(exts)
    elif ext in EXTENSIONS:
        extensions = set(EXTENSIONS[ext])
    else:
        extensions = {f'.{ext}'}
    
    total, files, results = count_dir(path, extensions)
    
    print(f"=== Lines of Code: {path} ===\n")
    print(f"Total: {total:,} lines across {files} files\n")
    
    # Top files
    if results:
        print("Top files:")
        for filepath, lines in sorted(results.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {lines:6,}  {os.path.relpath(filepath, path)}")
