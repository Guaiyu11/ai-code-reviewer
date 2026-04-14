#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 requirements-diff.py - 对比两个requirements.txt的差异
 分析新增、删除、版本变化的依赖
"""

import re
import sys
import argparse
from pathlib import Path
from dataclasses import dataclass


@dataclass
class Package:
    """包信息"""
    name: str
    version: str = None
    extras: str = None
    op: str = None  # >=, ==, !=, etc.
    original_line: str = None

    def __str__(self):
        if self.version:
            return f"{self.name}{self.op}{self.version}"
        return self.name

    @property
    def key(self) -> str:
        """用于比较的键 (小写规范化)"""
        name = self.name.lower().replace('-', '_').replace('_', '-')
        return name


def parse_requirements(filepath: Path) -> dict:
    """解析requirements文件，返回 {package_key: Package}"""
    packages = {}

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"错误: 无法读取文件 {filepath}: {e}", file=sys.stderr)
        return packages

    for line in lines:
        line = line.strip()

        # 跳过空行和注释
        if not line or line.startswith('#'):
            continue

        # 跳过 -r, -c, -e 等特殊指令
        if line.startswith('-'):
            continue

        pkg = parse_package_line(line)
        if pkg:
            packages[pkg.key] = pkg

    return packages


def parse_package_line(line: str) -> Package:
    """解析单行包规格"""
    original = line

    # 移除行尾注释
    if '#' in line:
        line = line.split('#')[0].strip()

    # 解析 extras: package[extra1,extra2]>=1.0
    extras_match = re.match(r'([a-zA-Z0-9_\-\.]+)(\[.*?\])?(.*)', line)
    if not extras_match:
        return None

    name = extras_match.group(1)
    extras = extras_match.group(2)
    remainder = extras_match.group(3) or ''

    # 解析版本约束
    version = None
    op = None

    version_patterns = [
        r'>=([0-9a-zA-Z\.\-_~]+)',
        r'<=([0-9A-Za-z\.\-_~]+)',
        r'==([0-9a-zA-Z\.\-_~]+)',
        r'!=([0-9a-zA-Z\.\-_~]+)',
        r'>([0-9a-zA-Z\.\-_~]+)',
        r'<([0-9a-zA-Z\.\-_~]+)',
        r'~=([0-9a-zA-Z\.\-_~]+)',  # compatible release
    ]

    for pattern in version_patterns:
        match = re.search(pattern, remainder)
        if match:
            version = match.group(1)
            op = pattern[0:2].replace('(', '').rstrip('~')
            break

    # 如果没有匹配到版本操作符但有版本号
    if not op and remainder.strip():
        version = remainder.strip()

    return Package(
        name=name,
        version=version,
        extras=extras,
        op=op,
        original_line=original
    )


def compare_requirements(old: dict, new: dict) -> dict:
    """对比两个requirements，返回差异"""
    result = {
        'added': [],      # 新增的包
        'removed': [],    # 删除的包
        'upgraded': [],   # 版本升级
        'downgraded': [], # 版本降级
        'unchanged': []   # 未变化的包
    }

    all_keys = set(old.keys()) | set(new.keys())

    for key in sorted(all_keys):
        old_pkg = old.get(key)
        new_pkg = new.get(key)

        if old_pkg and not new_pkg:
            result['removed'].append((old_pkg, None))
        elif new_pkg and not old_pkg:
            result['added'].append((None, new_pkg))
        elif old_pkg and new_pkg:
            if old_pkg.version == new_pkg.version:
                result['unchanged'].append((old_pkg, new_pkg))
            elif old_pkg.version and new_pkg.version:
                # 比较版本
                try:
                    old_ver = tuple(int(x) if x.isdigit() else x for x in re.split(r'[.\-]', old_pkg.version))
                    new_ver = tuple(int(x) if x.isdigit() else x for x in re.split(r'[.\-]', new_pkg.version))

                    if new_ver > old_ver:
                        result['upgraded'].append((old_pkg, new_pkg))
                    else:
                        result['downgraded'].append((old_pkg, new_pkg))
                except (ValueError, TypeError):
                    result['upgraded'].append((old_pkg, new_pkg))
            else:
                result['upgraded'].append((old_pkg, new_pkg))

    return result


def print_diff(diff: dict, show_unchanged: bool = False):
    """打印差异报告"""

    if diff['added']:
        print("\n🟢 新增依赖:")
        print("-" * 50)
        for _, pkg in diff['added']:
            print(f"  + {pkg.original_line}")

    if diff['removed']:
        print("\n🔴 删除依赖:")
        print("-" * 50)
        for pkg, _ in diff['removed']:
            print(f"  - {pkg.original_line}")

    if diff['upgraded']:
        print("\n🟡 升级依赖:")
        print("-" * 50)
        for old_pkg, new_pkg in diff['upgraded']:
            if old_pkg.version:
                print(f"  ^ {old_pkg.name}: {old_pkg.version} -> {new_pkg.version or '(any)'}")
            else:
                print(f"  ^ {old_pkg.name}: (any) -> {new_pkg.version or '(any)'}")

    if diff['downgraded']:
        print("\n🟠 降级依赖:")
        print("-" * 50)
        for old_pkg, new_pkg in diff['downgraded']:
            if old_pkg.version and new_pkg.version:
                print(f"  v {old_pkg.name}: {old_pkg.version} -> {new_pkg.version}")
            else:
                print(f"  v {old_pkg.name}: {old_pkg.version or '(any)'} -> {new_pkg.version or '(any)'}")

    if show_unchanged and diff['unchanged']:
        print("\n⚪ 未变化:")
        print("-" * 50)
        for pkg, _ in diff['unchanged']:
            print(f"    {pkg.original_line}")

    # 统计摘要
    total_added = len(diff['added'])
    total_removed = len(diff['removed'])
    total_changed = total_added + total_removed + len(diff['upgraded']) + len(diff['downgraded'])

    print("\n" + "=" * 50)
    print("📊 摘要:")
    print(f"  新增: {total_added}")
    print(f"  删除: {total_removed}")
    print(f"  版本变化: {len(diff['upgraded'])} 升级, {len(diff['downgraded'])} 降级")
    print(f"  未变化: {len(diff['unchanged'])}")
    print(f"  总变化: {total_changed}")


def main():
    parser = argparse.ArgumentParser(
        description='对比两个requirements.txt的差异',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('old', help='旧版本requirements文件')
    parser.add_argument('new', nargs='?', help='新版本requirements文件 (默认: stdin)')
    parser.add_argument('-s', '--show-unchanged', action='store_true', help='显示未变化的依赖')
    parser.add_argument('-o', '--output', help='输出到文件')
    parser.add_argument('--format', choices=['text', 'json', 'markdown'], default='text', help='输出格式')

    args = parser.parse_args()

    old_path = Path(args.old)
    if not old_path.exists():
        print(f"错误: 文件不存在: {old_path}", file=sys.stderr)
        sys.exit(1)

    old_packages = parse_requirements(old_path)

    if args.new:
        new_path = Path(args.new)
        if not new_path.exists():
            print(f"错误: 文件不存在: {new_path}", file=sys.stderr)
            sys.exit(1)
        new_packages = parse_requirements(new_path)
    else:
        # 从stdin读取
        import sys
        new_packages = parse_requirements(Path('-'))  # 需要特殊处理

    diff = compare_requirements(old_packages, new_packages)

    # 输出
    if args.format == 'text':
        print_diff(diff, args.show_unchanged)
    elif args.format == 'json':
        import json
        output = {
            'added': [{'name': str(n), 'line': n.original_line} for _, n in diff['added']],
            'removed': [{'name': str(o), 'line': o.original_line} for o, _ in diff['removed']],
            'upgraded': [{'name': str(n), 'old': str(o), 'new': str(n)} for o, n in diff['upgraded']],
            'downgraded': [{'name': str(n), 'old': str(o), 'new': str(n)} for o, n in diff['downgraded']],
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    elif args.format == 'markdown':
        print("## Requirements Diff\n")
        if diff['added']:
            print("### 新增")
            for _, pkg in diff['added']:
                print(f"- `{pkg.original_line}`")
        if diff['removed']:
            print("\n### 删除")
            for pkg, _ in diff['removed']:
                print(f"- ~~`{pkg.original_line}`~~")
        if diff['upgraded']:
            print("\n### 升级")
            for o, n in diff['upgraded']:
                print(f"- `{o.name}`: `{o.version}` -> `{n.version}`")

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            pass  # 已在上面打印


if __name__ == '__main__':
    main()
