#!/usr/bin/env python3
"""
Test Generator - Generate basic unit tests for Python code.
Usage: python test-generator.py <source_file.py>
"""

import sys
import os
import re

def extract_functions(content):
    """Extract function definitions and their docstrings."""
    functions = []
    lines = content.split('\n')
    
    in_func = False
    func_name = None
    func_start = None
    func_lines = []
    indent = 0
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        if stripped.startswith('def ') and '(' in stripped:
            # Save previous function
            if func_name:
                functions.append({
                    'name': func_name,
                    'start': func_start,
                    'lines': func_lines,
                    'params': func_params
                })
            
            func_name = stripped.split('(')[0].replace('def ', '')
            func_start = i + 1
            func_lines = [line]
            indent = len(line) - len(line.lstrip())
            
            # Extract parameters
            params_str = stripped.split('(')[1].rstrip('):')
            func_params = [p.strip() for p in params_str.split(',') if p.strip() and p.strip() != 'self']
            
            in_func = True
        elif in_func:
            if line.strip() == '' or line.startswith(' ') or line.startswith('\t'):
                func_lines.append(line)
            else:
                # End of function
                functions.append({
                    'name': func_name,
                    'start': func_start,
                    'lines': func_lines,
                    'params': func_params
                })
                in_func = False
                func_name = None
    
    # Don't forget last function
    if func_name:
        functions.append({
            'name': func_name,
            'start': func_start,
            'lines': func_lines,
            'params': func_params
        })
    
    return functions


def generate_tests(filename, functions):
    """Generate pytest-compatible test file."""
    base = os.path.basename(filename).replace('.py', '')
    test_lines = [
        f'"""Auto-generated tests for {filename}"""',
        'import pytest',
        f'from {base} import *',
        '',
        '',
    ]
    
    for func in functions:
        name = func['name']
        params = func['params']
        
        test_lines.append(f'def test_{name}():')
        test_lines.append(f'    """Test {name} function."""')
        
        if not params:
            test_lines.append(f'    # TODO: implement test')
            test_lines.append(f'    pass')
        else:
            # Generate mock args based on param types/names
            mock_args = []
            for p in params:
                if 'str' in p.lower() or 'name' in p.lower() or 'path' in p.lower():
                    mock_args.append("'test_value'")
                elif 'int' in p.lower() or 'num' in p.lower() or 'count' in p.lower():
                    mock_args.append('42')
                elif 'list' in p.lower() or 'arr' in p.lower():
                    mock_args.append('[]')
                elif 'dict' in p.lower() or 'obj' in p.lower():
                    mock_args.append('{}')
                elif 'bool' in p.lower():
                    mock_args.append('True')
                else:
                    mock_args.append('None')
            
            args_str = ', '.join(mock_args)
            test_lines.append(f'    result = {name}({args_str})')
            test_lines.append(f'    # Assert something about result')
            test_lines.append(f'    # assert result is not None')
        
        test_lines.append('')
    
    return '\n'.join(test_lines)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python test-generator.py <source_file.py>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    functions = extract_functions(content)
    print(f"Found {len(functions)} functions:")
    for f in functions:
        print(f"  - {f['name']}({', '.join(f['params'])})")
    
    tests = generate_tests(filepath, functions)
    
    out_path = filepath.replace('.py', '_test.py')
    # If same file name, use test_ prefix
    basename = os.path.basename(filepath)
    if '_test.py' in basename:
        out_path = filepath
    else:
        dir_path = os.path.dirname(filepath)
        name = basename.replace('.py', '')
        out_path = os.path.join(dir_path, f'test_{name}.py')
    
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(tests)
    
    print(f"\nGenerated: {out_path}")
