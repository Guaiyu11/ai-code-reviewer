#!/usr/bin/env python3
"""验证 cron 表达式是否合法。

Usage:
    python cron-validate.py "<expression>"
    python cron-validate.py --list  # 列出所有 cron 字段
"""

import argparse
import re


def validate_cron(expr):
    parts = expr.strip().split()
    if len(parts) != 5:
        return False, f"需要5个字段，当前 {len(parts)} 个"

    names = ["分钟", "小时", "日", "月", "星期"]
    constraints = [(0, 59), (0, 23), (1, 31), (1, 12), (0, 6)]

    for i, (part, (lo, hi), name) in enumerate(zip(parts, constraints, names)):
        if part == "*":
            continue
        if "/" in part:
            base, step = part.split("/")
            if base != "*":
                try:
                    base = int(base)
                    if not (lo <= base <= hi):
                        return False, f"{name} 字段基础值 {base} 超出范围 [{lo},{hi}]"
                except ValueError:
                    return False, f"{name} 字段无效: {part}"
            continue
        if "," in part:
            for p in part.split(","):
                try:
                    v = int(p)
                    if not (lo <= v <= hi):
                        return False, f"{name} 字段值 {v} 超出范围 [{lo},{hi}]"
                except ValueError:
                    return False, f"{name} 字段无效: {p}"
            continue
        if "-" in part:
            start, end = part.split("-")
            try:
                s, e = int(start), int(end)
                if not (lo <= s <= hi and lo <= e <= hi):
                    return False, f"{name} 字段范围 [{s},{e}] 超出 [{lo},{hi}]"
            except ValueError:
                return False, f"{name} 字段无效: {part}"
            continue
        try:
            v = int(part)
            if not (lo <= v <= hi):
                return False, f"{name} 字段值 {v} 超出范围 [{lo},{hi}]"
        except ValueError:
            return False, f"{name} 字段无效: {part}"

    return True, "有效"


def main():
    parser = argparse.ArgumentParser(description="验证 cron 表达式")
    parser.add_argument("expression", nargs="?", help="cron 表达式，如 '*/5 * * * *'")
    parser.add_argument("--list", action="store_true", help="列出 cron 字段说明")
    args = parser.parse_args()

    if args.list:
        print("cron 表达式格式: 分 时 日 月 周")
        print("  分钟:  0-59")
        print("  小时:  0-23")
        print("  日:    1-31")
        print("  月:    1-12")
        print("  星期:  0-6 (0=周日)")
        print("\n特殊字符: * 任一值  / 步长  , 列表  - 范围")
        print("\n示例:")
        print("  */5 * * * *   每5分钟")
        print("  0 9 * * 1-5  每周一到周五9点")
        print("  0 0 1 * *     每月1号午夜")
        return

    if not args.expression:
        parser.print_help()
        return

    valid, msg = validate_cron(args.expression)
    print(f"表达式: {args.expression}")
    print(f"结果: {'✓ 有效' if valid else '✗ 无效'}")
    if not valid:
        print(f"原因: {msg}")


if __name__ == "__main__":
    main()
