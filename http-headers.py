#!/usr/bin/env python3
"""
HTTP Headers - Show HTTP headers of a URL.
Usage: python http-headers.py <url>
"""

import sys
import urllib.request

def get_headers(url):
    """Get HTTP headers."""
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        req = urllib.request.Request(url, method='HEAD')
        with urllib.request.urlopen(req, timeout=10) as resp:
            return dict(resp.headers), resp.status
    except Exception as e:
        return None, str(e)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python http-headers.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    headers, status = get_headers(url)
    
    if headers is None:
        print(f"Error: {status}")
        sys.exit(1)
    
    print(f"=== HTTP Headers: {url} ===")
    print(f"Status: {status}\n")
    
    for key, value in sorted(headers.items()):
        print(f"{key}: {value}")
