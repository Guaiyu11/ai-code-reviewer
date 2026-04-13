#!/usr/bin/env python3
"""
Hex Viewer - View file in hexadecimal with ASCII sidebar.
Usage: python hexview.py <file> [--offset N] [--length N]
"""

import sys
import os

def hex_dump(filepath, offset=0, length=None):
    """Generate hex dump of file."""
    with open(filepath, 'rb') as f:
        if offset:
            f.seek(offset)
        data = f.read(length)
    
    result = []
    for i in range(0, len(data), 16):
        chunk = data[i:i+16]
        
        addr = f"{offset + i:08x}"
        
        hex_part = ''
        ascii_part = ''
        for j, byte in enumerate(chunk):
            hex_part += f"{byte:02x} "
            if j == 7:
                hex_part += ' '
            if 32 <= byte < 127:
                ascii_part += chr(byte)
            else:
                ascii_part += '.'
        
        hex_part = hex_part.ljust(42)
        hex_part += ' ' + ascii_part
        
        result.append(f"{addr}  {hex_part}")
    
    return '\n'.join(result)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python hexview.py <file> [--offset N] [--length N]")
        sys.exit(1)
    
    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    
    offset = 0
    length = 256
    
    for i, arg in enumerate(sys.argv):
        if arg == '--offset' and i + 1 < len(sys.argv):
            offset = int(sys.argv[i + 1])
        elif arg == '--length' and i + 1 < len(sys.argv):
            length = int(sys.argv[i + 1])
    
    dump = hex_dump(filepath, offset, length)
    print(dump)
