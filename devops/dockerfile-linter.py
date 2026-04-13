#!/usr/bin/env python3
"""
Dockerfile Linter - Lint Dockerfiles for best practices.
Usage: python dockerfile-linter.py [Dockerfile]
Scans Dockerfile in current dir if not specified.
"""

import sys
import os

ISSUES = {
    'no-tag': {'severity': 'WARNING', 'msg': 'No image tag specified (use :latest is discouraged)'},
    'no-user': {'severity': 'WARNING', 'msg': 'USER not set - container runs as root'},
    'apt-noclean': {'severity': 'INFO', 'msg': 'APT packages not cleaned up in same layer'},
    'curl-wget': {'severity': 'WARNING', 'msg': 'Using curl/wget to download scripts - verify source'},
    'expose-all': {'severity': 'INFO', 'msg': 'EXPOSE 0.0.0.0 - consider specific interfaces'},
    'privileged': {'severity': 'CRITICAL', 'msg': 'Container may run in privileged mode'},
    'pip-noreq': {'severity': 'WARNING', 'msg': 'pip install without --no-cache-dir'},
    'copy-all': {'severity': 'INFO', 'msg': 'COPY . used - consider copying only necessary files'},
    'add-instead-copy': {'severity': 'INFO', 'msg': 'ADD unpacks archives and follows URLs - COPY is preferred'},
    'no-healthcheck': {'severity': 'INFO', 'msg': 'No HEALTHCHECK defined'},
    'multi-stage-no': {'severity': 'INFO', 'msg': 'Consider multi-stage build to reduce image size'},
    'env-secret': {'severity': 'CRITICAL', 'msg': 'Secrets in ENV are visible in image history'},
    'run-sudo': {'severity': 'WARNING', 'msg': 'Using sudo in RUN - may not be installed in base image'},
    'latest-tag': {'severity': 'INFO', 'msg': 'Base image uses :latest tag'},
    'root-files': {'severity': 'INFO', 'msg': 'Files created by COPY/RUN owned by root'},
}

CHECKS = [
    (r'FROM\s+\S+:latest', 'latest-tag'),
    (r'FROM\s+\S+$', 'no-tag'),
    (r'USER\s+root', 'no-user'),
    (r'apt-get\s+install', 'apt-noclean'),
    (r'apt-get\s+install.*\s+&&\\\s+rm', 'apt-noclean', True),  # suppress if cleaned
    (r'curl\s+|wget\s+', 'curl-wget'),
    (r'EXPOSE\s+0\.0\.0\.0', 'expose-all'),
    (r'pip\s+install(?!\s+--no-cache)', 'pip-noreq'),
    (r'COPY\s+\.\s+', 'copy-all'),
    (r'^ADD\s+', 'add-instead-copy'),
    (r'HEALTHCHECK', 'no-healthcheck', True),
    (r'ENV\s+.*=(?!/).*', 'env-secret'),
    (r'sudo\s+', 'run-sudo'),
    (r'--privileged', 'privileged'),
]


def lint_dockerfile(content):
    """Lint Dockerfile content and return issues."""
    lines = content.split('\n')
    issues = []
    
    has_apt_install = False
    has_apt_clean = False
    has_healthcheck = False
    
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        
        if 'apt-get install' in stripped or 'apt install' in stripped:
            has_apt_install = True
        if 'rm -rf /var/lib/apt/lists' in stripped or 'apt-get clean' in stripped:
            has_apt_clean = True
        
        if stripped.startswith('HEALTHCHECK'):
            has_healthcheck = True
        
        # Check patterns
        for check in CHECKS:
            pattern, issue_key = check[0], check[1]
            suppress = len(check) > 2 and check[2]
            
            if suppress and has_apt_clean and issue_key == 'apt-noclean':
                continue
            
            if issue_key == 'no-healthcheck' and has_healthcheck:
                continue
            
            if issue_key == 'apt-noclean' and has_apt_clean:
                continue
            
            import re
            if re.search(pattern, stripped):
                issue = ISSUES.get(issue_key, {}).copy()
                issue['line'] = i
                issue['content'] = stripped[:80]
                issue['key'] = issue_key
                issues.append(issue)
    
    return issues


if __name__ == '__main__':
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = 'Dockerfile'
    
    if not os.path.exists(path):
        print(f"Error: File not found: {path}")
        sys.exit(1)
    
    with open(path, 'r') as f:
        content = f.read()
    
    print(f"=== Dockerfile Linter: {path} ===\n")
    
    issues = lint_dockerfile(content)
    
    if not issues:
        print("No issues found. Good job!")
    else:
        severity_order = ['CRITICAL', 'WARNING', 'INFO']
        for severity in severity_order:
            sev_issues = [i for i in issues if i['severity'] == severity]
            if sev_issues:
                print(f"[{severity}]")
                for issue in sev_issues:
                    print(f"  Line {issue['line']}: {issue['msg']}")
                    print(f"    -> {issue['content']}")
                print()
        
        total = len(issues)
        critical = sum(1 for i in issues if i['severity'] == 'CRITICAL')
        print(f"Total: {total} issues ({critical} critical)")
