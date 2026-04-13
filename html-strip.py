#!/usr/bin/env python3
"""
HTML Stripper - Remove HTML tags from content.
Usage: python html-strip.py <file|url> [--attrs] [--links]
"""

import sys
import os
import re

def strip_html(html):
    """Remove HTML tags from content."""
    # Remove script and style blocks
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', html)
    
    # Decode HTML entities
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&quot;', '"')
    text = text.replace('&#39;', "'")
    
    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def extract_links(html):
    """Extract all links from HTML."""
    hrefs = re.findall(r'href=["\']([^"\']+)["\']', html)
    srcs = re.findall(r'src=["\']([^"\']+)["\']', html)
    return list(set(hrefs + srcs))

def extract_attrs(html, tag='a'):
    """Extract attributes from specific tags."""
    if tag == 'a':
        return re.findall(r'<a[^>]*href=["\']([^"\']+)["\'][^>]*>([^<]*)</a>', html)
    elif tag == 'img':
        return re.findall(r'<img[^>]*src=["\']([^"\']+)["\'][^>]*alt=["\']([^"\']*)["\']', html)
    return []

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python html-strip.py <file|url> [--attrs] [--links]")
        sys.exit(1)
    
    target = sys.argv[1]
    
    if os.path.exists(target):
        with open(target, 'r', encoding='utf-8', errors='ignore') as f:
            html = f.read()
    else:
        import urllib.request
        try:
            with urllib.request.urlopen(target, timeout=10) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
        except:
            print(f"Error: Could not fetch URL: {target}")
            sys.exit(1)
    
    if '--links' in sys.argv:
        links = extract_links(html)
        print(f"Found {len(links)} links:")
        for link in links:
            print(f"  {link}")
    elif '--attrs' in sys.argv:
        attrs = extract_attrs(html)
        print(f"Found {len(attrs)} attributes:")
        for attr in attrs:
            print(f"  {attr}")
    else:
        text = strip_html(html)
        print(text)
