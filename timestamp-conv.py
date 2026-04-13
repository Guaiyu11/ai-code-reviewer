#!/usr/bin/env python3
"""
Timestamp Converter - Convert between Unix timestamps and human-readable dates.
Usage: python timestamp-conv.py [timestamp|datetime] [--to-epoch] [--to-iso] [--utc]
"""

import sys
import os
from datetime import datetime, timezone

def parse_timestamp(value):
    """Parse various timestamp formats."""
    value = value.strip()
    
    # Try as integer/float epoch
    try:
        ts = float(value)
        # Determine if seconds or milliseconds
        if ts > 1e12:
            ts = ts / 1000
        return ts
    except ValueError:
        pass
    
    # Try as ISO/datetime string
    formats = [
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%dT%H:%M:%S.%f',
        '%Y-%m-%dT%H:%M:%SZ',
        '%Y-%m-%dT%H:%M:%S.%fZ',
        '%Y/%m/%d %H:%M:%S',
        '%Y/%m/%d %H:%M',
        '%d-%m-%Y %H:%M:%S',
        '%m/%d/%Y %H:%M:%S',
        '%Y-%m-%d',
        '%d %b %Y %H:%M:%S',
        '%b %d, %Y %H:%M:%S',
    ]
    
    for fmt in formats:
        try:
            dt = datetime.strptime(value, fmt)
            return dt.timestamp()
        except ValueError:
            continue
    
    return None


def format_timestamp(ts, utc=False):
    """Format a Unix timestamp as human-readable strings."""
    dt = datetime.utcfromtimestamp(ts) if utc else datetime.fromtimestamp(ts)
    
    return {
        'unix': int(ts),
        'unix_ms': int(ts * 1000),
        'iso': dt.isoformat(),
        'iso_utc': dt.isoformat() + 'Z' if utc else dt.isoformat(),
        'utc': dt.strftime('%Y-%m-%d %H:%M:%S'),
        'local': dt.strftime('%Y-%m-%d %H:%M:%S'),
        'date': dt.strftime('%Y-%m-%d'),
        'time': dt.strftime('%H:%M:%S'),
        'relative': get_relative_time(dt),
        'weekday': dt.strftime('%A'),
        'timezone': 'UTC' if utc else 'local',
    }


def get_relative_time(dt):
    """Get human-readable relative time."""
    now = datetime.now()
    diff = now - dt
    
    seconds = diff.total_seconds()
    if seconds < 0:
        seconds = -seconds
        future = True
    else:
        future = False
    
    if seconds < 60:
        return ("in " if future else "") + f"{int(seconds)} seconds" + ("" if future else " ago")
    elif seconds < 3600:
        return ("in " if future else "") + f"{int(seconds/60)} minutes" + ("" if future else " ago")
    elif seconds < 86400:
        return ("in " if future else "") + f"{int(seconds/3600)} hours" + ("" if future else " ago")
    elif seconds < 604800:
        return ("in " if future else "") + f"{int(seconds/86400)} days" + ("" if future else " ago")
    elif seconds < 2592000:
        return ("in " if future else "") + f"{int(seconds/604800)} weeks" + ("" if future else " ago")
    else:
        return ("in " if future else "") + f"{int(seconds/2592000)} months" + ("" if future else " ago")


def now_formats():
    """Show current time in all formats."""
    ts = datetime.now().timestamp()
    print("=== Current Time ===\n")
    
    fmt = format_timestamp(ts)
    print(f"Unix (seconds):    {fmt['unix']}")
    print(f"Unix (milliseconds): {fmt['unix_ms']}")
    print(f"ISO 8601:          {fmt['iso']}")
    print(f"UTC:               {fmt['utc']}")
    print(f"Local:             {fmt['local']}")
    print(f"Relative:           {fmt['relative']}")
    print(f"Weekday:           {fmt['weekday']}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        now_formats()
        print("\n=== Usage ===")
        print("python timestamp-conv.py 1713000000       # epoch -> human")
        print("python timestamp-conv.py '2024-04-13 12:00'  # datetime -> epoch")
        print("python timestamp-conv.py now              # current time")
        sys.exit(0)
    
    value = sys.argv[1]
    utc = '--utc' in sys.argv
    to_epoch = '--to-epoch' in sys.argv
    to_iso = '--to-iso' in sys.argv
    
    if value.lower() == 'now':
        ts = datetime.now().timestamp()
        fmt = format_timestamp(ts, utc)
        print(f"Unix:    {fmt['unix']}")
        print(f"ISO:     {fmt['iso_utc']}")
        print(f"Relative: {fmt['relative']}")
        sys.exit(0)
    
    if to_epoch:
        # Convert datetime to epoch
        dt = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
        print(int(dt.timestamp()))
        sys.exit(0)
    
    if to_iso:
        ts = float(value)
        dt = datetime.fromtimestamp(ts)
        print(dt.isoformat())
        sys.exit(0)
    
    # Try to parse as timestamp or datetime
    ts = parse_timestamp(value)
    
    if ts is None:
        print(f"Error: Could not parse '{value}' as timestamp or datetime")
        sys.exit(1)
    
    fmt = format_timestamp(ts, utc)
    
    print(f"=== Timestamp: {value} ===\n")
    print(f"Unix (seconds):      {fmt['unix']}")
    print(f"Unix (milliseconds): {fmt['unix_ms']}")
    print(f"ISO 8601:            {fmt['iso']}")
    print(f"UTC:                 {fmt['utc']}")
    print(f"Local:               {fmt['local']}")
    print(f"Relative:            {fmt['relative']}")
    print(f"Weekday:             {fmt['weekday']}")
