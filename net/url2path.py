#!/usr/bin/env python3
"""
URL to Path - Convert URL to filesystem-safe filename.
Usage: python url2path.py <url>
"""

import sys
import re
import urllib.parse

def url_to_path(url):
    """Convert URL to safe filename."""
    parsed = urllib.parse.urlparse(url)
    path = parsed.netloc + parsed.path
    path = re.sub(r'[^\w\-_.]', '_', path)
    path = re.sub(r'_+', '_', path)
    path = path.strip('_')
    return path or 'index'

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python url2path.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    print(url_to_path(url))
