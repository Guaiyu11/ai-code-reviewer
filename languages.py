#!/usr/bin/env python3
"""
Languages - List supported programming languages.
Usage: python languages.py [--search TERM]
"""

import sys

LANGUAGES = {
    'python': ['py', 'python', 'py3'],
    'javascript': ['js', 'javascript', 'node'],
    'typescript': ['ts', 'typescript'],
    'java': ['java'],
    'c': ['c', '.c'],
    'cpp': ['cpp', 'c++', '.cpp'],
    'csharp': ['cs', 'c#', 'csharp'],
    'go': ['go', 'golang'],
    'rust': ['rs', 'rust'],
    'ruby': ['rb', 'ruby'],
    'php': ['php'],
    'swift': ['swift'],
    'kotlin': ['kt', 'kotlin'],
    'scala': ['scala'],
    'perl': ['pl', 'perl'],
    'lua': ['lua'],
    'r': ['r', 'rstats'],
    'matlab': ['m', 'matlab'],
    'julia': ['jl', 'julia'],
    'haskell': ['hs', 'haskell'],
    'elixir': ['ex', 'elixir'],
    'erlang': ['erl', 'erlang'],
    'clojure': ['clj', 'clojure'],
    'dart': ['dart'],
    'groovy': ['groovy'],
    'shell': ['sh', 'bash', 'shell'],
    'powershell': ['ps1', 'powershell'],
    'sql': ['sql'],
    'html': ['html'],
    'css': ['css'],
    'json': ['json'],
    'yaml': ['yaml', 'yml'],
    'xml': ['xml'],
    'markdown': ['md', 'markdown'],
}

def print_all():
    """Print all languages."""
    print("=== Supported Languages ===\n")
    for lang, aliases in sorted(LANGUAGES.items()):
        print(f"{lang:15s} {', '.join(aliases)}")

def search(term):
    """Search languages."""
    term = term.lower()
    results = []
    for lang, aliases in LANGUAGES.items():
        if term in lang or any(term in a for a in aliases):
            results.append((lang, aliases))
    
    if not results:
        print(f"No languages matching '{term}'")
    else:
        for lang, aliases in results:
            print(f"{lang:15s} {', '.join(aliases)}")

if __name__ == '__main__':
    if '--search' in sys.argv:
        idx = sys.argv.index('--search')
        if idx + 1 < len(sys.argv):
            search(sys.argv[idx + 1])
    else:
        print_all()
