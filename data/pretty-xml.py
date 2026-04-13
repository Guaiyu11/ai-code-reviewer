#!/usr/bin/env python3
"""
Pretty XML - Format XML for readability.
Usage: python pretty-xml.py <file.xml>
"""

import sys
import os

def pretty_xml(filepath):
    """Format XML."""
    import xml.dom.minidom
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    dom = xml.dom.minidom.parseString(content)
    return dom.toprettyxml(indent='  ')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python pretty-xml.py <file.xml>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    
    print(pretty_xml(filepath))
