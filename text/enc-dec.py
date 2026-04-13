#!/usr/bin/env python3
"""
Encode/Decode Tool - ROT13, Caesar cipher, Morse code, Base32.
Usage: python enc-dec.py <text> [--rot13] [--caesar N] [--morse] [--base32]
"""

import sys

def rot13(text):
    """ROT13 cipher."""
    import codecs
    return codecs.encode(text, 'rot_13')

def caesar(text, shift=3):
    """Caesar cipher."""
    result = []
    for c in text:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            result.append(chr((ord(c) - base + shift) % 26 + base))
        else:
            result.append(c)
    return ''.join(result)

def morse_encode(text):
    """Encode text to Morse code."""
    MORSE = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
        'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
        'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
        'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
        'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
        '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
        '8': '---..', '9': '----.', ' ': '/'
    }
    return ' '.join(MORSE.get(c.upper(), '') for c in text)

def base32_encode(text):
    """Encode to Base32."""
    import base64
    return base64.b32encode(text.encode()).decode()

def hex_encode(text):
    """Encode to hex."""
    return text.encode().hex()

def binary_encode(text):
    """Encode to binary."""
    return ' '.join(bin(ord(c)) for c in text)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python enc-dec.py <text> [--rot13] [--caesar N] [--morse] [--base32] [--hex] [--binary]")
        sys.exit(1)
    
    text = sys.argv[1]
    mode = None
    
    for arg in sys.argv:
        if arg in ('--rot13', '--caesar', '--morse', '--base32', '--hex', '--binary'):
            mode = arg[2:]
    
    if mode == 'rot13':
        print(rot13(text))
    elif mode == 'caesar':
        shift = 3
        for i, arg in enumerate(sys.argv):
            if arg == '--caesar' and i + 1 < len(sys.argv):
                shift = int(sys.argv[i + 1])
        print(caesar(text, shift))
    elif mode == 'morse':
        print(morse_encode(text))
    elif mode == 'base32':
        print(base32_encode(text))
    elif mode == 'hex':
        print(hex_encode(text))
    elif mode == 'binary':
        print(binary_encode(text))
    else:
        # Show all
        print(f"Original:  {text}")
        print(f"ROT13:     {rot13(text)}")
        print(f"Caesar:    {caesar(text)}")
        print(f"Morse:     {morse_encode(text)}")
        print(f"Base32:    {base32_encode(text)}")
        print(f"Hex:       {hex_encode(text)}")
