#!/usr/bin/env python3
"""查看 GitHub 仓库贡献者列表。

Usage:
    python github-contributors.py <owner/repo> [--token TOKEN]
"""

import argparse
import urllib.request
import json
import sys


def main():
    parser = argparse.ArgumentParser(description="查看 GitHub 贡献者")
    parser.add_argument("repo", help="仓库名（格式: owner/repo）")
    parser.add_argument("--token", default="", help="GitHub Token（可选）")
    args = parser.parse_args()

    headers = {"Accept": "application/vnd.github.v3+json"}
    if args.token:
        headers["Authorization"] = f"token {args.token}"

    url = f"https://api.github.com/repos/{args.repo}/contributors?per_page=50"
    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req) as r:
            data = json.loads(r.read())
        print(f"=== {args.repo} 贡献者 ===\n")
        for i, user in enumerate(data, 1):
            print(f"{i:>3}. {user['login']:<20} {user['contributions']:>5} commits  {user['html_url']}")
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
