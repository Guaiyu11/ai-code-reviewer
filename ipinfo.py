#!/usr/bin/env python3
"""
IP Info - Lookup IP address information (geo, hostname, ASN).
Usage: python ipinfo.py [ip|hostname]
"""

import sys
import socket

def lookup_ip(target):
    """Get IP info for target."""
    try:
        # Check if it's already an IP
        try:
            socket.inet_aton(target)
            ip = target
        except:
            # Resolve hostname
            ip = socket.gethostbyname(target)
        
        hostname = socket.getfqdn(ip)
        
        return {
            'ip': ip,
            'hostname': hostname,
        }
    except Exception as e:
        return {'error': str(e)}

def local_ips():
    """Get local IP addresses."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return None

if __name__ == '__main__':
    if len(sys.argv) < 2:
        local = local_ips()
        print(f"Local IP: {local or 'unknown'}")
        print(f"\nUsage: python ipinfo.py <ip|hostname>")
        sys.exit(0)
    
    target = sys.argv[1]
    info = lookup_ip(target)
    
    print("=== IP Info ===\n")
    
    if 'error' in info:
        print(f"Error: {info['error']}")
    else:
        print(f"IP:      {info['ip']}")
        print(f"Hostname: {info['hostname']}")
