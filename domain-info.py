#!/usr/bin/env python3
"""
Domain Info - Get DNS and WHOIS info for a domain.
Usage: python domain-info.py <domain>
"""

import sys
import socket
import whois
from datetime import datetime

def get_dns(domain):
    """Get DNS records."""
    try:
        ip = socket.gethostbyname(domain)
        return {'ip': ip}
    except:
        return {'ip': None}

def get_whois(domain):
    """Get WHOIS info."""
    try:
        w = whois.whois(domain)
        return {
            'registrar': w.registrar,
            'creation_date': w.creation_date,
            'expiration_date': w.expiration_date,
            'name_servers': w.name_servers,
        }
    except:
        return None

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python domain-info.py <domain>")
        sys.exit(1)
    
    domain = sys.argv[1].lower().replace('https://', '').replace('http://', '').split('/')[0]
    
    print(f"=== Domain Info: {domain} ===\n")
    
    dns = get_dns(domain)
    if dns.get('ip'):
        print(f"IP Address: {dns['ip']}")
    
    whois_info = get_whois(domain)
    if whois_info:
        print(f"\nRegistrar: {whois_info.get('registrar', 'N/A')}")
        
        if whois_info.get('creation_date'):
            cd = whois_info['creation_date']
            if isinstance(cd, list):
                cd = cd[0]
            print(f"Created: {cd}")
        
        if whois_info.get('expiration_date'):
            ed = whois_info['expiration_date']
            if isinstance(ed, list):
                ed = ed[0]
            print(f"Expires: {ed}")
        
        ns = whois_info.get('name_servers')
        if ns:
            if isinstance(ns, list):
                print(f"Name Servers: {', '.join(ns[:3])}")
            else:
                print(f"Name Servers: {ns}")
