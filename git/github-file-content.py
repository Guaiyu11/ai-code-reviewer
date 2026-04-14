#!/usr/bin/env python3
"""获取 GitHub 文件内容（无需 clone）。

Usage:
    python github-file-content.py <owner/repo> <path> [--branch BRANCH]
"""

import argparse
import urllib.request
import base64
import json
import sys


def main():
    parser = argparse.ArgumentParser(description="获取 GitHub 文件内容")
    parser.add_argument("repo", help="仓库名（格式: owner/repo）")
    parser.add_argument("path", help="文件路径，如 README.md")
    parser.add_argument("--branch", default="main", help="分支名，默认 main")
    args = parser.parse_args()

    url = f"https://api.github.com/repos/{args.repo}/contents/{args.path}?ref={args.branch}"
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github.v3+json"})

    try:
        with urllib.request.urlopen(req) as r:
            data = json.loads(r.read())
        if isinstance(data, list):
            print(f"这是一个目录，包含 {len(data)} 个文件/目录:")
            for item in data:
                print(f"  {item['type']:6} {item['name']}")
        else:
            content = base64.b64decode(data["content"]).decode("utf-8")
            print(f"文件: {data['path']} | SHA: {data['sha'][:8]}")
            print("-" * 40)
            print(content)
    except urllib.error.HTTPError as e:
        print(f"错误: 文件不存在或无权限 (HTTP {e.code})", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
