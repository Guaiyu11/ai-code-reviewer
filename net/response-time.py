#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 response-time.py - 测试网站响应时间，支持多次ping取平均
 测量DNS解析、连接、响应等各阶段耗时
"""

import sys
import time
import argparse
import socket
import urllib.request
import urllib.error
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ResponseTimeResult:
    """响应时间结果"""
    url: str
    dns_time: float = 0       # DNS解析时间 (ms)
    connect_time: float = 0   # 连接时间 (ms)
    ssl_time: float = 0       # SSL握手时间 (ms)
    ttfb_time: float = 0      # 首字节时间 (ms)
    total_time: float = 0      # 总时间 (ms)
    status_code: int = 0
    error: str = ''


def parse_url(url: str) -> tuple:
    """解析URL返回(host, port, scheme)"""
    if '://' not in url:
        url = 'https://' + url

    parsed = urllib.parse.urlparse(url)
    host = parsed.hostname or ''
    port = parsed.port or (443 if parsed.scheme == 'https' else 80)
    path = parsed.path or '/'
    if parsed.query:
        path += '?' + parsed.query

    return host, port, path, parsed.scheme


def measure_tcp_connect(host: str, port: int, timeout: int = 10) -> float:
    """测量TCP连接时间"""
    start = time.time()
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, port))
        sock.close()
        return (time.time() - start) * 1000
    except Exception:
        return -1


def measure_dns(host: str, timeout: int = 5) -> float:
    """测量DNS解析时间"""
    start = time.time()
    try:
        socket.gethostbyname(host)
        return (time.time() - start) * 1000
    except Exception:
        return -1


def measure_http_response(url: str, timeout: int = 30) -> ResponseTimeResult:
    """测量HTTP响应时间"""
    result = ResponseTimeResult(url=url)
    start_total = time.time()

    try:
        host, port, path, scheme = parse_url(url)

        # DNS解析
        start_dns = time.time()
        try:
            socket.gethostbyname(host)
        except socket.gaierror:
            result.error = f"DNS解析失败: {host}"
            return result
        result.dns_time = (time.time() - start_dns) * 1000

        # HTTP请求
        req = urllib.request.Request(url, headers={'User-Agent': 'ResponseTime/1.0'})

        start = time.time()
        try:
            response = urllib.request.urlopen(req, timeout=timeout)
            result.status_code = response.getcode()
        except urllib.error.HTTPError as e:
            result.status_code = e.code
        except urllib.error.URLError as e:
            result.error = str(e.reason)
            return result
        except Exception as e:
            result.error = str(e)
            return result

        result.total_time = (time.time() - start_total) * 1000
        result.ttfb_time = (time.time() - start) * 1000

    except Exception as e:
        result.error = str(e)

    return result


def measure_multiple(url: str, count: int = 5, delay: float = 0.5) -> List[ResponseTimeResult]:
    """多次测量"""
    results = []

    for i in range(count):
        result = measure_http_response(url)
        results.append(result)

        if i < count - 1 and delay > 0:
            time.sleep(delay)

    return results


def format_result(result: ResponseTimeResult) -> str:
    """格式化单个结果"""
    lines = []
    lines.append(f"URL: {result.url}")

    if result.error:
        lines.append(f"错误: {result.error}")
        return '\n'.join(lines)

    lines.append(f"状态码: {result.status_code}")
    lines.append(f"DNS解析: {result.dns_time:.2f} ms")
    lines.append(f"总响应时间: {result.total_time:.2f} ms")

    return '\n'.join(lines)


def format_summary(results: List[ResponseTimeResult]) -> str:
    """格式化汇总统计"""
    successful = [r for r in results if not r.error]
    failed = [r for r in results if r.error]

    lines = []
    lines.append("=" * 60)
    lines.append("📊 响应时间统计")
    lines.append("=" * 60)

    if successful:
        dns_times = [r.dns_time for r in successful]
        total_times = [r.total_time for r in successful]

        lines.append(f"\n✅ 成功: {len(successful)}/{len(results)}")

        lines.append(f"\n📈 DNS解析时间 (ms):")
        lines.append(f"   最小: {min(dns_times):.2f}")
        lines.append(f"   最大: {max(dns_times):.2f}")
        lines.append(f"   平均: {sum(dns_times)/len(dns_times):.2f}")

        lines.append(f"\n📈 响应时间 (ms):")
        lines.append(f"   最小: {min(total_times):.2f}")
        lines.append(f"   最大: {max(total_times):.2f}")
        lines.append(f"   平均: {sum(total_times)/len(total_times):.2f}")

        # 状态码分布
        from collections import Counter
        status_codes = Counter(r.status_code for r in successful)
        lines.append(f"\n📋 状态码分布:")
        for code, count in status_codes.items():
            lines.append(f"   {code}: {count} 次")

    if failed:
        lines.append(f"\n❌ 失败: {len(failed)}/{len(results)}")
        for r in failed:
            lines.append(f"   - {r.error}")

    # 时序图
    if successful:
        lines.append(f"\n📉 响应时间趋势:")
        for i, r in enumerate(successful, 1):
            bar_len = min(int(r.total_time / 10), 40)
            bar = '█' * bar_len + '░' * (40 - bar_len)
            lines.append(f"   {i:2d}. [{bar}] {r.total_time:.0f}ms")

    return '\n'.join(lines)


def ping_host(host: str, count: int = 4) -> dict:
    """Ping主机 (使用ICMP或HTTP)"""
    import subprocess

    result = {
        'host': host,
        'sent': count,
        'received': 0,
        'lost': 0,
        'min': 0,
        'max': 0,
        'avg': 0,
        'error': None
    }

    try:
        # Windows ping
        cmd = ['ping', '-n', str(count), host]
        output = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        # 解析输出
        for line in output.stdout.split('\n'):
            # 丢失
            if 'Lost' in line or '丢失' in line:
                parts = line.split(',')
                for p in parts:
                    if 'Lost' in p or '丢失' in p:
                        lost = p.split()[1].split('(')[0]
                        result['lost'] = int(lost)
                        result['received'] = count - int(lost)

            # 时间统计
            if 'Minimum' in line or '最短' in line:
                import re
                # 提取 min/max/avg
                match = re.search(r'(\d+)\s*ms.*?(\d+)\s*ms.*?(\d+)\s*ms', line.replace(',', ''))
                if match:
                    result['min'] = int(match.group(1))
                    result['max'] = int(match.group(2))
                    result['avg'] = int(match.group(3))

    except subprocess.TimeoutExpired:
        result['error'] = '超时'
    except Exception as e:
        result['error'] = str(e)

    return result


def main():
    parser = argparse.ArgumentParser(
        description='测试网站响应时间，支持多次测量取平均',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('url', help='目标URL或域名')
    parser.add_argument('-n', '--count', type=int, default=5, help='测量次数 (默认: 5)')
    parser.add_argument('-d', '--delay', type=float, default=0.5, help='测量间隔(秒, 默认: 0.5)')
    parser.add_argument('--ping', action='store_true', help='使用ICMP ping (需要系统ping)')
    parser.add_argument('-o', '--output', help='输出到文件')
    parser.add_argument('--json', action='store_true', help='JSON格式输出')

    args = parser.parse_args()

    url = args.url
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    print(f"🔍 测试: {url}")
    print(f"📊 测量次数: {args.count}\n")

    if args.ping:
        # ICMP ping
        import urllib.parse
        parsed = urllib.parse.urlparse(url)
        host = parsed.hostname

        print(f"PING {host}:\n")
        ping_result = ping_host(host, count=args.count)

        if ping_result['error']:
            print(f"❌ 错误: {ping_result['error']}")
        else:
            print(f"往返: 最小/平均/最大 = {ping_result['min']}/{ping_result['avg']}/{ping_result['max']} ms")
            print(f"丢失: {ping_result['lost']}/{ping_result['sent']} ({100*ping_result['lost']/max(ping_result['sent'],1):.0f}%)")

    else:
        # HTTP响应测量
        results = measure_multiple(url, count=args.count, delay=args.delay)
        print(format_summary(results))

    if args.json:
        import json
        data = [{
            'dns_time': r.dns_time,
            'total_time': r.total_time,
            'status_code': r.status_code,
            'error': r.error
        } for r in results]
        print(json.dumps(data, indent=2))

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(format_summary(results))
        print(f"\n结果已保存到: {args.output}")


if __name__ == '__main__':
    main()
