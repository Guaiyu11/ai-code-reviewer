#!/usr/bin/env python3
"""
Crontab Generator - Generate crontab syntax from human-readable schedule.
Usage: python crontab-gen.py <schedule> <command>
Schedule examples:
  every minute     -> * * * * *
  every hour       -> 0 * * * *
  every day        -> 0 0 * * *
  every week       -> 0 0 * * 0
  every month      -> 0 0 1 * *
  every weekday    -> 0 9 * * 1-5
  every 5 minutes  -> */5 * * * *
  every 30 seconds -> no standard cron, use wrapper
"""

import sys

SCHEDULES = {
    'every minute':     (None, None, None, None, None),
    'every hour':        (0, None, None, None, None),
    'every day':         (0, 0, None, None, None),
    'every week':        (0, 0, None, None, 0),
    'every month':       (0, 0, 1, None, None),
    'every weekday':     (0, 9, None, None, '1-5'),
    'every morning':     (0, 8, None, None, '1-5'),
    'every noon':        (0, 12, None, None, None),
    'every night':      (0, 22, None, None, None),
    'every midnight':   (0, 0, None, None, None),
}

def minute_of(hour):
    """Convert hour string to minute (for :30 etc)."""
    return 0

def parse_schedule(schedule_str):
    """Parse human-readable schedule to cron fields."""
    schedule_str = schedule_str.lower().strip()
    
    if schedule_str in SCHEDULES:
        return SCHEDULES[schedule_str]
    
    # Handle "every N minutes/hours"
    if 'minute' in schedule_str and 'every' in schedule_str:
        import re
        m = re.search(r'every\s+(\d+)\s+minutes?', schedule_str)
        if m:
            step = m.group(1)
            return (f'*/{step}', None, None, None, None)
    
    if 'hour' in schedule_str and 'every' in schedule_str:
        import re
        m = re.search(r'every\s+(\d+)\s+hours?', schedule_str)
        if m:
            step = m.group(1)
            return (0, f'*/{step}', None, None, None)
    
    return None

def format_cron(minute, hour, day, month, dow):
    """Format cron fields."""
    fields = [
        str(minute) if minute is not None else '*',
        str(hour) if hour is not None else '*',
        str(day) if day is not None else '*',
        str(month) if month is not None else '*',
        str(dow) if dow is not None else '*',
    ]
    return ' '.join(fields)

def generate_crontab(schedule_str, command, user=None):
    """Generate crontab entry."""
    parsed = parse_schedule(schedule_str)
    if parsed is None:
        return None, f"Unknown schedule: {schedule_str}"
    
    cron_line = format_cron(*parsed)
    entry = f"{cron_line} {command}"
    
    if user:
        entry = f"{user} {entry}"
    
    return entry, None

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python crontab-gen.py <schedule> <command> [--user USER]")
        print("\nSchedules:")
        for s in SCHEDULES:
            parsed = SCHEDULES[s]
            cron = format_cron(*parsed)
            print(f"  {s:20s} -> {cron}")
        print("\nExamples:")
        print("  python crontab-gen.py 'every day' 'backup.sh'")
        print("  python crontab-gen.py 'every 5 minutes' 'ping.sh'")
        sys.exit(1)
    
    schedule = sys.argv[1]
    command = sys.argv[2]
    user = None
    
    if '--user' in sys.argv:
        idx = sys.argv.index('--user')
        if idx + 1 < len(sys.argv):
            user = sys.argv[idx + 1]
    
    entry, error = generate_crontab(schedule, command, user)
    
    if error:
        print(f"Error: {error}")
        sys.exit(1)
    
    print(f"Schedule: {schedule}")
    print(f"Cron:     {entry}")
    print()
    print("Add to crontab:")
    print(f"  crontab -e")
    print(f"  # paste line above")
