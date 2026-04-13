#!/usr/bin/env python3
"""
Repeat - Repeat text or command N times.
Usage: python repeat.py <text|N> --times N [--command] [--delay S]
"""

import sys

def repeat_text(text, times, delay=0):
    """Repeat text."""
    for i in range(times):
        print(text)
        if delay > 0:
            import time
            time.sleep(delay)

def repeat_command(cmd, times, delay=0):
    """Repeat command."""
    import time
    import subprocess
    for i in range(times):
        print(f"[{i+1}/{times}] Running: {cmd}")
        subprocess.run(cmd, shell=True)
        if delay > 0 and i < times - 1:
            time.sleep(delay)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python repeat.py <text|N> --times N [--delay S]")
        sys.exit(1)
    
    text = sys.argv[1]
    times = 1
    delay = 0
    
    for i, arg in enumerate(sys.argv):
        if arg == '--times' and i + 1 < len(sys.argv):
            times = int(sys.argv[i + 1])
        elif arg == '--delay' and i + 1 < len(sys.argv):
            delay = float(sys.argv[i + 1])
    
    if '--command' in sys.argv:
        repeat_command(text, times, delay)
    else:
        repeat_text(text, times, delay)
