#!/usr/bin/env python3
"""
URL Shortener - Create short URLs (requires TinyURL API).
Usage: python url-shorten.py <url> [--service tinyurl|tinyurl]
"""

import sys
import urllib.request
import urllib.parse

def tinyurl(url):
    """Shorten URL using TinyURL API."""
    api = f"http://tinyurl.com/api-create.php?url={urllib.parse.quote(url)}"
    try:
        with urllib.request.urlopen(api, timeout=10) as resp:
            return resp.read().decode().strip()
    except Exception as e:
        return None, str(e)

def isgd(url):
    """Shorten URL using is.gd API."""
    api = f"https://is.gd/create.php?format=simple&url={urllib.parse.quote(url)}"
    try:
        with urllib.request.urlopen(api, timeout=10) as resp:
            return resp.read().decode().strip()
    except Exception as e:
        return None, str(e)

def virbr(url):
    """Shorten URL using v.gd API."""
    api = f"https://v.gd/create.php?format=simple&url={urllib.parse.quote(url)}"
    try:
        with urllib.request.urlopen(api, timeout=10) as resp:
            return resp.read().decode().strip()
    except Exception as e:
        return None, str(e)

SERVICES = {
    'tinyurl': tinyurl,
    'isgd': isgd,
    'vgd': virbr,
    'v.gd': virbr,
}

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python url-shorten.py <url> [--service tinyurl|isgd|vgd]")
        sys.exit(1)
    
    url = sys.argv[1]
    service = 'tinyurl'
    
    for i, arg in enumerate(sys.argv):
        if arg == '--service' and i + 1 < len(sys.argv):
            service = sys.argv[i + 1].lower()
    
    if service not in SERVICES:
        print(f"Unknown service: {service}")
        print("Services:", ', '.join(SERVICES.keys()))
        sys.exit(1)
    
    result = SERVICES[service](url)
    
    if isinstance(result, tuple):
        print(f"Error: {result[1]}")
        sys.exit(1)
    else:
        print(result)
