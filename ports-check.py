#!/usr/bin/env python3
"""
Ports Check - Check if common ports are open on localhost or a target host.
Usage: python ports-check.py [--host HOST] [--port PORT] [--range START END]
"""

import sys
import socket
import concurrent.futures
from datetime import datetime

COMMON_PORTS = {
    20: 'FTP Data',
    21: 'FTP Control',
    22: 'SSH',
    23: 'Telnet',
    25: 'SMTP',
    53: 'DNS',
    80: 'HTTP',
    110: 'POP3',
    143: 'IMAP',
    443: 'HTTPS',
    465: 'SMTPS',
    587: 'SMTP Submission',
    993: 'IMAPS',
    995: 'POP3S',
    1433: 'MSSQL',
    1521: 'Oracle DB',
    3306: 'MySQL',
    5432: 'PostgreSQL',
    5900: 'VNC',
    6379: 'Redis',
    8080: 'HTTP Alt',
    8443: 'HTTPS Alt',
    27017: 'MongoDB',
    11211: 'Memcached',
}


def check_port(host, port, timeout=2):
    """Check if a port is open on a host."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False


def scan_ports(host, ports, workers=50):
    """Scan multiple ports concurrently."""
    open_ports = []
    closed_ports = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(check_port, host, port): port for port in ports}
        for future in concurrent.futures.as_completed(futures):
            port = futures[future]
            try:
                is_open = future.result()
                if is_open:
                    open_ports.append(port)
                else:
                    closed_ports.append(port)
            except:
                closed_ports.append(port)
    
    return sorted(open_ports), sorted(closed_ports)


if __name__ == '__main__':
    host = 'localhost'
    ports = None
    timeout = 2
    
    for i, arg in enumerate(sys.argv):
        if arg == '--host' and i + 1 < len(sys.argv):
            host = sys.argv[i + 1]
        elif arg == '--port' and i + 1 < len(sys.argv):
            port = int(sys.argv[i + 1])
            ports = [port]
        elif arg == '--range' and i + 2 < len(sys.argv):
            start = int(sys.argv[i + 1])
            end = int(sys.argv[i + 2])
            ports = list(range(start, end + 1))
        elif arg == '--all':
            ports = list(COMMON_PORTS.keys())
    
    if ports is None:
        ports = list(COMMON_PORTS.keys())
    
    print(f"=== Port Scanner: {host} ===")
    print(f"Scanning {len(ports)} ports...\n")
    
    start_time = datetime.now()
    open_ports, closed = scan_ports(host, ports)
    elapsed = (datetime.now() - start_time).total_seconds()
    
    print(f"Completed in {elapsed:.2f}s\n")
    
    if open_ports:
        print(f"🟢 OPEN PORTS ({len(open_ports)}):")
        for port in open_ports:
            service = COMMON_PORTS.get(port, 'Unknown')
            print(f"  Port {port:5d}: {service} (OPEN)")
    else:
        print("No open ports found.")
    
    if '--verbose' in sys.argv and closed:
        print(f"\n🔴 CLOSED ({len(closed)}): {', '.join(map(str, closed[:20]))}" + (" ..." if len(closed) > 20 else ""))
