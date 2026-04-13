#!/usr/bin/env python3
"""
URL Decode All - Recursively decode all URL-encoded parts.
Usage: python url-decode-all.py <text>
"""

import sys
import urllib.parse

def decode_all(text):
    """Recursively decode URL encoding."""
    prev = None
    while prev != text:
        prev = text
        text = urllib.parse.unquote(text)
    return text

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python url-decode-all.py <text>")
        sys.exit(1)
    
    text = ' '.join(sys.argv[1:])
    result = decode_all(text)
    print(result)
