#!/usr/bin/env python3
"""
Extract URLs - Extract URLs from text.
Usage: python extract-urls.py <file|text>
"""

import sys
import os
import re

URL_RE = re.compile(r'https?://[^\s<>"{}|\\^`\[\]]+')

def extract_urls(text):
    """Extract URLs."""
    return set(URL_RE.findall(text))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python extract-urls.py <file|text>")
        sys.exit(1)
    
    target = sys.argv[1]
    
    if os.path.exists(target):
        with open(target, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
    else:
        text = target
    
    urls = extract_urls(text)
    
    if urls:
        print(f"Found {len(urls)} URLs:\n")
        for url in sorted(urls):
            print(url)
    else:
        print("No URLs found")
