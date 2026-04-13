#!/usr/bin/env python3
"""
Extract Links - Extract all URLs from HTML or text.
Usage: python extract-links.py <file|url> [--unique] [--domain DOMAIN]
"""

import sys
import os
import re
import urllib.parse

def extract_from_html(content):
    """Extract links from HTML."""
    links = set()
    
    # <a href>
    for match in re.finditer(r'<a\s[^>]*href=["\']([^"\']+)["\']', content, re.I):
        links.add(match.group(1))
    
    # <img src>
    for match in re.finditer(r'<img\s[^>]*src=["\']([^"\']+)["\']', content, re.I):
        links.add(match.group(1))
    
    # <link href>
    for match in re.finditer(r'<link\s[^>]*href=["\']([^"\']+)["\']', content, re.I):
        links.add(match.group(1))
    
    # <script src>
    for match in re.finditer(r'<script\s[^>]*src=["\']([^"\']+)["\']', content, re.I):
        links.add(match.group(1))
    
    return links

def extract_from_text(content):
    """Extract URLs from plain text."""
    url_pattern = re.compile(r'https?://[^\s<>"{}|\\^`\[\]]+')
    return set(url_pattern.findall(content))

def filter_by_domain(links, domain):
    """Filter links by domain."""
    filtered = set()
    for link in links:
        parsed = urllib.parse.urlparse(link)
        if domain in parsed.netloc:
            filtered.add(link)
    return filtered

def make_absolute(base_url, link):
    """Convert relative links to absolute."""
    if link.startswith('http'):
        return link
    if link.startswith('//'):
        return 'https:' + link
    if link.startswith('/'):
        parsed = urllib.parse.urlparse(base_url)
        return f"{parsed.scheme}://{parsed.netloc}{link}"
    return urllib.parse.urljoin(base_url, link)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python extract-links.py <file|url> [--unique] [--domain DOMAIN]")
        sys.exit(1)
    
    target = sys.argv[1]
    
    if os.path.exists(target):
        with open(target, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        links = extract_from_html(content)
    else:
        links = extract_from_text(target)
    
    domain = None
    for i, arg in enumerate(sys.argv):
        if arg == '--domain' and i + 1 < len(sys.argv):
            domain = sys.argv[i + 1]
    
    if domain:
        links = filter_by_domain(links, domain)
    
    if '--unique' in sys.argv:
        links = sorted(set(links))
    else:
        links = sorted(links)
    
    print(f"=== Found {len(links)} links ===\n")
    for link in links:
        print(link)
