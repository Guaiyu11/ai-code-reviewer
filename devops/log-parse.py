#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 log-parse.py - 解析日志文件，提取ERROR/WARN/INFO统计
 支持多级日志分析，生成可视化报告
"""

import re
import sys
import argparse
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime


# 日志级别模式
LOG_LEVELS = {
    'ERROR': r'\b(ERROR|SEVERE|FATAL|CRITICAL|CRIT)\b',
    'WARN': r'\b(WARN|WARNING)\b',
    'INFO': r'\b(INFO)\b',
    'DEBUG': r'\b(DEBUG|TRACE|VERBOSE)\b',
}

# 时间戳模式
TIMESTAMP_PATTERNS = [
    r'\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}',  # ISO格式
    r'\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}',       # 常见格式
    r'\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]',   # [2024-01-01 12:00:00]
    r'\w{3} \d{2} \d{2}:\d{2}:\d{2}',             # Syslog格式
]


def detect_timestamp(line: str) -> str:
    """检测行中的时间戳"""
    for pattern in TIMESTAMP_PATTERNS:
        match = re.search(pattern, line)
        if match:
            return match.group(0)
    return ''


def parse_log_file(filepath: Path) -> dict:
    """解析日志文件"""
    stats = {
        'total': 0,
        'levels': defaultdict(int),
        'messages': defaultdict(list),
        'timestamps': [],
        'errors': [],
        'warnings': []
    }

    current_time = None

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line_no, line in enumerate(f, 1):
                line = line.rstrip('\n\r')
                stats['total'] += 1

                # 检测时间戳
                ts = detect_timestamp(line)
                if ts:
                    current_time = ts
                    stats['timestamps'].append((ts, line_no))

                # 检测日志级别
                for level, pattern in LOG_LEVELS.items():
                    if re.search(pattern, line, re.IGNORECASE):
                        stats['levels'][level] += 1
                        # 记录错误和警告的详情
                        if level == 'ERROR':
                            stats['errors'].append((line_no, current_time, line[:200]))
                        elif level == 'WARN':
                            stats['warnings'].append((line_no, current_time, line[:200]))
                        break

    except Exception as e:
        print(f"错误: 无法读取文件 {filepath}: {e}", file=sys.stderr)

    return stats


def aggregate_by_time(stats: dict, interval: str = 'hour') -> dict:
    """按时间聚合统计"""
    if not stats['timestamps']:
        return {}

    # 解析时间戳并分组
    time_groups = defaultdict(int)

    for ts_str, _ in stats['timestamps']:
        try:
            # 简化处理：提取小时或日期
            if interval == 'hour':
                key = ts_str[:13] if len(ts_str) >= 13 else ts_str[:10]
            else:  # day
                key = ts_str[:10]
            time_groups[key] += 1
        except (ValueError, IndexError):
            continue

    return dict(sorted(time_groups.items()))


def print_report(stats: dict, top_n: int = 10):
    """打印分析报告"""
    print("\n" + "=" * 70)
    print("📊 日志分析报告")
    print("=" * 70)

    print(f"\n📈 总体统计:")
    print(f"  总行数: {stats['total']:,}")

    print(f"\n📋 日志级别分布:")
    total_level = sum(stats['levels'].values()) or 1
    for level in ['ERROR', 'WARN', 'INFO', 'DEBUG']:
        count = stats['levels'].get(level, 0)
        pct = 100 * count / total_level
        bar = '█' * int(pct / 5) + '░' * (20 - int(pct / 5))
        print(f"  {level:<6} [{bar}] {count:>6} ({pct:5.1f}%)")

    # 错误详情
    if stats['errors']:
        print(f"\n🔴 错误详情 (前 {min(top_n, len(stats['errors']))} 条):")
        print("-" * 70)
        for i, (line_no, ts, msg) in enumerate(stats['errors'][:top_n], 1):
            print(f"  {i}. Line {line_no}" + (f" [{ts}]" if ts else ""))
            print(f"     {msg}")
            print()

    # 警告详情
    if stats['warnings']:
        print(f"\n🟡 警告详情 (前 {min(top_n, len(stats['warnings']))} 条):")
        print("-" * 70)
        for i, (line_no, ts, msg) in enumerate(stats['warnings'][:top_n], 1):
            print(f"  {i}. Line {line_no}" + (f" [{ts}]" if ts else ""))
            print(f"     {msg}")
            print()

    # 时间分布
    time_dist = aggregate_by_time(stats, 'hour')
    if time_dist:
        print(f"\n⏰ 时间分布 (每小时):")
        print("-" * 50)
        max_count = max(time_dist.values()) or 1
        for time_key, count in list(time_dist.items())[:12]:  # 只显示最近12个
            bar_len = int(40 * count / max_count)
            bar = '█' * bar_len + '░' * (40 - bar_len)
            print(f"  {time_key:<18} [{bar}] {count}")

    # 错误模式检测
    if stats['errors']:
        print(f"\n🔍 错误模式分析:")
        error_messages = [msg for _, _, msg in stats['errors']]
        # 提取错误类型 (去除行号等数字)
        error_types = []
        for msg in error_messages:
            # 简化：提取第一个冒号后的内容作为错误类型
            parts = msg.split(':', 2)
            if len(parts) > 1:
                error_types.append(parts[1].strip()[:60])
            else:
                error_types.append(msg[:60])

        type_counter = Counter(error_types)
        for error_type, count in type_counter.most_common(5):
            print(f"  - [{count}x] {error_type}")


def main():
    parser = argparse.ArgumentParser(
        description='解析日志文件，提取ERROR/WARN/INFO统计',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('file', help='日志文件路径')
    parser.add_argument('-n', '--top', type=int, default=10, help='显示条数 (默认: 10)')
    parser.add_argument('-o', '--output', help='输出到文件')
    parser.add_argument('--json', action='store_true', help='JSON格式输出')

    args = parser.parse_args()

    filepath = Path(args.file)
    if not filepath.exists():
        print(f"错误: 文件不存在: {filepath}", file=sys.stderr)
        sys.exit(1)

    print(f"正在解析: {filepath}")
    stats = parse_log_file(filepath)

    if args.json:
        import json
        output = {
            'total': stats['total'],
            'levels': dict(stats['levels']),
            'error_count': len(stats['errors']),
            'warning_count': len(stats['warnings'])
        }
        print(json.dumps(output, indent=2))
    else:
        print_report(stats, top_n=args.top)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(f"日志分析报告 - {filepath}\n")
            f.write(f"总行数: {stats['total']}\n")
            f.write(f"ERROR: {stats['levels'].get('ERROR', 0)}\n")
            f.write(f"WARN: {stats['levels'].get('WARN', 0)}\n")
            f.write(f"INFO: {stats['levels'].get('INFO', 0)}\n")
        print(f"\n报告已保存到: {args.output}")


if __name__ == '__main__':
    main()
