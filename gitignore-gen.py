#!/usr/bin/env python3
"""
Gitignore Generator - Generate .gitignore files for various project types.
Usage: python gitignore-gen.py <type> [--output .gitignore]
Types: python, node, java, go, rust, ruby, php, dotnet, django, react, vue, angular, jekyll, hexo, Hugo, docker, terraform, vscode, vim, emacs, linux, macos, windows, all
"""

import sys
import os

GITIGNORES = {
    'python': '''
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
env/
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# Jupyter
.ipynb_checkpoints/
*.ipynb

# mypy
.mypy_cache/
''',

    'node': '''
# Dependencies
node_modules/
package-lock.json
yarn.lock
pnpm-lock.yaml

# Build outputs
dist/
build/
.next/
.nuxt/

# Logs
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.pnpm-debug.log*

# Environment
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Testing
coverage/
.nyc_output/
''',

    'docker': '''
# Docker
Dockerfile
docker-compose.yml
.docker/

# Build context
.dockerignore

# Container runtime
*.pid
*.seed
*.pid.lock

# Logs
*.log
''',

    'go': '''
# Binaries
*.exe
*.exe~
*.dll
*.so
*.dylib

# Go workspace
go.work

# Testing
*.test
*.out

# Vendor
vendor/

# IDE
.vscode/
.idea/
''',

    'rust': '''
# Build
/target/
Cargo.lock

# IDE
.vscode/
.idea/

# Environment
.env
.env.local
''',

    'terraform': '''
# Terraform
.tfstate/
.terraform/
*.tfstate.*
.terraform.lock.hcl

# Crash logs
crash.log
crash.*.log

# Logs
*.log

# Override
override.tf
override.tf.json
''',
}

def generate_gitignore(types):
    """Generate .gitignore for specified types."""
    content = []
    
    for t in types:
        t = t.lower()
        if t in GITIGNORES:
            content.append(f'# === {t.upper()} ===')
            content.append(GITIGNORES[t].strip())
            content.append('')
    
    return '\n'.join(content)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python gitignore-gen.py <type> [--output FILE]")
        print("\nTypes:", ', '.join(sorted(GITIGNORES.keys())))
        print("\nExamples:")
        print("  python gitignore-gen.py python --output .gitignore")
        print("  python gitignore-gen.py node docker --output .gitignore")
        print("  python gitignore-gen.py all --output .gitignore")
        sys.exit(1)
    
    types = [arg for arg in sys.argv[1:] if not arg.startswith('--')]
    output = None
    
    for i, arg in enumerate(sys.argv):
        if arg == '--output' and i + 1 < len(sys.argv):
            output = sys.argv[i + 1]
    
    content = generate_gitignore(types)
    
    if output:
        with open(output, 'w') as f:
            f.write(content)
        print(f"Generated: {output}")
    else:
        print(content)
