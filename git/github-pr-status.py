#!/usr/bin/env python3
"""查看 GitHub PR 状态。

Usage:
    python github-pr-status.py <owner> <repo> [--token TOKEN]
"""

import argparse
import urllib.request
import json
import sys


def get_prs(owner, repo, token):
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    url = f"https://api.github.com/repos/{owner}/{repo}/pulls?state=open&per_page=20"
    req = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())


def main():
    parser = argparse.ArgumentParser(description="查看 GitHub PR 状态")
    parser.add_argument("owner", help="仓库所有者")
    parser.add_argument("repo", help="仓库名")
    parser.add_argument("--token", default="", help="GitHub Token（可选）")
    args = parser.parse_args()

    try:
        prs = get_prs(args.owner, args.repo, args.token)
        print(f"=== {args.owner}/{args.repo} Open PRs ({len(prs)}) ===\n")
        for pr in prs:
            print(f"#{pr['number']} | {pr['title']}")
            print(f"  Author: {pr['user']['login']} | State: {pr['state']}")
            print(f"  {pr['html_url']}")
            print()
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
