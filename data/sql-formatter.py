#!/usr/bin/env python3
"""
SQL Formatter & Analyzer - Format SQL queries and detect performance issues.
Usage: python sql-formatter.py <query.sql> [--analyze]
"""

import sys
import os
import re

# SQL keywords
KEYWORDS = [
    'SELECT', 'FROM', 'WHERE', 'JOIN', 'LEFT', 'RIGHT', 'INNER', 'OUTER', 'FULL',
    'ON', 'AND', 'OR', 'NOT', 'IN', 'BETWEEN', 'LIKE', 'IS', 'NULL', 'AS',
    'ORDER', 'BY', 'GROUP', 'HAVING', 'LIMIT', 'OFFSET', 'UNION', 'ALL',
    'INSERT', 'INTO', 'VALUES', 'UPDATE', 'SET', 'DELETE', 'CREATE', 'TABLE',
    'ALTER', 'DROP', 'INDEX', 'PRIMARY', 'KEY', 'FOREIGN', 'REFERENCES',
    'CASCADE', 'DISTINCT', 'EXISTS', 'CASE', 'WHEN', 'THEN', 'ELSE', 'END',
    'COUNT', 'SUM', 'AVG', 'MIN', 'MAX', 'COALESCE', 'CAST', 'CONVERT',
    'INNER', 'CROSS', 'NATURAL', 'USING', 'PIVOT', 'UNPIVOT',
    'WITH', 'RECURSIVE', 'OVER', 'PARTITION', 'ROW_NUMBER', 'RANK', 'DENSE_RANK'
]

SQL_KEYWORDS_RE = re.compile(r'\b(' + '|'.join(KEYWORDS) + r')\b', re.IGNORECASE)
IDENTIFIER_RE = re.compile(r'([a-zA-Z_][a-zA-Z0-9_]*)')
STRING_RE = re.compile(r"'[^']*'")
NUMBER_RE = re.compile(r'\b\d+\b')


def format_sql(query, indent='  '):
    """Format SQL query with proper indentation."""
    # Uppercase keywords
    formatted = SQL_KEYWORDS_RE.sub(lambda m: m.group(1).upper(), query)
    
    lines = []
    current_line = ''
    depth = 0
    paren_depth = 0
    
    special_keywords = {'SELECT', 'FROM', 'WHERE', 'AND', 'OR', 'JOIN', 'LEFT JOIN', 'RIGHT JOIN',
                       'INNER JOIN', 'OUTER JOIN', 'FULL JOIN', 'CROSS JOIN', 'ON',
                       'ORDER BY', 'GROUP BY', 'HAVING', 'LIMIT', 'OFFSET',
                       'UNION', 'VALUES', 'SET', 'INSERT INTO', 'UPDATE'}
    
    special_lower = {k.lower() for k in special_keywords}
    
    tokens = formatted.split()
    i = 0
    while i < len(tokens):
        token = tokens[i]
        token_lower = token.lower()
        
        # Check for two-word keywords
        if i + 1 < len(tokens):
            two_word = token_lower + ' ' + tokens[i + 1].lower()
            if two_word in special_lower:
                if current_line.strip():
                    lines.append(indent * depth + current_line.strip())
                depth += 1
                current_line = token + ' ' + tokens[i + 1]
                i += 2
                continue
        
        # Single keyword
        if token_lower in special_lower:
            if current_line.strip():
                lines.append(indent * depth + current_line.strip())
            current_line = token
            depth += 1
        elif token == ',':
            if current_line.strip():
                lines.append(indent * depth + current_line.strip())
            current_line = ''
        elif token in ('(', ')'):
            if token == '(':
                current_line += token
            else:
                current_line = current_line.strip() + ' ' + token
                if current_line.strip():
                    lines.append(indent * depth + current_line.strip())
                current_line = ''
                depth = max(0, depth - 1)
        else:
            if current_line:
                current_line += ' ' + token
            else:
                current_line = token
        
        i += 1
    
    if current_line.strip():
        lines.append(indent * depth + current_line.strip())
    
    return '\n'.join(lines)


def analyze_sql(query):
    """Analyze SQL query for potential issues."""
    issues = []
    query_lower = query.lower()
    
    # SELECT *
    if re.search(r'select\s+\*', query_lower):
        issues.append({
            'severity': 'INFO',
            'msg': 'SELECT * found - consider specifying columns for clarity and performance'
        })
    
    # No WHERE clause
    if re.search(r'select\s+.*\s+from\s+[^\s]+\s*;?\s*$', query_lower) and 'where' not in query_lower:
        issues.append({
            'severity': 'WARNING',
            'msg': 'SELECT without WHERE clause - may return unnecessary data'
        })
    
    # Cartesian product risk
    joins = re.findall(r'join\s+\w+', query_lower)
    if len(joins) > 1 and ' on ' not in query_lower and ' using ' not in query_lower:
        issues.append({
            'severity': 'CRITICAL',
            'msg': f'Multiple JOINs ({len(joins)}) without ON/USING - risk of Cartesian product'
        })
    
    # Missing indexes (heuristic)
    from_tables = re.findall(r'from\s+([a-z_][a-z0-9_]*)', query_lower)
    where_cols = re.findall(r'where\s+([a-z_][a-z0-9_]*)\s*[=<>]', query_lower)
    if from_tables and where_cols:
        issues.append({
            'severity': 'INFO',
            'msg': f'Tables: {", ".join(set(from_tables))} | Filtered columns: {", ".join(set(where_cols))} - ensure indexes exist'
        })
    
    # LIKE with leading wildcard
    if '%' in query and '_' in query:
        issues.append({
            'severity': 'WARNING',
            'msg': 'LIKE pattern with leading wildcard (%) - cannot use index'
        })
    
    # ORDER BY RAND()
    if 'order by rand()' in query_lower:
        issues.append({
            'severity': 'CRITICAL',
            'msg': 'ORDER BY RAND() - extremely slow on large tables, use application-side sorting'
        })
    
    # Subquery in SELECT
    if query_lower.count('select') > 1:
        issues.append({
            'severity': 'INFO',
            'msg': 'Subquery detected - verify performance on large datasets'
        })
    
    # Large LIMIT without ORDER BY
    limit_match = re.search(r'limit\s+(\d+)', query_lower)
    if limit_match and 'order by' not in query_lower:
        limit_val = int(limit_match.group(1))
        if limit_val > 100:
            issues.append({
                'severity': 'WARNING',
                'msg': f'LIMIT {limit_val} without ORDER BY - results may be inconsistent'
            })
    
    return issues


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python sql-formatter.py <query.sql or SQL string> [--analyze]")
        print("\nExamples:")
        print("  echo 'select id,name from users where active=1' | python sql-formatter.py --analyze")
        sys.exit(1)
    
    analyze = '--analyze' in sys.argv
    
    # Read from file or argument
    path = sys.argv[1]
    if os.path.exists(path):
        with open(path, 'r') as f:
            query = f.read()
    else:
        query = path
    
    print("=== Original ===")
    print(query.strip())
    print()
    
    print("=== Formatted ===")
    formatted = format_sql(query)
    print(formatted)
    
    if analyze:
        print()
        print("=== Analysis ===")
        issues = analyze_sql(query)
        if not issues:
            print("No issues detected")
        else:
            severity_order = ['CRITICAL', 'WARNING', 'INFO']
            for sev in severity_order:
                sev_issues = [i for i in issues if i['severity'] == sev]
                if sev_issues:
                    print(f"[{sev}]")
                    for issue in sev_issues:
                        print(f"  - {issue['msg']}")
                    print()
