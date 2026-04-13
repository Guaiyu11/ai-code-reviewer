#!/usr/bin/env python3
"""
Cron Expression Parser - Parse, validate, and explain cron expressions.
Usage: python cron-parser.py "<expression>" [--next N]
Examples:
  python cron-parser.py "0 * * * *"           # Every hour
  python cron-parser.py "0 9 * * 1-5"         # Weekdays at 9am
  python cron-parser.py "*/15 * * * *"         # Every 15 min
"""

import sys
import re
from datetime import datetime, timedelta

FIELDS = ['minute', 'hour', 'day_of_month', 'month', 'day_of_week']

FIELD_RANGES = {
    'minute': (0, 59),
    'hour': (0, 23),
    'day_of_month': (1, 31),
    'month': (1, 12),
    'day_of_week': (0, 6),
}

WEEKDAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']


def parse_field(field_str, field_name):
    """Parse a single cron field and return set of values."""
    min_val, max_val = FIELD_RANGES[field_name]
    values = set()
    
    # Handle wildcard
    if field_str == '*':
        return set(range(min_val, max_val + 1))
    
    # Handle step values
    if '/' in field_str:
        parts = field_str.split('/')
        base = parts[0]
        step = int(parts[1])
        if base == '*':
            base_range = range(min_val, max_val + 1)
        elif '-' in base:
            start, end = map(int, base.split('-'))
            base_range = range(start, end + 1)
        else:
            base_range = range(int(base), max_val + 1)
        return set(base_range[::step])
    
    # Handle ranges
    if '-' in field_str and ',' not in field_str:
        start, end = map(int, field_str.split('-'))
        return set(range(start, end + 1))
    
    # Handle lists
    parts = field_str.split(',')
    for part in parts:
        if '-' in part:
            start, end = map(int, part.split('-'))
            values.update(range(start, end + 1))
        else:
            values.add(int(part))
    
    return values


def parse_cron(expression):
    """Parse a cron expression into field values."""
    parts = expression.strip().split()
    if len(parts) != 5:
        return None
    
    result = {}
    for i, field_name in enumerate(FIELDS):
        try:
            result[field_name] = parse_field(parts[i], field_name)
        except:
            return None
    
    return result


def explain_field(field_name, values):
    """Human-readable explanation of a cron field."""
    if values == set(range(FIELD_RANGES[field_name][0], FIELD_RANGES[field_name][1] + 1)):
        return 'every ' + field_name.replace('_', ' ')
    
    if field_name == 'minute':
        if values == {0}:
            return 'at minute 0'
        elif len(values) == 1:
            return f'at minute {list(values)[0]}'
        elif values == set(range(0, 60, 5)):
            return 'every 5 minutes'
        elif values == set(range(0, 60, 15)):
            return 'every 15 minutes'
        elif values == set(range(0, 60, 30)):
            return 'every 30 minutes'
        else:
            return f'every {", ".join(map(str, sorted(values)))} minutes'
    
    if field_name == 'hour':
        if len(values) == 1:
            return f'at hour {list(values)[0]}:00'
        sorted_hours = sorted(values)
        return f'at hours {", ".join(map(str, sorted_hours))}'
    
    if field_name == 'day_of_month':
        return f'on day {", ".join(map(str, sorted(values)))} of month'
    
    if field_name == 'month':
        return f'in {", ".join(MONTHS[v-1] for v in sorted(values))}'
    
    if field_name == 'day_of_week':
        return f'on {", ".join(WEEKDAYS[v] for v in sorted(values))}'
    
    return str(values)


def explain_cron(expression):
    """Explain a cron expression in plain English."""
    parsed = parse_cron(expression)
    if not parsed:
        return "Invalid cron expression"
    
    parts = []
    for field_name in FIELDS:
        parts.append(explain_field(field_name, parsed[field_name]))
    
    return ' | '.join(parts)


def next_runs(expression, n=5):
    """Find the next N runs of a cron expression."""
    parsed = parse_cron(expression)
    if not parsed:
        return ["Invalid cron expression"]
    
    runs = []
    current = datetime.now().replace(second=0, microsecond=0)
    current += timedelta(minutes=1)
    
    while len(runs) < n:
        # Check if current time matches all fields
        match = (
            current.minute in parsed['minute'] and
            current.hour in parsed['hour'] and
            current.day in parsed['day_of_month'] and
            current.month in parsed['month'] and
            current.weekday() in parsed['day_of_week']
        )
        
        if match:
            runs.append(current.strftime('%Y-%m-%d %H:%M (%A)'))
        
        # Fast forward
        if current.minute not in parsed['minute']:
            # Jump to next interesting minute
            mins = sorted(parsed['minute'])
            next_min = next((m for m in mins if m > current.minute), mins[0])
            if next_min <= current.minute:
                current += timedelta(hours=1)
            current = current.replace(minute=next_min)
        elif current.hour not in parsed['hour']:
            hours = sorted(parsed['hour'])
            next_hour = next((h for h in hours if h > current.hour), hours[0] + 24)
            current = current.replace(hour=next_hour % 24)
            if next_hour >= 24:
                current += timedelta(days=1)
        else:
            current += timedelta(minutes=1)
        
        # Safety limit
        if current > datetime.now() + timedelta(days=366):
            break
    
    return runs


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python cron-parser.py \"<cron_expr>\" [--next N]")
        print("\nFormat: minute hour day_of_month month day_of_week")
        print("Examples:")
        print('  0 * * * *         Every hour')
        print('  0 9 * * 1-5       Weekdays at 9am')
        print('  */15 * * * *      Every 15 minutes')
        print('  0 0 1 * *         First day of every month')
        sys.exit(1)
    
    expression = sys.argv[1]
    n_next = 5
    
    for i, arg in enumerate(sys.argv):
        if arg == '--next' and i + 1 < len(sys.argv):
            n_next = int(sys.argv[i + 1])
    
    # Validate format
    parts = expression.strip().split()
    if len(parts) != 5:
        print(f"Invalid: cron expression must have exactly 5 fields")
        print(f"Got {len(parts)} fields: {parts}")
        sys.exit(1)
    
    print(f"=== Cron Expression: {expression} ===\n")
    
    explanation = explain_cron(expression)
    print(f"Schedule: {explanation}")
    print()
    
    print(f"Next {n_next} runs:")
    for run in next_runs(expression, n_next):
        print(f"  {run}")
