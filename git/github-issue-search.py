#!/usr/bin/env python3
"""搜索 GitHub Issues。

Usage:
    python github-issue-search.py <owner/repo> <query> [--state open] [--token TOKEN]
"""

import argparse
import urllib.request
import json
import sys


def main():
    parser = argparse.ArgumentParser(description="搜索 GitHub Issues")
    parser.add_argument("repo", help="仓库名（格式: owner/repo）")
    parser.add_argument("query", help="搜索关键词")
    parser.add_argument("--state", default="open", choices=["open", "closed", "all"])
    parser.add_argument("--token", default="", help="GitHub Token（可选）")
    parser.add_argument("--limit", type=int, default=10, help="结果数量，默认10")
    args = parser.parse_args()

    headers = {"Accept": "application/vnd.github.v3+json"}
    if args.token:
        headers["Authorization"] = f"token {args.token}"

    url = f"https://api.github.com/search/issues?q={urllib.request.quote(args.query)}+repo:{args.repo}+is:issue+state:{args.state}&per_page={args.limit}"
    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req) as r:
            data = json.loads(r.read())
        print(f"=== {args.repo} Issues: '{args.query}' ({data['total_count']} 结果) ===\n")
        for issue in data.get("items", []):
            labels = [l["name"] for l in issue.get("labels", [])]
            print(f"#{issue['number']} | {issue['title']}")
            print(f"  State: {issue['state']} | Author: {issue['user']['login']}")
            if labels:
                print(f"  Labels: {', '.join(labels)}")
            print(f"  {issue['html_url']}")
            print()
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
