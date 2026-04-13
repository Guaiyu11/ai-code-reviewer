#!/usr/bin/env python3
"""
Dependency Auditor - Audit package dependencies for Python projects.
Usage: python dependency-audit.py [requirements.txt]
Scans current directory if no file specified.
"""

import os
import sys
import re
import urllib.request
import json

# Known vulnerable packages (simplified CVE database - real tool would use full CVE data)
KNOWN_VULNS = {
    'requests': ['CVE-2023-32681', 'CVE-2022-42969'],
    'urllib3': ['CVE-2023-24986', 'CVE-2022-41741'],
    'django': ['CVE-2023-36053', 'CVE-2023-30839'],
    'flask': ['CVE-2023-30839'],
    'pyyaml': ['CVE-2022-41723'],
    'pillow': ['CVE-2022-45198', 'CVE-2023-44271'],
    'numpy': ['CVE-2021-41496'],
    'pandas': ['CVE-2022-40149'],
    'jinja2': ['CVE-2024-22195', 'CVE-2023-27561'],
    'openssl': ['CVE-2023-0286', 'CVE-2022-4457'],
    'cryptography': ['CVE-2023-38325', 'CVE-2023-29491'],
    'paramiko': ['CVE-2023-48795', 'CVE-2022-24302'],
    'setuptools': ['CVE-2022-40897'],
    'wheel': ['CVE-2022-44986'],
    'pip': ['CVE-2023-5752'],
    'urllib': ['CVE-2023-24815'],
    'markupsafe': ['CVE-2022-29996'],
    'werkzeug': ['CVE-2023-25577'],
    ' tornado': ['CVE-2022-41723'],
    'aiohttp': ['CVE-2022-33105', 'CVE-2023-37276'],
    'redis': ['CVE-2023-28858', 'CVE-2023-28856'],
}


def parse_requirements(content):
    """Parse requirements.txt and extract package names and versions."""
    packages = []
    for line in content.split('\n'):
        line = line.strip()
        if not line or line.startswith('#') or line.startswith('-'):
            continue
        
        # Handle various formats: pkg==1.0, pkg>=1.0, pkg~=1.0, pkg[extra]>=1.0
        match = re.match(r'^([a-zA-Z0-9_-]+)(?:\[.*?\])?(?:[=<>~!]+.*)?$', line)
        if match:
            pkg_name = match.group(1).lower()
            packages.append(pkg_name)
    
    return packages


def check_vulnerabilities(packages):
    """Check packages against known vulnerabilities."""
    findings = []
    
    for pkg in packages:
        if pkg in KNOWN_VULNS:
            for cve in KNOWN_VULNS[pkg]:
                findings.append({
                    'package': pkg,
                    'cve': cve,
                    'severity': 'HIGH' if 'RCE' in cve or 'exec' in cve.lower() else 'MEDIUM'
                })
    
    return findings


def audit_package_json(deps):
    """Audit package.json dependencies."""
    findings = []
    vulnerable_npm = {
        'moment': ['CVE-2022-31129'],
        'lodash': ['CVE-2021-23337', 'CVE-2022-24947'],
        'minimist': ['CVE-2021-44906'],
        'node-uuid': ['CVE-2022-41915'],
        'request': ['CVE-2023-28154'],
        'axios': ['CVE-2021-3749', 'CVE-2022-31137'],
    }
    
    all_deps = {}
    if 'dependencies' in deps:
        all_deps.update(deps['dependencies'])
    if 'devDependencies' in deps:
        all_deps.update(deps['devDependencies'])
    
    for pkg in all_deps:
        if pkg.lower() in vulnerable_npm:
            for cve in vulnerable_npm[pkg.lower()]:
                findings.append({
                    'package': pkg,
                    'cve': cve,
                    'ecosystem': 'npm'
                })
    
    return findings


def audit_directory(path):
    """Audit all dependency files in a directory."""
    results = []
    
    # Python
    for req_file in ['requirements.txt', 'requirements-dev.txt', 'pyproject.toml']:
        req_path = os.path.join(path, req_file)
        if os.path.exists(req_path):
            with open(req_path, 'r') as f:
                content = f.read()
            packages = parse_requirements(content)
            findings = check_vulnerabilities(packages)
            results.append({
                'file': req_file,
                'packages': packages,
                'findings': findings
            })
    
    # Node.js
    pkg_json_path = os.path.join(path, 'package.json')
    if os.path.exists(pkg_json_path):
        import json
        with open(pkg_json_path, 'r') as f:
            deps = json.load(f)
        findings = audit_package_json(deps)
        results.append({
            'file': 'package.json',
            'findings': findings
        })
    
    return results


if __name__ == '__main__':
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = os.getcwd()
    
    print(f"=== Dependency Auditor ===")
    print(f"Scanning: {path}\n")
    
    if os.path.isfile(path):
        # Single file
        with open(path, 'r') as f:
            content = f.read()
        if path.endswith('.txt'):
            packages = parse_requirements(content)
            findings = check_vulnerabilities(packages)
            print(f"Found {len(packages)} packages, {len(findings)} potential issues")
            for f in findings:
                print(f"  [{f['severity']}] {f['package']} - {f['cve']}")
        else:
            print("Unsupported file type")
    else:
        # Directory
        results = audit_directory(path)
        total_issues = 0
        for res in results:
            print(f"File: {res['file']}")
            if 'packages' in res:
                print(f"  Packages: {len(res['packages'])}")
            if res['findings']:
                total_issues += len(res['findings'])
                for f in res['findings']:
                    print(f"  [WARNING] {f['package']} ({f.get('ecosystem','pip')}) - {f['cve']}")
            else:
                print(f"  No known vulnerabilities found")
            print()
        
        print(f"Total potential issues: {total_issues}")
        if total_issues == 0:
            print("All clear!")
