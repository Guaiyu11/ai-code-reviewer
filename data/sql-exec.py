#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 sql-exec.py - 执行SQL查询并格式化输出
 支持 SQLite 数据库
"""

import sys
import os
import argparse
import sqlite3
from pathlib import Path
from typing import Optional, List


def connect_db(db_path: str) -> sqlite3.Connection:
    """连接数据库"""
    if db_path == ':memory:' or db_path.startswith('mem:'):
        return sqlite3.connect(':memory:')
    return sqlite3.connect(db_path)


def execute_query(conn: sqlite3.Connection, query: str,
                 headers: bool = True, max_rows: int = 1000) -> tuple:
    """执行SQL查询"""
    cursor = conn.cursor()

    # 判断是否是查询语句
    is_select = query.strip().upper().startswith(('SELECT', 'PRAGMA', 'EXPLAIN'))

    try:
        cursor.execute(query)

        if is_select:
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description] if cursor.description else []

            # 限制行数
            if len(rows) > max_rows:
                rows = rows[:max_rows]

            return columns, rows, len(rows)
        else:
            conn.commit()
            return [], [], cursor.rowcount

    except sqlite3.Error as e:
        raise e


def format_table(columns: List[str], rows: List[tuple],
                max_col_width: int = 30) -> str:
    """格式化表格输出"""
    if not columns and not rows:
        return ""

    # 计算每列宽度
    col_widths = []
    for i, col in enumerate(columns):
        max_width = len(str(col))
        for row in rows:
            if i < len(row):
                max_width = max(max_width, len(str(row[i])))
        max_width = min(max_width, max_col_width)
        col_widths.append(max_width)

    # 构建分隔线
    sep = '+' + '+'.join('-' * (w + 2) for w in col_widths) + '+'

    # 格式化行
    lines = []

    # 表头
    if columns:
        lines.append(sep)
        header = '|' + '|'.join(
            f' {str(col)[:w].ljust(w)} ' for col, w in zip(columns, col_widths)
        ) + '|'
        lines.append(header)
        lines.append(sep)

    # 数据行
    for row in rows:
        row_str = '|' + '|'.join(
            f' {str(row[i])[:w].ljust(w)} ' if i < len(row) else ' ' * (w + 2)
            for i, w in enumerate(col_widths)
        ) + '|'
        lines.append(row_str)

    if columns:
        lines.append(sep)

    return '\n'.join(lines)


def format_csv(columns: List[str], rows: List[tuple]) -> str:
    """格式化为CSV"""
    import csv
    import io

    output = io.StringIO()
    writer = csv.writer(output)

    if columns:
        writer.writerow(columns)
    writer.writerows(rows)

    return output.getvalue()


def main():
    parser = argparse.ArgumentParser(
        description='执行SQL查询并格式化输出 (SQLite)',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('database', nargs='?', default=':memory:',
                       help='数据库文件 (默认: 内存数据库)')
    parser.add_argument('-q', '--query', help='SQL查询语句')
    parser.add_argument('-f', '--file', help='从文件读取SQL')
    parser.add_argument('--tables', action='store_true', help='列出所有表')
    parser.add_argument('--schema', help='查看表结构')
    parser.add_argument('-H', '--no-headers', action='store_true', help='不显示表头')
    parser.add_argument('-m', '--max-rows', type=int, default=1000, help='最大行数')
    parser.add_argument('--csv', action='store_true', help='CSV格式输出')
    parser.add_argument('--json', action='store_true', help='JSON格式输出')

    args = parser.parse_args()

    try:
        conn = connect_db(args.database)
        print(f"📂 已连接到: {args.database}\n")

        # 列出表
        if args.tables:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
            tables = cursor.fetchall()
            print("📋 数据库表:")
            for (name,) in tables:
                print(f"  - {name}")

                # 显示每表的行数
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM [{name}]")
                    count = cursor.fetchone()[0]
                    print(f"    行数: {count}")
                except:
                    pass
            conn.close()
            return

        # 查看表结构
        if args.schema:
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA table_info([{args.schema}])")
            columns = cursor.fetchall()
            print(f"📄 表结构: {args.schema}\n")
            print(f"{'列名':<20} {'类型':<15} {'可空':<8} {'默认值':<20} {'主键'}")
            print("-" * 70)
            for col in columns:
                print(f"{col[1]:<20} {col[2]:<15} {'否' if not col[3] else '是':<8} {str(col[4]):<20} {'是' if col[5] else ''}")
            conn.close()
            return

        # 确定查询
        query = None
        if args.query:
            query = args.query
        elif args.file:
            with open(args.file, 'r', encoding='utf-8') as f:
                query = f.read()
        else:
            # 交互模式
            print("SQLite 交互模式 (输入 .quit 退出):\n")
            while True:
                try:
                    query = input("sqlite> ")
                    if query.strip() in ('.quit', '.exit', 'exit', 'quit'):
                        break
                    if query.strip():
                        columns, rows, count = execute_query(
                            conn, query,
                            headers=not args.no_headers,
                            max_rows=args.max_rows
                        )
                        if columns or rows:
                            if args.json:
                                import json
                                print(json.dumps({
                                    'columns': columns,
                                    'rows': rows,
                                    'count': count
                                }, indent=2, default=str))
                            elif args.csv:
                                print(format_csv(columns, rows), end='')
                            else:
                                print(format_table(columns, rows))
                            print(f"\n({count} 行)\n")
                except KeyboardInterrupt:
                    print("\n")
                    break
                except EOFError:
                    break
                except sqlite3.Error as e:
                    print(f"❌ 错误: {e}\n")
            conn.close()
            return

        if not query:
            print("错误: 未提供查询语句", file=sys.stderr)
            sys.exit(1)

        # 执行查询
        columns, rows, count = execute_query(
            conn, query,
            headers=not args.no_headers,
            max_rows=args.max_rows
        )

        # 输出
        if args.json:
            import json
            print(json.dumps({
                'columns': columns,
                'rows': rows,
                'count': count
            }, indent=2, default=str))
        elif args.csv:
            print(format_csv(columns, rows), end='')
        else:
            print(format_table(columns, rows))

        print(f"\n({count} 行)")

        conn.close()

    except sqlite3.Error as e:
        print(f"❌ 数据库错误: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"❌ 文件不存在: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
