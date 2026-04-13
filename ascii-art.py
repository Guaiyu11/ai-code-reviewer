#!/usr/bin/env python3
"""
ASCII Art - Generate ASCII art text banners.
Usage: python ascii-art.py <text> [--font standard|banner|shadow|small|big]
"""

import sys

FONTS = {
    'standard': {
        'A': ['  A  ', ' A A ', 'AAAAA', 'A   A', 'A   A'],
        'B': ['BBBB ', 'B   B', 'BBBB ', 'B   B', 'BBBB '],
        'C': [' CCC ', 'C    ', 'C    ', 'C    ', ' CCC '],
        'D': ['DDDD ', 'D   D', 'D   D', 'D   D', 'DDDD '],
        'E': ['EEEEE', 'E    ', 'EEE  ', 'E    ', 'EEEEE'],
        'F': ['FFFFF', 'F    ', 'FFF  ', 'F    ', 'F    '],
        'G': [' GGG ', 'G    ', 'G  GG', 'G   G', ' GGG '],
        'H': ['H   H', 'H   H', 'HHHHH', 'H   H', 'H   H'],
        'I': ['IIIII', '  I  ', '  I  ', '  I  ', 'IIIII'],
        'J': ['JJJJJ', '   J ', '   J ', 'J  J ', ' JJ  '],
        'K': ['K   K', 'K  K ', 'KK   ', 'K  K ', 'K   K'],
        'L': ['L    ', 'L    ', 'L    ', 'L    ', 'LLLLL'],
        'M': ['M   M', 'MM MM', 'M M M', 'M   M', 'M   M'],
        'N': ['N   N', 'NN  N', 'N N N', 'N  NN', 'N   N'],
        'O': [' OOO ', 'O   O', 'O   O', 'O   O', ' OOO '],
        'P': ['PPPP ', 'P   P', 'PPPP ', 'P    ', 'P    '],
        'Q': [' QQQ ', 'Q   Q', 'Q Q Q', 'Q  Q ', ' QQ Q'],
        'R': ['RRRR ', 'R   R', 'RRRR ', 'R  R ', 'R   R'],
        'S': [' SSS ', 'S    ', ' SSS ', '    S', ' SSS '],
        'T': ['TTTTT', '  T  ', '  T  ', '  T  ', '  T  '],
        'U': ['U   U', 'U   U', 'U   U', 'U   U', ' UUU '],
        'V': ['V   V', 'V   V', 'V   V', ' V V ', '  V  '],
        'W': ['W   W', 'W   W', 'W W W', 'WW WW', 'W   W'],
        'X': ['X   X', ' X X ', '  X  ', ' X X ', 'X   X'],
        'Y': ['Y   Y', ' Y Y ', '  Y  ', '  Y  ', '  Y  '],
        'Z': ['ZZZZZ', '   Z ', '  Z  ', ' Z   ', 'ZZZZZ'],
        '0': [' 000 ', '0   0', '0   0', '0   0', ' 000 '],
        '1': ['  1  ', ' 11  ', '  1  ', '  1  ', '11111'],
        '2': [' 222 ', '2   2', '  22 ', ' 2   ', '22222'],
        '3': ['3333 ', '    3', ' 333 ', '    3', '3333 '],
        '4': ['4   4', '4   4', '44444', '    4', '    4'],
        '5': ['55555', '5    ', '5555 ', '    5', '5555 '],
        '6': [' 666 ', '6    ', '6666 ', '6   6', ' 666 '],
        '7': ['77777', '    7', '   7 ', '  7  ', '  7  '],
        '8': [' 888 ', '8   8', ' 888 ', '8   8', ' 888 '],
        '9': [' 999 ', '9   9', ' 9999', '    9', ' 999 '],
        ' ': ['    ', '    ', '    ', '    ', '    '],
        '-': ['    ', '    ', '7777', '    ', '    '],
        '.': ['    ', '    ', '    ', '    ', ' 88  '],
    }
}

def ascii_print(text, font='standard'):
    """Print text in ASCII art."""
    if font not in FONTS:
        font = 'standard'
    
    chars = [c.upper() for c in text]
    
    # Get all char art, padding to same height
    char_arts = []
    for c in chars:
        if c in FONTS[font]:
            char_arts.append(FONTS[font][c])
        else:
            char_arts.append(['    '] * 5)
    
    for line_idx in range(5):
        line = ''
        for art in char_arts:
            line += art[line_idx] + ' '
        print(line)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python ascii-art.py <text> [--font standard]")
        sys.exit(1)
    
    text = sys.argv[1]
    font = 'standard'
    
    for i, arg in enumerate(sys.argv):
        if arg == '--font' and i + 1 < len(sys.argv):
            font = sys.argv[i + 1]
    
    ascii_print(text, font)
