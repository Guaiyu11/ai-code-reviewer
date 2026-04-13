#!/usr/bin/env python3
"""
Open Path - Open file or URL in default application.
Usage: python open-path.py <path|url>
"""

import sys
import os
import webbrowser

def open_path(path):
    """Open file or URL."""
    if path.startswith(('http://', 'https://', 'file://')):
        webbrowser.open(path)
    elif os.path.exists(path):
        full_path = os.path.abspath(path)
        if sys.platform == 'win32':
            os.startfile(full_path)
        elif sys.platform == 'darwin':
            import subprocess
            subprocess.run(['open', full_path])
        else:
            import subprocess
            subprocess.run(['xdg-open', full_path])
    else:
        print(f"Path not found: {path}")
        return
    
    print(f"Opened: {path}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python open-path.py <path|url>")
        sys.exit(1)
    
    open_path(sys.argv[1])
