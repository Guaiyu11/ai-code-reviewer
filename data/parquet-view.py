#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 parquet-view.py - 查看parquet文件内容和元数据
 需要 pyarrow 或 pandas (通过pip安装)
"""

import sys
import os
import argparse
import struct
from pathlib import Path


def read_parquet_metadata(filepath: Path) -> dict:
    """读取parquet文件元数据 (不依赖外部库)"""
    metadata = {
        'file': str(filepath),
        'size': filepath.stat().st_size,
        'can_read': False,
        'error': None
    }

    try:
        with open(filepath, 'rb') as f:
            # 读取PAR1魔数
            magic = f.read(4)
            if magic != b'PAR1':
                metadata['error'] = '不是有效的PARQUET文件'
                return metadata

            # 跳到文件末尾读取footer
            f.seek(-8, 2)
            footer_size = struct.unpack('<I', f.read(4))[0]
            f.seek(-8 - footer_size, 2)
            metadata['can_read'] = True

            # 基本信息
            metadata['note'] = '需要 pyarrow 或 pandas 来解析内容'

    except Exception as e:
        metadata['error'] = str(e)

    return metadata


def read_with_pyarrow(filepath: Path, max_rows: int = 100) -> dict:
    """使用pyarrow读取parquet"""
    try:
        import pyarrow.parquet as pq

        # 读取文件
        table = pq.read_table(filepath)

        # 获取元数据
        metadata = {
            'file': str(filepath),
            'size': filepath.stat().st_size,
            'rows': table.num_rows,
            'columns': table.num_columns,
            'schema': [],
            'can_read': True
        }

        # 解析schema
        schema = table.schema
        for field in schema:
            col_info = {
                'name': field.name,
                'type': str(field.type),
            }
            metadata['schema'].append(col_info)

        # 读取部分数据
        if table.num_rows > 0:
            limited_table = table.slice(0, min(max_rows, table.num_rows))
            metadata['sample_data'] = limited_table.to_pandas().to_dict('records')

        return metadata

    except ImportError:
        return {
            'file': str(filepath),
            'error': 'pyarrow未安装，请运行: pip install pyarrow'
        }
    except Exception as e:
        return {
            'file': str(filepath),
            'error': str(e)
        }


def read_with_pandas(filepath: Path, max_rows: int = 100) -> dict:
    """使用pandas读取parquet"""
    try:
        import pandas as pd

        # 读取文件
        df = pd.read_parquet(filepath)

        # 获取元数据
        metadata = {
            'file': str(filepath),
            'size': filepath.stat().st_size,
            'rows': len(df),
            'columns': len(df.columns),
            'schema': [],
            'can_read': True
        }

        # 解析schema
        for col in df.columns:
            col_info = {
                'name': col,
                'type': str(df[col].dtype)
            }
            metadata['schema'].append(col_info)

        # 读取样本数据
        if len(df) > 0:
            sample = df.head(max_rows)
            metadata['sample_data'] = sample.to_dict('records')

        return metadata

    except ImportError:
        return None  # pandas也不可用
    except Exception as e:
        return {
            'file': str(filepath),
            'error': str(e)
        }


def format_size(size: int) -> str:
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def print_metadata(metadata: dict, max_rows: int = 10):
    """打印元数据"""
    print("\n" + "=" * 60)
    print("📄 Parquet 文件信息")
    print("=" * 60)

    print(f"\n📍 文件: {metadata['file']}")
    print(f"📏 大小: {format_size(metadata.get('size', 0))}")

    if 'error' in metadata and not metadata.get('can_read'):
        print(f"\n❌ 错误: {metadata['error']}")
        print("\n💡 提示: 安装以下库以读取内容:")
        print("   pip install pyarrow")
        print("   pip install pandas")
        return

    if metadata.get('can_read'):
        print(f"\n📊 基本信息:")
        print(f"   行数: {metadata.get('rows', 'N/A'):,}")
        print(f"   列数: {metadata.get('columns', 'N/A')}")

        if 'schema' in metadata:
            print(f"\n📋 Schema ({len(metadata['schema'])} 列):")
            print(f"   {'列名':<30} {'类型'}")
            print(f"   {'-' * 50}")
            for col in metadata['schema']:
                print(f"   {col['name']:<30} {col['type']}")

        if 'sample_data' in metadata and metadata['sample_data']:
            print(f"\n📝 样本数据 (前 {len(metadata['sample_data'])} 行):")
            sample = metadata['sample_data']
            if sample:
                keys = list(sample[0].keys())
                # 打印表头
                header = ' | '.join(str(k)[:15].ljust(15) for k in keys)
                print(f"   {header}")
                print(f"   {'-' * len(header)}")
                # 打印行
                for row in sample[:max_rows]:
                    values = ' | '.join(str(row.get(k, ''))[:15].ljust(15) for k in keys)
                    print(f"   {values}")


def main():
    parser = argparse.ArgumentParser(
        description='查看parquet文件内容和元数据',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('file', help='Parquet文件路径')
    parser.add_argument('-n', '--rows', type=int, default=10, help='显示行数')
    parser.add_argument('-j', '--json', action='store_true', help='JSON格式输出')
    parser.add_argument('--no-data', action='store_true', help='只显示元数据')

    args = parser.parse_args()

    filepath = Path(args.file)
    if not filepath.exists():
        print(f"错误: 文件不存在: {filepath}", file=sys.stderr)
        sys.exit(1)

    print(f"🔍 读取: {filepath}")

    # 尝试使用可用的库读取
    metadata = None

    # 先尝试pyarrow
    metadata = read_with_pyarrow(filepath, max_rows=args.rows)

    if metadata and not metadata.get('can_read'):
        # 再尝试pandas
        metadata = read_with_pandas(filepath, max_rows=args.rows)

    if metadata is None:
        # 使用基础读取
        metadata = read_parquet_metadata(filepath)

    if args.json:
        import json
        print(json.dumps(metadata, indent=2, default=str))
    else:
        print_metadata(metadata, max_rows=args.rows)


if __name__ == '__main__':
    main()
