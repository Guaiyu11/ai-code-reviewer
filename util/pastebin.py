#!/usr/bin/env python3
"""
Pastebin - Upload text to pastebin services.
Usage: python pastebin.py <file|text> [--service dpaste|dpaste|ix]
"""

import sys
import os
import urllib.request
import urllib.parse

SERVICES = {
    'dpaste': {
        'url': 'https://dpaste.com/api/',
        'data': {'content': None, 'syntax': 'text', 'expiry_days': 7},
    },
}

def upload_dp(text, url='https://dpaste.com/api/', expiry_days=7):
    """Upload to dpaste."""
    data = urllib.parse.urlencode({
        'content': text,
        'syntax': 'text',
        'expiry_days': expiry_days,
    }).encode()
    
    req = urllib.request.Request(url, data=data)
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = resp.read().decode().strip()
    return result

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python pastebin.py <file|text> [--service dpaste]")
        sys.exit(1)
    
    target = sys.argv[1]
    
    if os.path.exists(target):
        with open(target, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        text = target
    
    service = 'dpaste'
    for i, arg in enumerate(sys.argv):
        if arg == '--service' and i + 1 < len(sys.argv):
            service = sys.argv[i + 1]
    
    if service == 'dpaste':
        url = upload_dp(text)
        print(f"Pasted: {url}")
    else:
        print(f"Unknown service: {service}")
