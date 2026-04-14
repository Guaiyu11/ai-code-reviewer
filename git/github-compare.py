#!/usr/bin/env python3
"""对比 GitHub 仓库两个分支/标签的差异（显示 commit 列表）。

Usage:
    python github-compare.py <owner/repo> <base> <head> [--token TOKEN]
Example:
    python github-compare.py owner/repo main feature-branch
"""

import argparse
import urllib.request
import json
import sys


def main():
    parser = argparse.ArgumentParser(description="对比 GitHub 分支/标签")
    parser.add_argument("repo", help="仓库名（格式: owner/repo）")
    parser.add_argument("base", help="基准分支，如 main")
    parser.add_argument("head", help="对比分支，如 feature-branch")
    parser.add_argument("--token", default="", help="GitHub Token（可选）")
    args = parser.parse_args()

    headers = {"Accept": "application/vnd.github.v3+json"}
    if args.token:
        headers["Authorization"] = f"token {args.token}"

    url = f"https://api.github.com/repos/{args.repo}/compare/{args.base}...{args.head}"
    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req) as r:
            data = json.loads(r.read())
        print(f"=== {args.repo}: {args.base} vs {args.head} ===")
        print(f"Ahead: {data['ahead_by']} | Behind: {data['behind_by']}")
        print(f"Total commits: {len(data['commits'])}\n")
        for commit in data["commits"][:20]:
            c = commit["commit"]
            print(f"  {c['author']['name']}: {c['message'].split(chr(10))[0][:60]}")
        if len(data["commits"]) > 20:
            print(f"  ... and {len(data['commits']) - 20} more")
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
