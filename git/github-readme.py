#!/usr/bin/env python3
"""下载并显示 GitHub 仓库 README。

Usage:
    python github-readme.py <owner/repo> [--raw]
"""

import argparse
import urllib.request
import base64
import json
import sys


def main():
    parser = argparse.ArgumentParser(description="获取 GitHub README")
    parser.add_argument("repo", help="仓库名（格式: owner/repo）")
    parser.add_argument("--raw", action="store_true", help="输出原始 Markdown")
    args = parser.parse_args()

    headers = {"Accept": "application/vnd.github.v3+json"}
    url = f"https://api.github.com/repos/{args.repo}/readme"
    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req) as r:
            data = json.loads(r.read())
        content = base64.b64decode(data["content"]).decode("utf-8")
        print(content)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
