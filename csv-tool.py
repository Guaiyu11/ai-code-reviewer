#!/usr/bin/env python3
"""
CSV Tool - Query, filter, join CSV files with SQL-like syntax.
Usage: python csv-tool.py <file.csv> [--query "SELECT * WHERE col > 5"]
"""

import sys
import os
import csv
import io
import re

def read_csv(filepath):
    """Read CSV into list of dicts."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        return list(reader), reader.fieldnames

def filter_csv(rows, fieldnames, where):
    """Filter rows based on WHERE clause."""
    # Simple WHERE parser: col OP value
    # Ops: =, !=, >, <, >=, <=, LIKE, IN
    match = re.match(r'(\w+)\s*(!=|=|<|>|<=|>=)\s*(.+)', where.strip())
    if not match:
        return rows
    
    col, op, val = match.group(1), match.group(2), match.group(3).strip()
    val = val.strip('"\'')
    
    results = []
    for row in rows:
        if col not in row:
            continue
        cell = row[col]
        
        # Try numeric comparison
        try:
            cell_num = float(cell)
            val_num = float(val)
            if op == '=': ok = cell_num == val_num
            elif op == '!=': ok = cell_num != val_num
            elif op == '>': ok = cell_num > val_num
            elif op == '<': ok = cell_num < val_num
            elif op == '>=': ok = cell_num >= val_num
            elif op == '<=': ok = cell_num <= val_num
            else: ok = False
        except:
            # String comparison
            if op == '=': ok = cell == val
            elif op == '!=': ok = cell != val
            elif op == '>': ok = cell > val
            elif op == '<': ok = cell < val
            else: ok = False
        
        if ok:
            results.append(row)
    
    return results

def output_csv(rows, fieldnames):
    """Output as CSV."""
    if not rows:
        return
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(rows)

def output_table(rows, fieldnames, limit=20):
    """Output as ASCII table."""
    if not rows:
        return
    
    widths = {f: len(f) for f in fieldnames}
    for row in rows[:limit]:
        for f in fieldnames:
            widths[f] = max(widths[f], len(str(row.get(f, ''))))
    
    header = '|'.join(f" {fieldnames[i]:<widths[fieldnames[i]]} " for i in range(len(fieldnames)))
    sep = '+' + '+'.join('-' * (widths[f] + 2) for f in fieldnames) + '+'
    
    print(sep)
    print(header)
    print(sep)
    
    for row in rows[:limit]:
        line = '|'.join(f" {str(row.get(f, '')):<widths[f]} " for f in fieldnames)
        print(line)
    
    print(sep)
    if len(rows) > limit:
        print(f"... ({len(rows) - limit} more rows)")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python csv-tool.py <file.csv> [--query 'WHERE col = value'] [--table] [--limit N]")
        sys.exit(1)
    
    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    
    rows, fieldnames = read_csv(filepath)
    
    where = None
    output_mode = 'csv'
    limit = 20
    
    for i, arg in enumerate(sys.argv):
        if arg == '--query' and i + 1 < len(sys.argv):
            where = sys.argv[i + 1]
        elif arg == '--table':
            output_mode = 'table'
        elif arg == '--limit' and i + 1 < len(sys.argv):
            limit = int(sys.argv[i + 1])
    
    if where:
        # Extract WHERE clause
        match = re.search(r'WHERE\s+(.+)', where, re.I)
        if match:
            rows = filter_csv(rows, fieldnames, match.group(1))
    
    rows = rows[:limit]
    
    if output_mode == 'table':
        output_table(rows, fieldnames, limit)
    else:
        output_csv(rows, fieldnames)
