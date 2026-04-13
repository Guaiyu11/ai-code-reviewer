#!/usr/bin/env python3
"""
MAC Vendor - Lookup MAC address vendor/OUI.
Usage: python mac-vendor.py <mac>
"""

import sys

# Common OUI prefixes
OUI_DB = {
    '00:00:0c': 'Cisco',
    '00:1a:2b': 'Ayecom Technology',
    '00:50:56': 'VMware',
    '08:00:27': 'VirtualBox',
    '00:0c:29': 'VMware',
    '00:15:5d': 'Microsoft Hyper-V',
    '00:1c:42': 'Parallels',
    'b8:27:eb': 'Raspberry Pi',
    'dc:a6:32': 'Raspberry Pi',
    'e4:5f:01': 'Raspberry Pi',
    '00:1e:68': 'Quanta',
    '3c:d9:2b': 'Hewlett Packard',
    '00:1f:29': 'Hewlett Packard',
    '00:25:90': 'Super Micro Computer',
    '00:1b:21': 'Intel',
    '00:1e:67': 'Intel',
    '00:1f:3b': 'Intel',
    '00:26:bb': 'Apple',
    'f8:1e:df': 'Apple',
    '3c:06:30': 'Apple',
    '00:23:df': 'Netgear',
    '00:24:b2': 'Netgear',
    '00:26:f2': 'Netgear',
    '00:1e:2a': 'Cisco-Linksys',
    '00:1c:10': 'Cisco-Linksys',
    '20:cf:30': 'D-Link',
    '00:1b:11': 'D-Link',
    '00:22:b0': 'D-Link',
    '00:1e:58': 'D-Link',
    'f4:ec:38': 'D-Link',
    '00:1f:3c': 'Dell',
    '00:1d:09': 'Dell',
    '00:1e:4f': 'Dell',
    '00:1a:a0': 'Dell',
    '18:03:73': 'Dell',
    '14:fe:b5': 'Dell',
    '34:17:eb': 'Dell',
    'b0:83:fe': 'Dell',
    '18:a9:05': 'Hewlett Packard',
    '94:57:a5': 'Hewlett Packard',
    '38:63:bb': 'Hewlett Packard',
    'e4:11:5b': 'Hewlett Packard',
    '00:23:ae': 'Dell',
    'f8:bc:12': 'Dell',
    '00:14:22': 'Dell',
    '14:18:77': 'Dell',
    '00:0d:56': 'Dell',
    '80:18:44': 'Dell',
    'a4:ba:db': 'Dell',
    'ec:f4:bb': 'Dell',
    '24:6e:96': 'Dell',
    '44:a8:42': 'Dell',
    '5c:26:0a': 'Dell',
    '34:e6:d7': 'Dell',
    'ac:87:a3': 'Dell',
    'b0:ca:68': 'Dell',
    '58:8a:5a': 'Dell',
    'd4:81:d7': 'Dell',
    '00:1a:a0': 'Dell',
    '00:1e:4f': 'Dell',
    '00:1f:3c': 'Dell',
}

def lookup_mac(mac):
    """Lookup MAC vendor."""
    mac = mac.upper().replace('-', ':')
    
    # Normalize to XX:XX:XX format
    if len(mac) == 12:
        mac = ':'.join(mac[i:i+2] for i in range(0, 12, 2))
    
    prefix = mac[:8]
    
    return OUI_DB.get(prefix, 'Unknown')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python mac-vendor.py <mac>")
        print("\nExamples:")
        print("  python mac-vendor.py 00:1a:2b:xx:xx:xx")
        print("  python mac-vendor.py 00-1A-2B-xx-xx-xx")
        print("  python mac-vendor.py 001a2bxxxxxx")
        sys.exit(1)
    
    mac = sys.argv[1]
    vendor = lookup_mac(mac)
    print(f"MAC: {mac}")
    print(f"Vendor: {vendor}")
