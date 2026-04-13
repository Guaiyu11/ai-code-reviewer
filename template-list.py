#!/usr/bin/env python3
"""
Template List - List all files in directory with template detection.
Usage: python template-list.py <directory>
"""

import sys
import os

TEMPLATE_EXTS = {'.html', '.htm', '.jinja', '.jinja2', '.tpl', '.twig', '.handlebars', '.hbs'}

def list_templates(path):
    """List template files."""
    results = []
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for f in files:
            if f.startswith('.'):
                continue
            ext = os.path.splitext(f)[1].lower()
            if ext in TEMPLATE_EXTS or 'template' in f.lower() or 'layout' in f.lower():
                full = os.path.join(root, f)
                results.append(full)
    return results

if __name__ == '__main__':
    if len(sys.argv) < 2:
        path = '.'
    else:
        path = sys.argv[1]
    
    templates = list_templates(path)
    
    print(f"=== Templates in {path} ===\n")
    print(f"Found: {len(templates)} template files\n")
    
    for t in templates[:50]:
        print(os.path.relpath(t, path))
