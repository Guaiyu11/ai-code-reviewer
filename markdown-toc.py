#!/usr/bin/env python3
"""
Markdown TOC Generator - Generate table of contents from Markdown files.
Usage: python markdown-toc.py <file.md> [--depth N] [--bullets]
"""

import sys
import os
import re

def extract_headers(content, max_depth=3):
    """Extract headers from Markdown content."""
    headers = []
    lines = content.split('\n')
    
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        # ATX-style headers (# to ######)
        match = re.match(r'^(#{1,6})\s+(.+)$', stripped)
        if match:
            level = len(match.group(1))
            if level <= max_depth:
                text = match.group(2).strip()
                # Remove inline code markers
                text = re.sub(r'`([^`]+)`', r'\1', text)
                anchor = re.sub(r'[^a-z0-9\s-]', '', text.lower())
                anchor = re.sub(r'\s+', '-', anchor)
                headers.append({
                    'level': level,
                    'text': text,
                    'anchor': anchor,
                    'line': i
                })
    
    return headers

def generate_toc(headers, bullets=False):
    """Generate TOC from headers."""
    if not headers:
        return ""
    
    lines = ['## Table of Contents', '']
    
    for h in headers:
        indent = '  ' * (h['level'] - 1)
        if bullets:
            lines.append(f'{indent}- [{h["text"]}](#{h["anchor"]})')
        else:
            lines.append(f'{indent}1. [{h["text"]}](#{h["anchor"]})')
    
    return '\n'.join(lines)

def add_anchors(content, headers):
    """Add HTML anchor tags to headers in content."""
    lines = content.split('\n')
    
    # Reverse iterate to preserve line numbers when adding
    for i in reversed(range(len(lines))):
        stripped = lines[i].strip()
        match = re.match(r'^(#{1,6})\s+(.+)$', stripped)
        if match:
            level = len(match.group(1))
            text = match.group(2).strip()
            anchor = re.sub(r'[^a-z0-9\s-]', '', text.lower())
            anchor = re.sub(r'\s+', '-', anchor)
            # Don't add anchor if already has one
            if '{#' not in text:
                lines[i] = f'<a id="{anchor}" href="#{anchor}"></a>\n{lines[i]}'
    
    return '\n'.join(lines)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python markdown-toc.py <file.md> [--depth N] [--bullets] [--inject]")
        print("\nExamples:")
        print("  python markdown-toc.py README.md              # Generate TOC")
        print("  python markdown-toc.py README.md --bullets    # Bullet-style TOC")
        print("  python markdown-toc.py README.md --depth 2   # Only H1 and H2")
        print("  python markdown-toc.py README.md --inject     # Inject TOC into file")
        sys.exit(1)
    
    filepath = sys.argv[1]
    max_depth = 3
    bullets = False
    inject = False
    
    for i, arg in enumerate(sys.argv):
        if arg == '--depth' and i + 1 < len(sys.argv):
            max_depth = int(sys.argv[i + 1])
        elif arg == '--bullets':
            bullets = True
        elif arg == '--inject':
            inject = True
    
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    headers = extract_headers(content, max_depth)
    toc = generate_toc(headers, bullets)
    
    print("=== Markdown TOC Generator ===\n")
    print(toc)
    
    if inject:
        # Insert TOC after first H1 if present
        new_content = content
        lines = content.split('\n')
        insert_line = 0
        
        for i, line in enumerate(lines):
            if re.match(r'^#\s+', line.strip()):
                insert_line = i + 1
                break
        
        toc_with_newlines = '\n' + toc + '\n'
        new_content = '\n'.join(lines[:insert_line]) + toc_with_newlines + '\n'.join(lines[insert_line:])
        
        # Add anchors
        new_content = add_anchors(new_content, headers)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"\nTOC injected into {filepath}")
