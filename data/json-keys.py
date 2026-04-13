#!/usr/bin/env python3
"""
JSON Keys - Extract all keys from JSON.
Usage: python json-keys.py <file.json>
"""

import sys
import os
import json

def extract_keys(obj, prefix=''):
    """Recursively extract all keys."""
    keys = []
    
    if isinstance(obj, dict):
        for key, value in obj.items():
            full_key = f"{prefix}.{key}" if prefix else key
            keys.append(full_key)
            keys.extend(extract_keys(value, full_key))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            keys.extend(extract_keys(item, f"{prefix}[{i}]"))
    
    return keys

def get_value(obj, path):
    """Get value by dot-path."""
    parts = path.replace('][', '.').replace('[', '.').replace(']', '').split('.')
    result = obj
    for part in parts:
        if part.isdigit():
            result = result[int(part)]
        else:
            result = result.get(part)
            if result is None:
                return None
    return result

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python json-keys.py <file.json> [--get PATH]")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    keys = extract_keys(data)
    
    print(f"=== JSON Keys: {os.path.basename(filepath)} ===\n")
    print(f"Total keys: {len(keys)}\n")
    
    for key in sorted(keys):
        print(key)
    
    if '--get' in sys.argv:
        idx = sys.argv.index('--get')
        path = sys.argv[idx + 1]
        value = get_value(data, path)
        print(f"\n{path} = {value}")
