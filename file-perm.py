#!/usr/bin/env python3
"""
File Permissions - Show file permissions in octal.
Usage: python file-perm.py <file>
"""

import sys
import os
import stat

def get_perm_string(path):
    """Get permission string."""
    st = os.stat(path)
    mode = st.st_mode
    
    # Octal
    octal = oct(stat.S_IMODE(mode))[-3:]
    
    # Human readable
    def rwx(bits, offset):
        mode_bits = (mode >> offset) & 7
        result = ''
        for check, char in [(4, 'r'), (2, 'w'), (1, 'x')]:
            result += char if mode_bits & check else '-'
        return result
    
    user = rwx(6, 6)
    group = rwx(3, 3)
    other = rwx(0, 0)
    
    return octal, f"{user}{group}{other}"

def get_owner_info(path):
    """Get owner information."""
    try:
        import pwd
        st = os.stat(path)
        owner = pwd.getpwuid(st.st_uid).pw_name
        return owner
    except:
        return str(os.stat(path).st_uid)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python file-perm.py <file>")
        sys.exit(1)
    
    path = sys.argv[1]
    octal, human = get_perm_string(path)
    owner = get_owner_info(path)
    
    print(f"File:      {path}")
    print(f"Permissions: {octal} ({human})")
    print(f"Owner:     {owner}")
