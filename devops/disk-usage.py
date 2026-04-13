#!/usr/bin/env python3
"""
Disk Usage - Show disk usage statistics.
Usage: python disk-usage.py [--path PATH] [--depth N]
"""

import sys
import os
import shutil

def get_usage(path):
    """Get disk usage for path."""
    try:
        usage = shutil.disk_usage(path)
        return {
            'total': usage.total,
            'used': usage.used,
            'free': usage.free,
            'percent': (usage.used / usage.total) * 100,
        }
    except:
        return None

def format_bytes(size):
    """Format bytes to human readable."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} PB"

def dir_usage(path, depth=0, max_depth=3):
    """Show directory sizes."""
    if depth > max_depth:
        return {}
    
    sizes = {}
    try:
        entries = os.listdir(path)
    except PermissionError:
        return sizes
    
    for entry in entries:
        if entry.startswith('.'):
            continue
        full = os.path.join(path, entry)
        try:
            if os.path.isdir(full):
                total = 0
                for dirpath, dirnames, filenames in os.walk(full):
                    for f in filenames:
                        try:
                            total += os.path.getsize(os.path.join(dirpath, f))
                        except:
                            pass
                sizes[entry] = total
            else:
                sizes[entry] = os.path.getsize(full)
        except:
            pass
    
    return sizes

if __name__ == '__main__':
    path = '/'
    max_depth = 3
    
    for i, arg in enumerate(sys.argv):
        if arg == '--path' and i + 1 < len(sys.argv):
            path = sys.argv[i + 1]
        elif arg == '--depth' and i + 1 < len(sys.argv):
            max_depth = int(sys.argv[i + 1])
    
    # Overall disk usage
    usage = get_usage(path)
    
    if usage:
        print(f"=== Disk Usage: {path} ===\n")
        print(f"Total:  {format_bytes(usage['total'])}")
        print(f"Used:   {format_bytes(usage['used'])} ({usage['percent']:.1f}%)")
        print(f"Free:   {format_bytes(usage['free'])}")
        print()
        
        # Visual bar
        bar_width = 50
        filled = int(usage['percent'] / 100 * bar_width)
        bar = '█' * filled + '░' * (bar_width - filled)
        print(f"[{bar}]")
    
    # Directory sizes
    if os.path.isdir(path):
        print(f"\n=== Directory Sizes (depth {max_depth}) ===\n")
        sizes = dir_usage(path, 0, max_depth)
        
        sorted_sizes = sorted(sizes.items(), key=lambda x: x[1], reverse=True)
        
        for name, size in sorted_sizes[:20]:
            bar_len = int(size / sorted_sizes[0][1] * 20) if sorted_sizes else 0
            bar = '|' * bar_len
            print(f"{format_bytes(size):>10s}  {name[:30]:30s} {bar}")
