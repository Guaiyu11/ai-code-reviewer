#!/usr/bin/env python3
"""
IP Config - Show IP addresses and network info.
Usage: python ipc.py
"""

import sys
import socket
import urllib.request

def get_local_ip():
    """Get local IP address."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "unknown"

def get_public_ip():
    """Get public IP address."""
    try:
        with urllib.request.urlopen('https://api.ipify.org', timeout=5) as resp:
            return resp.read().decode().strip()
    except:
        return "unknown"

def get_hostname():
    """Get hostname."""
    return socket.gethostname()

def get_fqdn():
    """Get fully qualified domain name."""
    try:
        return socket.getfqdn()
    except:
        return "unknown"

if __name__ == '__main__':
    print("=== Network Configuration ===\n")
    print(f"Hostname:     {get_hostname()}")
    print(f"FQDN:         {get_fqdn()}")
    print(f"Local IP:     {get_local_ip()}")
    print(f"Public IP:    {get_public_ip()}")
