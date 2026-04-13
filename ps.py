#!/usr/bin/env python3
"""
Process List - List running processes with filtering.
Usage: python ps.py [--user USER] [--cpu] [--mem] [--top N]
"""

import sys
import psutil
import os
from datetime import datetime

def list_processes(user=None, sort_by='pid', top=None):
    """List running processes."""
    processes = []
    
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'create_time']):
        try:
            info = proc.info
            if user and info['username'] != user:
                continue
            processes.append(info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    # Sort
    if sort_by == 'cpu':
        processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
    elif sort_by == 'mem':
        processes.sort(key=lambda x: x.get('memory_percent', 0), reverse=True)
    else:
        processes.sort(key=lambda x: x.get('pid', 0))
    
    if top:
        processes = processes[:top]
    
    return processes

def format_cpu(cpu):
    """Format CPU percent."""
    if cpu is None:
        return 'N/A'
    return f"{cpu:.1f}%"

def format_mem(mem):
    """Format memory percent."""
    if mem is None:
        return 'N/A'
    return f"{mem:.1f}%"

def format_time(timestamp):
    """Format start time."""
    if timestamp is None:
        return 'N/A'
    try:
        return datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
    except:
        return 'N/A'

if __name__ == '__main__':
    sort_by = 'pid'
    user = None
    top = None
    
    for arg in sys.argv:
        if arg == '--cpu':
            sort_by = 'cpu'
        elif arg == '--mem':
            sort_by = 'mem'
        elif arg == '--user' and len(sys.argv) > 1:
            idx = sys.argv.index(arg)
            user = sys.argv[idx + 1]
        elif arg.isdigit():
            top = int(arg)
    
    processes = list_processes(user=user, sort_by=sort_by, top=top)
    
    print(f"PID      {'Name':<25s} {'CPU%':>6s}  {'MEM%':>6s}  {'User':<20s}")
    print('-' * 90)
    
    for proc in processes:
        print(f"{proc['pid']:<8d} {proc['name']:<25s} {format_cpu(proc['cpu_percent']):>6s}  {format_mem(proc['memory_percent']):>6s}  {str(proc['username']).split('\\\\')[-1][:20]:<20s}")
    
    print(f"\nTotal: {len(processes)} processes")
