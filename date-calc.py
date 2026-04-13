#!/usr/bin/env python3
"""
Date Calc - Calculate dates and time differences.
Usage: python date-calc.py <date> [--add DAYS] [--diff DATE1 DATE2]
"""

import sys
from datetime import datetime, timedelta

def add_days(date_str, days):
    """Add days to date."""
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    result = dt + timedelta(days=days)
    return result.strftime('%Y-%m-%d')

def diff_dates(date1, date2):
    """Get difference between dates."""
    d1 = datetime.strptime(date1, '%Y-%m-%d')
    d2 = datetime.strptime(date2, '%Y-%m-%d')
    delta = abs((d2 - d1).days)
    return delta

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python date-calc.py <date> [--add DAYS] [--diff DATE1 DATE2]")
        sys.exit(1)
    
    date = sys.argv[1]
    
    if '--add' in sys.argv:
        idx = sys.argv.index('--add')
        days = int(sys.argv[idx + 1])
        print(add_days(date, days))
    elif '--diff' in sys.argv:
        idx = sys.argv.index('--diff')
        d1 = sys.argv[idx + 1]
        d2 = sys.argv[idx + 2]
        print(f"Difference: {diff_dates(d1, d2)} days")
    else:
        dt = datetime.strptime(date, '%Y-%m-%d')
        print(f"Weekday: {dt.strftime('%A')}")
        print(f"Day of year: {dt.timetuple().tm_yday}")
        print(f"Week number: {dt.isocalendar()[1]}")
