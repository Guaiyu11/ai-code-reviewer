#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 patch-apply.py - 生成和应用代码差异补丁
 支持创建.diff文件和打补丁
"""

import subprocess
import sys
import os
import argparse
import re
from pathlib import Path


def run_git(args: list) -> tuple:
    """运行git命令"""
    try:
        result = subprocess.run(
            ['git'] + args,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return e.stdout or '', e.stderr or ''
    except FileNotFoundError:
        return '', 'git命令未找到'


def create_patch(commit_range: str = None, staged: bool = False,
                 output_file: str = None) -> str:
    """生成补丁文件"""
    args = ['diff']

    if staged:
        args.append('--cached')

    if commit_range:
        args.append(commit_range)
    else:
        # 未指定的参数，获取所有变更
        if not staged:
            args.append('HEAD')

    args.extend(['--', '.'])

    stdout, stderr = run_git(args)

    if stderr and not stdout:
        print(f"警告: {stderr}", file=sys.stderr)

    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(stdout)
        print(f"补丁已保存到: {output_file}")
        print(f"补丁大小: {len(stdout)} 字节")
    else:
        print(stdout)

    return stdout


def apply_patch(patch_file: str, check_only: bool = False,
                reverse: bool = False, threeway: bool = False) -> bool:
    """应用补丁"""
    if not Path(patch_file).exists():
        print(f"错误: 补丁文件不存在: {patch_file}", file=sys.stderr)
        return False

    with open(patch_file, 'r', encoding='utf-8') as f:
        patch_content = f.read()

    if not patch_content.strip():
        print("补丁文件为空")
        return False

    args = ['apply']

    if check_only:
        args.append('--check')
        print("🔍 检查模式 (--check)")

    if reverse:
        args.append('--reverse')
        print("🔄 反向应用")

    if threeway:
        args.append('--3way')
        print("🔗 三路合并模式")

    args.append(patch_file)

    stdout, stderr = run_git(args)

    if stderr:
        print(stderr)

    if stdout:
        print(stdout)

    # 检查结果
    if check_only:
        if 'error' in stderr.lower() or 'failed' in stderr.lower():
            print("❌ 补丁检查失败")
            return False
        else:
            print("✅ 补丁检查通过")
            return True
    else:
        print("✅ 补丁应用成功")
        return True


def format_patch(commit: str = 'HEAD', output_dir: str = None) -> list:
    """生成格式化补丁 (用于邮件列表风格)"""
    args = ['format-patch', '--stdout', '-1', commit]

    stdout, stderr = run_git(args)

    if stderr:
        print(f"警告: {stderr}", file=sys.stderr)

    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # 提取每个补丁
        patches = stdout.split('\n\n')
        for i, patch in enumerate(patches):
            if patch.startswith('From ') or patch.startswith('From:'):
                # 提取 From 行作为文件名
                from_match = re.search(r'^From: (.+?) <', patch, re.MULTILINE)
                date_match = re.search(r'^Date: (.+?)$', patch, re.MULTILINE)
                subject_match = re.search(r'^Subject: (.+?)$', patch, re.MULTILINE)

                filename = f"{i+1:04d}_"
                if subject_match:
                    filename += re.sub(r'[^\w\-]', '_', subject_match.group(1))[:50]
                else:
                    filename += f"patch_{i+1}"

                filename += '.patch'

                filepath = output_path / filename
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(patch)
                print(f"保存: {filepath}")
    else:
        print(stdout)

    return []


def diff_stats(commit_range: str = None) -> dict:
    """获取diff统计信息"""
    args = ['diff', '--stat']
    if commit_range:
        args.append(commit_range)

    stdout, _ = run_git(args)
    print(stdout)

    # 解析统计
    stats = {}
    for line in stdout.split('\n'):
        if '|' in line:
            parts = line.split('|')
            file = parts[0].strip()
            changes = parts[1].strip() if len(parts) > 1 else ''
            stats[file] = changes

    return stats


def main():
    parser = argparse.ArgumentParser(
        description='生成和应用代码差异补丁',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s create -o changes.diff          # 创建完整补丁
  %(prog)s create --staged -o staged.diff  # 创建已暂存补丁
  %(prog)s create HEAD~5..HEAD -o diff.diff  # 创建指定范围补丁
  %(prog)s apply changes.diff              # 应用补丁
  %(prog)s check changes.diff              # 检查补丁能否应用
  %(prog)s reverse changes.diff            # 反向应用补丁
  %(prog)s format -o patches/             # 生成邮件列表风格补丁
        """
    )
    subparsers = parser.add_subparsers(dest='command', help='子命令')

    # create 子命令
    create_parser = subparsers.add_parser('create', help='生成补丁')
    create_parser.add_argument('range', nargs='?', help='提交范围 (如 HEAD~5..HEAD)')
    create_parser.add_argument('--staged', action='store_true', help='生成已暂存的变更')
    create_parser.add_argument('-o', '--output', required=True, help='输出文件')

    # apply 子命令
    apply_parser = subparsers.add_parser('apply', help='应用补丁')
    apply_parser.add_argument('patch', help='补丁文件')
    apply_parser.add_argument('--check', action='store_true', help='只检查不应用')
    apply_parser.add_argument('--reverse', action='store_true', help='反向应用')
    apply_parser.add_argument('--3way', action='store_true', help='三路合并')

    # format 子命令
    format_parser = subparsers.add_parser('format', help='生成格式化补丁')
    format_parser.add_argument('commit', nargs='?', default='HEAD', help='提交')
    format_parser.add_argument('-o', '--output', help='输出目录')

    # stats 子命令
    stats_parser = subparsers.add_parser('stats', help='查看diff统计')
    stats_parser.add_argument('range', nargs='?', help='提交范围')

    args = parser.parse_args()

    if not args.command:
        # 默认行为：创建补丁
        create_patch(output_file='changes.diff')
    elif args.command == 'create':
        create_patch(
            commit_range=args.range,
            staged=args.staged,
            output_file=args.output
        )
    elif args.command == 'apply':
        success = apply_patch(
            args.patch,
            check_only=args.check,
            reverse=args.reverse,
            threeway=args.threeway
        )
        sys.exit(0 if success else 1)
    elif args.command == 'format':
        format_patch(commit=args.commit, output_dir=args.output)
    elif args.command == 'stats':
        diff_stats(commit_range=args.range)


if __name__ == '__main__':
    main()
