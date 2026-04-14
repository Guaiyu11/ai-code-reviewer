#!/usr/bin/env python3
"""查看 GitHub Trending 仓库。

Usage:
    python github-trending.py [--language python] [--since daily]
"""

import argparse
import urllib.request
import json
import sys


def main():
    parser = argparse.ArgumentParser(description="查看 GitHub Trending")
    parser.add_argument("--language", default="", help="编程语言，如 python/go/javascript")
    parser.add_argument("--since", default="daily", choices=["daily", "weekly", "monthly"])
    args = parser.parse_args()

    lang = f"?since={args.since}" if args.language else ""
    url = f"https://api.github.com/search/repositories?q=stars:>1+created:>2024-01-01{lang}&sort=stars&order=desc&per_page=20"

    headers = {"Accept": "application/vnd.github.v3+json"}
    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req) as r:
            data = json.loads(r.read())
        items = data.get("items", [])
        print(f"=== GitHub Trending ({args.since}) {args.language if args.language else 'All'} ===\n")
        for i, repo in enumerate(items, 1):
            print(f"{i:>2}. {repo['full_name']}")
            print(f"    Stars: {repo['stargazers_count']:,} | Forks: {repo['forks_count']} | Lang: {repo.get('language', '?')}")
            print(f"    {repo.get('description', 'No description')[:70]}")
            print()
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
