#!/usr/bin/env python3
"""获取 GitHub 仓库信息。

Usage:
    python github-repo-info.py <owner/repo> [--token TOKEN]
"""

import argparse
import urllib.request
import json
import sys


def main():
    parser = argparse.ArgumentParser(description="获取 GitHub 仓库信息")
    parser.add_argument("repo", help="仓库名（格式: owner/repo）")
    parser.add_argument("--token", default="", help="GitHub Token（可选）")
    args = parser.parse_args()

    headers = {"Accept": "application/vnd.github.v3+json"}
    if args.token:
        headers["Authorization"] = f"token {args.token}"

    req = urllib.request.Request(
        f"https://api.github.com/repos/{args.repo}", headers=headers
    )
    try:
        with urllib.request.urlopen(req) as r:
            data = json.loads(r.read())
        print(f"仓库: {data['full_name']}")
        print(f"描述: {data['description']}")
        print(f"语言: {data['language']}")
        print(f"Stars: {data['stargazers_count']}")
        print(f"Forks: {data['forks_count']}")
        print(f"Open Issues: {data['open_issues_count']}")
        print(f"License: {data['license']['name'] if data.get('license') else 'None'}")
        print(f"创建: {data['created_at'][:10]}")
        print(f"更新: {data['updated_at'][:10]}")
        print(f"URL: {data['html_url']}")
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
