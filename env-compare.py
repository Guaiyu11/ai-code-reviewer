#!/usr/bin/env python3
"""
ENV Compare - Compare two .env files and show differences.
Usage: python env-compare.py <file1.env> <file2.env>
"""

import sys
import os

def parse_env(content):
    """Parse .env file."""
    env = {}
    for line in content.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if '=' in line:
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env

def compare_envs(env1, env2):
    """Compare two env dicts."""
    added = set(env2.keys()) - set(env1.keys())
    removed = set(env1.keys()) - set(env2.keys())
    changed = []
    same = []
    
    for k in set(env1.keys()) & set(env2.keys()):
        if env1[k] != env2[k]:
            changed.append((k, env1[k], env2[k]))
        else:
            same.append(k)
    
    return added, removed, changed, same

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python env-compare.py <file1.env> <file2.env>")
        sys.exit(1)
    
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    
    for f in [file1, file2]:
        if not os.path.exists(f):
            print(f"Error: File not found: {f}")
            sys.exit(1)
    
    with open(file1, 'r') as f:
        env1 = parse_env(f.read())
    
    with open(file2, 'r') as f:
        env2 = parse_env(f.read())
    
    added, removed, changed, same = compare_envs(env1, env2)
    
    print(f"=== ENV Compare: {file1} vs {file2} ===\n")
    
    if added:
        print(f"➕ Added in {file2} ({len(added)}):")
        for k in sorted(added):
            print(f"  {k} = {env2[k]}")
        print()
    
    if removed:
        print(f"➖ Removed from {file2} ({len(removed)}):")
        for k in sorted(removed):
            print(f"  {k} = {env1[k]}")
        print()
    
    if changed:
        print(f"🔄 Changed ({len(changed)}):")
        for k, v1, v2 in sorted(changed, key=lambda x: x[0]):
            print(f"  {k}:")
            print(f"    - {v1}")
            print(f"    + {v2}")
        print()
    
    print(f"Same: {len(same)} keys")
