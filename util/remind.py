#!/usr/bin/env python3
"""
Reminder - Set a reminder to notify after a duration.
Usage: python remind.py <seconds|minutes|hours> <message>
Example: python remind.py 30 "Check the oven"
"""

import sys
import time
import os

def notify(message):
    """Send system notification."""
    if sys.platform == 'darwin':
        os.system(f"osascript -e 'display notification \"{message}\" with title \"Reminder\"'")
    elif sys.platform == 'win32':
        os.system(f'msgsrv * \"{message}\"')
    else:
        print(f"\a\a\a{message}")
        print("\n=== REMINDER ===")
        print(message)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python remind.py <duration> <message>")
        print("\nExample:")
        print("  python remind.py 30 'Check oven'")
        print("  python remind.py 2h 'Meeting in 2 hours'")
        print("  python remind.py 30m 'Break time'")
        sys.exit(1)
    
    duration_str = sys.argv[1]
    message = ' '.join(sys.argv[2:])
    
    # Parse duration
    multiplier = 1
    if duration_str.endswith('s'):
        multiplier = 1
        duration_str = duration_str[:-1]
    elif duration_str.endswith('m'):
        multiplier = 60
        duration_str = duration_str[:-1]
    elif duration_str.endswith('h'):
        multiplier = 3600
        duration_str = duration_str[:-1]
    
    try:
        duration = int(duration_str) * multiplier
    except:
        print(f"Invalid duration: {duration_str}")
        sys.exit(1)
    
    print(f"Reminder set for {duration} seconds...")
    time.sleep(duration)
    notify(message)
