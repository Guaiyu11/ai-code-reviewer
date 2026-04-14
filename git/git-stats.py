#!/usr/bin/env python3
"""显示 Git 仓库提交统计。

Usage:
    python git-stats.py [--days 30]
"""

import argparse
import subprocess
from datetime import datetime, timedelta
from collections import Counter


def main():
    parser = argparse.ArgumentParser(description="Git 提交统计")
    parser.add_argument("--days", type=int, default=30, help="统计天数，默认30天")
    args = parser.parse_args()

    since = (datetime.now() - timedelta(days=args.days)).strftime("%Y-%m-%d")
    result = subprocess.run(
        ["git", "log", f"--since={since}", "--format=%ae"],
        capture_output=True, text=True
    )
    authors = [a.strip() for a in result.stdout.strip().split("\n") if a.strip()]
    total = len(authors)

    print(f"=== 最近 {args.days} 天提交统计 ===")
    print(f"总提交数: {total}")
    print(f"贡献者数: {len(set(authors))}")
    print(f"\n提交排行:")
    for author, count in Counter(authors).most_common(10):
        bar = "█" * count
        print(f"  {count:>3} {bar} {author}")


if __name__ == "__main__":
    main()
