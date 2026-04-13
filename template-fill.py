#!/usr/bin/env python3
"""
Template Filler - Fill template variables from JSON/ENV data.
Usage: python template-fill.py <template.txt> <data.json|data.env>
Variables: {{name}}, {{value}}, ${ENV_VAR}
"""

import sys
import os
import re
import json

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

def fill_template(template, data):
    """Fill template with data."""
    result = template
    
    # {{key}} style
    for key, value in data.items():
        result = result.replace('{{' + key + '}}', str(value))
        result = result.replace('{{ ' + key + ' }}', str(value))
    
    # ${KEY} style
    for key, value in data.items():
        result = result.replace('${' + key + '}', str(value))
        result = result.replace('${' + key.upper() + '}', str(value))
    
    return result

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python template-fill.py <template.txt> <data.json|data.env>")
        print("\nExample template.txt:")
        print("  Hello {{name}}!")
        print("  Your email is ${EMAIL}")
        print("\nExample data.json:")
        print('  {"name": "Alice", "email": "alice@example.com"}')
        sys.exit(1)
    
    template_path = sys.argv[1]
    data_path = sys.argv[2]
    
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    
    if data_path.endswith('.json'):
        with open(data_path, 'r') as f:
            data = json.load(f)
    else:
        with open(data_path, 'r') as f:
            data = parse_env(f.read())
    
    result = fill_template(template, data)
    print(result)
