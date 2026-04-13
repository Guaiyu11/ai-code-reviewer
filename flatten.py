#!/usr/bin/env python3
"""
Flatten - Flatten nested lists/dicts to CSV.
Usage: python flatten.py <json-file>
"""

import sys
import os
import json

def flatten(obj, prefix=''):
    """Flatten nested dict/list to key=value pairs."""
    rows = []
    
    if isinstance(obj, dict):
        for k, v in obj.items():
            new_key = f"{prefix}.{k}" if prefix else k
            if isinstance(v, (dict, list)):
                rows.extend(flatten(v, new_key))
            else:
                rows.append((new_key, str(v)))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            new_key = f"{prefix}[{i}]"
            if isinstance(item, (dict, list)):
                rows.extend(flatten(item, new_key))
            else:
                rows.append((new_key, str(item)))
    
    return rows

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python flatten.py <json-file>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    rows = flatten(data)
    
    for key, value in rows:
        print(f"{key}={value}")
