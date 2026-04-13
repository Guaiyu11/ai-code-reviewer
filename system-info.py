#!/usr/bin/env python3
"""
System Info - Show system information.
Usage: python system-info.py [--all]
"""

import sys
import os
import platform
import socket
import shutil
import psutil

def get_system_info():
    """Get comprehensive system information."""
    info = {}
    
    # Platform
    info['platform'] = platform.platform()
    info['system'] = platform.system()
    info['release'] = platform.release()
    info['version'] = platform.version()
    info['machine'] = platform.machine()
    info['processor'] = platform.processor()
    
    # Python
    info['python_version'] = platform.python_version()
    
    # Hostname
    info['hostname'] = socket.gethostname()
    
    try:
        info['fqdn'] = socket.getfqdn()
    except:
        info['fqdn'] = 'unknown'
    
    # CPU
    info['cpu_count'] = psutil.cpu_count()
    info['cpu_percent'] = psutil.cpu_percent(interval=1)
    
    # Memory
    mem = psutil.virtual_memory()
    info['mem_total'] = mem.total
    info['mem_used'] = mem.used
    info['mem_percent'] = mem.percent
    
    # Disk
    disk = psutil.disk_usage('/')
    info['disk_total'] = disk.total
    info['disk_used'] = disk.used
    info['disk_percent'] = disk.percent
    
    # Network
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        info['local_ip'] = s.getsockname()[0]
        s.close()
    except:
        info['local_ip'] = 'unknown'
    
    return info

def format_bytes(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} PB"

def print_info(info):
    """Print system information."""
    print("=== System Information ===\n")
    
    print(f"Platform:    {info['platform']}")
    print(f"Hostname:    {info['hostname']}")
    print(f"Python:      {info['python_version']}")
    print()
    
    print("=== CPU ===\n")
    print(f"Cores:       {info['cpu_count']} (logical)")
    print(f"Usage:       {info['cpu_percent']}%")
    print()
    
    print("=== Memory ===\n")
    print(f"Total:       {format_bytes(info['mem_total'])}")
    print(f"Used:        {format_bytes(info['mem_used'])} ({info['mem_percent']:.1f}%)")
    print()
    
    print("=== Disk ===\n")
    print(f"Total:       {format_bytes(info['disk_total'])}")
    print(f"Used:        {format_bytes(info['disk_used'])} ({info['disk_percent']:.1f}%)")
    print()
    
    print("=== Network ===\n")
    print(f"Local IP:    {info['local_ip']}")

if __name__ == '__main__':
    try:
        info = get_system_info()
        print_info(info)
    except ImportError:
        print("System info requires psutil: pip install psutil")
