#!/usr/bin/env python3
"""
Copy Path - Copy file path to clipboard.
Usage: python copy-path.py <path> [--unix]
"""

import sys
import os

def copy_to_clipboard(text):
    """Copy text to clipboard."""
    if sys.platform == 'win32':
        import subprocess
        subprocess.run(['clip'], input=text.encode(), check=True)
    elif sys.platform == 'darwin':
        import subprocess
        subprocess.run(['pbcopy'], input=text.encode(), check=True)
    else:
        import subprocess
        subprocess.run(['xclip', '-selection', 'clipboard'], input=text.encode(), check=True)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python copy-path.py <path> [--unix]")
        sys.exit(1)
    
    path = sys.argv[1]
    
    if not os.path.exists(path):
        print(f"Error: Path not found: {path}")
        sys.exit(1)
    
    abs_path = os.path.abspath(path)
    
    if '--unix' in sys.argv:
        abs_path = abs_path.replace('\\', '/').replace('C:', '/mnt/c')
    
    try:
        copy_to_clipboard(abs_path)
        print(f"Copied: {abs_path}")
    except Exception as e:
        print(f"Error copying to clipboard: {e}")
