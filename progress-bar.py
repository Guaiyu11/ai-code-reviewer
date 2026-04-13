#!/usr/bin/env python3
"""
Progress Bar - Show progress bar in terminal.
Usage: python progress-bar.py [--total N] [--desc TEXT]
"""

import sys
import time

def progress_bar(current, total, width=50, desc=''):
    """Draw a progress bar."""
    if total == 0:
        percent = 100
    else:
        percent = min(100, int(current / total * 100))
    
    filled = int(width * percent / 100)
    bar = '█' * filled + '░' * (width - filled)
    
    prefix = f"\r{desc}: " if desc else "\rProgress: "
    sys.stdout.write(f"{prefix}[{bar}] {percent}% ({current}/{total})")
    sys.stdout.flush()

def interactive(total, interval=0.1, desc='Progress'):
    """Interactive progress simulation."""
    for i in range(total + 1):
        progress_bar(i, total, desc=desc)
        time.sleep(interval)
    print()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--total', type=int, default=100)
    parser.add_argument('--desc', default='')
    parser.add_argument('--interval', type=float, default=0.05)
    args = parser.parse_args()
    
    interactive(args.total, args.interval, args.desc)
