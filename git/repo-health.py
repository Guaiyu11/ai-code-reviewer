#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 repo-health.py - 检查仓库健康度
 分析提交频率、贡献者活跃度、issue响应率等指标
"""

import subprocess
import sys
import argparse
import re
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict


def run_git(args: list, repo_path: Path = None) -> tuple:
    """运行git命令"""
    cmd = ['git', '-C', str(repo_path)] if repo_path else ['git']
    cmd.extend(args)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return '', e.stderr
    except FileNotFoundError:
        return '', 'git not found'


def get_commit_stats(repo_path: Path, days: int = 90) -> dict:
    """获取提交统计"""
    since = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

    # 获取提交数量
    stdout, _ = run_git(['rev-list', '--count', f'--since={since}', 'HEAD'], repo_path)
    total_commits = int(stdout.strip() or 0)

    # 获取每周提交数
    stdout, _ = run_git(['log', '--since', since, '--format=%ad', '--date=short'],
                       repo_path)
    commits_by_week = defaultdict(int)
    for date_str in stdout.strip().split('\n'):
        if date_str:
            try:
                date = datetime.strptime(date_str.strip(), '%Y-%m-%d')
                week = date.strftime('%Y-W%W')
                commits_by_week[week] += 1
            except ValueError:
                pass

    # 计算平均提交频率
    weeks = len(commits_by_week) or 1
    avg_commits_per_week = total_commits / weeks

    return {
        'total': total_commits,
        'by_week': commits_by_week,
        'avg_per_week': avg_commits_per_week,
        'weeks': weeks
    }


def get_contributor_stats(repo_path: Path, days: int = 90) -> dict:
    """获取贡献者统计"""
    since = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

    # 获取贡献者列表
    stdout, _ = run_git(['log', '--since', since, '--format=%ae'], repo_path)
    emails = [e.strip() for e in stdout.strip().split('\n') if e.strip()]
    unique_contributors = len(set(emails))

    # 获取每位贡献者的提交数
    stdout, _ = run_git(['shortlog', '--since', since, '-sn'], repo_path)
    contributors = []
    for line in stdout.strip().split('\n'):
        parts = line.strip().split(None, 1)
        if parts:
            commits = int(parts[0])
            name = parts[1] if len(parts) > 1 else 'Unknown'
            contributors.append({'name': name, 'commits': commits})

    return {
        'unique_contributors': unique_contributors,
        'top_contributors': contributors[:10],
        'total_contributors': len(contributors)
    }


def get_issue_stats(repo_path: Path = None, github_repo: str = None) -> dict:
    """获取issue统计 (需要GitHub CLI或手动输入)"""
    stats = {
        'open': 0,
        'closed': 0,
        'avg_response_time': None,
        'avg_close_time': None
    }

    # 尝试使用gh CLI
    if github_repo:
        try:
            # 获取open issues
            result = subprocess.run(
                ['gh', 'issue', 'list', '--repo', github_repo, '--state', 'open', '--limit', '100', '--json', 'createdAt,comments'],
                capture_output=True, text=True, check=True
            )
            import json
            open_issues = json.loads(result.stdout)
            stats['open'] = len(open_issues)

            # 获取closed issues
            result = subprocess.run(
                ['gh', 'issue', 'list', '--repo', github_repo, '--state', 'closed', '--limit', '100', '--json', 'createdAt,closedAt,comments'],
                capture_output=True, text=True, check=True
            )
            closed_issues = json.loads(result.stdout)
            stats['closed'] = len(closed_issues)

        except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError):
            pass

    return stats


def get_branch_stats(repo_path: Path) -> dict:
    """获取分支统计"""
    # 获取所有分支
    stdout, _ = run_git(['branch', '-a'], repo_path)
    all_branches = [b.strip() for b in stdout.strip().split('\n') if b.strip()]

    # 获取本地分支
    local = [b for b in all_branches if not b.startswith('remotes/')]

    # 获取远程分支
    remote = [b for b in all_branches if b.startswith('remotes/')]

    # 获取最近更新的分支
    stdout, _ = run_git(['for-each-ref', '--sort=-committerdate',
                         '--format=%(refname:short) %(committerdate:short)',
                         'refs/heads'], repo_path)
    recent_branches = []
    for line in stdout.strip().split('\n'):
        if line:
            parts = line.split()
            if len(parts) >= 2:
                recent_branches.append({'name': parts[0], 'date': parts[1]})

    return {
        'local': len(local),
        'remote': len(set(remote)),
        'recent': recent_branches[:5]
    }


def calculate_health_score(commit_stats: dict, contributor_stats: dict,
                           branch_stats: dict, issue_stats: dict) -> dict:
    """计算健康度分数"""
    scores = {}
    details = []

    # 提交活跃度 (满分30)
    if commit_stats['total'] == 0:
        commit_score = 0
        details.append(('提交活跃度', 0, '无提交'))
    elif commit_stats['avg_per_week'] < 1:
        commit_score = 10
        details.append(('提交活跃度', 10, f'平均每周 {commit_stats["avg_per_week"]:.1f} 次提交'))
    elif commit_stats['avg_per_week'] < 5:
        commit_score = 20
        details.append(('提交活跃度', 20, f'平均每周 {commit_stats["avg_per_week"]:.1f} 次提交'))
    else:
        commit_score = 30
        details.append(('提交活跃度', 30, f'平均每周 {commit_stats["avg_per_week"]:.1f} 次提交'))

    scores['commit'] = commit_score

    # 贡献者多样性 (满分25)
    contributor_count = contributor_stats['unique_contributors']
    if contributor_count == 0:
        contributor_score = 0
    elif contributor_count == 1:
        contributor_score = 10
    elif contributor_count <= 5:
        contributor_score = 20
    else:
        contributor_score = 25

    details.append(('贡献者多样性', contributor_score, f'{contributor_count} 位贡献者'))
    scores['contributor'] = contributor_score

    # 分支管理 (满分15)
    branch_score = 15 if branch_stats['local'] <= 10 else 10
    details.append(('分支管理', branch_score, f'{branch_stats["local"]} 本地分支'))
    scores['branch'] = branch_score

    # Issue管理 (满分30)
    if issue_stats['open'] == 0 and issue_stats['closed'] == 0:
        issue_score = 15  # 不知道数据
    else:
        close_rate = issue_stats['closed'] / (issue_stats['open'] + issue_stats['closed'])
        issue_score = int(close_rate * 30)
    details.append(('Issue处理', issue_score, f'{issue_stats["closed"]} 已关闭, {issue_stats["open"]} 待处理'))
    scores['issue'] = issue_score

    total = sum(scores.values())

    return {
        'total': total,
        'max': 100,
        'percentage': total,
        'breakdown': details,
        'grade': 'A' if total >= 90 else 'B' if total >= 75 else 'C' if total >= 60 else 'D'
    }


def main():
    parser = argparse.ArgumentParser(
        description='检查仓库健康度',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('path', nargs='?', default='.', help='仓库路径 (默认: 当前目录)')
    parser.add_argument('-d', '--days', type=int, default=90, help='分析天数 (默认: 90)')
    parser.add_argument('--repo', help='GitHub仓库 (用于issue统计, 格式: owner/repo)')
    parser.add_argument('-o', '--output', help='输出到文件')

    args = parser.parse_args()

    repo_path = Path(args.path).resolve()
    if not (repo_path / '.git').exists():
        print(f"错误: 不是git仓库: {repo_path}", file=sys.stderr)
        sys.exit(1)

    print(f"🔍 分析仓库: {repo_path}")
    print(f"📅 分析周期: 最近 {args.days} 天\n")

    # 收集各项统计
    print("收集提交统计...")
    commit_stats = get_commit_stats(repo_path, args.days)

    print("收集贡献者统计...")
    contributor_stats = get_contributor_stats(repo_path, args.days)

    print("收集分支统计...")
    branch_stats = get_branch_stats(repo_path)

    print("收集Issue统计...")
    issue_stats = get_issue_stats(repo_path, args.repo)

    # 计算健康度
    health = calculate_health_score(commit_stats, contributor_stats, branch_stats, issue_stats)

    # 输出报告
    print("\n" + "=" * 60)
    print(f"📊 仓库健康度报告")
    print("=" * 60)

    print(f"\n🏆 综合评分: {health['total']}/100 ({health['grade']}级)")

    print("\n📈 详细指标:")
    for name, score, detail in health['breakdown']:
        bar = '█' * (score // 5) + '░' * (20 - score // 5)
        print(f"  {name:<15} [{bar}] {score:2d}/30  {detail}")

    print("\n📅 提交统计:")
    print(f"  总提交数: {commit_stats['total']}")
    print(f"  平均每周: {commit_stats['avg_per_week']:.1f} 次")
    print(f"  活跃周数: {commit_stats['weeks']}")

    print("\n👥 贡献者统计:")
    print(f"  活跃贡献者数: {contributor_stats['unique_contributors']}")
    if contributor_stats['top_contributors']:
        print("  Top贡献者:")
        for c in contributor_stats['top_contributors'][:5]:
            print(f"    - {c['name']}: {c['commits']} commits")

    print("\n🌿 分支统计:")
    print(f"  本地分支: {branch_stats['local']}")
    print(f"  远程分支: {branch_stats['remote']}")
    if branch_stats['recent']:
        print("  最近更新:")
        for b in branch_stats['recent'][:3]:
            print(f"    - {b['name']} ({b['date']})")

    print("\n📋 Issue统计:")
    print(f"  开放: {issue_stats['open']}")
    print(f"  已关闭: {issue_stats['closed']}")

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(f"仓库健康度报告 - {repo_path.name}\n")
            f.write(f"评分: {health['total']}/100 ({health['grade']}级)\n")
        print(f"\n报告已保存到: {args.output}")


if __name__ == '__main__':
    main()
