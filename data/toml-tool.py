#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 toml-tool.py - TOML格式的读写、验证、转换工具
 支持TOML与JSON/YAML互转
"""

import sys
import argparse
import json
from pathlib import Path


try:
    import tomllib  # Python 3.11+
except ImportError:
    try:
        import tomli as tomllib  # 尝试tomli
    except ImportError:
        tomllib = None


def parse_toml(content: str) -> dict:
    """解析TOML内容"""
    if tomllib is None:
        # 尝试使用内置的tomllib (Python 3.11+) 或 tomli
        import re
        # 简单的手动解析器处理基本类型
        return simple_toml_parse(content)

    import io
    return tomllib.loads(content)


def simple_toml_parse(content: str) -> dict:
    """简单的TOML解析器 (基础功能)"""
    import re

    result = {}
    current_section = result
    sections = [result]

    for line in content.split('\n'):
        line = line.strip()

        # 跳过空行和注释
        if not line or line.startswith('#'):
            continue

        # 节标题
        section_match = re.match(r'\[([^\]]+)\]', line)
        if section_match:
            section_name = section_match.group(1)
            if '.' in section_name:
                parts = section_name.split('.')
                current = result
                for part in parts[:-1]:
                    if part not in current:
                        current[part] = {}
                    current = current[part]
                current_section = current
                sections.append(current)
            else:
                if section_name not in result:
                    result[section_name] = {}
                current_section = result[section_name]
            continue

        # 键值对
        kv_match = re.match(r'([a-zA-Z0-9_\-]+)\s*=\s*(.+)', line)
        if kv_match:
            key = kv_match.group(1)
            value = kv_match.group(2).strip()

            # 去除引号
            if (value.startswith('"') and value.endswith('"')) or \
               (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]
            # 布尔值
            elif value.lower() == 'true':
                value = True
            elif value.lower() == 'false':
                value = False
            # 数字
            else:
                try:
                    if '.' in value:
                        value = float(value)
                    else:
                        value = int(value)
                except ValueError:
                    pass

            current_section[key] = value

    return result


def dump_toml(data: dict, indent: int = 0) -> str:
    """将dict转换为TOML字符串"""
    lines = []
    indent_str = '  ' * indent

    for key, value in data.items():
        if isinstance(value, dict):
            # 新的节
            if indent == 0:
                lines.append(f'[{key}]')
            else:
                lines.append(f'[{key}]')
            sub_lines = dump_toml(value, indent + 1)
            if sub_lines:
                lines.append(sub_lines)
        else:
            # 键值对
            if isinstance(value, str):
                if '\n' in value:
                    value = f'"""{value}"""'
                else:
                    value = f'"{value}"'
            elif isinstance(value, bool):
                value = 'true' if value else 'false'
            lines.append(f'{key} = {value}')

    return '\n'.join(lines)


def validate_toml(content: str) -> tuple:
    """验证TOML格式"""
    try:
        parse_toml(content)
        return True, "TOML格式有效"
    except Exception as e:
        return False, str(e)


def toml_to_json(toml_content: str, pretty: bool = True) -> str:
    """TOML转JSON"""
    data = parse_toml(toml_content)
    return json.dumps(data, indent=2 if pretty else None, ensure_ascii=False)


def toml_to_yaml(toml_content: str) -> str:
    """TOML转YAML (简化实现)"""
    data = parse_toml(toml_content)

    def format_yaml(obj, level: int = 0) -> str:
        lines = []
        indent = '  ' * level

        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, dict):
                    lines.append(f'{indent}{key}:')
                    lines.append(format_yaml(value, level + 1))
                elif isinstance(value, list):
                    lines.append(f'{indent}{key}:')
                    for item in value:
                        if isinstance(item, dict):
                            lines.append(f'{indent}  - {format_yaml(item, level + 2).strip()}')
                        else:
                            lines.append(f'{indent}  - {item}')
                else:
                    value_str = f'"{value}"' if isinstance(value, str) else str(value)
                    lines.append(f'{indent}{key}: {value_str}')
        elif isinstance(obj, list):
            for item in obj:
                if isinstance(item, dict):
                    lines.append(f'{indent}- {format_yaml(item, level + 1).strip()}')
                else:
                    lines.append(f'{indent}- {item}')

        return '\n'.join(lines)

    return format_yaml(data)


def main():
    parser = argparse.ArgumentParser(
        description='TOML格式的读写、验证、转换工具',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('file', nargs='?', help='TOML文件')
    parser.add_argument('--validate', action='store_true', help='验证TOML格式')
    parser.add_argument('--to-json', action='store_true', help='转换为JSON')
    parser.add_argument('--to-yaml', action='store_true', help='转换为YAML')
    parser.add_argument('--pretty', action='store_true', default=True, help='格式化输出')
    parser.add_argument('-k', '--key', help='获取指定键的值 (支持点号路径)')
    parser.add_argument('-o', '--output', help='输出到文件')
    parser.add_argument('--stdin', action='store_true', help='从stdin读取')

    args = parser.parse_args()

    # 读取输入
    content = ''
    if args.stdin:
        content = sys.stdin.read()
    elif args.file:
        filepath = Path(args.file)
        if not filepath.exists():
            print(f"错误: 文件不存在: {filepath}", file=sys.stderr)
            sys.exit(1)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        print("错误: 请指定文件或使用 --stdin", file=sys.stderr)
        sys.exit(1)

    # 验证
    if args.validate:
        valid, msg = validate_toml(content)
        if valid:
            print(f"✅ {msg}")
        else:
            print(f"❌ {msg}")
            sys.exit(1)
        return

    # 转换
    if args.to_json:
        output = toml_to_json(content, pretty=args.pretty)
    elif args.to_yaml:
        output = toml_to_yaml(content)
    elif args.key:
        data = parse_toml(content)
        # 解析键路径
        keys = args.key.split('.')
        value = data
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                value = None
                break

        if value is not None:
            if isinstance(value, (dict, list)):
                output = json.dumps(value, indent=2, ensure_ascii=False)
            else:
                output = str(value)
        else:
            print(f"❌ 键不存在: {args.key}", file=sys.stderr)
            sys.exit(1)
    else:
        # 默认：打印解析后的数据
        data = parse_toml(content)
        output = json.dumps(data, indent=2, ensure_ascii=False)

    # 输出
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"已保存到: {args.output}")
    else:
        print(output)


if __name__ == '__main__':
    main()
