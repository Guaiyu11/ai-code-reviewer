#!/usr/bin/env python3
"""
API Docs Generator - Generate Markdown API documentation from Python source.
Usage: python api-docs-gen.py <source_file.py> [--output README_API.md]
"""

import sys
import os
import re

def parse_python_docstring(content):
    """Parse a Python file and extract functions/classes with docstrings."""
    lines = content.split('\n')
    items = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # Class definition
        if stripped.startswith('class ') and '(' in stripped:
            name = stripped.split('(')[0].replace('class ', '')
            indent = len(line) - len(line.lstrip())
            docstring = extract_docstring(lines, i + 1)
            items.append({'type': 'class', 'name': name, 'doc': docstring, 'indent': indent})
            i += 1
            # Skip to end of class
            while i < len(lines) and (lines[i].strip() == '' or lines[i].startswith(' ' * (indent + 1)) or lines[i].startswith('\t')):
                if stripped := lines[i].strip():
                    if stripped.startswith('def ') or stripped.startswith('class '):
                        break
                i += 1
            continue
        
        # Function definition
        if stripped.startswith('def ') and '(' in stripped:
            name = stripped.split('(')[0].replace('def ', '')
            indent = len(line) - len(line.lstrip())
            docstring = extract_docstring(lines, i + 1)
            
            # Extract params
            params_str = stripped.split('(', 1)[1].rstrip('):')
            params = []
            for p in params_str.split(','):
                p = p.strip()
                if p and p != 'self':
                    # Handle default values
                    if '=' in p:
                        p = p.split('=')[0].strip()
                    params.append(p.strip())
            
            items.append({
                'type': 'function',
                'name': name,
                'params': params,
                'doc': docstring
            })
        
        i += 1
    
    return items


def extract_docstring(lines, start):
    """Extract docstring starting from line after def/class."""
    if start >= len(lines):
        return None
    
    stripped = lines[start].strip()
    
    # Triple quote docstring
    if stripped.startswith('"""') or stripped.startswith("'''"):
        quote = stripped[:3]
        if stripped.count(quote) >= 2:
            # Single line
            return stripped.strip(quote).strip()
        
        # Multi-line
        doc_lines = []
        for j in range(start + 1, len(lines)):
            if quote in lines[j]:
                break
            doc_lines.append(lines[j].strip())
        return ' '.join(doc_lines) if doc_lines else None
    
    return None


def generate_markdown(items, title=None):
    """Generate Markdown documentation."""
    md_lines = []
    
    if title:
        md_lines.append(f"# {title}")
        md_lines.append("")
    
    md_lines.append("## API Reference")
    md_lines.append("")
    
    classes = [i for i in items if i['type'] == 'class']
    functions = [i for i in items if i['type'] == 'function']
    
    if classes:
        md_lines.append("### Classes")
        md_lines.append("")
        for cls in classes:
            md_lines.append(f"#### `{cls['name']}`")
            md_lines.append("")
            if cls['doc']:
                md_lines.append(f"{cls['doc']}")
            else:
                md_lines.append("*No documentation.*")
            md_lines.append("")
    
    if functions:
        md_lines.append("### Functions")
        md_lines.append("")
        for func in functions:
            params = ', '.join(func.get('params', []))
            md_lines.append(f"#### `{func['name']}({params})`")
            md_lines.append("")
            if func.get('doc'):
                md_lines.append(f"{func['doc']}")
            else:
                md_lines.append("*No documentation.*")
            md_lines.append("")
    
    return '\n'.join(md_lines)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python api-docs-gen.py <source_file.py> [--output OUTPUT.md]")
        sys.exit(1)
    
    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    
    output = None
    for i, arg in enumerate(sys.argv):
        if arg == '--output' and i + 1 < len(sys.argv):
            output = sys.argv[i + 1]
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    items = parse_python_docstring(content)
    
    title = f"API Documentation: {os.path.basename(filepath)}"
    md = generate_markdown(items, title)
    
    if output:
        with open(output, 'w', encoding='utf-8') as f:
            f.write(md)
        print(f"Generated: {output}")
    else:
        print(md)
