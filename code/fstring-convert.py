#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 fstring-convert.py - 将Python的 % 格式化字符串转换为 f-string
 支持 %s, %d, %f, %x 等常见格式说明符
"""

import re
import sys
import argparse
from pathlib import Path


def parse_format_string(format_str: str) -> list:
    """
    解析 % 格式化字符串，返回变量名列表和格式说明符
    例如: "Hello %s, you have %d messages" -> [('s', 'name'), ('d', 'count')]
    """
    # 正则匹配 % 格式说明符
    pattern = r'%(?:\([a-zA-Z_][a-zA-Z0-9_]*\))?[diouxXeEfFgGcrsab%]|%\([a-zA-Z_][a-zA-Z0-9_]*\)s'

    matches = list(re.finditer(pattern, format_str))
    parsed = []

    for i, match in enumerate(matches):
        spec = match.group()
        start, end = match.span()

        # 找出这个说明符对应的变量名
        if spec == '%%':
            parsed.append(('%%', '%%', start, end))
            continue

        # 检查是否有命名参数
        named_match = re.match(r'%\(([a-zA-Z_][a-zA-Z0-9_]*)\)', spec)
        if named_match:
            var_name = named_match.group(1)
            fmt_spec = spec[matched.end():] if (matched := re.match(r'%\([a-zA-Z_][a-zA-Z0-9_]*\)([diouxXeEfFgGcrsab%])', spec)) else 's'
            parsed.append((var_name, fmt_spec, start, end))
        else:
            # 位置参数，用索引
            parsed.append((i, spec[-1] if spec else 's', start, end))

    return parsed


def convert_format_to_fstring(line: str, indent: str = '') -> str:
    """将一行代码中的 % 格式化转换为 f-string"""

    # 匹配字符串格式化表达式
    # 例如: "Hello %s" % name  或 "Value: %d" % (x, y)
    pattern = r"(?P<quote>['\"])(?P<format_string>.*?)(?P=quote)\s*%\s*(?P<args>\(.*?\)|[a-zA-Z_][a-zA-Z0-9_]*)"

    def replace_format(m):
        format_str = m.group('format_string')
        args_str = m.group('args')

        # 解析格式字符串
        spec_pattern = r'%(?:\([a-zA-Z_][a-zA-Z0-9_]*\)|[diouxXeEfFgGcrsab%])|%\([a-zA-Z_][a-zA-Z0-9_]*\)s'
        specs = list(re.finditer(spec_pattern, format_str))

        if not specs:
            return m.group(0)

        # 提取变量名或索引
        replacements = []
        for spec in specs:
            spec_text = spec.group()
            if spec_text == '%%':
                replacements.append("'%%'")
                continue

            # 尝试提取命名参数名
            named = re.match(r'%\(([a-zA-Z_][a-zA-Z0-9_]*)\)', spec_text)
            if named:
                var_name = named.group(1)
                replacements.append(f"{{{var_name}}}")
            else:
                # 位置参数 - 需要解析args
                fmt_spec = spec_text[-1] if spec_text else 's'
                replacements.append(f"{{{args_str.strip()[1:-1]}}}")  # 简化处理

        # 重建f-string
        # 这个简化版本只处理基本替换
        result = format_str

        # 替换 %s -> {}, %d -> {}, 等等
        result = re.sub(r'%s', '{}', result)
        result = re.sub(r'%d', '{:d}', result)
        result = re.sub(r'%f', '{:f}', result)
        result = re.sub(r'%r', '{!r}', result)

        # 处理命名参数
        result = re.sub(r'%\(([a-zA-Z_][a-zA-Z0-9_]*)\)s', r'{\1}', result)
        result = re.sub(r'%\(([a-zA-Z_][a-zA-Z0-9_]*)\)d', r'{\1:d}', result)

        # 去掉转义的 %
        result = result.replace('%%', '%')

        return f"f'{result}'"

    # 处理带括号的参数
    if '%' in line:
        # 简单替换策略
        original = line

        # 替换 %(name)s 格式
        line = re.sub(r"f?['\"]%\\(([a-zA-Z_][a-zA-Z0-9_]*)\\)s['\"]", r"f'{\1}'", line)
        line = re.sub(r"f?['\"]%\\(([a-zA-Z_][a-zA-Z0-9_]*)\\)d['\"]", r"f'{\1:d}'", line)

        # 替换 %s %d 等
        line = re.sub(r"f?['\"]([^'\"]*)%s([^'\"]*)['\"]", r"f'\1{}\2'", line)
        line = re.sub(r"f?['\"]([^'\"]*)%d([^'\"]*)['\"]", r"f'\1{:d}\2'", line)
        line = re.sub(r"f?['\"]([^'\"]*)%f([^'\"]*)['\"]", r"f'\1{:f}\2'", line)
        line = re.sub(r"f?['\"]([^'\"]*)%r([^'\"]*)['\"]", r"f'\1{!r}\2'", line)

        # 替换 %%
        line = line.replace('%%', '%')

        return line

    return line


def simple_convert(line: str) -> str:
    """简化转换 - 处理常见模式"""

    # 模式1: "text %s" % var -> f"text {var}"
    # 模式2: "text %s" % (var,) -> f"text {var}"
    # 模式3: "text %(name)s" % dict -> f"text {dict[name]}"

    # 检查是否包含 % 格式化
    if ' % ' not in line and ' %' not in line:
        return line, False

    # 尝试匹配并转换
    # 匹配: "..." % (...)
    match = re.search(r"(?P<before>f?['\"])(?P<str_part>.*?)(?P=before)\s*%\s*(?P<args>\(.*?\)|[a-zA-Z_][a-zA-Z0-9_]*)", line)
    if not match:
        return line, False

    str_part = match.group('str_part')
    args_str = match.group('args')
    quote = match.group('before')

    # 解析参数
    if args_str.startswith('('):
        # 元组参数
        args = [a.strip() for a in args_str.strip('()').split(',')]
    else:
        # 单个变量
        args = [args_str.strip()]

    # 替换格式说明符为{}
    result = str_part
    arg_idx = 0

    # 按顺序替换
    while '%s' in result and arg_idx < len(args):
        result = result.replace('%s', '{' + args[arg_idx] + '}', 1)
        arg_idx += 1

    # 处理 %d, %f 等
    for spec in ['%d', '%f', '%r', '%x']:
        if spec in result:
            result = result.replace(spec, '{' + args[arg_idx] + '}', 1)
            arg_idx += 1

    # 处理 %%
    result = result.replace('%%', '%')

    # 重建行
    before = line[:match.start()]
    after = line[match.end():]
    converted = before + f"f{quote}" + result + quote + after

    return converted, True


def convert_file(filepath: Path, dry_run: bool = True) -> list:
    """转换文件，返回修改列表"""
    changes = []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        return changes

    for i, line in enumerate(lines, 1):
        original = line.rstrip('\n\r')
        converted, changed = simple_convert(original)

        if changed:
            changes.append({
                'line': i,
                'before': original,
                'after': converted
            })

            if not dry_run:
                lines[i - 1] = converted + '\n'

    if not dry_run and changes:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(lines)

    return changes


def main():
    parser = argparse.ArgumentParser(
        description='将Python的 %% 格式化字符串转换为 f-string',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('file', help='要转换的Python文件')
    parser.add_argument('-w', '--write', action='store_true', help='直接写入文件 (默认是预览模式)')
    parser.add_argument('-o', '--output', help='输出到指定文件')

    args = parser.parse_args()

    filepath = Path(args.file)
    if not filepath.exists():
        print(f"错误: 文件不存在: {filepath}", file=sys.stderr)
        sys.exit(1)

    changes = convert_file(filepath, dry_run=not (args.write or args.output))

    if not changes:
        print("✅ 未发现需要转换的 % 格式化字符串")
        return

    print(f"📊 发现 {len(changes)} 处需要转换:\n")

    for change in changes:
        print(f"行 {change['line']}:")
        print(f"  - {change['before']}")
        print(f"  + {change['after']}")
        print()

    if args.write:
        print("✅ 文件已更新 (使用 --write 确认)")
    elif args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            for change in changes:
                f.write(f"# Line {change['line']}\n")
                f.write(f"# - {change['before']}\n")
                f.write(f"+ {change['after']}\n\n")
        print(f"差异已保存到: {args.output}")
    else:
        print("💡 使用 --write 直接写入文件")


if __name__ == '__main__':
    main()
