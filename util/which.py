#!/usr/bin/env python3
"""
Which - Find executable in PATH.
Usage: python which.py <command>
"""

import sys
import os

def which(cmd):
    """Find command in PATH."""
    # Handle with/without extension
    for path in os.environ.get('PATH', '').split(os.pathsep):
        for name in [cmd, f"{cmd}.exe", f"{cmd}.bat", f"{cmd}.cmd", f"{cmd}.ps1"]:
            full = os.path.join(path, name)
            if os.path.isfile(full) and os.access(full, os.X_OK):
                return full
    return None

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python which.py <command>")
        sys.exit(1)
    
    cmd = sys.argv[1]
    result = which(cmd)
    
    if result:
        print(result)
    else:
        print(f"Command not found: {cmd}")
        sys.exit(1)
