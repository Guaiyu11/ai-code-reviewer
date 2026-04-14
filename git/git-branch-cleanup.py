#!/usr/bin/env python3
"""删除已合并到 main 的本地分支。

Usage:
    python git-branch-cleanup.py [--dry-run] [--branch main]
"""

import argparse
import subprocess
import sys


def get_merged_branches(branch):
    result = subprocess.run(
        ["git", "branch", "--merged", branch],
        capture_output=True, text=True
    )
    branches = [b.strip() for b in result.stdout.strip().split("\n") if b.strip() and b.strip() != branch]
    return branches


def delete_branch(branch, dry_run):
    if dry_run:
        print(f"  [DRY-RUN] Would delete: {branch}")
    else:
        subprocess.run(["git", "branch", "-d", branch])
        print(f"  Deleted: {branch}")


def main():
    parser = argparse.ArgumentParser(description="清理已合并的本地分支")
    parser.add_argument("--dry-run", action="store_true", help="仅预览，不删除")
    parser.add_argument("--branch", default="main", help="目标分支，默认 main")
    args = parser.parse_args()

    merged = get_merged_branches(args.branch)
    if not merged:
        print("没有已合并的分支需要清理。")
        return

    print(f"发现 {len(merged)} 个已合并分支（目标: {args.branch}）:")
    for branch in merged:
        delete_branch(branch, args.dry_run)

    if args.dry_run:
        print(f"\n[DRY-RUN] 以上分支将被删除。重新运行不加 --dry-run 来实际删除。")


if __name__ == "__main__":
    main()
