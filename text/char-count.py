#!/usr/bin/env python3
"""
Character Count - Count characters, words, sentences in text.
Usage: python char-count.py <file|text>
"""

import sys
import os
import re

def count_chars(text):
    """Count various character types."""
    counts = {
        'total': len(text),
        'chars': sum(1 for c in text if c.isalpha()),
        'digits': sum(1 for c in text if c.isdigit()),
        'spaces': sum(1 for c in text if c.isspace()),
        'punct': sum(1 for c in text if c in '.,;:!?-()[]{}"'),        'upper': sum(1 for c in text if c.isupper()),
        'lower': sum(1 for c in text if c.islower()),
        'lines': text.count('\n') + 1,
        'words': len(text.split()),
        'sentences': len(re.split(r'[.!?]+', text)),
    }
    return counts

def char_freq(text):
    """Get character frequency."""
    freq = {}
    for c in text.lower():
        if c.isalpha():
            freq[c] = freq.get(c, 0) + 1
    return sorted(freq.items(), key=lambda x: x[1], reverse=True)

def word_freq(text, top=20):
    """Get word frequency."""
    words = re.findall(r'\b[a-zA-Z]{2,}\b', text.lower())
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    return sorted(freq.items(), key=lambda x: x[1], reverse=True)[:top]

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python char-count.py <file|text> [--freq] [--words]")
        sys.exit(1)
    
    target = sys.argv[1]
    
    if os.path.exists(target):
        with open(target, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
    else:
        text = target
    
    counts = count_chars(text)
    
    print(f"=== Character Counts ===\n")
    print(f"Characters: {counts['chars']}")
    print(f"Digits:      {counts['digits']}")
    print(f"Spaces:      {counts['spaces']}")
    print(f"Punctuation: {counts['punct']}")
    print(f"Uppercase:  {counts['upper']}")
    print(f"Lowercase:  {counts['lower']}")
    print(f"Lines:      {counts['lines']}")
    print(f"Words:      {counts['words']}")
    print(f"Sentences:  {counts['sentences']}")
    print(f"Total chars: {counts['total']}")
    
    if '--freq' in sys.argv:
        print("\n=== Character Frequency ===")
        for char, count in char_freq(text)[:20]:
            bar = '|' * (count // 10)
            print(f"  '{char}': {count:5d} {bar}")
    
    if '--words' in sys.argv:
        print("\n=== Word Frequency ===")
        for word, count in word_freq(text):
            bar = '|' * (count // 5)
            print(f"  {word:20s} {count:5d} {bar}")
