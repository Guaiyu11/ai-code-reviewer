#!/usr/bin/env python3
"""
Now - Show current timestamp in multiple formats.
Usage: python now.py [--unix|--iso|--date|--time]
"""

import sys
from datetime import datetime

now = datetime.now()

if '--unix' in sys.argv:
    print(int(now.timestamp()))
elif '--iso' in sys.argv:
    print(now.isoformat())
elif '--date' in sys.argv:
    print(now.strftime('%Y-%m-%d'))
elif '--time' in sys.argv:
    print(now.strftime('%H:%M:%S'))
else:
    print(f"Unix:       {int(now.timestamp())}")
    print(f"ISO:         {now.isoformat()}")
    print(f"Date:        {now.strftime('%Y-%m-%d')}")
    print(f"Time:        {now.strftime('%H:%M:%S')}")
    print(f"RFC3339:     {now.strftime('%Y-%m-%dT%H:%M:%S')}")
