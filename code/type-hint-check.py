#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 type-hint-check.py - 检查Python文件中的类型注解完整性
 找出缺少类型注解的函数参数和返回值
"""

import ast
import os
import sys
import argparse
from pathlib import Path
from typing import Optional


class TypeHintChecker(ast.NodeVisitor):
    """使用AST分析类型注解完整性"""

    def __init__(self, filename: str):
        self.filename = filename
        self.issues = []

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self._check_function(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self._check_function(node)
        self.generic_visit(node)

    def _check_function(self, node):
        func_name = node.name
        lineno = node.lineno

        # 跳过私有函数和特殊方法
        if func_name.startswith('_') and not func_name.startswith('__'):
            return

        # 检查参数类型注解
        missing_arg_types = []
        for arg in node.args.args:
            if arg.annotation is None:
                missing_arg_types.append(arg.arg)

        # 检查可变默认参数缺少类型注解
        defaults = node.args.defaults
        args_with_defaults = node.args.args[-len(defaults):] if defaults else []
        mutable_args = []
        for arg, default in zip(args_with_defaults, defaults):
            if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                if arg.annotation is None and arg.arg not in ('self', 'cls'):
                    mutable_args.append(arg.arg)

        # 检查返回值类型注解
        returns = node.returns

        # 报告问题
        if missing_arg_types:
            self.issues.append({
                'file': self.filename,
                'line': lineno,
                'type': 'missing_arg_type',
                'func': func_name,
                'detail': f"缺少参数类型注解: {', '.join(missing_arg_types)}"
            })

        if mutable_args:
            self.issues.append({
                'file': self.filename,
                'line': lineno,
                'type': 'mutable_default',
                'func': func_name,
                'detail': f"可变默认参数缺少类型注解: {', '.join(mutable_args)}"
            })

        if returns is None and func_name not in ('__init__', '__post_init__', '__aenter__', '__aexit__'):
            # 排除明确无返回值的
            self.issues.append({
                'file': self.filename,
                'line': lineno,
                'type': 'missing_return_type',
                'func': func_name,
                'detail': "缺少返回值类型注解"
            })

    def visit_ClassDef(self, node: ast.ClassDef):
        # 跳过私有类
        if not node.name.startswith('_'):
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    # 检查实例变量和类变量的类型注解
                    for inner in ast.walk(item):
                        if isinstance(inner, ast.AnnAssign):
                            if isinstance(inner.target, ast.Name):
                                if inner.target.id in ('self', 'cls'):
                                    continue
        self.generic_visit(node)


def check_file(filepath: Path) -> list:
    """检查单个Python文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
        tree = ast.parse(source, filename=str(filepath))
        checker = TypeHintChecker(str(filepath))
        checker.visit(tree)
        return checker.issues
    except SyntaxError as e:
        return [{
            'file': str(filepath),
            'line': e.lineno or 0,
            'type': 'syntax_error',
            'func': '',
            'detail': f"语法错误: {e.msg}"
        }]
    except Exception as e:
        return [{
            'file': str(filepath),
            'line': 0,
            'type': 'error',
            'func': '',
            'detail': f"解析错误: {str(e)}"
        }]


def check_directory(root: Path, recursive: bool = True) -> list:
    """检查目录下所有Python文件"""
    all_issues = []
    pattern = '**/*.py' if recursive else '*.py'

    for filepath in root.glob(pattern):
        if filepath.name == '__init__.py':
            continue
        issues = check_file(filepath)
        all_issues.extend(issues)

    return all_issues


def main():
    parser = argparse.ArgumentParser(
        description='检查Python文件中的类型注解完整性',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('path', nargs='?', default='.', help='检查路径 (默认: 当前目录)')
    parser.add_argument('-r', '--no-recursive', action='store_true', help='不递归扫描子目录')
    parser.add_argument('--ignore', nargs='+', default=['__pycache__', '.git', 'venv', '.venv'],
                        help='忽略的目录')
    parser.add_argument('-o', '--output', help='输出到文件')
    parser.add_argument('--format', choices=['text', 'json'], default='text', help='输出格式')

    args = parser.parse_args()

    root = Path(args.path).resolve()
    if not root.exists():
        print(f"错误: 路径不存在: {root}", file=sys.stderr)
        sys.exit(1)

    print(f"正在检查: {root}")

    issues = check_directory(root, recursive=not args.no_recursive)

    if not issues:
        print("✅ 所有函数和参数都有完整的类型注解!")
        return

    # 按类型分组统计
    stats = {}
    for issue in issues:
        t = issue['type']
        stats[t] = stats.get(t, 0) + 1

    print("\n📊 问题统计:")
    for t, count in sorted(stats.items(), key=lambda x: -x[1]):
        label = {
            'missing_arg_type': '缺少参数类型注解',
            'missing_return_type': '缺少返回值类型注解',
            'mutable_default': '可变默认参数缺类型注解',
            'syntax_error': '语法错误',
            'error': '解析错误'
        }.get(t, t)
        print(f"  {label}: {count}")

    print("\n📋 详细列表:")
    print("-" * 70)

    for issue in sorted(issues, key=lambda x: (x['file'], x['line'])):
        icon = {
            'missing_arg_type': '🔴',
            'missing_return_type': '🟡',
            'mutable_default': '🟠',
            'syntax_error': '❌',
            'error': '❌'
        }.get(issue['type'], '⚪')

        func_info = f"{issue['func']}()" if issue['func'] else ""
        print(f"{icon} {issue['file']}:{issue['line']} {func_info}")
        print(f"   └─ {issue['detail']}")

    print("-" * 70)
    print(f"总计: {len(issues)} 个问题")


if __name__ == '__main__':
    main()
