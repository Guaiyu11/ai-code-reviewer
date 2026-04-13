#!/usr/bin/env python3
"""
Unit Converter - Convert between units of measurement.
Usage: python unit-conv.py <value> <from_unit> <to_unit>
Example: python unit-conv.py 100 km mi
"""

import sys

CONVERSIONS = {
    ('km', 'mi'): (1, 0.621371),
    ('mi', 'km'): (1, 1.60934),
    ('m', 'ft'): (1, 3.28084),
    ('ft', 'm'): (1, 0.3048),
    ('kg', 'lb'): (1, 2.20462),
    ('lb', 'kg'): (1, 0.453592),
    ('g', 'oz'): (1, 0.035274),
    ('oz', 'g'): (1, 28.3495),
    ('c', 'f'): (lambda x: x * 9/5 + 32, lambda x: (x - 32) * 5/9),
    ('f', 'c'): (lambda x: (x - 32) * 5/9, lambda x: x * 9/5 + 32),
    ('km', 'm'): (1000, 0.001),
    ('m', 'km'): (0.001, 1000),
    ('cm', 'in'): (1, 0.393701),
    ('in', 'cm'): (1, 2.54),
    ('l', 'gal'): (1, 0.264172),
    ('gal', 'l'): (1, 3.78541),
    ('mb', 'gb'): (1024, 1/1024),
    ('gb', 'mb'): (1, 1024),
    ('kb', 'mb'): (1024, 1/1024),
    ('mb', 'kb'): (1, 1024),
    ('bytes', 'kb'): (1024, 1/1024),
    ('kb', 'bytes'): (1, 1024),
    ('mb', 'gb'): (1024, 1/1024),
}

def convert(value, from_unit, to_unit):
    key = (from_unit.lower(), to_unit.lower())
    
    if key not in CONVERSIONS:
        # Try reverse
        reverse_key = (to_unit.lower(), from_unit.lower())
        if reverse_key in CONVERSIONS:
            factor, _ = CONVERSIONS[reverse_key]
            return value / factor
        return None
    
    factor, _ = CONVERSIONS[key]
    if callable(factor):
        return factor(value)
    return value * factor

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python unit-conv.py <value> <from_unit> <to_unit>")
        print("\nSupported units:")
        print("  Length: km, mi, m, ft, cm, in")
        print("  Weight: kg, lb, g, oz")
        print("  Temp: c (Celsius), f (Fahrenheit)")
        print("  Volume: l, gal")
        print("  Data: bytes, kb, mb, gb")
        sys.exit(1)
    
    value = float(sys.argv[1])
    from_unit = sys.argv[2].lower()
    to_unit = sys.argv[3].lower()
    
    result = convert(value, from_unit, to_unit)
    
    if result is None:
        print(f"Conversion not supported: {from_unit} -> {to_unit}")
        sys.exit(1)
    
    print(f"{value} {from_unit} = {result:.6g} {to_unit}")
