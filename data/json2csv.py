#!/usr/bin/env python3
"""
JSON to CSV - Convert JSON to CSV.
Usage: python json2csv.py <file.json> [--flatten]
"""

import sys
import os
import json
import csv

def flatten_json(obj, prefix=''):
    """Flatten nested JSON."""
    items = {}
    
    if isinstance(obj, dict):
        for k, v in obj.items():
            new_key = f"{prefix}.{k}" if prefix else k
            if isinstance(v, (dict, list)):
                items.update(flatten_json(v, new_key))
            else:
                items[new_key] = v
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            items.update(flatten_json(item, f"{prefix}[{i}]"))
    else:
        items[prefix] = obj
    
    return items

def json_to_csv(filepath, flatten=False):
    """Convert JSON to CSV."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if not isinstance(data, list):
        data = [data]
    
    if flatten:
        rows = [flatten_json(item) for item in data]
    else:
        rows = data
    
    if not rows:
        return
    
    # Get all unique keys
    all_keys = set()
    for row in rows:
        all_keys.update(row.keys())
    
    keys = sorted(all_keys)
    writer = csv.DictWriter(sys.stdout, fieldnames=keys)
    writer.writeheader()
    writer.writerows(rows)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python json2csv.py <file.json> [--flatten]")
        sys.exit(1)
    
    filepath = sys.argv[1]
    flatten = '--flatten' in sys.argv
    
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    
    json_to_csv(filepath, flatten)
