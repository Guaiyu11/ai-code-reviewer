#!/usr/bin/env python3
"""
Sentence Case - Convert text to sentence case.
Usage: python sentence-case.py <file|text> [--inplace]
"""

import sys
import os

def to_sentence_case(text):
    """Convert text to sentence case."""
    sentences = text.split('. ')
    result = []
    for i, sent in enumerate(sentences):
        sent = sent.strip()
        if sent:
            sent = sent[0].upper() + sent[1:] if len(sent) > 1 else sent.upper()
            result.append(sent)
    return '. '.join(result)

def process_file(filepath, inplace=False):
    """Process file."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    result = to_sentence_case(content)
    
    if inplace:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"Updated: {filepath}")
    else:
        print(result)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python sentence-case.py <file|text> [--inplace]")
        sys.exit(1)
    
    target = sys.argv[1]
    
    if os.path.exists(target):
        process_file(target, '--inplace' in sys.argv)
    else:
        print(to_sentence_case(target))
