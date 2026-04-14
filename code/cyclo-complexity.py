#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 cyclo-complexity.py - 计算圈复杂度，详细报告每个函数的分值
 圈复杂度衡量代码的复杂程度，数值越高表示越难维护
"""

import ast
import os
import sys
import argparse
from pathlib import Path
from dataclasses import dataclass


@dataclass
class FunctionMetrics:
    """函数度量数据"""
    name: str
    lineno: int
    complexity: int
    file: str
    arg_count: int = 0

    @property
    def rating(self) -> str:
        """复杂度评级"""
        if self.complexity <= 10:
            return "✅ 低 (易测试)"
        elif self.complexity <= 20:
            return "🟡 中 (需关注)"
        elif self.complexity <= 50:
            return "🟠 高 (难测试)"
        else:
            return "🔴 极高 (需重构)"


class CycloComplexityVisitor(ast.NodeVisitor):
    """计算圈复杂度的AST访问器"""

    def __init__(self, filename: str):
        self.filename = filename
        self.functions = []
        self.current_function = None
        self.current_class = None

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self._analyze_function(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self._analyze_function(node)
        self.generic_visit(node)

    def _analyze_function(self, node):
        # 跳过短的私有函数
        if node.name.startswith('_') and len(node.body) < 5:
            return

        complexity = self._calculate_complexity(node)
        qual_name = node.name
        if self.current_class:
            qual_name = f"{self.current_class}.{node.name}"

        self.functions.append(FunctionMetrics(
            name=qual_name,
            lineno=node.lineno,
            complexity=complexity,
            file=self.filename,
            arg_count=len(node.args.args)
        ))

    def visit_ClassDef(self, node: ast.ClassDef):
        old_class = self.current_class
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = old_class

    def _calculate_complexity(self, node: ast.FunctionDef) -> int:
        """计算函数的圈复杂度"""
        complexity = 1  # 基础复杂度

        for child in ast.walk(node):
            # if/elif/else
            if isinstance(child, ast.If):
                complexity += 1
                # 检查条件中的布尔操作符
                complexity += self._count_bool_ops(child.test)

            # 三元表达式
            elif isinstance(child, ast.IfExp):
                complexity += 1

            # for循环
            elif isinstance(child, (ast.For, ast.AsyncFor)):
                complexity += 1

            # while循环
            elif isinstance(child, ast.While):
                complexity += 1

            # except处理器
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1

            # and/or布尔操作
            elif isinstance(child, (ast.BoolOp, ast.And, ast.Or)):
                pass  # 已在_if处理

            # try分支
            elif isinstance(child, ast.Try):
                complexity += len(child.handlers)
                if child.orelse:
                    complexity += 1

            # with语句
            elif isinstance(child, (ast.With, ast.AsyncWith)):
                complexity += 1

        return complexity

    def _count_bool_ops(self, node) -> int:
        """计算布尔操作符数量"""
        if isinstance(node, ast.BoolOp):
            return len(node.values) - 1
        return 0


def analyze_file(filepath: Path) -> list:
    """分析单个文件的圈复杂度"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
        tree = ast.parse(source, filename=str(filepath))
        visitor = CycloComplexityVisitor(str(filepath))
        visitor.visit(tree)
        return visitor.functions
    except Exception:
        return []


def analyze_directory(root: Path) -> list:
    """分析目录下所有Python文件"""
    all_functions = []

    for filepath in root.rglob('*.py'):
        if '__pycache__' in str(filepath):
            continue
        functions = analyze_file(filepath)
        all_functions.extend(functions)

    return all_functions


def main():
    parser = argparse.ArgumentParser(
        description='计算Python函数的圈复杂度',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
圈复杂度等级:
  1-10:   ✅ 低    - 代码清晰，易于测试和维护
  11-20:  🟡 中    - 代码尚可，需要适当测试
  21-50:  🟠 高    - 代码复杂，需要充分测试
  51+:    🔴 极高  - 代码极复杂，强烈建议重构
        """
    )
    parser.add_argument('path', nargs='?', default='.', help='文件或目录 (默认: 当前目录)')
    parser.add_argument('-t', '--threshold', type=int, default=10, help='显示阈值 (默认: 10)')
    parser.add_argument('-o', '--output', help='输出到文件')
    parser.add_argument('--top', type=int, help='只显示复杂度最高的N个函数')
    parser.add_argument('-s', '--sort', choices=['complexity', 'name', 'file'], default='complexity',
                        help='排序方式')

    args = parser.parse_args()

    root = Path(args.path).resolve()
    if not root.exists():
        print(f"错误: 路径不存在: {root}", file=sys.stderr)
        sys.exit(1)

    if root.is_file():
        functions = analyze_file(root)
        print(f"文件: {root}")
    else:
        functions = analyze_directory(root)
        print(f"目录: {root}")

    if not functions:
        print("未找到可分析的函数")
        return

    # 统计
    total = len(functions)
    high = sum(1 for f in functions if f.complexity > args.threshold)
    avg = sum(f.complexity for f in functions) / total

    print(f"\n📊 统计:")
    print(f"  函数总数: {total}")
    print(f"  超过阈值({args.threshold}): {high}")
    print(f"  平均复杂度: {avg:.1f}")

    # 过滤和排序
    display_functions = [f for f in functions if f.complexity >= args.threshold]

    if args.top:
        display_functions = sorted(display_functions, key=lambda x: -x.complexity)[:args.top]

    if args.sort == 'complexity':
        display_functions.sort(key=lambda x: -x.complexity)
    elif args.sort == 'name':
        display_functions.sort(key=lambda x: x.name)
    elif args.sort == 'file':
        display_functions.sort(key=lambda x: (x.file, x.lineno))

    if display_functions:
        print(f"\n📋 函数详情 (复杂度 >= {args.threshold}):")
        print("-" * 70)

        for func in display_functions:
            rating = func.rating
            print(f"{rating} {func.name}")
            print(f"   文件: {func.file}:{func.lineno} | 复杂度: {func.complexity} | 参数: {func.arg_count}")

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            for func in sorted(display_functions, key=lambda x: -x.complexity):
                f.write(f"{func.complexity} {func.file}:{func.lineno} {func.name}\n")
        print(f"\n结果已保存到: {args.output}")


if __name__ == '__main__':
    main()
