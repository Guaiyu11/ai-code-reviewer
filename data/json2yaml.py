#!/usr/bin/env python3
"""
JSON ↔ YAML Converter - Convert between JSON and YAML.
Usage: python json2yaml.py <file> [--to-json | --to-yaml] [--pretty]
"""

import sys
import os
import json

try:
    import yaml
    HAS_YAML = True
except:
    HAS_YAML = False

def json_to_yaml(data, indent=2):
    """Convert JSON to YAML."""
    if not HAS_YAML:
        return "YAML library not installed (pip install pyyaml)"
    
    return yaml.dump(data, indent=indent, default_flow_style=False, sort_keys=False)

def yaml_to_json(content):
    """Convert YAML to JSON."""
    if not HAS_YAML:
        return "YAML library not installed (pip install pyyaml)"
    
    data = yaml.safe_load(content)
    return json.dumps(data, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python json2yaml.py <file|json> [--to-json | --to-yaml] [--pretty]")
        sys.exit(1)
    
    target = sys.argv[1]
    
    if os.path.exists(target):
        with open(target, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        content = target
    
    mode = None
    if '--to-json' in sys.argv:
        mode = 'to_json'
    elif '--to-yaml' in sys.argv:
        mode = 'to_yaml'
    else:
        # Auto-detect
        if content.strip().startswith('{') or content.strip().startswith('['):
            mode = 'to_yaml'
        else:
            mode = 'to_json'
    
    print(f"Mode: {mode}\n")
    
    if mode == 'to_yaml':
        try:
            data = json.loads(content)
            print(json_to_yaml(data))
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}")
            sys.exit(1)
    else:
        print(yaml_to_json(content))
