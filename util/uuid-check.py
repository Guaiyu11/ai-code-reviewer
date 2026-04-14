#!/usr/bin/env python3
"""验证 UUID 格式。

Usage:
    python uuid-check.py [uuid...]
"""

import argparse
import uuid
import sys


def validate_uuid(val):
    try:
        u = uuid.UUID(val)
        return True, str(u)
    except ValueError:
        return False, None


def main():
    parser = argparse.ArgumentParser(description="验证 UUID 格式")
    parser.add_argument("uuids", nargs="*", help="UUID 值（可多个）")
    args = parser.parse_args()

    if not args.uuids:
        # 交互模式
        print("输入 UUID 进行验证（输入空行退出）:")
        while True:
            try:
                line = input("> ").strip()
                if not line:
                    break
                valid, result = validate_uuid(line)
                print(f"  {'✓ 有效' if valid else '✗ 无效'} {result or line}")
            except EOFError:
                break
        return

    for val in args.uuids:
        valid, result = validate_uuid(val)
        status = "✓" if valid else "✗"
        print(f"{status} {val} {'-> ' + result if valid else ''}")


if __name__ == "__main__":
    main()
