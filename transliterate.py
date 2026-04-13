#!/usr/bin/env python3
"""
Transliterate - Convert text between Latin, Cyrillic, Greek alphabets.
Usage: python transliterate.py <text> [--to cyrillic|greek|ascii]
"""

import sys
import unicodedata

CYRILLIC = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
    'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
    'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
    'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
    'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
    'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'Yo',
    'Ж': 'Zh', 'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M',
    'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
    'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch',
    'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya',
}

def to_cyrillic(text):
    """Convert Latin to Cyrillic."""
    result = []
    i = 0
    while i < len(text):
        two = text[i:i+2].lower()
        if two in ('yo', 'yu', 'ya'):
            result.append({'yo': 'ё', 'yu': 'ю', 'ya': 'я'}[two])
            i += 2
        else:
            c = text[i]
            result.append(CYRILLIC.get(c, CYRILLIC.get(c.lower(), c)))
            i += 1
    return ''.join(result)

def to_ascii(text):
    """Convert to ASCII (strip accents)."""
    nfkd = unicodedata.normalize('NFKD', text)
    return ''.join(c for c in nfkd if not unicodedata.combining(c))

def to_greek(text):
    """Very basic Latin to Greek transliteration."""
    greek_map = {
        'a': 'α', 'b': 'β', 'c': 'κ', 'd': 'δ', 'e': 'ε', 'f': 'φ', 'g': 'γ',
        'h': 'η', 'i': 'ι', 'j': 'ξ', 'k': 'κ', 'l': 'λ', 'm': 'μ', 'n': 'ν',
        'o': 'ο', 'p': 'π', 'q': 'κ', 'r': 'ρ', 's': 'σ', 't': 'τ', 'u': 'υ',
        'v': 'β', 'w': 'ω', 'x': 'χ', 'y': 'ψ', 'z': 'ζ',
    }
    return ''.join(greek_map.get(c.lower(), c) for c in text)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python transliterate.py <text> [--to cyrillic|greek|ascii]")
        sys.exit(1)
    
    text = sys.argv[1]
    target = 'ascii'
    
    for i, arg in enumerate(sys.argv):
        if arg == '--to' and i + 1 < len(sys.argv):
            target = sys.argv[i + 1].lower()
    
    if target == 'cyrillic':
        print(to_cyrillic(text))
    elif target == 'greek':
        print(to_greek(text))
    elif target == 'ascii':
        print(to_ascii(text))
    else:
        print(f"Unknown target: {target}")
        print("Options: --to cyrillic|greek|ascii")
