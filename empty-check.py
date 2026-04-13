#!/usr/bin/env python3
"""
Empty Check - Check if files or directories are empty.
Usage: python empty-check.py <path> [--delete]
"""

import sys
import os

def is_empty(path):
    """Check if file or directory is empty."""
    if os.path.isfile(path):
        return os.path.getsize(path) == 0
    elif os.path.isdir(path):
        return len(os.listdir(path)) == 0
    return None

def check_dir(path):
    """Check directory for empty items."""
    results = []
    for root, dirs, files in os.walk(path):
        for d in dirs:
            full = os.path.join(root, d)
            if is_empty(full):
                results.append(('DIR', full))
        for f in files:
            full = os.path.join(root, f)
            if is_empty(full):
                results.append(('FILE', full))
    return results

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python empty-check.py <path> [--delete]")
        sys.exit(1)
    
    path = sys.argv[1]
    delete = '--delete' in sys.argv
    
    if os.path.isfile(path):
        empty = is_empty(path)
        print(f"{path}: {'EMPTY' if empty else 'NOT EMPTY'} ({os.path.getsize(path)} bytes)")
    elif os.path.isdir(path):
        results = check_dir(path)
        if not results:
            print(f"No empty items in {path}")
        else:
            print(f"Empty items in {path}:")
            for type_, full in results:
                print(f"  {type_}: {full}")
                if delete:
                    if type_ == 'DIR':
                        os.rmdir(full)
                    else:
                        os.remove(full)
                    print(f"    -> Deleted")
