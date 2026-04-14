#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 secrets-scanner.py - 扫描代码中的硬编码密钥、API Key、密码
 使用正则匹配常见敏感信息模式
"""

import re
import os
import sys
import argparse
from pathlib import Path

# 常见敏感信息正则模式
SECRET_PATTERNS = {
    "API Key (Generic)": r"(?i)(api[_-]?key|apikey)\s*[=:]\s*['\"]?([a-zA-Z0-9_\-]{16,})['\"]?",
    "AWS Access Key": r"(?i)(aws[_-]?(access[_-]?key[_-]?id|secret[_-]?access[_-]?key))\s*[=:]\s*['\"]?([A-Z0-9]{20,})['\"]?",
    "AWS Secret Key": r"(?i)aws[_-]?secret[_-]?access[_-]?key\s*[=:]\s*['\"]?([A-Za-z0-9/+=]{40})['\"]?",
    "GitHub Token": r"(?i)(github|ghp|gho|ghu|ghs|ghr)_[a-zA-Z0-9]{36,}",
    "Private Key": r"-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----",
    "Generic Secret": r"(?i)(secret|password|passwd|pwd|token|auth)[_\-]?(key|token|secret|password)?\s*[=:]\s*['\"]?([a-zA-Z0-9_\-!@#$%^&*()+=]{8,})['\"]?",
    "Database URL": r"(?i)(mysql|postgres|postgresql|mongodb|redis):\/\/[^\s'\"]{10,}",
    "Slack Token": r"xox[baprs]-[0-9]{10,13}-[0-9]{10,13}-[a-zA-Z0-9]{24,}",
    "Stripe Key": r"(?i)sk_live_[0-9a-zA-Z]{24,}",
    "SendGrid Key": r"(?i)SG\.[a-zA-Z0-9_\-]{22}\.[a-zA-Z0-9_\-]{43}",
    "JWT Token": r"eyJ[a-zA-Z0-9]{10,}\.eyJ[a-zA-Z0-9]{10,}\.[a-zA-Z0-9_\-]{10,}",
    "Hardcoded IP + Port": r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}:[0-9]{2,5}",
    "Bearer Token": r"(?i)bearer\s+[a-zA-Z0-9_\-\.=]{20,}",
    "Basic Auth URL": r"https?:\/\/[^\s:'\"@]+:[^\s:'\"@]+@[^\s'\"<>{]+",
}

# 排除目录
EXCLUDE_DIRS = {'.git', '__pycache__', '.pytest_cache', 'node_modules', 'venv', '.venv', 'env', '.env', '.tox'}

# 排除文件扩展名
EXCLUDE_EXTENSIONS = {'.exe', '.bin', '.zip', '.tar', '.gz', '.jpg', '.png', '.gif', '.pdf', '.pyc', '.pyo'}


def scan_file(filepath: Path, patterns: dict) -> list:
    """扫描单个文件中的敏感信息"""
    findings = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    except Exception:
        return findings

    for line_no, line in enumerate(lines, 1):
        # 跳过注释行
        stripped = line.strip()
        if stripped.startswith('#') or stripped.startswith('//'):
            continue

        for name, pattern in patterns.items():
            matches = re.finditer(pattern, line)
            for match in matches:
                # 脱敏显示
                matched_text = match.group(0)
                if len(matched_text) > 40:
                    display = matched_text[:20] + "..." + matched_text[-8:]
                else:
                    display = matched_text[:4] + "****"
                findings.append({
                    'file': str(filepath),
                    'line': line_no,
                    'type': name,
                    'match': display,
                    'full_match': matched_text
                })
    return findings


def scan_directory(root_dir: Path, extensions: list = None, exclude_dirs: set = None) -> list:
    """递归扫描目录"""
    findings = []
    exclude_dirs = exclude_dirs or EXCLUDE_DIRS
    patterns = SECRET_PATTERNS

    for filepath in root_dir.rglob('*'):
        if filepath.is_dir():
            if filepath.name in exclude_dirs or any(
                part in exclude_dirs for part in filepath.parts
            ):
                continue
            continue

        # 按扩展名过滤
        if extensions and filepath.suffix not in extensions:
            continue

        # 排除特定扩展名
        if filepath.suffix.lower() in EXCLUDE_EXTENSIONS:
            continue

        findings.extend(scan_file(filepath, patterns))

    return findings


def main():
    parser = argparse.ArgumentParser(
        description='扫描代码中的硬编码密钥、API Key、密码等敏感信息',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('path', nargs='?', default='.', help='扫描路径 (默认: 当前目录)')
    parser.add_argument('-e', '--extensions', nargs='+', default=['.py', '.js', '.ts', '.java', '.go', '.rb', '.php', '.yaml', '.yml', '.json', '.env', '.txt', '.sh'],
                        help='要扫描的文件扩展名')
    parser.add_argument('-o', '--output', help='输出结果到文件')
    parser.add_argument('-q', '--quiet', action='store_true', help='只输出发现的问题数量')
    parser.add_argument('-f', '--full-match', action='store_true', help='显示完整匹配内容(不含脱敏)')

    args = parser.parse_args()

    root = Path(args.path).resolve()
    if not root.exists():
        print(f"错误: 路径不存在: {root}", file=sys.stderr)
        sys.exit(1)

    print(f"正在扫描: {root}")
    print(f"扩展名过滤: {', '.join(args.extensions)}")
    print("-" * 60)

    findings = scan_directory(root, extensions=args.extensions)

    if not findings:
        print("未发现敏感信息泄露!")
        return

    # 按文件分组显示
    current_file = None
    for finding in sorted(findings, key=lambda x: (x['file'], x['line'])):
        if finding['file'] != current_file:
            print(f"\n📄 {finding['file']}")
            current_file = finding['file']

        match_display = finding['full_match'] if args.full_match else finding['match']
        print(f"  Line {finding['line']:4d} | {finding['type']:<25} | {match_display}")

    print("-" * 60)
    print(f"总计发现: {len(findings)} 处敏感信息泄露")

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            for finding in findings:
                f.write(f"{finding['file']}:{finding['line']} | {finding['type']} | {finding['full_match']}\n")
        print(f"结果已保存到: {args.output}")


if __name__ == '__main__':
    main()
