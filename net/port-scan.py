#!/usr/bin/env python3
"""
Port Scan - Scan common ports on a host.
Usage: python port-scan.py <host> [--top N]
"""

import sys
import socket

COMMON_PORTS = {
    21: 'FTP',
    22: 'SSH',
    23: 'Telnet',
    25: 'SMTP',
    53: 'DNS',
    80: 'HTTP',
    110: 'POP3',
    143: 'IMAP',
    443: 'HTTPS',
    465: 'SMTPS',
    587: 'SMTP',
    993: 'IMAPS',
    995: 'POP3S',
    3306: 'MySQL',
    3389: 'RDP',
    5432: 'PostgreSQL',
    5900: 'VNC',
    6379: 'Redis',
    8080: 'HTTP-Alt',
    8443: 'HTTPS-Alt',
    27017: 'MongoDB',
}

def scan_port(host, port, timeout=1):
    """Scan single port."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def scan_ports(host, ports):
    """Scan multiple ports."""
    open_ports = []
    for port in ports:
        if scan_port(host, port):
            open_ports.append(port)
    return open_ports

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python port-scan.py <host> [--top N]")
        sys.exit(1)
    
    host = sys.argv[1]
    top_n = 20
    
    for i, arg in enumerate(sys.argv):
        if arg == '--top' and i + 1 < len(sys.argv):
            top_n = int(sys.argv[i + 1])
    
    ports = list(COMMON_PORTS.keys())[:top_n]
    
    print(f"Scanning {host} ({len(ports)} ports)...\n")
    
    open_ports = scan_ports(host, ports)
    
    if open_ports:
        print(f"Open ports found: {len(open_ports)}\n")
        for port in open_ports:
            service = COMMON_PORTS.get(port, 'Unknown')
            print(f"  Port {port:5d}: {service} (OPEN)")
    else:
        print("No open ports found")
