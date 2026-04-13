#!/usr/bin/env python3
"""
Case Converter - Convert strings between different case styles.
Usage: python caseconvert.py <text> [--to kebab|snake|camel|pascal|upper|lower|title|constant]
"""

import sys
import re

def to_kebab(text):
    """Convert to kebab-case."""
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'([a-z])([A-Z])', r'\1-\2', text)
    return text.lower()

def to_snake(text):
    """Convert to snake_case."""
    text = re.sub(r'[\s-]+', '_', text)
    text = re.sub(r'([a-z])([A-Z])', r'\1_\2', text)
    return text.lower()

def to_camel(text):
    """Convert to camelCase."""
    parts = re.split(r'[\s_-]+', text)
    return parts[0].lower() + ''.join(p.title() for p in parts[1:])

def to_pascal(text):
    """Convert to PascalCase."""
    parts = re.split(r'[\s_-]+', text)
    return ''.join(p.title() for p in parts)

def to_upper(text):
    return text.upper()

def to_lower(text):
    return text.lower()

def to_title(text):
    return text.title()

def to_constant(text):
    """Convert to CONSTANT_CASE."""
    return to_snake(text).upper()

CONVERTERS = {
    'kebab': to_kebab,
    'snake': to_snake,
    'camel': to_camel,
    'pascal': to_pascal,
    'upper': to_upper,
    'lower': to_lower,
    'title': to_title,
    'constant': to_constant,
}

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python caseconvert.py <text> [--to kebab|snake|camel|pascal|upper|lower|title]")
        print("\nExamples:")
        print("  python caseconvert.py 'hello world'")
        print("  python caseconvert.py 'hello_world' --to camel")
        sys.exit(1)
    
    text = sys.argv[1]
    target = 'all'
    
    for i, arg in enumerate(sys.argv):
        if arg == '--to' and i + 1 < len(sys.argv):
            target = sys.argv[i + 1].lower()
    
    if target == 'all':
        print("=== Case Conversions ===\n")
        for name, func in CONVERTERS.items():
            print(f"{name:12s}: {func(text)}")
    elif target in CONVERTERS:
        print(CONVERTERS[target](text))
    else:
        print(f"Unknown target: {target}")
        print("Options:", ', '.join(CONVERTERS.keys()))
