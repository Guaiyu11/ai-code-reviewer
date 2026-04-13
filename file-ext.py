#!/usr/bin/env python3
"""
File Extension - Show or change file extensions.
Usage: python file-ext.py <file> [--set EXT]
"""

import sys
import os

def get_ext(filepath):
    """Get file extension."""
    _, ext = os.path.splitext(filepath)
    return ext

def set_ext(filepath, new_ext):
    """Change file extension."""
    base, _ = os.path.splitext(filepath)
    if not new_ext.startswith('.'):
        new_ext = '.' + new_ext
    new_path = base + new_ext
    os.rename(filepath, new_path)
    return new_path

def show_info(filepath):
    """Show extension info."""
    base, ext = os.path.splitext(filepath)
    print(f"File:      {filepath}")
    print(f"Base:      {base}")
    print(f"Extension: {ext or '(none)'}")
    print(f"Name only: {os.path.basename(base)}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python file-ext.py <file> [--set EXT]")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    if '--set' in sys.argv:
        idx = sys.argv.index('--set')
        new_ext = sys.argv[idx + 1]
        new_path = set_ext(filepath, new_ext)
        print(f"Renamed: {new_path}")
    else:
        show_info(filepath)
