#!/usr/bin/env python3
"""
Batch Rename - Rename multiple files with patterns.
Usage: python batch-rename.py <directory> --pattern <regex> --replace <replacement> [--preview]
Patterns:
  --prefix PREFIX    Add prefix to all files
  --suffix SUFFIX    Add suffix to all files (before extension)
  --number START     Rename to 01, 02, 03...
  --lower            Convert to lowercase
  --upper            Convert to uppercase
"""

import sys
import os
import re
import shutil

def preview_rename(files, func):
    """Preview what the rename would look like."""
    results = []
    for f in files:
        new = func(f)
        if new != f:
            results.append((f, new))
    return results

def rename_files(directory, func, dry_run=True):
    """Rename files according to function."""
    renamed = []
    errors = []
    
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if not os.path.isfile(filepath):
            continue
        
        new_name = func(filename)
        if new_name == filename:
            continue
        
        new_path = os.path.join(directory, new_name)
        
        if os.path.exists(new_path) and not dry_run:
            errors.append(f"Exists: {new_name}")
            continue
        
        if dry_run:
            renamed.append((filename, new_name))
        else:
            try:
                shutil.move(filepath, new_path)
                renamed.append((filename, new_name))
            except Exception as e:
                errors.append(f"Error renaming {filename}: {e}")
    
    return renamed, errors

def make_pattern_func(pattern, replacement):
    """Create rename function from regex pattern."""
    def func(filename):
        base, ext = os.path.splitext(filename)
        new_base = re.sub(pattern, replacement, base)
        return new_base + ext
    return func

def make_prefix_func(prefix):
    """Create rename function that adds prefix."""
    def func(filename):
        base, ext = os.path.splitext(filename)
        return prefix + base + ext
    return func

def make_suffix_func(suffix):
    """Create rename function that adds suffix before extension."""
    def func(filename):
        base, ext = os.path.splitext(filename)
        return base + suffix + ext
    return func

def make_number_func(start=1):
    """Create rename function that numbers files."""
    counter = [start - 1]
    def func(filename):
        counter[0] += 1
        base, ext = os.path.splitext(filename)
        return f"{counter[0]:03d}_{base}{ext}"
    return func

def make_case_func(mode):
    """Create rename function for case conversion."""
    def func_lower(filename):
        base, ext = os.path.splitext(filename)
        return base.lower() + ext.lower()
    
    def func_upper(filename):
        base, ext = os.path.splitext(filename)
        return base.upper() + ext.upper()
    
    if mode == 'lower':
        return func_lower
    elif mode == 'upper':
        return func_upper
    return lambda x: x

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python batch-rename.py <directory> [options]")
        print("\nOptions:")
        print("  --pattern REGEX      Regex pattern to match")
        print("  --replace TEXT       Replacement text")
        print("  --prefix TEXT        Add prefix")
        print("  --suffix TEXT        Add suffix (before extension)")
        print("  --number [START]     Number files 001, 002, ...")
        print("  --lower              Convert to lowercase")
        print("  --upper              Convert to uppercase")
        print("  --execute            Actually rename (default is preview)")
        sys.exit(1)
    
    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"Error: Not a directory: {directory}")
        sys.exit(1)
    
    dry_run = '--execute' not in sys.argv
    
    func = None
    
    if '--pattern' in sys.argv and '--replace' in sys.argv:
        pi = sys.argv.index('--pattern')
        ri = sys.argv.index('--replace')
        func = make_pattern_func(sys.argv[pi + 1], sys.argv[ri + 1])
    elif '--prefix' in sys.argv:
        pi = sys.argv.index('--prefix')
        func = make_prefix_func(sys.argv[pi + 1])
    elif '--suffix' in sys.argv:
        si = sys.argv.index('--suffix')
        func = make_suffix_func(sys.argv[si + 1])
    elif '--number' in sys.argv:
        start = 1
        if '--number' in sys.argv:
            ni = sys.argv.index('--number')
            if ni + 1 < len(sys.argv) and sys.argv[ni + 1].isdigit():
                start = int(sys.argv[ni + 1])
        func = make_number_func(start)
    elif '--lower' in sys.argv:
        func = make_case_func('lower')
    elif '--upper' in sys.argv:
        func = make_case_func('upper')
    
    if func is None:
        print("Error: No rename option specified")
        sys.exit(1)
    
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    print(f"=== Batch Rename: {directory} ===\n")
    
    if dry_run:
        print("PREVIEW MODE (use --execute to actually rename)\n")
    
    renamed, errors = rename_files(directory, func, dry_run)
    
    for old, new in renamed:
        print(f"  {old}")
        print(f"  -> {new}")
        print()
    
    if errors:
        print(f"\nErrors ({len(errors)}):")
        for e in errors:
            print(f"  {e}")
    
    print(f"\nTotal: {len(renamed)} file(s) renamed")
