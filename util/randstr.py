#!/usr/bin/env python3
"""
RandStr - Generate random strings.
Usage: python randstr.py [length] [--alphanumeric|--alpha|--numeric|--hex]
"""

import sys
import secrets
import string

def generate(length=16, charset=None):
    """Generate random string."""
    if charset is None:
        charset = string.ascii_letters + string.digits
    return ''.join(secrets.choice(charset) for _ in range(length))

if __name__ == '__main__':
    length = 16
    charset = None
    
    for arg in sys.argv:
        if arg.isdigit():
            length = int(arg)
        elif arg == '--alphanumeric':
            charset = string.ascii_letters + string.digits
        elif arg == '--alpha':
            charset = string.ascii_letters
        elif arg == '--numeric':
            charset = string.digits
        elif arg == '--hex':
            charset = string.hexdigits.lower()
    
    print(generate(length, charset))
