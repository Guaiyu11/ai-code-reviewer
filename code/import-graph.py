#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 import-graph.py - 生成Python项目的import依赖关系图
 输出Graphviz DOT格式，可转换为PNG/SVG等
"""

import ast
import os
import sys
import argparse
from pathlib import Path
from collections import defaultdict


class ImportVisitor(ast.NodeVisitor):
    """收集import信息"""

    def __init__(self, filename: str, package_root: str):
        self.filename = filename
        self.package_root = package_root
        self.imports = []  # 当前文件导入的模块
        self.imported_by = []  # 导入当前文件的模块

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            self.imports.append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module:
            self.imports.append(node.module)
        self.generic_visit(node)


def get_module_name(filepath: Path, package_root: Path) -> str:
    """从文件路径推断模块名"""
    try:
        rel = filepath.relative_to(package_root)
        parts = list(rel.parts[:-1]) + [filepath.stem]
        return '.'.join(parts)
    except ValueError:
        return filepath.stem


def parse_file(filepath: Path, package_root: Path) -> ImportVisitor:
    """解析Python文件收集import信息"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
        tree = ast.parse(source, filename=str(filepath))
        visitor = ImportVisitor(str(filepath), str(package_root))
        visitor.visit(tree)
        return visitor
    except SyntaxError:
        return ImportVisitor(str(filepath), str(package_root))
    except Exception:
        return ImportVisitor(str(filepath), str(package_root))


def build_graph(root: Path) -> dict:
    """构建模块依赖图"""
    modules = {}  # module_name -> ImportVisitor
    graph = defaultdict(set)  # module -> set of imported modules

    # 收集所有Python文件
    py_files = list(root.rglob('*.py'))
    py_files = [f for f in py_files if '__pycache__' not in str(f) and f.name != '__init__.py']

    for filepath in py_files:
        module_name = get_module_name(filepath, root)
        visitor = parse_file(filepath, root)
        modules[module_name] = visitor

        # 过滤外部模块
        internal_imports = set()
        for imp in visitor.imports:
            # 只保留内部模块
            if imp.startswith('.'):
                # 相对导入
                internal_imports.add(imp.lstrip('.'))
            elif imp in modules or any(imp.startswith(m + '.') for m in modules):
                internal_imports.add(imp.split('.')[0])

        for imp in internal_imports:
            if imp in modules:
                graph[module_name].add(imp)

    return graph, modules


def to_dot(graph: dict, modules: dict, output_file: str = None):
    """生成DOT格式输出"""
    lines = [
        'digraph import_graph {',
        '    rankdir=LR;',
        '    node [shape=box, style=rounded];',
        '    edge [color=gray50, arrowsize=0.8];',
        '    graph [label="Python Import Dependency Graph", fontsize=14];',
        ''
    ]

    # 添加节点
    for module_name in sorted(modules.keys()):
        label = module_name.split('.')[-1]  # 只显示最后一部分
        lines.append(f'    "{module_name}" [label="{label}"];')

    lines.append('')

    # 添加边 (import关系: A -> B 表示A imports B)
    seen_edges = set()
    for module, imports in sorted(graph.items()):
        for imp in sorted(imports):
            edge = (module, imp)
            if edge not in seen_edges:
                seen_edges.add(edge)
                lines.append(f'    "{module}" -> "{imp}";')

    lines.append('}')

    content = '\n'.join(lines)

    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"DOT图已保存到: {output_file}")
        print(f"转换为PNG: dot -Tpng {output_file} -o output.png")
        print(f"转换为SVG: dot -Tsvg {output_file} -o output.svg")
    else:
        print(content)


def main():
    parser = argparse.ArgumentParser(
        description='生成Python项目的import依赖关系图 (DOT格式)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python import-graph.py .                        # 生成当前目录的依赖图
  python import-graph.py ./src -o import.dot      # 生成并保存DOT文件
  dot -Tpng import.dot -o import.png             # 转换为PNG
        """
    )
    parser.add_argument('path', nargs='?', default='.', help='项目根目录 (默认: 当前目录)')
    parser.add_argument('-o', '--output', help='输出DOT文件路径')
    parser.add_argument('--ignore', nargs='+', default=['__pycache__', '.git', 'venv', '.venv', 'tests'],
                        help='忽略的目录')

    args = parser.parse_args()

    root = Path(args.path).resolve()
    if not root.exists():
        print(f"错误: 路径不存在: {root}", file=sys.stderr)
        sys.exit(1)

    print(f"正在分析: {root}")
    graph, modules = build_graph(root)

    print(f"发现 {len(modules)} 个模块")
    total_imports = sum(len(imps) for imps in graph.values())
    print(f"发现 {total_imports} 个内部依赖关系")

    to_dot(graph, modules, args.output)


if __name__ == '__main__':
    main()
