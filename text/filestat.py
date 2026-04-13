#!/usr/bin/env python3
"""
File Stats - Show detailed file statistics (size, dates, type, hash).
Usage: python filestat.py <file>
"""

import sys
import os
import hashlib
from datetime import datetime

def get_file_info(filepath):
    """Get detailed file information."""
    stat = os.stat(filepath)
    
    info = {
        'path': os.path.abspath(filepath),
        'size': stat.st_size,
        'size_human': format_size(stat.st_size),
        'created': datetime.fromtimestamp(stat.st_ctime),
        'modified': datetime.fromtimestamp(stat.st_mtime),
        'accessed': datetime.fromtimestamp(stat.st_atime),
        'is_file': os.path.isfile(filepath),
        'is_dir': os.path.isdir(filepath),
    }
    
    # Extension
    _, ext = os.path.splitext(filepath)
    info['extension'] = ext.lower()
    
    # MIME type guess
    mime_types = {
        '.txt': 'text/plain',
        '.py': 'text/x-python',
        '.js': 'text/javascript',
        '.json': 'application/json',
        '.xml': 'application/xml',
        '.html': 'text/html',
        '.css': 'text/css',
        '.md': 'text/markdown',
        '.pdf': 'application/pdf',
        '.zip': 'application/zip',
        '.gz': 'application/gzip',
        '.jpg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.mp3': 'audio/mpeg',
        '.mp4': 'video/mp4',
    }
    info['mime_type'] = mime_types.get(ext.lower(), 'application/octet-stream')
    
    # Hash for small files
    if info['size'] < 10 * 1024 * 1024:  # < 10MB
        h = hashlib.sha256()
        try:
            with open(filepath, 'rb') as f:
                while chunk := f.read(8192):
                    h.update(chunk)
            info['sha256'] = h.hexdigest()
        except:
            pass
    
    return info

def format_size(size):
    """Format size in human-readable form."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} PB"

def format_datetime(dt):
    """Format datetime."""
    return dt.strftime('%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python filestat.py <file>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    
    info = get_file_info(filepath)
    
    print(f"=== File Stats: {os.path.basename(filepath)} ===\n")
    print(f"Path:      {info['path']}")
    print(f"Size:      {info['size_human']} ({info['size']:,} bytes)")
    print(f"Type:      {info['mime_type']}")
    print(f"Extension: {info['extension'] or '(none)'}")
    print()
    print(f"Created:   {format_datetime(info['created'])}")
    print(f"Modified:  {format_datetime(info['modified'])}")
    print(f"Accessed:  {format_datetime(info['accessed'])}")
    
    if 'sha256' in info:
        print()
        print(f"SHA256:    {info['sha256']}")
