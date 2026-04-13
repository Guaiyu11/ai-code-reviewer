#!/usr/bin/env python3
"""
Count Words - Count words in text or file.
Usage: python count-words.py <file|text>
"""

import sys
import os
import re

def count_words(text):
    """Count words."""
    words = re.findall(r'\b\w+\b', text)
    return len(words)

def count_chars_no_space(text):
    """Count characters excluding spaces."""
    return len(text.replace(' ', '').replace('\n', '').replace('\t', ''))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python count-words.py <file|text>")
        sys.exit(1)
    
    target = sys.argv[1]
    
    if os.path.exists(target):
        with open(target, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
    else:
        text = target
    
    words = count_words(text)
    chars = len(text)
    chars_no_space = count_chars_no_space(text)
    lines = text.count('\n') + 1
    paragraphs = len([p for p in text.split('\n\n') if p.strip()])
    
    print(f"Words:         {words:,}")
    print(f"Characters:    {chars:,}")
    print(f"No spaces:     {chars_no_space:,}")
    print(f"Lines:         {lines:,}")
    print(f"Paragraphs:    {paragraphs:,}")
