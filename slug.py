#!/usr/bin/env python3
"""
Slug - Convert text to URL slug.
Usage: python slug.py <text>
"""

import sys
import re

def to_slug(text):
    """Convert text to URL slug."""
    # Lowercase
    slug = text.lower()
    # Replace spaces with hyphens
    slug = re.sub(r'\s+', '-', slug)
    # Remove non-alphanumeric
    slug = re.sub(r'[^a-z0-9\-]', '', slug)
    # Remove duplicate hyphens
    slug = re.sub(r'-+', '-', slug)
    # Strip hyphens from ends
    slug = slug.strip('-')
    return slug

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python slug.py <text>")
        sys.exit(1)
    
    text = ' '.join(sys.argv[1:])
    print(to_slug(text))
