#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 health-check.py - 对多个URL/主机做健康检查，支持阈值配置
 支持HTTP/TCP/Ping检查，返回健康状态报告
"""

import sys
import socket
import time
import argparse
import urllib.request
import urllib.error
import json
from pathlib import Path
from dataclasses import dataclass
from typing import Optional


@dataclass
class HealthCheckResult:
    """健康检查结果"""
    url: str
    status: str  # healthy, unhealthy, timeout, error
    response_time: float = 0
    status_code: int = 0
    error: str = ''
    timestamp: str = ''


def check_http(url: str, timeout: int = 10) -> HealthCheckResult:
    """HTTP/HTTPS健康检查"""
    result = HealthCheckResult(url=url, status='unknown')

    try:
        start = time.time()
        req = urllib.request.Request(url, headers={'User-Agent': 'HealthCheck/1.0'})
        response = urllib.request.urlopen(req, timeout=timeout)
        result.response_time = (time.time() - start) * 1000  # ms
        result.status_code = response.getcode()
        result.status = 'healthy' if result.status_code < 400 else 'unhealthy'
        result.timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    except urllib.error.HTTPError as e:
        result.status_code = e.code
        result.status = 'unhealthy'
        result.error = f'HTTP {e.code}'
        result.timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    except urllib.error.URLError as e:
        result.status = 'error'
        result.error = str(e.reason)
        result.timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    except socket.timeout:
        result.status = 'timeout'
        result.error = 'Connection timeout'
        result.timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        result.status = 'error'
        result.error = str(e)
        result.timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    return result


def check_tcp(host: str, port: int, timeout: int = 5) -> HealthCheckResult:
    """TCP端口健康检查"""
    result = HealthCheckResult(url=f'{host}:{port}', status='unknown')

    try:
        start = time.time()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, port))
        sock.close()
        result.response_time = (time.time() - start) * 1000
        result.status = 'healthy'
        result.timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    except socket.timeout:
        result.status = 'timeout'
        result.error = 'Connection timeout'
        result.timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    except ConnectionRefusedError:
        result.status = 'unhealthy'
        result.error = 'Connection refused'
        result.timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        result.status = 'error'
        result.error = str(e)
        result.timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    return result


def check_ping(host: str, count: int = 4, timeout: int = 5) -> HealthCheckResult:
    """Ping健康检查 (跨平台)"""
    import subprocess
    result = HealthCheckResult(url=f'ping://{host}', status='unknown')

    try:
        # Windows ping
        cmd = ['ping', '-n', str(count), '-w', str(timeout * 1000), host]
        output = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout * count + 5)

        if output.returncode == 0:
            result.status = 'healthy'
            # 提取平均响应时间
            for line in output.stdout.split('\n'):
                if 'Average' in line or '平均' in line:
                    import re
                    match = re.search(r'(\d+)\s*ms', line)
                    if match:
                        result.response_time = float(match.group(1))
        else:
            result.status = 'unhealthy'
            result.error = 'Host unreachable'
    except subprocess.TimeoutExpired:
        result.status = 'timeout'
        result.error = 'Ping timeout'
    except Exception as e:
        result.status = 'error'
        result.error = str(e)

    result.timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    return result


def parse_url(url: str) -> tuple:
    """解析URL，返回(host, port, scheme)"""
    if '://' not in url:
        # 默认HTTP
        url = 'http://' + url

    parsed = urllib.parse.urlparse(url)
    host = parsed.hostname or ''
    port = parsed.port or (443 if parsed.scheme == 'https' else 80)
    return host, port, parsed.scheme


def load_targets_from_file(filepath: Path) -> list:
    """从文件加载检查目标"""
    targets = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    targets.append(line)
    except Exception as e:
        print(f"错误: 无法读取文件 {filepath}: {e}", file=sys.stderr)
    return targets


def main():
    parser = argparse.ArgumentParser(
        description='对多个URL/主机做健康检查',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('targets', nargs='*', help='检查目标 (URL或host:port)')
    parser.add_argument('-f', '--file', help='从文件加载目标列表')
    parser.add_argument('-t', '--timeout', type=int, default=10, help='超时时间(秒)')
    parser.add_argument('-w', '--warning-threshold', type=int, default=1000,
                       help='响应时间警告阈值(ms)')
    parser.add_argument('-c', '--critical-threshold', type=int, default=3000,
                       help='响应时间critical阈值(ms)')
    parser.add_argument('-o', '--output', help='输出到文件(JSON格式)')
    parser.add_argument('--json', action='store_true', help='JSON格式输出到stdout')
    parser.add_argument('--repeat', type=int, default=1, help='重复检查次数')

    args = parser.parse_args()

    # 收集目标
    targets = []
    if args.file:
        targets.extend(load_targets_from_file(Path(args.file)))
    targets.extend(args.targets)

    if not targets:
        print("错误: 未指定检查目标", file=sys.stderr)
        print("用法: health-check.py <url> [url...]")
        print("      health-check.py -f targets.txt")
        sys.exit(1)

    print(f"🔍 开始健康检查 ({len(targets)} 个目标)")
    print(f"⏱️  超时: {args.timeout}s | 警告阈值: {args.warning_threshold}ms | Critical: {args.critical_threshold}ms\n")

    all_results = []

    for target in targets:
        target = target.strip()
        if not target:
            continue

        # 判断检查类型
        if target.startswith('tcp://'):
            _, host, port = target[6:].partition(':')
            result = check_tcp(host, int(port), args.timeout)
        elif target.startswith('ping://'):
            host = target[7:]
            result = check_ping(host, count=4, timeout=args.timeout)
        elif ':' in target and not target.startswith('http'):
            # host:port 格式
            host, port = target.rsplit(':', 1)
            result = check_tcp(host, int(port), args.timeout)
        else:
            # HTTP URL
            result = check_http(target, args.timeout)

        # 判断状态
        if result.status == 'healthy':
            if result.response_time > args.critical_threshold:
                result.status = 'critical'
            elif result.response_time > args.warning_threshold:
                result.status = 'warning'

        all_results.append(result)

        # 打印结果
        icon = {'healthy': '✅', 'warning': '⚠️', 'unhealthy': '❌',
               'timeout': '⏱️', 'error': '❎', 'critical': '🔴'}.get(result.status, '❓')
        print(f"{icon} {result.url}")
        print(f"   状态: {result.status.upper()} | "
              f"响应: {result.response_time:.0f}ms | "
              f"{result.timestamp}")

        if result.error:
            print(f"   错误: {result.error}")

    # 汇总统计
    healthy = sum(1 for r in all_results if r.status == 'healthy')
    warning = sum(1 for r in all_results if r.status == 'warning')
    unhealthy = sum(1 for r in all_results if r.status in ('unhealthy', 'error', 'timeout', 'critical'))

    print("\n" + "=" * 60)
    print("📊 汇总:")
    print(f"  ✅ 健康: {healthy}/{len(all_results)}")
    print(f"  ⚠️  警告: {warning}/{len(all_results)}")
    print(f"  ❌ 不健康: {unhealthy}/{len(all_results)}")

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump([{
                'url': r.url,
                'status': r.status,
                'response_time_ms': r.response_time,
                'status_code': r.status_code,
                'error': r.error,
                'timestamp': r.timestamp
            } for r in all_results], f, indent=2)
        print(f"\n结果已保存到: {args.output}")

    if args.json:
        print(json.dumps([{
            'url': r.url,
            'status': r.status,
            'response_time_ms': r.response_time,
            'status_code': r.status_code,
            'error': r.error,
            'timestamp': r.timestamp
        } for r in all_results], indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
