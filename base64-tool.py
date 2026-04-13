#!/usr/bin/env python3
"""
Base64 Tool - Encode/decode Base64, URL-encode, HTML-encode.
Usage: python base64-tool.py <string|file> [--decode] [--url] [--html]
"""

import sys
import os
import base64
import urllib.parse
import html

def auto_decode(s):
    """Try to detect and decode various formats."""
    results = {}
    original = s
    
    # Raw
    results['raw'] = s
    
    # Base64
    try:
        decoded = base64.b64decode(s).decode('utf-8')
        results['base64_decoded'] = decoded
    except:
        pass
    
    # URL decode
    try:
        decoded = urllib.parse.unquote(s)
        if decoded != s:
            results['url_decoded'] = decoded
    except:
        pass
    
    # HTML decode
    try:
        decoded = html.unescape(s)
        if decoded != s:
            results['html_decoded'] = decoded
    except:
        pass
    
    return results


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python base64-tool.py <string|file> [--encode64] [--decode64] [--url] [--html]")
        sys.exit(1)
    
    target = sys.argv[1]
    mode = None
    for arg in sys.argv:
        if arg == '--decode64':
            mode = 'decode64'
        elif arg == '--url':
            mode = 'url'
        elif arg == '--html':
            mode = 'html'
        elif arg == '--encode64':
            mode = 'encode64'
    
    # Read file or use string
    if os.path.exists(target):
        with open(target, 'rb') as f:
            data = f.read()
        is_binary = True
    else:
        data = target.encode('utf-8')
        is_binary = False
    
    print("=== Base64/URL/HTML Tool ===\n")
    
    if mode == 'decode64':
        try:
            decoded = base64.b64decode(target).decode('utf-8')
            print(f"Base64 -> UTF-8:\n{decoded}")
        except Exception as e:
            print(f"Base64 decode error: {e}")
    elif mode == 'encode64':
        encoded = base64.b64encode(data).decode()
        print(encoded)
    elif mode == 'url':
        print(urllib.parse.quote(target))
    elif mode == 'html':
        print(html.escape(target))
    else:
        # Auto-detect
        print(f"Input: {target[:200]}")
        print()
        
        # Show all encodings
        print(f"Base64:    {base64.b64encode(data).decode()}")
        print(f"URL:       {urllib.parse.quote(target)}")
        print(f"HTML:      {html.escape(target)}")
        print(f"Hex:       {data.hex()[:200]}")
        
        # Try decoding
        results = auto_decode(target)
        for fmt, val in results.items():
            if fmt != 'raw':
                print(f"\n[{fmt}] -> {val[:200]}")
