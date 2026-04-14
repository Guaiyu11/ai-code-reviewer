#!/usr/bin/env python3
"""计算文件哈希值（MD5/SHA256/SHA512）。

Usage:
    python file-hash.py <file> [--algo sha256]
"""

import argparse
import hashlib
import sys


def main():
    parser = argparse.ArgumentParser(description="计算文件哈希")
    parser.add_argument("file", help="文件路径")
    parser.add_argument("--algo", default="sha256", choices=["md5", "sha1", "sha256", "sha512"],
                        help="哈希算法，默认 sha256")
    args = parser.parse_args()

    try:
        with open(args.file, "rb") as f:
            data = f.read()
        h = hashlib.new(args.algo)
        h.update(data)
        print(f"{args.algo.upper()}: {h.hexdigest()}  {args.file}")
    except FileNotFoundError:
        print(f"文件不存在: {args.file}", file=sys.stderr)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
