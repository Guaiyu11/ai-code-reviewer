#!/usr/bin/env python3
"""
Strftime - Format dates with various format codes.
Usage: python strftime.py [--format FORMAT] [--tz TIMEZONE]
"""

import sys
from datetime import datetime

FORMATS = {
    'date': '%Y-%m-%d',
    'time': '%H:%M:%S',
    'datetime': '%Y-%m-%d %H:%M:%S',
    'iso': '%Y-%m-%dT%H:%M:%S',
    'us': '%m/%d/%Y',
    'eu': '%d/%m/%Y',
    'long': '%B %d, %Y',
    'short': '%b %d, %Y',
    'unix': None,  # Special
    'epoch': None,  # Same as unix
}

def format_date(fmt, dt=None):
    """Format date."""
    if fmt in ('unix', 'epoch'):
        return str(int(dt.timestamp()))
    return dt.strftime(fmt)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        # Show all formats for current time
        now = datetime.now()
        print(f"=== Current Date/Time: {now} ===\n")
        for name, fmt in FORMATS.items():
            result = format_date(fmt, now) if fmt else format_date(name, now)
            print(f"{name:12s}: {result}")
    else:
        fmt = sys.argv[1]
        dt = datetime.now()
        print(format_date(fmt, dt))
