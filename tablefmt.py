#!/usr/bin/env python3
"""
Table Formatter - Format CSV/TSV/JSON data as ASCII or Markdown tables.
Usage: python tablefmt.py <file.csv> [--format markdown|ascii|grid] [--transpose]
"""

import sys
import os
import csv
import json
import io

def parse_csv(filepath):
    """Parse CSV/TSV file."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Detect delimiter
    first_line = content.split('\n')[0]
    if '\t' in first_line:
        delimiter = '\t'
    elif ';' in first_line:
        delimiter = ';'
    else:
        delimiter = ','
    
    reader = csv.reader(io.StringIO(content), delimiter=delimiter)
    rows = list(reader)
    return rows

def parse_json(filepath):
    """Parse JSON array as rows."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        data = json.load(f)
    
    if isinstance(data, list) and len(data) > 0:
        if isinstance(data[0], dict):
            headers = list(data[0].keys())
            rows = [headers] + [[row.get(h, '') for h in headers] for row in data]
            return rows
    return [[str(data)]]

def format_ascii_table(rows, transposed=False):
    """Format as ASCII table."""
    if not rows:
        return ""
    
    if transposed:
        # Transpose: rows become columns
        max_len = max(len(r) for r in rows)
        rows = [r + [''] * (max_len - len(r)) for r in rows]
        cols = list(zip(*rows))
        rows = [list(c) for c in cols]
    
    # Calculate column widths
    widths = [max(len(str(row[i])) for row in rows) for i in range(len(rows[0]))]
    
    lines = []
    # Header separator
    sep = '+' + '+'.join('-' * (w + 2) for w in widths) + '+'
    
    for ri, row in enumerate(rows):
        line = '|' + '|'.join(f' {str(row[i]):<widths[i]} ' for i in range(len(row))) + '|'
        lines.append(line)
        if ri == 0:
            lines.append(sep)
    
    return '\n'.join(lines)

def format_markdown_table(rows, transposed=False):
    """Format as Markdown table."""
    if not rows:
        return ""
    
    if transposed:
        max_len = max(len(r) for r in rows)
        rows = [r + [''] * (max_len - len(r)) for r in rows]
        cols = list(zip(*rows))
        rows = [list(c) for c in cols]
    
    widths = [max(len(str(row[i])) for row in rows) for i in range(len(rows[0]))]
    
    lines = []
    for ri, row in enumerate(rows):
        line = '|' + '|'.join(f' {str(row[i]):<widths[i]} ' for i in range(len(row))) + '|'
        lines.append(line)
        if ri == 0:
            lines.append('|' + '|'.join('-' * (w + 2) for w in widths) + '|')
    
    return '\n'.join(lines)

def format_grid_table(rows):
    """Format as box-drawing grid."""
    if not rows:
        return ""
    
    widths = [max(len(str(row[i])) for row in rows) for i in range(len(rows[0]))]
    
    horiz = '+' + '+'.join('=' * (w + 2) for w in widths) + '+'
    sep = '+' + '+'.join('-' * (w + 2) for w in widths) + '+'
    
    lines = []
    for ri, row in enumerate(rows):
        if ri == 0:
            lines.append(horiz)
        else:
            lines.append(sep)
        line = '\u2502' + '\u2502'.join(f' {str(row[i]):<widths[i]} ' for i in range(len(row))) + '\u2502'
        lines.append(line)
    lines.append(horiz)
    
    return '\n'.join(lines)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python tablefmt.py <file.csv|json> [--format markdown|ascii|grid] [--transpose]")
        sys.exit(1)
    
    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    
    fmt = 'ascii'
    transposed = '--transpose' in sys.argv
    
    for i, arg in enumerate(sys.argv):
        if arg == '--format' and i + 1 < len(sys.argv):
            fmt = sys.argv[i + 1].lower()
    
    if filepath.endswith('.json'):
        rows = parse_json(filepath)
    else:
        rows = parse_csv(filepath)
    
    print(f"Rows: {len(rows)}, Columns: {len(rows[0]) if rows else 0}\n")
    
    if fmt == 'markdown':
        print(format_markdown_table(rows, transposed))
    elif fmt == 'grid':
        print(format_grid_table(rows))
    else:
        print(format_ascii_table(rows, transposed))
