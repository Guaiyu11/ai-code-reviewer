#!/usr/bin/env python3
"""
Keycode - Show keyboard key codes (for terminal UI).
Usage: python keycode.py
Press keys to see their escape sequences.
"""

import sys
import tty
import termios
import os

def get_key():
    """Get a single keypress."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def key_info(ch):
    """Get information about a keypress."""
    codes = {
        'arrow_up': '\x1b[A',
        'arrow_down': '\x1b[B',
        'arrow_right': '\x1b[C',
        'arrow_left': '\x1b[D',
        'home': '\x1b[H',
        'end': '\x1b[F',
        'page_up': '\x1b[5~',
        'page_down': '\x1b[6~',
        'insert': '\x1b[2~',
        'delete': '\x1b[3~',
    }
    
    for name, code in codes.items():
        if ch == code:
            return name, repr(ch)
    
    if ord(ch) == 3:
        return 'Ctrl+C', 'EXIT'
    if ord(ch) == 4:
        return 'Ctrl+D', 'EXIT'
    
    return 'char', repr(ch), ord(ch)

if __name__ == '__main__':
    print("=== Keycode Viewer ===")
    print("Press keys to see their codes. Ctrl+C or Ctrl+D to exit.\n")
    
    while True:
        ch = get_key()
        name, info = key_info(ch)
        
        if info == 'EXIT':
            print(f"\n{name} - Exiting")
            break
        
        print(f"{name:15s} {info:20s}", end='  ')
        if ch.isprintable():
            print(f"'{ch}'")
        else:
            print()
