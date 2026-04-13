#!/usr/bin/env python3
"""
INI Editor - Read, parse, and edit INI/CFG files.
Usage: python ini-edit.py <file.ini> [--get SECTION KEY] [--set SECTION KEY=VALUE]
"""

import sys
import os
import configparser

def read_ini(filepath):
    """Read INI file."""
    parser = configparser.ConfigParser()
    parser.read(filepath, encoding='utf-8', errors='ignore')
    return parser

def print_ini(parser):
    """Print INI contents."""
    for section in parser.sections():
        print(f"[{section}]")
        for key, value in parser.items(section):
            if key != '__name__':
                print(f"  {key} = {value}")
        print()

def get_value(parser, section, key):
    """Get a value."""
    try:
        return parser.get(section, key)
    except:
        return None

def set_value(parser, filepath, section, key, value):
    """Set a value and save."""
    if not parser.has_section(section):
        parser.add_section(section)
    parser.set(section, key, value)
    with open(filepath, 'w') as f:
        parser.write(f)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python ini-edit.py <file.ini> [--get S K] [--set S K=V]")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    
    parser = read_ini(filepath)
    
    get_section = None
    get_key = None
    set_section = None
    set_kv = None
    
    for i, arg in enumerate(sys.argv):
        if arg == '--get' and i + 2 < len(sys.argv):
            get_section = sys.argv[i + 1]
            get_key = sys.argv[i + 2]
        elif arg == '--set' and i + 1 < len(sys.argv):
            kv = sys.argv[i + 1]
            if '=' in kv:
                set_section, set_kv = kv.split('=', 1)
                set_section = set_section.strip()
    
    if set_section and set_kv:
        if '.' in set_kv and '=' not in set_kv:
            # set S K=V
            parts = set_kv.split('=', 1)
            key, value = parts[0].strip(), parts[1].strip()
            set_value(parser, filepath, set_section, key, value)
            print(f"Set [{set_section}] {key} = {value}")
        else:
            print("Error: use --set SECTION KEY=VALUE")
    elif get_section and get_key:
        value = get_value(parser, get_section, get_key)
        print(value if value is not None else "")
    else:
        print_ini(parser)
