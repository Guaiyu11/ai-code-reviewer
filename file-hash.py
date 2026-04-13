#!/usr/bin/env python3
"""
File Hasher - Calculate hashes of files with progress.
Usage: python file-hash.py <file> [--algorithm md5|sha1|sha256|sha512]
"""

import sys
import os
import hashlib

ALGOS = {
    'md5': hashlib.md5,
    'sha1': hashlib.sha1,
    'sha256': hashlib.sha256,
    'sha512': hashlib.sha512,
}

def hash_file(filepath, algo='sha256', show_progress=False):
    """Calculate file hash with optional progress."""
    h = ALGOS[algo]()
    size = os.path.getsize(filepath)
    read = 0
    
    with open(filepath, 'rb') as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            h.update(chunk)
            read += len(chunk)
            if show_progress and size > 0:
                pct = read / size * 100
                print(f"\r{pct:.1f}% ({read:,}/{size:,} bytes)", end='', flush=True)
    
    if show_progress:
        print()
    
    return h.hexdigest()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python file-hash.py <file> [--algo md5|sha1|sha256|sha512]")
        print("\nAlgorithms:", ', '.join(ALGOS.keys()))
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    
    algo = 'sha256'
    for i, arg in enumerate(sys.argv):
        if arg == '--algo' and i + 1 < len(sys.argv):
            algo = sys.argv[i + 1].lower()
    
    if algo not in ALGOS:
        print(f"Unknown algorithm: {algo}")
        sys.exit(1)
    
    size_mb = os.path.getsize(filepath) / 1024 / 1024
    show_progress = size_mb > 10
    
    print(f"Calculating {algo.upper()} for {filepath} ({size_mb:.1f} MB)...")
    
    result = hash_file(filepath, algo, show_progress)
    print(f"\n{algo.upper()}: {result}")
    
    # Also show other hashes
    if algo != 'md5':
        print(f"MD5:    {hash_file(filepath, 'md5')}")
    if algo != 'sha1':
        print(f"SHA1:   {hash_file(filepath, 'sha1')}")
