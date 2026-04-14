#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 find-big-files.py - 找出仓库中最大的N个文件
 按文件大小排序，支持过滤文件类型
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path


def get_git_files(repo_path: Path = None) -> list:
    """获取git仓库中的所有文件"""
    cmd = ['git', 'ls-files']
    if repo_path:
        cmd[0:0] = ['git', '-C', str(repo_path)]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            cwd=repo_path
        )
        return [f.strip() for f in result.stdout.split('\n') if f.strip()]
    except subprocess.CalledProcessError:
        # 不是git仓库，返回所有文件
        return None


def get_file_size(filepath: Path) -> int:
    """获取文件大小"""
    try:
        return filepath.stat().st_size
    except (OSError, FileNotFoundError):
        return 0


def find_big_files(root: Path, n: int = 10, min_size: int = 0,
                   extensions: list = None, use_git: bool = True) -> list:
    """找出最大的文件"""
    files = []

    if use_git:
        git_files = get_git_files(root)
        if git_files is not None:
            # 在git跟踪的文件中查找
            for git_file in git_files:
                filepath = root / git_file
                if filepath.exists() and filepath.is_file():
                    size = get_file_size(filepath)
                    if size >= min_size:
                        if extensions is None or filepath.suffix in extensions:
                            files.append((str(filepath.relative_to(root)), size))
        else:
            use_git = False

    if not use_git:
        # 非git仓库，递归查找所有文件
        for filepath in root.rglob('*'):
            if filepath.is_file():
                # 排除隐藏目录
                if any(part.startswith('.') for part in filepath.parts):
                    continue
                size = get_file_size(filepath)
                if size >= min_size:
                    if extensions is None or filepath.suffix in extensions:
                        rel_path = str(filepath.relative_to(root))
                        files.append((rel_path, size))

    # 按大小排序
    files.sort(key=lambda x: x[1], reverse=True)

    return files[:n]


def format_size(size: int) -> str:
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} PB"


def main():
    parser = argparse.ArgumentParser(
        description='找出仓库中最大的N个文件',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('path', nargs='?', default='.', help='仓库路径 (默认: 当前目录)')
    parser.add_argument('-n', '--count', type=int, default=10, help='显示数量 (默认: 10)')
    parser.add_argument('-m', '--min-size', type=int, default=0,
                        help='最小文件大小 (字节, 默认: 0)')
    parser.add_argument('-e', '--extensions', nargs='+',
                        help='只显示指定扩展名 (如 .py .js)')
    parser.add_argument('-a', '--all', action='store_true', help='包含git忽略的文件')
    parser.add_argument('--no-git', action='store_true', help='不使用git追踪列表')
    parser.add_argument('-o', '--output', help='输出到文件')
    parser.add_argument('-s', '--sum', action='store_true', help='显示总计大小')

    args = parser.parse_args()

    root = Path(args.path).resolve()
    if not root.exists():
        print(f"错误: 路径不存在: {root}", file=sys.stderr)
        sys.exit(1)

    print(f"正在扫描: {root}")
    if args.extensions:
        print(f"扩展名过滤: {', '.join(args.extensions)}")

    files = find_big_files(
        root,
        n=args.count,
        min_size=args.min_size,
        extensions=args.extensions,
        use_git=not args.no_git
    )

    if not files:
        print("未找到符合条件的文件")
        return

    # 计算总大小
    total_size = sum(size for _, size in files)

    print(f"\n📊 最大的 {len(files)} 个文件:\n")
    print(f"{'排名':<6} {'大小':<12} {'路径'}")
    print("-" * 80)

    for i, (path, size) in enumerate(files, 1):
        print(f"{i:<6} {format_size(size):<12} {path}")

    print("-" * 80)
    print(f"{'':6} {format_size(total_size):<12} 总计")

    if args.sum:
        print(f"\n💾 磁盘使用分析:")
        by_extension = {}
        for path, size in files:
            ext = Path(path).suffix or '(无扩展名)'
            if ext not in by_extension:
                by_extension[ext] = {'count': 0, 'size': 0}
            by_extension[ext]['count'] += 1
            by_extension[ext]['size'] += size

        for ext, info in sorted(by_extension.items(), key=lambda x: -x[1]['size']):
            print(f"  {ext}: {info['count']} 个文件, {format_size(info['size'])}")

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            for path, size in files:
                f.write(f"{size}\t{path}\n")
        print(f"\n结果已保存到: {args.output}")


if __name__ == '__main__':
    main()
