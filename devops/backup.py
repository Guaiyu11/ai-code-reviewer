#!/usr/bin/env python3
"""
Backup - Create timestamped backup copies of files.
Usage: python backup.py <file> [--restore]
"""

import sys
import os
import shutil
from datetime import datetime

def backup_file(filepath):
    """Create timestamped backup."""
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        return None
    
    base, ext = os.path.splitext(filepath)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = f"{base}.{timestamp}{ext}"
    
    shutil.copy2(filepath, backup_path)
    return backup_path

def restore_latest(filepath):
    """Restore from latest backup."""
    base, ext = os.path.splitext(filepath)
    dir_path = os.path.dirname(filepath) or '.'
    name = os.path.basename(base)
    
    backups = []
    for f in os.listdir(dir_path):
        if f.startswith(name) and f != os.path.basename(filepath):
            backups.append(f)
    
    if not backups:
        print("No backups found")
        return
    
    backups.sort()
    latest = backups[-1]
    latest_path = os.path.join(dir_path, latest)
    
    shutil.copy2(latest_path, filepath)
    print(f"Restored {latest} -> {filepath}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python backup.py <file> [--restore]")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    if '--restore' in sys.argv:
        restore_latest(filepath)
    else:
        backup = backup_file(filepath)
        if backup:
            print(f"Backed up: {backup}")
