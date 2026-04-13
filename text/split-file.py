#!/usr/bin/env python3
"""
Split File - Split file into chunks.
Usage: python split-file.py <file> [--lines N] [--bytes N] [--prefix PREFIX]
"""

import sys
import os

def split_by_lines(filepath, lines_per_chunk=1000, prefix=None):
    """Split file into chunks by line count."""
    if prefix is None:
        base, ext = os.path.splitext(filepath)
        prefix = f"{base}_chunk"
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        chunk_num = 0
        while True:
            lines = [f.readline() for _ in range(lines_per_chunk)]
            lines = [l for l in lines if l]
            if not lines:
                break
            chunk_path = f"{prefix}_{chunk_num:03d}{os.path.splitext(filepath)[1]}"
            with open(chunk_path, 'w', encoding='utf-8') as chunk_file:
                chunk_file.writelines(lines)
            print(f"Created: {chunk_path}")
            chunk_num += 1

def split_by_bytes(filepath, bytes_per_chunk=1024*1024, prefix=None):
    """Split file into chunks by byte size."""
    if prefix is None:
        base, ext = os.path.splitext(filepath)
        prefix = f"{base}_chunk"
    
    with open(filepath, 'rb') as f:
        chunk_num = 0
        while True:
            data = f.read(bytes_per_chunk)
            if not data:
                break
            chunk_path = f"{prefix}_{chunk_num:03d}"
            with open(chunk_path, 'wb') as chunk_file:
                chunk_file.write(data)
            print(f"Created: {chunk_path} ({len(data)} bytes)")
            chunk_num += 1

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python split-file.py <file> [--lines N] [--bytes N] [--prefix PREFIX]")
        sys.exit(1)
    
    filepath = sys.argv[1]
    lines = 1000
    bytes_per_chunk = None
    prefix = None
    
    for i, arg in enumerate(sys.argv):
        if arg == '--lines' and i + 1 < len(sys.argv):
            lines = int(sys.argv[i + 1])
        elif arg == '--bytes' and i + 1 < len(sys.argv):
            bytes_per_chunk = int(sys.argv[i + 1])
        elif arg == '--prefix' and i + 1 < len(sys.argv):
            prefix = sys.argv[i + 1]
    
    if bytes_per_chunk:
        split_by_bytes(filepath, bytes_per_chunk, prefix)
    else:
        split_by_lines(filepath, lines, prefix)
