#!/usr/bin/env python3
"""
Join Files - Join split files back together.
Usage: python join-files.py <pattern> <output> [--numeric]
Example: python join-files.py "chunk_*" output.txt
"""

import sys
import os
import glob

def join_files(pattern, output, numeric=False):
    """Join files matching pattern."""
    files = glob.glob(pattern)
    
    if not files:
        print(f"No files matching: {pattern}")
        return
    
    if numeric:
        files.sort(key=lambda x: int(''.join(filter(str.isdigit, x)) or 0))
    else:
        files.sort()
    
    with open(output, 'wb') as out:
        for f in files:
            with open(f, 'rb') as inp:
                out.write(inp.read())
            print(f"Joined: {f}")
    
    print(f"Output: {output} ({len(files)} files)")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python join-files.py <pattern> <output> [--numeric]")
        sys.exit(1)
    
    pattern = sys.argv[1]
    output = sys.argv[2]
    numeric = '--numeric' in sys.argv
    
    join_files(pattern, output, numeric)
