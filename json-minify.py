#!/usr/bin/env python3
"""
JSON Minifier - Minify or prettify JSON.
Usage: python json-minify.py <file> [--minify] [--pretty]
"""

import sys
import os
import json

def minify_json(content):
    """Minify JSON by removing whitespace."""
    data = json.loads(content)
    return json.dumps(data, separators=(',', ':'))

def prettify_json(content, indent=2):
    """Prettify JSON with indentation."""
    data = json.loads(content)
    return json.dumps(data, indent=indent)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python json-minify.py <file> [--minify] [--pretty]")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    try:
        json.loads(content)  # Validate
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
        sys.exit(1)
    
    if '--minify' in sys.argv:
        print(minify_json(content))
    elif '--pretty' in sys.argv:
        print(prettify_json(content))
    else:
        # Show stats
        orig_size = len(content)
        minified = minify_json(content)
        mini_size = len(minified)
        print(f"Original: {orig_size} bytes")
        print(f"Minified: {mini_size} bytes")
        print(f"Savings:  {orig_size - mini_size} bytes ({100*(orig_size-mini_size)/orig_size:.1f}%)")
        print()
        print("=== Minified ===")
        print(minified)
