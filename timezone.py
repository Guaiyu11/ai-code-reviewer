#!/usr/bin/env python3
"""
Timezone Convert - Convert times between timezones.
Usage: python timezone.py <time> <from_tz> <to_tz>
Example: python timezone.py "10:00" America/New_York Europe/London
"""

import sys

def convert_time(time_str, from_tz, to_tz):
    """Convert time between timezones."""
    try:
        from datetime import datetime
        import pytz
        
        # Parse time (assume today)
        today = datetime.now().strftime('%Y-%m-%d')
        naive_dt = datetime.strptime(f"{today} {time_str}", '%Y-%m-%d %H:%M')
        
        # Apply source timezone
        from_tz_obj = pytz.timezone(from_tz)
        naive_dt = from_tz_obj.localize(naive_dt)
        
        # Convert to target timezone
        to_tz_obj = pytz.timezone(to_tz)
        target_dt = naive_dt.astimezone(to_tz_obj)
        
        return target_dt.strftime('%H:%M %Z')
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python timezone.py <time> <from_tz> <to_tz>")
        print("\nExample: python timezone.py 10:00 America/New_York Europe/London")
        sys.exit(1)
    
    time_str = sys.argv[1]
    from_tz = sys.argv[2]
    to_tz = sys.argv[3]
    
    result = convert_time(time_str, from_tz, to_tz)
    print(f"{time_str} {from_tz} = {result}")
