#!/usr/bin/env python3
"""
Stopwatch / Timer - Simple CLI stopwatch and countdown timer.
Usage: python stopwatch.py [--countdown SECONDS] [--interval SECONDS] [--command CMD]
"""

import sys
import os
import time
import subprocess
from datetime import datetime, timedelta

def stopwatch():
    """Run a simple stopwatch."""
    print("Press Ctrl+C to stop\n")
    start = time.time()
    try:
        while True:
            elapsed = time.time() - start
            mins, secs = divmod(int(elapsed), 60)
            hours, mins = divmod(mins, 60)
            print(f"\r{hours:02d}:{mins:02d}:{secs:02d}", end='', flush=True)
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n\nTotal: {elapsed:.2f} seconds")

def countdown(seconds):
    """Run a countdown timer."""
    print(f"Countdown: {seconds} seconds")
    print("Press Ctrl+C to cancel\n")
    
    end = time.time() + seconds
    try:
        while True:
            remaining = end - time.time()
            if remaining <= 0:
                print("\r00:00:00")
                print("\aBEEP! Time's up!")
                return
            mins, secs = divmod(int(remaining), 60)
            hours, mins = divmod(mins, 60)
            print(f"\r{hours:02d}:{mins:02d}:{secs:02d}", end='', flush=True)
            time.sleep(1)
    except KeyboardInterrupt:
        remaining = end - time.time()
        print(f"\n\nCancelled. {remaining:.1f} seconds remaining.")

def interval_timer(interval, command=None):
    """Run a command at regular intervals."""
    print(f"Interval: {interval} seconds")
    if command:
        print(f"Command: {command}")
    print("Press Ctrl+C to stop\n")
    
    next_run = time.time() + interval
    count = 0
    try:
        while True:
            now = time.time()
            if now >= next_run:
                count += 1
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Run #{count}")
                if command:
                    result = subprocess.run(command, shell=True, capture_output=True, text=True)
                    if result.stdout:
                        print(result.stdout[:500].strip())
                    if result.returncode != 0 and result.stderr:
                        print(f"Error: {result.stderr[:200].strip()}")
                next_run = now + interval
            time.sleep(0.1)
    except KeyboardInterrupt:
        print(f"\n\nStopped after {count} runs.")

if __name__ == '__main__':
    countdown_secs = None
    interval_secs = None
    command = None
    
    for i, arg in enumerate(sys.argv):
        if arg == '--countdown' and i + 1 < len(sys.argv):
            countdown_secs = int(sys.argv[i + 1])
        elif arg == '--interval' and i + 1 < len(sys.argv):
            interval_secs = int(sys.argv[i + 1])
        elif arg == '--command' and i + 1 < len(sys.argv):
            command = sys.argv[i + 1]
    
    if countdown_secs:
        countdown(countdown_secs)
    elif interval_secs:
        interval_timer(interval_secs, command)
    else:
        print("Usage: python stopwatch.py [--countdown SECONDS] [--interval SECONDS --command CMD]")
        print("\nExamples:")
        print("  python stopwatch.py                    # Stopwatch")
        print("  python stopwatch.py --countdown 60    # 60 second countdown")
        print("  python stopwatch.py --interval 30 --command 'echo done'  # Every 30s")
        print("\nPress Ctrl+C to stop")
        print()
        stopwatch()
