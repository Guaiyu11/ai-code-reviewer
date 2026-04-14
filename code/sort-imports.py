#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 sort-imports.py - 自动排序Python的import语句
 排序规则: 标准库 -> 第三方库 -> 本地/项目模块
"""

import ast
import sys
import argparse
import re
from pathlib import Path
from collections import defaultdict


# 标准库模块列表 (常用)
STDLIB_MODULES = {
    # 内建模块
    'builtins', 'exceptions', 'gc', 'itertools', 'functools', 'operator',
    # 系统
    'os', 'sys', 'io', 'io', 'builtins', 'exec', 'eval', 'compile',
    'ast', 'token', 'tokenize', 'inspect', 'traceback', 'warnings',
    # 文件/目录
    'pathlib', 'os.path', 'shutil', 'tempfile', 'fileinput', 'stat',
    # 数据结构
    'collections', 'abc', 'copy', 'reprlib', 'types', 'weakref', 'enum',
    # 文本处理
    'string', 're', 'textwrap', 'unicodedata', 'difflib',
    # 日期时间
    'datetime', 'time', 'calendar', 'zoneinfo',
    # 压缩/归档
    'zipfile', 'tarfile', 'gzip', 'bz2', 'lzma', 'zipimport',
    # 序列化
    'json', 'pickle', 'marshal', 'csv', 'configparser', 'tomllib',
    # 加密
    'hashlib', 'hmac', 'secrets', 'ssl', 'tls',
    # 数学
    'math', 'cmath', 'decimal', 'fractions', 'random', 'statistics',
    # 网络
    'socket', 'select', ' selectors', 'asyncio', 'ssl', 'mimetypes',
    'urllib', 'http', 'ftplib', 'imaplib', 'smtplib', 'telnetlib',
    # 进程/并发
    'subprocess', 'multiprocessing', 'threading', 'concurrent',
    # 调试
    'pdb', 'timeit', 'profile', 'cProfile', 'pstats', 'trace',
    # 性能
    'functools', 'itertools', 'operator', 'contextlib',
    # 格式
    'pprint', 'format',
}

# 第三方库的常见前缀
THIRD_PARTY_PREFIXES = {
    'django', 'flask', 'fastapi', 'pandas', 'numpy', 'scipy', 'matplotlib',
    'requests', 'httpx', 'aiohttp', 'urllib3', 'chardet', 'idna',
    'sqlalchemy', 'psycopg2', 'pymysql', 'redis', 'pymongo',
    'pytest', 'unittest', 'coverage', 'tox', 'flake8', 'black', 'ruff',
    'mypy', 'pyright', 'pylint', 'bandit', 'safety',
    'jinja2', 'mako', 'chevron', '_yaml',
    'cryptography', 'pyjwt', 'passlib', 'bcrypt',
    'pillow', 'opencv', 'cv2',
    'tensorflow', 'torch', 'keras', 'sklearn',
    'boto3', 'botocore', 'google', 'azure', 'aliyun',
    'openai', 'anthropic', 'cohere',
    'celery', 'rq', 'huey',
    'pydantic', 'dataclasses', 'attrs',
    'tqdm', 'click', 'typer', 'cliff', 'cement',
    'pyppeteer', 'selenium', 'playwright',
    'email', 'html', 'xml', 'html.parser', 'xml.etree',
    'IPython', 'jupyter',
    'pip', 'setuptools', 'wheel', 'packaging', 'distutils',
    'venv', 'virtualenv', 'conda',
}

# 常见绝对导入前缀
THIRD_PARTY_EXTRA = {
    'pkg_resources', 'importlib', 'typing', 'warnings',
}


def classify_import(module_name: str) -> tuple:
    """
    分类导入语句
    返回: (category, module_name)
    category: 'stdlib', 'third_party', 'local', 'future', 'unknown'
    """
    if module_name.startswith('_'):
        return 'local', module_name

    # future 导入放最前
    # if module_name == '__future__':
    #     return 'future', module_name

    # 获取顶层模块名
    top_module = module_name.split('.')[0]

    # 检查标准库
    if top_module in STDLIB_MODULES or module_name in STDLIB_MODULES:
        return 'stdlib', module_name

    # 检查第三方库
    if top_module in THIRD_PARTY_PREFIXES:
        return 'third_party', module_name

    # 检查第三方前缀
    for prefix in THIRD_PARTY_PREFIXES:
        if top_module.startswith(prefix) or module_name.startswith(prefix):
            return 'third_party', module_name

    # 检查 extra
    if top_module in THIRD_PARTY_EXTRA:
        return 'third_party', module_name

    # 本地/项目模块 (通常是相对导入或自定义包)
    return 'local', module_name


def parse_imports(source: str) -> dict:
    """解析源代码中的所有import语句"""
    imports = {
        'future': [],
        'stdlib': [],
        'third_party': [],
        'local': [],
        'unknown': [],
    }

    lines = source.split('\n')
    in_multiline_import = False
    current_import = []
    current_import_line = 0

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # 跳过空行和注释
        if not stripped or stripped.startswith('#'):
            continue

        # 检查多行导入
        if 'import' in stripped or 'from' in stripped:
            if in_multiline_import:
                current_import.append(line)
                if stripped.endswith(')') or not line.endswith('\\'):
                    # 结束多行导入
                    full_import = '\n'.join(current_import)
                    imports = classify_and_add(imports, full_import, current_import_line)
                    in_multiline_import = False
                    current_import = []
            elif line.endswith('\\') or '(' in stripped:
                in_multiline_import = True
                current_import.append(line)
                current_import_line = i
            else:
                # 单行导入
                imports = classify_and_add(imports, line, i)
        elif in_multiline_import:
            current_import.append(line)
            if stripped.endswith(')') or not line.endswith('\\'):
                full_import = '\n'.join(current_import)
                imports = classify_and_add(imports, full_import, current_import_line)
                in_multiline_import = False
                current_import = []

    return imports


def classify_and_add(imports: dict, line: str, line_no: int) -> dict:
    """分类并添加导入语句"""
    stripped = line.strip()

    # from xxx import yyy
    from_match = re.match(r'from\s+(\.+)?([\w\.]+)', stripped)
    if from_match:
        dots = from_match.group(1) or ''
        module = from_match.group(2)
        if dots:
            module = dots + module

        category, _ = classify_import(module)
        imports[category].append((line_no, stripped))

    # import xxx
    import_match = re.match(r'import\s+([\w\.\s,]+)', stripped)
    if import_match:
        modules = import_match.group(1).split(',')
        for module in modules:
            module = module.strip()
            if module:
                category, _ = classify_import(module)
                imports[category].append((line_no, stripped))
                break  # 只添加一次

    return imports


def sort_imports(source: str) -> str:
    """对import语句排序"""
    lines = source.split('\n')

    # 收集所有import行及其行号
    imports = parse_imports(source)

    # 确定import开始的行
    first_import_line = float('inf')
    for category in imports.values():
        for line_no, _ in category:
            first_import_line = min(first_import_line, line_no)

    if first_import_line == float('inf'):
        return source  # 没有import

    # 删除原有的import行
    import_lines = set()
    for category in imports.values():
        for line_no, _ in category:
            import_lines.add(line_no)

    new_lines = []
    for i, line in enumerate(lines, 1):
        if i not in import_lines:
            new_lines.append(line)

    # 构建排序后的import块
    sorted_imports = []

    # future 导入 (如果有)
    if imports['future']:
        for _, stmt in imports['future']:
            sorted_imports.append(stmt)
        sorted_imports.append('')

    # 标准库
    if imports['stdlib']:
        for _, stmt in sorted(imports['stdlib'], key=lambda x: x[1]):
            sorted_imports.append(stmt)
        sorted_imports.append('')

    # 第三方库
    if imports['third_party']:
        for _, stmt in sorted(imports['third_party'], key=lambda x: x[1]):
            sorted_imports.append(stmt)
        sorted_imports.append('')

    # 本地/项目模块
    if imports['local']:
        for _, stmt in sorted(imports['local'], key=lambda x: x[1]):
            sorted_imports.append(stmt)

    # 未知
    if imports['unknown']:
        for _, stmt in sorted(imports['unknown'], key=lambda x: x[1]):
            sorted_imports.append(stmt)

    # 插入排序后的import
    result_lines = []
    import_idx = 0
    line_idx = 0

    for i, line in enumerate(lines):
        if i + 1 not in import_lines:
            result_lines.append(line)
            if i + 1 > first_import_line and import_idx < len(sorted_imports):
                # 插入import
                result_lines.append('')
                result_lines.extend(sorted_imports)
                import_idx = len(sorted_imports)

    # 如果import在文件开头
    if first_import_line == 1:
        result_lines = sorted_imports + [''] + [l for l in lines if l.strip() and lines.index(l) + 1 not in import_lines]

    return '\n'.join(result_lines)


def main():
    parser = argparse.ArgumentParser(
        description='自动排序Python的import语句',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
排序规则:
  1. from __future__ import ... (future)
  2. 标准库 import ... (stdlib)
  3. 第三方库 import ... (third_party)
  4. 本地/项目模块 import ... (local)
        """
    )
    parser.add_argument('file', help='要排序的Python文件')
    parser.add_argument('-w', '--write', action='store_true', help='直接写入文件 (默认是预览模式)')
    parser.add_argument('-i', '--in-place', action='store_true', dest='in_place',
                        help='直接修改文件 (等同于 --write)')
    parser.add_argument('--stdout', action='store_true', help='输出到stdout')

    args = parser.parse_args()

    filepath = Path(args.file)
    if not filepath.exists():
        print(f"错误: 文件不存在: {filepath}", file=sys.stderr)
        sys.exit(1)

    with open(filepath, 'r', encoding='utf-8') as f:
        original = f.read()

    sorted_code = sort_imports(original)

    if args.stdout or not (args.write or args.in_place):
        print(sorted_code)
        if not args.stdout:
            print("\n💡 使用 --write 或 -i 写入文件")
    else:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(sorted_code)
        print(f"✅ 文件已更新: {filepath}")


if __name__ == '__main__':
    main()
