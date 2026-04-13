#!/usr/bin/env python3
"""
Uptime - Show system uptime.
Usage: python uptime.py
"""

import sys
import os
import time

if sys.platform == 'win32':
    import ctypes
    
    class LASTINPUTINFO(ctypes.Structure):
        _fields_ = [('cbSize', ctypes.c_uint), ('dwTime', ctypes.c_uint)]
    
    def get_idle_time():
        lib = ctypes.windll.user32
        lastInput = LASTINPUTINFO()
        lastInput.cbSize = ctypes.sizeof(lastInput)
        lib.GetLastInputInfo(ctypes.byref(lastInput))
        millis = (ctypes.windll.kernel32.GetTickCount() - lastInput.dwTime) / 1000.0
        return millis
else:
    def get_idle_time():
        return 0

def get_uptime():
    """Get system uptime."""
    if sys.platform == 'win32':
        import ctypes
        ticks = ctypes.windll.kernel32.GetTickCount()
        return ticks / 1000.0
    else:
        try:
            with open('/proc/uptime') as f:
                return float(f.read().split()[0])
        except:
            return 0

def format_uptime(seconds):
    """Format uptime."""
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    mins = int((seconds % 3600) // 60)
    return f"{days}d {hours}h {mins}m"

def format_idle(seconds):
    """Format idle time."""
    mins = int(seconds // 60)
    return f"{mins}m"

if __name__ == '__main__':
    uptime = get_uptime()
    print(f"System uptime: {format_uptime(uptime)}")
    
    if sys.platform == 'win32':
        idle = get_idle_time()
        print(f"User idle:     {format_idle(idle)}")
