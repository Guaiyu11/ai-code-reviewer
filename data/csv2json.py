#!/usr/bin/env python3
"""
CSV to JSON - Convert CSV to JSON.
Usage: python csv2json.py <file.csv> [--key KEY]
"""

import sys
import os
import csv
import json

def csv_to_json(filepath, key_field=None):
    """Convert CSV to JSON."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    if key_field:
        result = {}
        for row in rows:
            k = row.get(key_field, 'unknown')
            result[k] = row
    else:
        result = rows
    
    return json.dumps(result, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python csv2json.py <file.csv> [--key KEY]")
        sys.exit(1)
    
    filepath = sys.argv[1]
    key_field = None
    
    for i, arg in enumerate(sys.argv):
        if arg == '--key' and i + 1 < len(sys.argv):
            key_field = sys.argv[i + 1]
    
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    
    print(csv_to_json(filepath, key_field))
