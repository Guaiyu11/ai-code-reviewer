#!/usr/bin/env python3
"""从 JSON 文件中提取指定路径的值（类似 JSONPath 简化版）。

Usage:
    python json-path.py <file.json> <path>
Example:
    python json-path.py data.json "data.users[0].name"
"""

import argparse
import json
import re
import sys


def extract(data, path):
    current = data
    parts = re.findall(r"\[([^\]]+)\]|\.(\w+)", path)
    for bracket, dot in parts:
        key = bracket if bracket else dot
        try:
            if isinstance(current, dict):
                current = current[key]
            elif isinstance(current, list):
                current = current[int(key)]
        except (KeyError, IndexError, ValueError):
            return None
    return current


def main():
    parser = argparse.ArgumentParser(description="从 JSON 提取路径值")
    parser.add_argument("file", help="JSON 文件路径")
    parser.add_argument("path", help="路径，如 data.users[0].name")
    args = parser.parse_args()

    try:
        with open(args.file) as f:
            data = json.load(f)
        result = extract(data, args.path)
        if result is None:
            print(f"路径不存在: {args.path}")
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
    except FileNotFoundError:
        print(f"文件不存在: {args.file}", file=sys.stderr)
    except json.JSONDecodeError as e:
        print(f"JSON 解析错误: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
