#!/usr/bin/env python3
"""
Env Exec - Run command with environment from .env file.
Usage: python env-exec.py <file.env> <command>
"""

import sys
import os
import subprocess

def load_env(filepath):
    """Load .env file."""
    env = {}
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    return env

def exec_with_env(env, command):
    """Execute command with environment."""
    env_vars = os.environ.copy()
    env_vars.update(env)
    
    result = subprocess.run(command, shell=True, env=env_vars)
    return result.returncode

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python env-exec.py <file.env> <command>")
        sys.exit(1)
    
    env_file = sys.argv[1]
    command = ' '.join(sys.argv[2:])
    
    if not os.path.exists(env_file):
        print(f"Error: File not found: {env_file}")
        sys.exit(1)
    
    env = load_env(env_file)
    print(f"Loaded {len(env)} env variables from {env_file}")
    print(f"Running: {command}\n")
    
    rc = exec_with_env(env, command)
    sys.exit(rc)
