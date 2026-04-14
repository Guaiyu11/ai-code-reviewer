#!/usr/bin/env python3
"""计算 Python 文件的圈复杂度（简单版）。

Usage:
    python code-complexity.py <file.py>
"""

import argparse
import ast
import sys


class ComplexityVisitor(ast.NodeVisitor):
    def __init__(self):
        self.complexity = 1
        self.functions = []

    def visit_FunctionDef(self, node):
        func_complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                func_complexity += 1
            elif isinstance(child, ast.BoolOp):
                func_complexity += len(child.values) - 1
        self.functions.append((node.name, func_complexity))
        self.complexity += func_complexity
        self.generic_visit(node)


def main():
    parser = argparse.ArgumentParser(description="计算代码圈复杂度")
    parser.add_argument("file", help="Python 文件路径")
    args = parser.parse_args()

    try:
        with open(args.file) as f:
            tree = ast.parse(f.read())
        visitor = ComplexityVisitor()
        visitor.visit(tree)

        print(f"文件: {args.file}")
        print(f"总复杂度: {visitor.complexity}")
        print(f"\n函数复杂度:")
        for name, c in sorted(visitor.functions, key=lambda x: -x[1]):
            level = " 高" if c > 10 else " 中" if c > 5 else " 低"
            print(f"  {c:>3}{level}  {name}")
    except FileNotFoundError:
        print(f"文件不存在: {args.file}", file=sys.stderr)
    except SyntaxError as e:
        print(f"语法错误: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
