#!/usr/bin/env python3
"""
Find Duplicates - Find duplicate files by hash or name.
Usage: python finddup.py <directory> [--hash] [--name] [--delete]
"""

import sys
import os
import hashlib

def find_by_name(directory):
    """Find files with same name."""
    name_map = {}
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.startswith('.'):
                continue
            if f not in name_map:
                name_map[f] = []
            name_map[f].append(os.path.join(root, f))
    
    return {k: v for k, v in name_map.items() if len(v) > 1}

def find_by_hash(directory):
    """Find files with same content hash."""
    hash_map = {}
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.startswith('.'):
                continue
            full = os.path.join(root, f)
            try:
                h = hashlib.sha256()
                with open(full, 'rb') as fh:
                    while chunk := fh.read(8192):
                        h.update(chunk)
                key = h.hexdigest()[:16]
                if key not in hash_map:
                    hash_map[key] = []
                hash_map[key].append(full)
            except:
                pass
    
    return {k: v for k, v in hash_map.items() if len(v) > 1}

def delete_files(paths):
    """Delete duplicate files (keeps first)."""
    deleted = 0
    for p in paths[1:]:
        try:
            os.remove(p)
            print(f"Deleted: {p}")
            deleted += 1
        except Exception as e:
            print(f"Error deleting {p}: {e}")
    return deleted

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python finddup.py <directory> [--hash] [--name] [--delete]")
        sys.exit(1)
    
    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"Error: Not a directory: {directory}")
        sys.exit(1)
    
    mode = 'hash' if '--hash' in sys.argv else 'name' if '--name' in sys.argv else 'hash'
    
    print(f"=== Finding duplicates by {mode} ===\n")
    
    if mode == 'hash':
        dups = find_by_hash(directory)
    else:
        dups = find_by_name(directory)
    
    if not dups:
        print("No duplicates found.")
    else:
        print(f"Found {len(dups)} duplicate groups:\n")
        total_dup = 0
        for key, paths in dups.items():
            print(f"[{key[:16]}...] {len(paths)} files:")
            for p in paths:
                print(f"  {p}")
            print()
            total_dup += len(paths) - 1
        
        print(f"Total: {total_dup} duplicate files")
        
        if '--delete' in sys.argv:
            print(f"\nDeleting duplicates (keeping first in each group)...")
            deleted = 0
            for paths in dups.values():
                deleted += delete_files(paths)
            print(f"Deleted {deleted} files.")
