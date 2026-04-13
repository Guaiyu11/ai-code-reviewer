#!/usr/bin/env python3
"""
PDF Info - Show PDF file metadata.
Usage: python pdf-info.py <file.pdf>
"""

import sys
import os

def pdf_info(filepath):
    """Get PDF info."""
    try:
        with open(filepath, 'rb') as f:
            header = f.read(20)
            
            if not header.startswith(b'%PDF'):
                return None, "Not a PDF file"
            
            f.seek(0, 2)
            size = f.tell()
            
            return {
                'size': size,
                'format': 'PDF',
            }, None
    except Exception as e:
        return None, str(e)

def extract_pdf_metadata(filepath):
    """Try to extract more metadata."""
    try:
        import re
        with open(filepath, 'rb') as f:
            content = f.read().decode('latin-1', errors='ignore')
        
        info = {}
        
        # Look for common metadata
        patterns = {
            'Title': r'/Title\s*\((.*?)\)',
            'Author': r'/Author\s*\((.*?)\)',
            'Creator': r'/Creator\s*\((.*?)\)',
            'Producer': r'/Producer\s*\((.*?)\)',
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, content)
            if match:
                info[key] = match.group(1)
        
        return info
    except:
        return {}

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python pdf-info.py <file.pdf>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    
    info, error = pdf_info(filepath)
    
    if error:
        print(f"Error: {error}")
        sys.exit(1)
    
    size_mb = info['size'] / 1024 / 1024
    
    print(f"=== PDF Info: {os.path.basename(filepath)} ===\n")
    print(f"Format:      PDF")
    print(f"Size:        {size_mb:.2f} MB ({info['size']:,} bytes)")
    
    metadata = extract_pdf_metadata(filepath)
    if metadata:
        print("\nMetadata:")
        for key, value in metadata.items():
            print(f"  {key}: {value}")
