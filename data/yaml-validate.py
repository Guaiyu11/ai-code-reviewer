#!/usr/bin/env python3
"""验证 YAML 文件语法。

Usage:
    python yaml-validate.py <file.yaml>
"""

import argparse
import sys

try:
    import yaml
except ImportError:
    yaml = None


def main():
    parser = argparse.ArgumentParser(description="验证 YAML 语法")
    parser.add_argument("file", help="YAML 文件路径")
    args = parser.parse_args()

    if yaml is None:
        print("需要 PyYAML: pip install pyyaml", file=sys.stderr)
        sys.exit(1)

    try:
        with open(args.file) as f:
            yaml.safe_load(f)
        print(f"✓ YAML 语法正确: {args.file}")
    except FileNotFoundError:
        print(f"文件不存在: {args.file}", file=sys.stderr)
    except yaml.YAMLError as e:
        print(f"✗ YAML 语法错误:", file=sys.stderr)
        print(e, file=sys.stderr)


if __name__ == "__main__":
    main()
