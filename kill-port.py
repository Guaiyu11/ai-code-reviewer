#!/usr/bin/env python3
"""
Kill Port - Kill process using a specific port.
Usage: python kill-port.py <port>
"""

import sys

def find_process_by_port(port):
    """Find process using port."""
    import subprocess
    try:
        result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if f':{port}' in line and 'LISTENING' in line:
                parts = line.split()
                if len(parts) >= 5:
                    pid = parts[-1]
                    return pid
    except:
        pass
    return None

def kill_process(pid):
    """Kill process by PID."""
    import subprocess
    try:
        subprocess.run(['taskkill', '/F', '/PID', pid], capture_output=True)
        print(f"Killed process {pid}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python kill-port.py <port>")
        sys.exit(1)
    
    port = sys.argv[1]
    pid = find_process_by_port(port)
    
    if pid:
        print(f"Process {pid} is using port {port}")
        kill_process(pid)
    else:
        print(f"No process found using port {port}")
