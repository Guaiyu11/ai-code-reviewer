#!/usr/bin/env python3
"""获取 GitHub 最新 Release 信息。

Usage:
    python github-latest-release.py <owner/repo> [--token TOKEN]
"""

import argparse
import urllib.request
import json
import sys


def main():
    parser = argparse.ArgumentParser(description="获取 GitHub 最新 Release")
    parser.add_argument("repo", help="仓库名（格式: owner/repo）")
    parser.add_argument("--token", default="", help="GitHub Token（可选）")
    args = parser.parse_args()

    headers = {"Accept": "application/vnd.github.v3+json"}
    if args.token:
        headers["Authorization"] = f"token {args.token}"

    url = f"https://api.github.com/repos/{args.repo}/releases/latest"
    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req) as r:
            data = json.loads(r.read())
        print(f"版本: {data['tag_name']}")
        print(f"标题: {data['name']}")
        print(f"发布者: {data['author']['login']}")
        print(f"日期: {data['published_at'][:10]}")
        print(f"预发布: {data['prerelease']}")
        print(f"URL: {data['html_url']}")
        if data.get("body"):
            print(f"\n更新内容:\n{data['body'][:500]}")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"没有找到 Release: {args.repo}")
        else:
            print(f"错误: {e}", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
