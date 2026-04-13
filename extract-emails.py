#!/usr/bin/env python3
"""
Extract Emails - Extract email addresses from text.
Usage: python extract-emails.py <file|text>
"""

import sys
import os
import re

EMAIL_RE = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

def extract_emails(text):
    """Extract email addresses."""
    return set(EMAIL_RE.findall(text))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python extract-emails.py <file|text>")
        sys.exit(1)
    
    target = sys.argv[1]
    
    if os.path.exists(target):
        with open(target, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
    else:
        text = target
    
    emails = extract_emails(text)
    
    if emails:
        print(f"Found {len(emails)} email addresses:\n")
        for email in sorted(emails):
            print(email)
    else:
        print("No email addresses found")
