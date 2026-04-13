#!/usr/bin/env python3
"""
Password Generator - Generate secure random passwords.
Usage: python password-gen.py [length] [--pins] [--uuid] [-- pronounceable]
"""

import sys
import os
import random
import string
import secrets

def generate_random(length=16, charset=None):
    """Generate random password with specified character set."""
    if charset is None:
        charset = string.ascii_letters + string.digits + '!@#$%^&*'
    
    return ''.join(secrets.choice(charset) for _ in range(length))

def generate_pin(length=6):
    """Generate random PIN."""
    return ''.join(secrets.choice(string.digits) for _ in range(length))

def generate_passphrase(wordlist=None, num_words=4, separator='-'):
    """Generate pronounceable passphrase."""
    if wordlist is None:
        wordlist = [
            'apple', 'banana', 'cherry', 'dragon', 'eagle', 'forest',
            'galaxy', 'harbor', 'island', 'jungle', 'kernel', 'lemon',
            'mountain', 'nebula', 'ocean', 'planet', 'quantum', 'river',
            'sunset', 'thunder', 'umbrella', 'valley', 'winter', 'yellow',
            'zebra', 'anchor', 'breeze', 'castle', 'diamond', 'ember',
            'falcon', 'glacier', 'horizon', 'ivory', 'jasper', 'kindle',
            'lantern', 'marble', 'nectar', 'orange', 'palace', 'quartz',
            'rocket', 'silver', 'tiger', 'unity', 'velvet', 'willow',
            'xenon', 'yacht', 'zephyr', 'amber', 'blaze', 'coral',
            'delta', 'echo', 'flame', 'golden', 'haven', 'indigo'
        ]
    
    words = [secrets.choice(wordlist) for _ in range(num_words)]
    return separator.join(words)

def check_strength(password):
    """Estimate password strength."""
    score = 0
    feedback = []
    
    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if len(password) >= 16:
        score += 1
    
    if any(c in string.ascii_lowercase for c in password):
        score += 1
    if any(c in string.ascii_uppercase for c in password):
        score += 1
    if any(c in string.digits for c in password):
        score += 1
    if any(c in '!@#$%^&*' for c in password):
        score += 1
    
    # Check for common patterns
    common = ['123456', 'password', 'qwerty', 'abc123', 'admin']
    if any(p in password.lower() for p in common):
        score = min(score, 2)
        feedback.append('Contains common pattern')
    
    if score <= 3:
        strength = 'WEAK'
    elif score <= 5:
        strength = 'MEDIUM'
    else:
        strength = 'STRONG'
    
    return strength, score, feedback

if __name__ == '__main__':
    length = 16
    count = 5
    
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    for a in args:
        if a.isdigit():
            length = int(a)
    
    pins = '--pins' in sys.argv
    uuid_fmt = '--uuid' in sys.argv
    pronounceable = '--pronounceable' in sys.argv
    
    print('=== Password Generator ===\n')
    
    if pins:
        print(f'PINs ({length} digits):')
        for _ in range(count):
            print(f'  {generate_pin(length)}')
    elif uuid_fmt:
        import uuid
        print(f'UUIDs:')
        for _ in range(count):
            print(f'  {uuid.uuid4()}')
    elif pronounceable:
        print(f'Passphrases ({length} words):')
        for _ in range(count):
            pw = generate_passphrase(num_words=length)
            strength, score, feedback = check_strength(pw)
            print(f'  {pw}  [{strength}]')
    else:
        print(f'Passwords (length={length}):')
        for _ in range(count):
            pw = generate_random(length)
            strength, score, feedback = check_strength(pw)
            print(f'  {pw}  [{strength}]')
