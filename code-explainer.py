#!/usr/bin/env python3
"""
Code Explainer - Explain complex code in plain English.
Usage: python code-explainer.py <file> [--lang en|zh|es]
"""

import sys
import os
import base64

def explain_code(content: str) -> str:
    """Simple code explanation using pattern recognition."""
    lines = content.split('\n')
    explanations = []
    
    # Detect language
    if any('def ' in l for l in lines):
        lang = 'python'
    elif any('function ' in l or 'const ' in l for l in lines):
        lang = 'javascript'
    elif any('func ' in l or 'package ' in l for l in lines):
        lang = 'go'
    elif any('public class' in l or 'private void' in l for l in lines):
        lang = 'java'
    else:
        lang = 'unknown'
    
    explanations.append(f"## Language: {lang.upper()}")
    explanations.append(f"## Total lines: {len(lines)}")
    explanations.append(f"## Non-empty lines: {sum(1 for l in lines if l.strip())}")
    
    # Analyze functions/methods
    funcs = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if lang == 'python' and stripped.startswith('def '):
            name = stripped.split('(')[0].replace('def ', '')
            funcs.append(f"  - `{name}` defined at line {i+1}")
        elif lang == 'javascript' and ('function ' in stripped or stripped.startswith('const ') or stripped.startswith('async ')):
            if 'function ' in stripped:
                name = stripped.split('(')[0].replace('function ', '')
                funcs.append(f"  - `{name}()` at line {i+1}")
        elif stripped.startswith('//') or stripped.startswith('#'):
            explanations.append(f"  Comment at line {i+1}: {stripped[:80]}")
    
    if funcs:
        explanations.append("## Functions/Methods:")
        explanations.extend(funcs)
    
    # Imports
    imports = [l.strip() for l in lines if ('import ' in l or 'from ' in l) and not l.strip().startswith('#')]
    if imports:
        explanations.append("## Dependencies:")
        for imp in imports[:10]:
            explanations.append(f"  - {imp}")
    
    # Quick complexity hints
    if '{' in content or 'def ' in content:
        explanations.append("## Structure: Contains block structures (conditionals/loops)")
    
    return '\n'.join(explanations)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python code-explainer.py <file> [--lang LANG]")
        sys.exit(1)
    
    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    result = explain_code(content)
    print(result)
