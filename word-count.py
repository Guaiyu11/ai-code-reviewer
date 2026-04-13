#!/usr/bin/env python3
"""
Word/Line Counter - Count words, lines, characters, bytes in text files.
Usage: python word-count.py <file> [--words] [--lines] [--chars] [--bytes]
"""

import sys
import os

def count_file(filepath):
    """Count words, lines, chars, bytes in a file."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    return {
        'bytes': os.path.getsize(filepath),
        'lines': len(content.split('\n')),
        'words': len(content.split()),
        'chars': len(content),
        'chars_no_space': len(content.replace(' ', '').replace('\n', '')),
    }

def count_text(text):
    """Count stats for a string."""
    return {
        'lines': len(text.split('\n')),
        'words': len(text.split()),
        'chars': len(text),
        'chars_no_space': len(text.replace(' ', '').replace('\n', '')),
    }

def top_words(text, n=20):
    """Find most common words."""
    import re
    from collections import Counter
    
    # Extract words
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    
    # Common stop words to exclude
    stopwords = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 
                 'had', 'her', 'was', 'one', 'our', 'out', 'has', 'his', 'its',
                 'may', 'see', 'now', 'way', 'who', 'did', 'get', 'use', 'too',
                 'this', 'that', 'with', 'from', 'they', 'been', 'have', 'were',
                 'will', 'would', 'could', 'there', 'their', 'what', 'when',
                 'which', 'your', 'also', 'more', 'than', 'them', 'some', 'into',
                 'only', 'just', 'over', 'such', 'very', 'even', 'most', 'any'}
    
    filtered = [w for w in words if w not in stopwords]
    counter = Counter(filtered)
    return counter.most_common(n)

def read_time(chars):
    """Estimate reading time."""
    words = chars / 5  # avg word length
    minutes = words / 200  # avg reading speed
    if minutes < 1:
        return f"{int(minutes * 60)} seconds"
    elif minutes < 60:
        return f"{int(minutes)} minutes"
    else:
        return f"{minutes / 60:.1f} hours"

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python word-count.py <file|text> [--words] [--lines] [--top N]")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    if os.path.exists(filepath):
        stats = count_file(filepath)
        print(f"=== File: {filepath} ===\n")
        print(f"Lines:         {stats['lines']:,}")
        print(f"Words:         {stats['words']:,}")
        print(f"Characters:    {stats['chars']:,}")
        print(f"Bytes:         {stats['bytes']:,}")
        print(f"Reading time:  ~{read_time(stats['chars'])}")
        
        # Top words
        top_n = 10
        for i, arg in enumerate(sys.argv):
            if arg == '--top' and i + 1 < len(sys.argv):
                top_n = int(sys.argv[i + 1])
        
        if top_n > 0:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            print(f"\nTop {top_n} words:")
            for word, count in top_words(content, top_n):
                bar = '|' * (count // 100)
                print(f"  {word:20s} {count:5,} {bar}")
    else:
        stats = count_text(filepath)
        print(f"Lines:   {stats['lines']}")
        print(f"Words:   {stats['words']}")
        print(f"Chars:   {stats['chars']}")
