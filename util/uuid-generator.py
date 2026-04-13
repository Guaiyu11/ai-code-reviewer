#!/usr/bin/env python3
"""
UUID Generator - Generate various UUID formats and validate UUIDs.
Usage: python uuid-generator.py [N] [--format TYPE]
Types: v1 (time), v4 (random), nil
"""

import sys
import uuid
import time

def generate_uuid(version=4, count=1):
    """Generate UUIDs of specified version."""
    uuids = []
    for _ in range(count):
        if version == 1:
            u = uuid.uuid1()
        elif version == 4:
            u = uuid.uuid4()
        elif version == 3:
            u = uuid.uuid3(uuid.NAMESPACE_DNS, str(time.time()))
        else:
            u = uuid.uuid4()
        uuids.append(u)
    return uuids

def format_uuid(u, fmt='std'):
    """Format UUID in different styles."""
    s = str(u)
    if fmt == 'std':
        return s  # 6ba7b810-9dad-11d1-80b4-00c04fd430c8
    elif fmt == 'urn':
        return u.urn  # urn:uuid:6ba7b810-9dad-11d1-80b4-00c04fd430c8
    elif fmt == 'hex':
        return s.replace('-', '')  # 6ba7b8109dad11d180b400c04fd430c8
    elif fmt == 'curl':
        return '{' + s + '}'  # {6ba7b810-9dad-11d1-80b4-00c04fd430c8}
    elif fmt == 'upper':
        return s.upper()
    return s

def is_valid_uuid(s):
    """Check if a string is a valid UUID."""
    try:
        uuid.UUID(s)
        return True
    except:
        return False

if __name__ == '__main__':
    count = 1
    version = 4
    fmt = 'std'
    
    for i, arg in enumerate(sys.argv):
        if arg.isdigit():
            count = int(arg)
        elif arg == '--format' and i + 1 < len(sys.argv):
            fmt = sys.argv[i + 1].lower()
        elif arg == '--v1':
            version = 1
        elif arg == '--v4':
            version = 4
    
    if count > 100:
        print(f"Max 100 UUIDs at once. Got {count}.")
        count = 100
    
    uuids = generate_uuid(version, count)
    
    print(f"=== UUID Generator (v{version}) ===\n")
    for u in uuids:
        print(format_uuid(u, fmt))
