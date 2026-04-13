#!/usr/bin/env python3
"""
Binary/Decimal/Hex Converter.
Usage: python binary-dec.py <value> [--from bin|dec|hex] [--to bin|dec|hex]
"""

import sys

def convert(value, from_base, to_base):
    """Convert between bases."""
    # First convert to decimal
    try:
        decimal = int(value, from_base)
    except ValueError:
        return None
    
    # Then convert to target
    if to_base == 'dec':
        return str(decimal)
    elif to_base == 'hex':
        return hex(decimal)
    elif to_base == 'bin':
        return bin(decimal)
    elif to_base == 'oct':
        return oct(decimal)
    return str(decimal)

def detect_base(value):
    """Detect number base from string."""
    v = value.lower().strip()
    if v.startswith('0x'):
        return 'hex'
    elif v.startswith('0b'):
        return 'bin'
    elif v.startswith('0o'):
        return 'oct'
    elif v.isdigit():
        return 'dec'
    return 'dec'

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python binary-dec.py <value> [--from bin|dec|hex] [--to bin|dec|hex]")
        sys.exit(1)
    
    value = sys.argv[1]
    from_base = 'auto'
    to_base = None
    
    for i, arg in enumerate(sys.argv):
        if arg == '--from' and i + 1 < len(sys.argv):
            from_base = sys.argv[i + 1].lower()
        if arg == '--to' and i + 1 < len(sys.argv):
            to_base = sys.argv[i + 1].lower()
    
    if from_base == 'auto':
        from_base = detect_base(value)
    
    if to_base is None:
        # Show all
        bases = ['dec', 'hex', 'bin', 'oct']
        bases.remove(from_base)
        print(f"Input: {value} ({from_base})")
        print(f"\n{from_base}: {value}")
        for base in bases:
            result = convert(value, from_base, base)
            if result:
                print(f"{base}: {result}")
    else:
        result = convert(value, from_base, to_base)
        if result:
            print(result)
        else:
            print("Conversion failed")
            sys.exit(1)
