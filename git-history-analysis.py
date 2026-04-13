#!/usr/bin/env python3
"""
Git History Analysis - Analyze git commit history for insights.
Usage: python git-history-analysis.py [--repo PATH] [--max N]
"""

import subprocess
import sys
import os
import re
from collections import Counter, defaultdict
from datetime import datetime

def run_git(cmd, repo_path=None):
    """Run a git command and return output."""
    try:
        result = subprocess.run(
            ['git'] + cmd,
            cwd=repo_path or os.getcwd(),
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout.strip(), result.returncode
    except Exception as e:
        return str(e), 1


def get_commit_history(max_count=500):
    """Get commit history."""
    cmd = ['log', f'--max-count={max_count}', '--pretty=format:%H|%an|%ae|%ad|%s', '--date=iso']
    output, rc = run_git(cmd)
    if rc != 0:
        return []
    
    commits = []
    for line in output.split('\n'):
        if '|' in line:
            parts = line.split('|')
            if len(parts) >= 5:
                commits.append({
                    'hash': parts[0],
                    'author': parts[1],
                    'email': parts[2],
                    'date': parts[3].strip(),
                    'message': '|'.join(parts[4:]).strip()
                })
    return commits


def get_commits_by_author(commits):
    """Count commits by author."""
    authors = Counter(c['author'] for c in commits)
    return authors.most_common()


def get_commits_by_day(commits):
    """Count commits by day of week."""
    days = []
    for c in commits:
        try:
            dt = datetime.fromisoformat(c['date'].split()[0])
            days.append(dt.strftime('%A'))
        except:
            pass
    return Counter(days)


def analyze_commit_messages(commits):
    """Analyze commit message patterns."""
    conventional = 0
    fix_patterns = 0
    feat_patterns = 0
    
    conventional_types = ['feat:', 'fix:', 'docs:', 'style:', 'refactor:', 'perf:', 'test:', 'chore:', 'ci:']
    
    for c in commits:
        msg = c['message'].lower()
        if any(msg.startswith(t) for t in conventional_types):
            conventional += 1
        if any(f in msg for f in ['fix', 'bug', 'patch', 'hotfix']):
            fix_patterns += 1
        if any(f in msg for f in ['feat', 'feature', 'add', 'new']):
            feat_patterns += 1
    
    return {
        'conventional': conventional,
        'fix_patterns': fix_patterns,
        'feat_patterns': feat_patterns,
        'total': len(commits)
    }


def get_file_stats(commits):
    """Get stats on changed files."""
    total_additions = 0
    total_deletions = 0
    files_changed = set()
    
    cmd = ['log', '--numstat', '--format=%H', f'--max-count={min(len(commits), 200)}']
    output, rc = run_git(cmd)
    
    if rc == 0:
        for line in output.split('\n'):
            parts = line.split('\t')
            if len(parts) == 3:
                try:
                    add = int(parts[0]) if parts[0] != '-' else 0
                    dele = int(parts[1]) if parts[1] != '-' else 0
                    total_additions += add
                    total_deletions += dele
                    files_changed.add(parts[2])
                except:
                    pass
    
    return {
        'additions': total_additions,
        'deletions': total_deletions,
        'files': len(files_changed)
    }


if __name__ == '__main__':
    repo_path = None
    max_count = 500
    
    for i, arg in enumerate(sys.argv):
        if arg == '--repo' and i + 1 < len(sys.argv):
            repo_path = sys.argv[i + 1]
        elif arg == '--max' and i + 1 < len(sys.argv):
            max_count = int(sys.argv[i + 1])
    
    if not os.path.exists(repo_path or '.'):
        print(f"Error: Directory not found: {repo_path or '.'}")
        sys.exit(1)
    
    # Check if git repo
    _, rc = run_git(['status'], repo_path)
    if rc != 0:
        print("Error: Not a git repository")
        sys.exit(1)
    
    print("=== Git History Analysis ===\n")
    
    commits = get_commit_history(max_count)
    print(f"Total commits analyzed: {len(commits)}")
    
    # Authors
    print("\n## Top Contributors:")
    for author, count in get_commits_by_author(commits)[:10]:
        pct = count / len(commits) * 100
        print(f"  {author}: {count} commits ({pct:.1f}%)")
    
    # Day of week
    print("\n## Commits by Day:")
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_counts = get_commits_by_day(commits)
    for day in day_order:
        count = day_counts.get(day, 0)
        bar = '|' + chr(9608) * (count // 5)
        print(f"  {day:10s}: {count:4d} {bar}")
    
    # Message patterns
    print("\n## Commit Message Analysis:")
    patterns = analyze_commit_messages(commits)
    print(f"  Conventional commits: {patterns['conventional']} ({patterns['conventional']/patterns['total']*100:.1f}%)")
    print(f"  Bug fix related:      {patterns['fix_patterns']} ({patterns['fix_patterns']/patterns['total']*100:.1f}%)")
    print(f"  Feature related:      {patterns['feat_patterns']} ({patterns['feat_patterns']/patterns['total']*100:.1f}%)")
    
    # File stats
    print("\n## Change Statistics:")
    stats = get_file_stats(commits)
    print(f"  Files changed: {stats['files']}")
    print(f"  Lines added:   +{stats['additions']:,}")
    print(f"  Lines deleted: -{stats['deletions']:,}")
    if stats['additions'] > stats['deletions']:
        print(f"  Net change:    +{stats['additions'] - stats['deletions']:,} lines")
    else:
        print(f"  Net change:    {stats['additions'] - stats['deletions']:,} lines")
