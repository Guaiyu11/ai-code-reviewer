#!/usr/bin/env python3
"""
ENV to JSON Converter - Convert .env files to JSON and vice versa.
Usage: python env-to-json.py <file.env> [--to-json] [--to-env] [--validate]
"""

import sys
import os
import json
import re

def parse_env(content):
    """Parse .env content into a dictionary."""
    env = {}
    
    for line_num, line in enumerate(content.split('\n'), 1):
        line = line.strip()
        
        # Skip empty lines and comments
        if not line or line.startswith('#'):
            continue
        
        # Handle KEY=value and KEY="value" and KEY='value'
        match = re.match(r'^([A-Za-z_][A-Za-z0-9_]*)=(.*)$', line)
        if not match:
            print(f"Warning: Line {line_num}: Invalid format - {line[:50]}")
            continue
        
        key = match.group(1)
        value = match.group(2).strip()
        
        # Remove quotes
        if (value.startswith('"') and value.endswith('"')) or \
           (value.startswith("'") and value.endswith("'")):
            value = value[1:-1]
        
        # Handle inline comments (only outside quotes)
        if '#' in value and not value.startswith('"'):
            value = value.split('#')[0].strip()
        
        env[key] = value
    
    return env


def env_to_json(env_dict):
    """Convert env dict to JSON."""
    return json.dumps(env_dict, indent=2, ensure_ascii=False)


def json_to_env(data):
    """Convert JSON to .env format."""
    lines = []
    for key, value in data.items():
        # Quote values with spaces or special chars
        if ' ' in str(value) or '\n' in str(value) or '#' in str(value):
            value = f'"{value}"'
        lines.append(f"{key}={value}")
    return '\n'.join(lines)


def validate_env(env_dict):
    """Validate .env file and check for common issues."""
    issues = []
    
    # Check for empty values
    for key, value in env_dict.items():
        if value == '':
            issues.append(f"Empty value: {key}")
    
    # Common variable name checks
    common_vars = ['DATABASE_URL', 'SECRET_KEY', 'API_KEY', 'PORT', 'HOST', 'DEBUG']
    for var in common_vars:
        if var not in env_dict:
            issues.append(f"Missing recommended variable: {var}")
    
    # Check for debug=true in production-like files
    if any(x in os.path.basename(getattr(sys, 'argv', ['.env'])[1] or '').lower() 
            for x in ['prod', 'production', 'live']):
        if env_dict.get('DEBUG', '').lower() == 'true':
            issues.append("CRITICAL: DEBUG=true in production config!")
        if env_dict.get('SECRET_KEY', '') == '':
            issues.append("CRITICAL: SECRET_KEY is empty in production config!")
    
    return issues


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python env-to-json.py <file.env> [--to-json] [--to-env] [--validate]")
        print("\nExamples:")
        print("  python env-to-json.py .env              # Show parsed .env as JSON")
        print("  python env-to-json.py .env --validate   # Validate .env file")
        print("  python env-to-json.py config.json       # Convert JSON to .env")
        print("  echo 'FOO=bar' | python env-to-json.py -  # Read from stdin")
        sys.exit(1)
    
    path = sys.argv[1]
    validate = '--validate' in sys.argv
    
    # Read input
    if path == '-' or path == '/dev/stdin':
        content = sys.stdin.read()
    elif os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        print(f"Error: File not found: {path}")
        sys.exit(1)
    
    print(f"=== ENV/JSON Converter: {path} ===\n")
    
    if path.endswith('.json') or '--to-env' in sys.argv:
        # JSON -> ENV
        try:
            data = json.loads(content)
            output = json_to_env(data)
            print(output)
        except json.JSONDecodeError as e:
            print(f"JSON Parse Error: {e}")
            sys.exit(1)
    else:
        # ENV -> JSON
        env_dict = parse_env(content)
        
        if validate:
            print(f"Parsed {len(env_dict)} variables:")
            issues = validate_env(env_dict)
            if issues:
                print("\nValidation issues:")
                for issue in issues:
                    print(f"  - {issue}")
            else:
                print("\nNo issues found.")
            print()
        
        output = env_to_json(env_dict)
        print(output)
