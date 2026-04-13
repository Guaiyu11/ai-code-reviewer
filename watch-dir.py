#!/usr/bin/env python3
"""
Watch Files - Monitor files for changes.
Usage: python watch-files.py <directory> [--ext py|js] [--command CMD]
"""

import sys
import os
import time
import hashlib

def get_file_hash(filepath):
    """Get file hash."""
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()

def watch_directory(directory, extensions=None, command=None):
    """Watch directory for file changes."""
    import subprocess
    
    hashes = {}
    
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for f in files:
            if f.startswith('.'):
                continue
            ext = os.path.splitext(f)[1].lower()
            if extensions and ext not in extensions:
                continue
            filepath = os.path.join(root, f)
            try:
                hashes[filepath] = get_file_hash(filepath)
            except:
                pass
    
    print(f"Watching {len(hashes)} files. Press Ctrl+C to stop.\n")
    
    while True:
        changes = []
        
        for filepath in list(hashes.keys()):
            try:
                new_hash = get_file_hash(filepath)
                if new_hash != hashes[filepath]:
                    changes.append(filepath)
                    hashes[filepath] = new_hash
            except FileNotFoundError:
                changes.append(f"{filepath} (deleted)")
                del hashes[filepath]
            except:
                pass
        
        if changes:
            print(f"Changes detected:")
            for c in changes:
                print(f"  {c}")
            
            if command:
                subprocess.run(command, shell=True)
        
        time.sleep(2)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python watch-files.py <directory> [--ext py|js] [--command CMD]")
        sys.exit(1)
    
    directory = sys.argv[1]
    extensions = None
    command = None
    
    for i, arg in enumerate(sys.argv):
        if arg == '--ext' and i + 1 < len(sys.argv):
            ext = sys.argv[i + 1].lower()
            if not ext.startswith('.'):
                ext = '.' + ext
            extensions = {ext}
        elif arg == '--command' and i + 1 < len(sys.argv):
            command = sys.argv[i + 1]
    
    if not os.path.isdir(directory):
        print(f"Error: Not a directory: {directory}")
        sys.exit(1)
    
    watch_directory(directory, extensions, command)
