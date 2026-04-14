#!/usr/bin/env python3
"""对比两个 .env 文件的差异。

Usage:
    python env-diff.py .env.example .env.local
"""

import argparse
import os


def parse_env(path):
    if not os.path.exists(path):
        return {}
    env = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip("\"'")
    return env


def main():
    parser = argparse.ArgumentParser(description="对比两个 .env 文件")
    parser.add_argument("file1")
    parser.add_argument("file2")
    args = parser.parse_args()

    env1 = parse_env(args.file1)
    env2 = parse_env(args.file2)

    all_keys = set(env1) | set(env2)

    print(f"{'键':<30} {'文件1':<25} {'文件2':<25} {'状态'}")
    print("-" * 95)

    for key in sorted(all_keys):
        v1 = env1.get(key, "（不存在）")
        v2 = env2.get(key, "（不存在）")
        if v1 == v2:
            status = "="
        elif key not in env1:
            status = "+ 新增"
        elif key not in env2:
            status = "- 缺失"
        else:
            status = "! 不同"
        print(f"{key:<30} {str(v1):<25} {str(v2):<25} {status}")


if __name__ == "__main__":
    main()
