#!/usr/bin/env python3
"""
URL Encoder/Decoder - Encode or decode URL components.
Usage: python url-encode.py <text|url> [--decode] [--component]
"""

import sys
import urllib.parse

def encode_url(text, component=False):
    """URL encode text."""
    if component:
        return urllib.parse.quote_plus(text)
    return urllib.parse.quote(text)

def decode_url(text):
    """URL decode text."""
    return urllib.parse.unquote(text)

def parse_query(text):
    """Parse query string."""
    params = urllib.parse.parse_qs(text)
    return params

def build_query(params):
    """Build query string from dict."""
    return urllib.parse.urlencode(params, doseq=True)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python url-encode.py <text|url> [--decode] [--parse] [--build KEY=VALUE...]")
        sys.exit(1)
    
    text = sys.argv[1]
    
    if '--decode' in sys.argv:
        print(decode_url(text))
    elif '--parse' in sys.argv:
        params = parse_query(text)
        print("Query Parameters:")
        for k, v in params.items():
            print(f"  {k} = {v}")
    elif '--build' in sys.argv:
        params = {}
        for arg in sys.argv[2:]:
            if '=' in arg:
                k, v = arg.split('=', 1)
                params[k] = v
        print(build_query(params))
    else:
        # Show all encodings
        print(f"Original:           {text}")
        print(f"quote:              {encode_url(text, False)}")
        print(f"quote_plus:         {encode_url(text, True)}")
