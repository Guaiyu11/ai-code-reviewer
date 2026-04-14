#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 service-restart.py - 一键重启系统服务
 支持 systemd / sysvinit / launchd (macOS)
"""

import sys
import os
import subprocess
import argparse
import time
from pathlib import Path


def run_cmd(cmd: list, check: bool = True) -> tuple:
    """运行命令"""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=check)
        return result.stdout.strip(), result.stderr.strip()
    except subprocess.CalledProcessError as e:
        return e.stdout.strip() if e.stdout else '', e.stderr.strip() if e.stderr else ''
    except FileNotFoundError:
        return '', f"命令未找到: {cmd[0]}"


def detect_init_system() -> str:
    """检测系统初始化方式"""
    if sys.platform == 'darwin':
        return 'launchd'

    # 检查systemd
    stdout, _ = run_cmd(['which', 'systemctl'], check=False)
    if stdout and 'systemctl' in stdout:
        # 确认systemd正在运行
        _, err = run_cmd(['systemctl', 'is-system-running'], check=False)
        if 'running' in err.lower() or not err:
            return 'systemd'

    # 检查sysvinit
    stdout, _ = run_cmd(['which', 'service'], check=False)
    if stdout and 'service' in stdout:
        return 'sysvinit'

    # 检查OpenRC
    stdout, _ = run_cmd(['which', 'rc-service'], check=False)
    if stdout:
        return 'openrc'

    return 'unknown'


def systemd_restart(service: str, force: bool = False) -> bool:
    """systemd服务重启"""
    print(f"🔄 通过systemd重启服务: {service}")

    # 检查服务是否存在
    stdout, _ = run_cmd(['systemctl', 'is-active', service], check=False)
    if stdout != 'active' and not force:
        print(f"   服务未运行: {service}")
        return False

    # 停止服务
    print(f"   停止服务...")
    stdout, err = run_cmd(['sudo', 'systemctl', 'stop', service], check=False)
    if err and 'error' in err.lower():
        print(f"   ⚠️ 停止失败: {err}")
    else:
        print(f"   ✅ 已停止")

    time.sleep(1)

    # 启动服务
    print(f"   启动服务...")
    stdout, err = run_cmd(['sudo', 'systemctl', 'start', service], check=False)
    if err and 'error' in err.lower():
        print(f"   ❌ 启动失败: {err}")
        return False

    # 检查状态
    stdout, _ = run_cmd(['systemctl', 'is-active', service], check=False)
    if stdout == 'active':
        print(f"   ✅ 服务已启动")
        return True
    else:
        print(f"   ❌ 服务启动失败")
        return False


def systemd_status(service: str) -> str:
    """获取systemd服务状态"""
    stdout, _ = run_cmd(['systemctl', 'is-active', service], check=False)
    return stdout


def sysvinit_restart(service: str, force: bool = False) -> bool:
    """sysvinit服务重启"""
    print(f"🔄 通过sysvinit重启服务: {service}")

    # 检查服务脚本是否存在
    init_path = f'/etc/init.d/{service}'
    if not Path(init_path).exists():
        print(f"   ❌ 服务脚本不存在: {init_path}")
        return False

    # 停止
    print(f"   停止服务...")
    stdout, err = run_cmd(['sudo', 'service', service, 'stop'], check=False)
    time.sleep(1)

    # 启动
    print(f"   启动服务...")
    stdout, err = run_cmd(['sudo', 'service', service, 'start'], check=False)
    if err and ('fail' in err.lower() or 'error' in err.lower()):
        print(f"   ❌ 启动失败: {err}")
        return False

    print(f"   ✅ 服务已重启")
    return True


def launchd_restart(service: str) -> bool:
    """macOS launchd服务重启"""
    print(f"🔄 通过launchd重启服务: {service}")

    # 获取service路径
    service_path = f'~/Library/LaunchAgents/{service}.plist'
    service_path = os.path.expanduser(service_path)

    if not Path(service_path).exists():
        # 尝试系统路径
        service_path = f'/Library/LaunchAgents/{service}.plist'
        if not Path(service_path).exists():
            print(f"   ❌ 服务配置不存在")
            return False

    # 卸载
    stdout, err = run_cmd(['launchctl', 'unload', service_path], check=False)
    time.sleep(1)

    # 加载
    stdout, err = run_cmd(['launchctl', 'load', service_path], check=False)
    if err and 'already' not in err.lower():
        print(f"   ❌ 启动失败: {err}")
        return False

    print(f"   ✅ 服务已重启")
    return True


def list_services(init_system: str):
    """列出可用的服务"""
    print(f"📋 系统 ({init_system}) 中的服务:\n")

    if init_system == 'systemd':
        stdout, _ = run_cmd(['systemctl', 'list-units', '--type=service', '--state=running',
                            '--no-pager', '--no-legend'], check=False)
        for line in stdout.split('\n'):
            if '.service' in line:
                parts = line.split()
                if parts:
                    print(f"  {parts[0]}")

    elif init_system == 'sysvinit':
        stdout, _ = run_cmd(['service', '--status-all'], check=False)
        for line in stdout.split('\n'):
            if line.strip():
                print(f"  {line.strip()}")

    elif init_system == 'launchd':
        stdout, _ = run_cmd(['launchctl', 'list'], check=False)
        for line in stdout.split('\n')[1:]:  # 跳过header
            if line.strip():
                parts = line.split()
                if len(parts) >= 3:
                    print(f"  {parts[2]}")


def main():
    parser = argparse.ArgumentParser(
        description='一键重启系统服务 (systemd/sysvinit/launchd)',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('service', nargs='?', help='服务名称')
    parser.add_argument('-l', '--list', action='store_true', help='列出可用服务')
    parser.add_argument('-f', '--force', action='store_true', help='强制重启')
    parser.add_argument('-s', '--status', help='查看服务状态')
    parser.add_argument('--init', choices=['systemd', 'sysvinit', 'launchd', 'auto'],
                       default='auto', help='指定初始化系统')

    args = parser.parse_args()

    # 检测或指定初始化系统
    if args.init == 'auto':
        init_system = detect_init_system()
        print(f"🔍 检测到系统初始化方式: {init_system}\n")
    else:
        init_system = args.init

    if args.list:
        list_services(init_system)
        return

    if args.status:
        if init_system == 'systemd':
            status = systemd_status(args.status)
            print(f"服务状态: {status}")
        else:
            print("状态查看仅支持systemd")
        return

    if not args.service:
        print("错误: 请指定服务名称")
        print("用法: service-restart.py <service>")
        print("      service-restart.py --list")
        sys.exit(1)

    service = args.service
    if not service.endswith('.service'):
        service = f'{service}.service'

    if init_system == 'systemd':
        success = systemd_restart(service, force=args.force)
    elif init_system == 'sysvinit':
        service = service.replace('.service', '')
        success = sysvinit_restart(service, force=args.force)
    elif init_system == 'launchd':
        service = service.replace('.service', '')
        success = launchd_restart(service)
    else:
        print(f"❌ 不支持的初始化系统: {init_system}")
        sys.exit(1)

    if not success:
        sys.exit(1)


if __name__ == '__main__':
    main()
