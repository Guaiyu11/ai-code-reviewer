#!/usr/bin/env python3
"""
URL Parser - Parse, extract, and build URLs.
Usage: python url-parser.py <url> [--param KEY] [--set KEY=VALUE] [--build]
"""

import sys
import os
import urllib.parse

def parse_url(url):
    """Parse URL into components."""
    parsed = urllib.parse.urlparse(url)
    
    return {
        'scheme': parsed.scheme,
        'netloc': parsed.netloc,
        'hostname': parsed.hostname,
        'port': parsed.port,
        'path': parsed.path,
        'params': urllib.parse.parse_qs(parsed.params),
        'query': urllib.parse.parse_qs(parsed.query),
        'fragment': parsed.fragment,
    }

def get_param(url, key):
    """Get a specific parameter from URL."""
    parsed = urllib.parse.urlparse(url)
    params = urllib.parse.parse_qs(parsed.query)
    return params.get(key, [None])[0]

def set_param(url, key, value):
    """Set a parameter in URL."""
    parsed = urllib.parse.urlparse(url)
    params = urllib.parse.parse_qs(parsed.query)
    params[key] = [value]
    new_query = urllib.parse.urlencode(params, doseq=True)
    new_parsed = parsed._replace(query=new_query)
    return new_parsed.geturl()

def build_url(scheme='https', netloc='', path='/', params='', query='', fragment=''):
    """Build URL from components."""
    if isinstance(query, dict):
        query = urllib.parse.urlencode(query, doseq=True)
    parsed = urllib.parse.ParseResult(scheme, netloc, path, params, query, fragment)
    return parsed.geturl()

def extract_links(text):
    """Extract all URLs from text."""
    import re
    url_pattern = re.compile(r'https?://[^\s<>"{}|\\^`\[\]]+')
    return url_pattern.findall(text)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python url-parser.py <url> [--param KEY] [--set KEY=VALUE] [--build]")
        print("\nExamples:")
        print("  python url-parser.py 'https://example.com/path?q=1&r=2'")
        print("  python url-parser.py 'https://example.com' --set key=value")
        print("  python url-parser.py 'https://example.com' --build --scheme https --netloc api.example.com --path /v1/users")
        sys.exit(1)
    
    url = sys.argv[1]
    
    if '--build' in sys.argv:
        kwargs = {}
        for i, arg in enumerate(sys.argv):
            if arg in ('--scheme', '--netloc', '--path', '--query', '--fragment'):
                if i + 1 < len(sys.argv) and not sys.argv[i + 1].startswith('--'):
                    kwargs[arg[2:]] = sys.argv[i + 1]
        result = build_url(**kwargs)
        print(result)
        sys.exit(0)
    
    # Parse mode
    parsed = parse_url(url)
    
    print("=== URL Parser ===\n")
    print(f"Full URL:  {url}\n")
    print(f"Scheme:    {parsed['scheme']}")
    print(f"Host:      {parsed['hostname']}")
    print(f"Port:      {parsed['port'] or '(default)'}")
    print(f"Path:      {parsed['path']}")
    
    if parsed['query']:
        print("\nQuery Parameters:")
        for key, values in parsed['query'].items():
            for v in values:
                print(f"  {key} = {v}")
    
    if parsed['fragment']:
        print(f"\nFragment: {parsed['fragment']}")
    
    # Get specific param
    if '--param' in sys.argv:
        pi = sys.argv.index('--param')
        key = sys.argv[pi + 1]
        value = get_param(url, key)
        print(f"\n[{key}] = {value}")
    
    # Set param
    if '--set' in sys.argv:
        si = sys.argv.index('--set')
        keyval = sys.argv[si + 1]
        if '=' in keyval:
            key, value = keyval.split('=', 1)
            new_url = set_param(url, key, value)
            print(f"\nNew URL: {new_url}")
