#!/usr/bin/env python3
"""
Passphrase Generator - Generate random passphrases from wordlist.
Usage: python passphrase-gen.py [num_words] [--strength weak|medium|strong]
"""

import sys
import secrets

WEAK = ['red', 'blue', 'green', 'dog', 'cat', 'sun', 'moon', 'star', 'tree', 'rock']
MEDIUM = ['apple', 'banana', 'cherry', 'dragon', 'eagle', 'forest', 'galaxy', 'harbor', 'island', 'jungle', 'kernel', 'lemon', 'mountain', 'nebula', 'ocean', 'planet', 'quantum', 'river', 'sunset', 'thunder', 'umbrella', 'valley', 'winter', 'yellow', 'zebra']
STRONG = ['anchor', 'blizzard', 'cascade', 'diamond', 'eclipse', 'fortress', 'glacier', 'horizon', 'infinity', 'jasper', 'kindle', 'lantern', 'marble', 'nectar', 'obsidian', 'palace', 'quartz', 'rainbow', 'sapphire', 'thunder', 'velocity', 'whirlwind', 'xylophone', 'zephyr']

def generate(words, count=4, sep='-'):
    return sep.join(secrets.choice(words) for _ in range(count))

if __name__ == '__main__':
    num_words = 4
    strength = 'medium'
    
    for arg in sys.argv:
        if arg.isdigit():
            num_words = int(arg)
        elif arg in ('--strength',):
            pass
    
    for a in sys.argv:
        if a == 'weak':
            strength = 'weak'
        elif a == 'medium':
            strength = 'medium'
        elif a == 'strong':
            strength = 'strong'
    
    wordlist = STRONG if strength == 'strong' else MEDIUM if strength == 'medium' else WEAK
    
    print(f"Strength: {strength}, Words: {num_words}\n")
    for i in range(5):
        print(generate(wordlist, num_words))
