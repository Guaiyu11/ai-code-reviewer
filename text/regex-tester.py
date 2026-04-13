#!/usr/bin/env python3
"""
Regex Tester - Test and debug regular expressions with live matching.
Usage: python regex-tester.py "<pattern>" [text]
"""

import sys
import re

def test_regex(pattern, text, flags=0):
    """Test a regex pattern against text."""
    results = {
        'valid': True,
        'matches': [],
        'groups': [],
        'error': None
    }
    
    try:
        compiled = re.compile(pattern, flags)
        results['compiled'] = str(compiled)
        
        if text:
            matches = compiled.finditer(text)
            for m in matches:
                match_dict = {
                    'match': m.group(),
                    'span': m.span(),
                    'groups': m.groups(),
                }
                if m.groupdict():
                    match_dict['named_groups'] = m.groupdict()
                results['matches'].append(match_dict)
        
        # Show what the pattern matches
        if text:
            results['highlighted'] = highlight_matches(text, compiled)
        
    except re.error as e:
        results['valid'] = False
        results['error'] = str(e)
    
    return results


def highlight_matches(text, compiled):
    """Return text with matches highlighted using ANSI codes."""
    highlighted = text
    matches = list(compiled.finditer(text))
    if not matches:
        return text
    
    # Replace from end to start to preserve positions
    offset = 0
    for m in matches:
        start, end = m.start() + offset, m.end() + offset
        match_text = highlighted[start:end]
        highlighted = highlighted[:start] + f'\033[92m{match_text}\033[0m' + highlighted[end:]
        offset += len('\033[92m\033[0m')
    
    return highlighted


def explain_pattern(pattern):
    """Give a plain-English explanation of a regex pattern."""
    explanations = []
    
    # Simple replacements
    replacements = [
        (r'^', 'start of string'),
        (r'$', 'end of string'),
        (r'\b', 'word boundary'),
        (r'\d', 'any digit'),
        (r'\D', 'any non-digit'),
        (r'\w', 'any word character'),
        (r'\W', 'any non-word character'),
        (r'\s', 'any whitespace'),
        (r'\S', 'any non-whitespace'),
        (r'.', 'any character'),
        (r'.*', 'any characters (greedy)'),
        (r'.*?', 'any characters (lazy)'),
        (r'\+', 'one or more'),
        (r'\*', 'zero or more'),
        (r'\?', 'zero or one / optional'),
        (r'\|', 'OR'),
    ]
    
    # Remove escaping for display
    clean = pattern
    for old, new in replacements:
        clean = clean.replace(old, f'[{new}]')
    
    # Quantifiers
    for m in re.finditer(r'\{(\d+)(?:,(\d*))?\}', pattern):
        if m.group(2) is None:
            clean = clean.replace(m.group(), f'[exactly {m.group(1)} times]')
        elif m.group(2) == '':
            clean = clean.replace(m.group(), f'[{m.group(1)} or more times]')
        else:
            clean = clean.replace(m.group(), f'[{m.group(1)}-{m.group(2)} times]')
    
    return clean


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python regex-tester.py \"<pattern>\" [text] [--flags FLAGS]")
        print("\nExamples:")
        print('  python regex-tester.py "\\d+" "abc123def456"')
        print('  python regex-tester.py "[a-z]+@[a-z]+\\.[a-z]+" "contact@example.com"')
        print('  python regex-tester.py "^\\w{3,}$" --flags I')
        print("\nFlags: I=ignorecase, M=multiline, S=dotall")
        sys.exit(1)
    
    pattern = sys.argv[1]
    text = ''
    flags = 0
    
    for i, arg in enumerate(sys.argv):
        if arg == '--flags' and i + 1 < len(sys.argv):
            flag_str = sys.argv[i + 1].upper()
            if 'I' in flag_str:
                flags |= re.IGNORECASE
            if 'M' in flag_str:
                flags |= re.MULTILINE
            if 'S' in flag_str:
                flags |= re.DOTALL
    
    if len(sys.argv) > 2 and sys.argv[2] != '--flags':
        text = sys.argv[2]
    
    print(f"=== Regex Tester ===\n")
    print(f"Pattern: {pattern}")
    print(f"Flags:   {flags}")
    if text:
        print(f"Text:    {text[:200]}{'...' if len(text) > 200 else ''}\n")
    
    result = test_regex(pattern, text, flags)
    
    if not result['valid']:
        print(f"[ERROR] {result['error']}")
        sys.exit(1)
    
    # Explanation
    explanation = explain_pattern(pattern)
    print(f"Meaning: {explanation}\n")
    
    if text:
        # Highlighted
        if result.get('highlighted'):
            print("Highlighted:")
            print(result['highlighted'])
            print()
        
        # Match details
        print(f"Matches: {len(result['matches'])}")
        for i, match in enumerate(result['matches']):
            print(f"  [{i}] '{match['match']}' at position {match['span']}")
            if match['groups']:
                print(f"       groups: {match['groups']}")
            if match.get('named_groups'):
                print(f"       named:  {match['named_groups']}")
