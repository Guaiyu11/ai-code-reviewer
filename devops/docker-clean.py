#!/usr/bin/env python3
"""清理 Docker 悬空镜像和已停止容器。

Usage:
    python docker-clean.py [--dry-run]
"""

import argparse
import subprocess


def run(cmd, dry_run):
    if dry_run:
        print(f"  [DRY-RUN] {cmd}")
    else:
        subprocess.run(cmd, shell=True)


def main():
    parser = argparse.ArgumentParser(description="清理 Docker 悬空资源")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    print("清理已停止容器...")
    run("docker container prune -f", args.dry_run)

    print("清理悬空镜像...")
    run("docker image prune -f", args.dry_run)

    print("清理无标签镜像...")
    run("docker image prune -a -f", args.dry_run)

    if args.dry_run:
        print("\n[DRY-RUN] 以上资源将被清理。")


if __name__ == "__main__":
    main()
