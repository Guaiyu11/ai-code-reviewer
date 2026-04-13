#!/usr/bin/env python3
"""
World Time - Show current time in multiple timezones.
Usage: python worldtime.py [--list] [tz1 tz2 tz3 ...]
"""

import sys
from datetime import datetime
import os

try:
    import pytz
    HAS_PYTZ = True
except:
    HAS_PYTZ = False

COMMON_TZ = [
    'America/New_York',
    'America/Los_Angeles',
    'America/Chicago',
    'Europe/London',
    'Europe/Paris',
    'Europe/Berlin',
    'Asia/Tokyo',
    'Asia/Shanghai',
    'Asia/Singapore',
    'Asia/Dubai',
    'Australia/Sydney',
    'Pacific/Auckland',
    'UTC',
]

def get_timezones(tz_list):
    """Get current time for list of timezones."""
    if not HAS_PYTZ:
        return "pytz not installed (pip install pytz)"
    
    import pytz
    results = []
    for tz_name in tz_list:
        try:
            tz = pytz.timezone(tz_name)
            now = datetime.now(tz)
            results.append(f"{tz_name:30s} {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        except:
            results.append(f"{tz_name:30s} INVALID")
    return '\n'.join(results)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python worldtime.py [--list] [tz1 tz2 ...]")
        print("\nCommon timezones:")
        for tz in COMMON_TZ:
            print(f"  {tz}")
        sys.exit(0)
    
    if '--list' in sys.argv:
        for tz in COMMON_TZ:
            print(tz)
    else:
        tzs = [a for a in sys.argv[1:] if not a.startswith('--')]
        if not tzs:
            tzs = COMMON_TZ[:6]
        print(get_timezones(tzs))
