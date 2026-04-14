#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 dns-lookup.py - 多类型DNS查询工具
 支持 A/AAAA/CNAME/MX/TXT/NS/SOA/SPF/PTR 查询
"""

import sys
import socket
import argparse
import dns.resolver
import dns.query
import dns.zone
import dns.name
import dns.reversename
from typing import Optional


# DNS记录类型
DNS_TYPES = {
    'A': socket.AF_INET,      # IPv4地址
    'AAAA': socket.AF_INET6,  # IPv6地址
    'CNAME': 5,               # 别名
    'MX': 15,                 # 邮件交换
    'TXT': 16,                # 文本记录
    'NS': 2,                  # 域名服务器
    'SOA': 6,                 # 起始授权记录
    'SPF': 99,                # SPF记录
    'PTR': 12,                # 指针记录 (反向DNS)
    'SRV': 33,                # 服务定位器
    'CAA': 257,               # CA授权
    'DS': 43,                 # 委托签名
    'DNSKEY': 48,             # DNS密钥
}


def format_result(records: list, record_type: str) -> str:
    """格式化DNS记录结果"""
    if not records:
        return "  (无记录)"

    lines = []
    for record in records:
        if record_type == 'MX':
            lines.append(f"  {record.preference:>3} {record.exchange}")
        elif record_type == 'TXT' or record_type == 'SPF':
            lines.append(f'  "{record.strings[0].decode() if isinstance(record.strings[0], bytes) else record.strings[0]}"')
        elif record_type == 'SOA':
            lines.append(f"  {record.mname} {record.rname} (serial={record.serial})")
        elif record_type == 'SRV':
            lines.append(f"  {record.priority:>3} {record.weight:>3} {record.port} {record.target}")
        elif record_type == 'NS':
            lines.append(f"  {record}")
        elif record_type == 'CNAME':
            lines.append(f"  {record}")
        elif hasattr(record, 'address'):
            lines.append(f"  {record.address}")
        else:
            lines.append(f"  {record}")

    return '\n'.join(lines)


def dns_lookup(domain: str, query_type: str = 'A',
              dns_server: str = None, timeout: int = 10) -> dict:
    """执行DNS查询"""
    result = {
        'domain': domain,
        'type': query_type,
        'records': [],
        'error': None
    }

    try:
        resolver = dns.resolver.Resolver()
        resolver.timeout = timeout
        resolver.lifetime = timeout

        if dns_server:
            resolver.nameservers = [dns_server]

        # PTR查询需要特殊处理
        if query_type == 'PTR':
            domain = dns.reversename.from_address(domain)

        answers = resolver.resolve(domain, query_type)

        for rdata in answers:
            result['records'].append(rdata)

    except dns.resolver.NXDOMAIN:
        result['error'] = "域名不存在 (NXDOMAIN)"
    except dns.resolver.NoAnswer:
        result['error'] = "无响应记录 (NOANSWER)"
    except dns.resolver.NoNameservers:
        result['error'] = "无可用DNS服务器 (NONAMESERVERS)"
    except dns.exception.Timeout:
        result['error'] = "查询超时"
    except Exception as e:
        result['error'] = str(e)

    return result


def reverse_lookup(ip: str) -> dict:
    """反向DNS查询"""
    return dns_lookup(ip, 'PTR')


def zone_transfer(domain: str, dns_server: str = None) -> dict:
    """尝试区域传输 (AXFR)"""
    result = {
        'domain': domain,
        'records': [],
        'error': None
    }

    try:
        # 确定nameserver
        if not dns_server:
            resolver = dns.resolver.Resolver()
            ns_answers = resolver.resolve(domain, 'NS')
            dns_server = str(ns_answers[0])

        # 获取域名区域
        zone_name = dns.name.from_text(domain)
        if not zone_name.is_absolute():
            zone_name = zone_name.concatenate(zone_name)

        # 执行AXFR
        axfr = dns.query.xfr(dns_server, zone_name, lifetime=30)
        zone = dns.zone.from_xfr(axfr)

        for name, node in zone.items():
            for rdataset in node.rdatasets:
                result['records'].append(f"{name} {rdataset}")

    except Exception as e:
        result['error'] = f"区域传输失败: {e}"

    return result


def get_dns_info(domain: str) -> dict:
    """获取域名的完整DNS信息"""
    info = {}

    # 常用记录类型
    types_to_check = ['A', 'AAAA', 'MX', 'TXT', 'NS', 'CNAME']

    for record_type in types_to_check:
        result = dns_lookup(domain, record_type)
        if result['records']:
            info[record_type] = result['records']
        elif result['error'] and 'NXDOMAIN' not in result['error']:
            info[record_type] = result['error']

    return info


def main():
    parser = argparse.ArgumentParser(
        description='多类型DNS查询工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
支持查询类型: A, AAAA, CNAME, MX, TXT, NS, SOA, SPF, SRV, PTR

示例:
  %(prog)s example.com                    # A记录查询
  %(prog)s example.com -t MX              # MX记录查询
  %(prog)s example.com -t ALL             # 所有常见记录
  %(prog)s 8.8.8.8 --ptr                 # 反向DNS查询
  %(prog)s example.com --axfr             # 区域传输
  %(prog)s example.com -s 8.8.8.8         # 指定DNS服务器
        """
    )
    parser.add_argument('domain', help='域名或IP地址')
    parser.add_argument('-t', '--type', default='A',
                       help=f'DNS记录类型 (默认: A), 可选: {", ".join(DNS_TYPES.keys())}')
    parser.add_argument('-s', '--server', help='指定DNS服务器')
    parser.add_argument('--ptr', action='store_true', help='反向DNS查询')
    parser.add_argument('--axfr', action='store_true', help='尝试区域传输')
    parser.add_argument('--all', action='store_true', help='查询所有常见记录')
    parser.add_argument('-o', '--output', help='输出到文件')
    parser.add_argument('--json', action='store_true', help='JSON格式输出')

    args = parser.parse_args()

    domain = args.domain

    # JSON输出
    output_data = {}

    if args.all or args.type == 'ALL':
        # 查询所有常见记录
        print(f"🔍 查询 {domain} 的DNS信息...\n")
        info = get_dns_info(domain)

        for record_type, records in info.items():
            print(f"📋 {record_type} 记录:")
            if isinstance(records, list):
                print(format_result(records, record_type))
            else:
                print(f"  错误: {records}")
            print()
            output_data[record_type] = str(records) if isinstance(records, list) else records

    elif args.ptr:
        # 反向查询
        print(f"🔍 反向查询: {domain}")
        result = reverse_lookup(domain)
        if result['records']:
            print(f"\n✅ PTR记录:")
            print(format_result(result['records'], 'PTR'))
            output_data = result
        else:
            print(f"\n❌ {result['error']}")
            output_data = result

    elif args.axfr:
        # 区域传输
        print(f"🔍 尝试区域传输: {domain}")
        result = zone_transfer(domain, args.server)
        if result['records']:
            print(f"\n✅ 区域传输成功 ({len(result['records'])} 条记录):")
            for record in result['records'][:50]:
                print(f"  {record}")
            output_data = result
        else:
            print(f"\n❌ {result['error']}")
            output_data = result

    else:
        # 单个记录查询
        record_type = args.type.upper()
        print(f"🔍 查询 {domain} 的 {record_type} 记录")

        result = dns_lookup(domain, record_type, dns_server=args.server)

        if result['records']:
            print(f"\n✅ {record_type} 记录:")
            print(format_result(result['records'], record_type))
            output_data = {
                'domain': domain,
                'type': record_type,
                'records': [str(r) for r in result['records']]
            }
        else:
            print(f"\n❌ {result['error']}")
            output_data = result

    if args.json:
        import json
        print(json.dumps(output_data, indent=2, ensure_ascii=False))

    if args.output:
        import json
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        print(f"\n结果已保存到: {args.output}")


if __name__ == '__main__':
    main()
