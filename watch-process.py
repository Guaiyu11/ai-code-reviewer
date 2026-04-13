#!/usr/bin/env python3
"""
Watch Process - Monitor a process's CPU and memory usage.
Usage: python watch-process.py <pid> [--interval N]
"""

import sys
import psutil
import time

def watch_process(pid, interval=2):
    """Watch process stats."""
    try:
        proc = psutil.Process(pid)
        print(f"Watching: {proc.name()} (PID {pid})")
        print(f"Interval: {interval}s\n")
        
        while True:
            try:
                cpu = proc.cpu_percent(interval=0.1)
                mem = proc.memory_info()
                mem_mb = mem.rss / 1024 / 1024
                threads = proc.num_threads()
                status = proc.status()
                
                print(f"CPU: {cpu:5.1f}%  MEM: {mem_mb:7.1f} MB  Threads: {threads}  Status: {status}")
                time.sleep(interval)
            except psutil.NoSuchProcess:
                print(f"\nProcess {pid} has exited")
                break
    except psutil.NoSuchProcess:
        print(f"Process {pid} not found")
    except KeyboardInterrupt:
        print("\nStopped")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python watch-process.py <pid> [--interval N]")
        sys.exit(1)
    
    pid = int(sys.argv[1])
    interval = 2
    
    for i, arg in enumerate(sys.argv):
        if arg == '--interval' and i + 1 < len(sys.argv):
            interval = float(sys.argv[i + 1])
    
    watch_process(pid, interval)
