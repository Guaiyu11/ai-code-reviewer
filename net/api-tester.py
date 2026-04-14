#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 api-tester.py - 发送HTTP请求，支持GET/POST/PUT/DELETE
 打印完整响应信息，支持自定义headers和body
"""

import sys
import json
import argparse
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path
from typing import Optional, Dict


def format_headers(headers: Dict[str, str]) -> str:
    """格式化headers显示"""
    return '\n'.join(f'  {k}: {v}' for k, v in headers.items())


def format_response(response: urllib.request.urlopen, body: str = None,
                    max_body: int = 10240) -> str:
    """格式化响应输出"""
    lines = []
    lines.append("=" * 60)
    lines.append("📨 HTTP 响应")
    lines.append("=" * 60)

    # 状态行
    lines.append(f"\n🔢 状态码: {response.status}")
    lines.append(f"📍 URL: {response.geturl()}")

    # 响应头
    lines.append("\n📋 响应头:")
    headers = dict(response.headers)
    lines.append(format_headers(headers))

    # 响应体
    try:
        body_bytes = response.read()
        lines.append(f"\n📦 响应体 ({len(body_bytes)} 字节):")

        # 尝试解码
        try:
            body_text = body_bytes.decode('utf-8')
        except UnicodeDecodeError:
            body_text = body_bytes.decode('latin-1')

        # 格式化JSON
        if body_text.strip().startswith(('{', '[')):
            try:
                parsed = json.loads(body_text)
                body_text = json.dumps(parsed, indent=2, ensure_ascii=False)
            except json.JSONDecodeError:
                pass

        # 截断
        if len(body_text) > max_body:
            body_text = body_text[:max_body] + f"\n... (截断, 共{len(body_text)}字节)"

        lines.append(body_text)

    except Exception as e:
        lines.append(f"\n⚠️ 无法读取响应体: {e}")

    return '\n'.join(lines)


def send_request(method: str, url: str, headers: Dict[str, str] = None,
                 body: str = None, data_file: str = None,
                 timeout: int = 30, follow_redirects: bool = True) -> dict:
    """发送HTTP请求"""
    result = {
        'success': False,
        'status_code': 0,
        'error': None,
        'response': None
    }

    # 处理headers
    if headers is None:
        headers = {}
    if 'User-Agent' not in headers:
        headers['User-Agent'] = 'api-tester/1.0'

    # 处理body
    if data_file:
        with open(data_file, 'r', encoding='utf-8') as f:
            body = f.read()

    if body and method in ('POST', 'PUT', 'PATCH'):
        # 如果body是JSON，添加Content-Type
        if 'Content-Type' not in headers:
            try:
                json.loads(body)
                headers['Content-Type'] = 'application/json'
            except (json.JSONDecodeError, TypeError):
                headers['Content-Type'] = 'application/x-www-form-urlencoded'

    # 构建请求
    try:
        req = urllib.request.Request(url, data=body.encode('utf-8') if body else None,
                                     headers=headers, method=method)

        # 发送请求
        with urllib.request.urlopen(req, timeout=timeout) as response:
            result['success'] = True
            result['status_code'] = response.status
            result['response'] = response

    except urllib.error.HTTPError as e:
        result['status_code'] = e.code
        result['error'] = f"HTTP {e.code}: {e.reason}"
        result['response'] = e
    except urllib.error.URLError as e:
        result['error'] = f"连接错误: {e.reason}"
    except TimeoutError:
        result['error'] = "请求超时"
    except Exception as e:
        result['error'] = str(e)

    return result


def main():
    parser = argparse.ArgumentParser(
        description='发送HTTP请求测试API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s GET https://api.github.com/users
  %(prog)s POST https://httpbin.org/post -d '{"name":"test"}'
  %(prog)s PUT https://httpbin.org/put -H "Authorization: Bearer xxx"
  %(prog)s DELETE https://httpbin.org/delete
        """
    )
    parser.add_argument('method', choices=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD'],
                       help='HTTP方法')
    parser.add_argument('url', help='请求URL')
    parser.add_argument('-d', '--data', help='请求体数据')
    parser.add_argument('-f', '--file', help='从文件读取请求体')
    parser.add_argument('-H', '--header', action='append', dest='headers',
                       help='自定义请求头 (格式: Key: Value)')
    parser.add_argument('-t', '--timeout', type=int, default=30, help='超时时间(秒)')
    parser.add_argument('--no-redirect', action='store_true', help='禁止重定向')
    parser.add_argument('-o', '--output', help='保存响应到文件')

    args = parser.parse_args()

    # 解析headers
    headers = {}
    if args.headers:
        for h in args.headers:
            if ':' in h:
                key, value = h.split(':', 1)
                headers[key.strip()] = value.strip()

    # 发送请求
    print(f"📤 {args.method} {args.url}")
    if headers:
        print(f"📋 请求头:")
        for k, v in headers.items():
            print(f"   {k}: {v}")
    if args.data:
        print(f"📦 请求体: {args.data[:100]}{'...' if len(args.data) > 100 else ''}")

    print()

    result = send_request(
        method=args.method,
        url=args.url,
        headers=headers,
        body=args.data,
        data_file=args.file,
        timeout=args.timeout
    )

    if result['success']:
        print(format_response(result['response']))

        if args.output:
            try:
                body = result['response'].read()
                with open(args.output, 'wb') as f:
                    f.write(body)
                print(f"\n✅ 响应已保存到: {args.output}")
            except:
                pass
    else:
        print(f"❌ 请求失败: {result['error']}")
        if result['status_code']:
            print(f"   状态码: {result['status_code']}")
        sys.exit(1)


if __name__ == '__main__':
    main()
