#!/usr/bin/env python3
"""
Color Test - Print terminal colors (ANSI 256 color palette).
Usage: python color-test.py [--truecolor]
"""

import sys

def print_256():
    """Print 256 color palette."""
    print("=== ANSI 256 Color Palette ===\n")
    for i in range(256):
        print(f"\033[48;5;{i}m{i:3d}\033[0m", end='  ')
        if i % 16 == 15:
            print()

def print_truecolor():
    """Print truecolor gradient test."""
    print("\n=== Truecolor Gradient Test ===\n")
    for r in range(0, 256, 51):
        row = ''
        for g in range(0, 256, 51):
            row += f"\033[48;2;{r};{g};0m  \033[0m"
        print(row)

if __name__ == '__main__':
    if '--truecolor' in sys.argv:
        print_truecolor()
    else:
        print_256()
    
    print("\n\n=== Common Colors ===\n")
    colors = [
        ('Black', '0', '0'),
        ('Red', '196', '1'),
        ('Green', '46', '2'),
        ('Yellow', '226', '3'),
        ('Blue', '21', '4'),
        ('Magenta', '201', '5'),
        ('Cyan', '51', '6'),
        ('White', '231', '7'),
    ]
    for name, code, ansi in colors:
        fg = 255 if int(code) < 128 else 0
        print(f"\033[38;5;{code}m\033[48;5;0m{name:10s} {code} \033[0m", end='  ')
        print(f"\033[38;5;0m\033[48;5;{code}m{name:10s} {code} \033[0m")
