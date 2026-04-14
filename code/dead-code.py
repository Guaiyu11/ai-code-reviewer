#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 dead-code.py - 检测未使用的函数/类 (基于AST分析)
 分析函数定义和调用，找出从未被调用的定义
"""

import ast
import os
import sys
import argparse
from pathlib import Path
from collections import defaultdict


class CodeAnalyzer(ast.NodeVisitor):
    """分析代码中的定义和引用"""

    def __init__(self, filename: str):
        self.filename = filename
        self.definitions = {}  # name -> set of (type, lineno)
        self.references = defaultdict(set)  # name -> set of lineno where it's referenced
        self.current_class = None

    def _get_qualified_name(self, name: str) -> str:
        """获取带类前缀的限定名"""
        if self.current_class and not name.startswith('__'):
            return f"{self.current_class}.{name}"
        return name

    def visit_FunctionDef(self, node: ast.FunctionDef):
        name = node.name
        # 跳过特殊方法和私有函数
        if name.startswith('_') and name not in ('__init__', '__new__', '__call__'):
            self.generic_visit(node)
            return

        qual_name = self._get_qualified_name(name)
        self.definitions[qual_name] = (self.definitions.get(qual_name, set()) | {(node.name, node.lineno)})

        old_class = self.current_class
        if isinstance(node, ast.ClassDef):
            self.current_class = node.name
        self.generic_visit(node)
        self.current_class = old_class

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_ClassDef(self, node: ast.ClassDef):
        name = node.name
        if not name.startswith('_'):
            self.definitions[name] = (self.definitions.get(name, set()) | {(name, node.lineno)})

        old_class = self.current_class
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = old_class

    def visit_Name(self, node: ast.Name):
        if isinstance(node.ctx, ast.Load):
            self.references[node.id].add(node.lineno)
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute):
        # 处理 self.method() 形式的调用
        if isinstance(node.value, ast.Name) and node.value.id == 'self':
            self.references[node.attr].add(node.lineno)
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        # 直接函数调用
        if isinstance(node.func, ast.Name):
            self.references[node.func.id].add(node.lineno)
        # 方法调用 obj.method()
        elif isinstance(node.func, ast.Attribute):
            self.references[node.func.attr].add(node.lineno)
        self.generic_visit(node)


def analyze_file(filepath: Path) -> tuple:
    """分析单个文件，返回(定义, 引用)"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
        tree = ast.parse(source, filename=str(filepath))
        visitor = CodeAnalyzer(str(filepath))
        visitor.visit(tree)
        return visitor.definitions, visitor.references
    except Exception as e:
        return {}, {}


def find_dead_code(project_root: Path) -> dict:
    """查找整个项目的死代码"""
    all_definitions = {}  # module_name -> definitions
    all_references = defaultdict(set)  # name -> set of (module, lineno)

    py_files = [f for f in project_root.rglob('*.py')
                if '__pycache__' not in str(f) and f.name != '__init__.py']

    for filepath in py_files:
        module_name = filepath.stem
        defs, refs = analyze_file(filepath)

        # 合并定义
        for name, info in defs.items():
            full_name = f"{module_name}.{name}" if '.' not in name else name
            if full_name not in all_definitions:
                all_definitions[full_name] = []
            for item in info:
                all_definitions[full_name].append((str(filepath), item[1]))

        # 合并引用
        for name, lines in refs.items():
            all_references[name].update(lines)

    # 找出未被引用的定义
    dead_code = {}
    for name, locations in all_definitions.items():
        base_name = name.split('.')[-1]
        # 检查是否被引用（考虑各种调用形式）
        is_used = (
            base_name in all_references or
            name in all_references or
            any(base_name in refs for refs in all_references.values())
        )
        if not is_used:
            dead_code[name] = locations

    return dead_code, all_definitions


def main():
    parser = argparse.ArgumentParser(
        description='检测Python项目中未使用的函数/类 (基于AST分析)',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('path', nargs='?', default='.', help='项目目录 (默认: 当前目录)')
    parser.add_argument('-o', '--output', help='输出结果到文件')
    parser.add_argument('-q', '--quiet', action='store_true', help='只显示统计信息')
    parser.add_argument('--ignore', nargs='+', default=['__pycache__', '.git', 'venv', 'tests'],
                        help='忽略的目录')

    args = parser.parse_args()

    root = Path(args.path).resolve()
    if not root.exists():
        print(f"错误: 路径不存在: {root}", file=sys.stderr)
        sys.exit(1)

    print(f"正在分析: {root}")

    dead_code, all_defs = find_dead_code(root)

    if not dead_code:
        print("✅ 未发现死代码!")
        return

    print(f"\n📊 统计:")
    print(f"  总定义数: {len(all_defs)}")
    print(f"  死代码数: {len(dead_code)}")
    print(f"  存活率: {100 * (len(all_defs) - len(dead_code)) / max(len(all_defs), 1):.1f}%")

    if not args.quiet:
        print("\n💀 死代码列表:")
        print("-" * 60)

        for name, locations in sorted(dead_code.items()):
            for filepath, lineno in locations:
                print(f"  📄 {filepath}:{lineno}")
                print(f"     └─ {name}")

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            for name, locations in sorted(dead_code.items()):
                for filepath, lineno in locations:
                    f.write(f"{filepath}:{lineno} {name}\n")
        print(f"\n结果已保存到: {args.output}")


if __name__ == '__main__':
    main()
