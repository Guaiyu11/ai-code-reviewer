#!/usr/bin/env python3
"""
AI Code Reviewer - Automatically analyze code issues and provide fix suggestions.
Pure CLI tool, no browser required.
"""

import ast
import re
import sys
from pathlib import Path
from typing import List, Dict, Optional


class CodeIssue:
    def __init__(self, line: int, severity: str, category: str, message: str, suggestion: str = ""):
        self.line = line
        self.severity = severity
        self.category = category
        self.message = message
        self.suggestion = suggestion

    def __str__(self):
        emoji = {"error": "🔴", "warning": "🟡", "info": "🔵", "style": "🟢"}.get(self.severity, "⚪")
        out = f"{emoji} [{self.severity.upper()}] Line {self.line}: {self.message}"
        if self.suggestion:
            out += f"\n   💡 Suggestion: {self.suggestion}"
        return out


class AICodeReviewer:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.content = ""
        self.lines = []
        self.issues: List[CodeIssue] = []

    def load(self) -> bool:
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.content = f.read()
            self.lines = self.content.split('\n')
            return True
        except Exception as e:
            print(f"Error loading file: {e}")
            return False

    def review(self) -> List[CodeIssue]:
        self.issues = []
        self._check_syntax()
        self._check_style()
        self._check_security()
        self._check_best_practices()
        self._check_performance()
        return self.issues

    def _check_syntax(self):
        try:
            ast.parse(self.content)
        except SyntaxError as e:
            self.issues.append(CodeIssue(
                line=e.lineno or 1,
                severity="error",
                category="syntax",
                message=f"Syntax error: {e.msg}",
                suggestion="Fix the syntax error and ensure proper Python formatting."
            ))

    def _check_style(self):
        # Check for TODO/FIXME without description
        for i, line in enumerate(self.lines, 1):
            if re.match(r'\s*(TODO|FIXME|HACK|XXX):?\s*$', line, re.IGNORECASE):
                self.issues.append(CodeIssue(
                    line=i, severity="warning", category="style",
                    message="TODO/FIXME marker without description",
                    suggestion="Add a description explaining what needs to be done."
                ))

            # Check line length
            if len(line) > 120 and not line.strip().startswith('#'):
                self.issues.append(CodeIssue(
                    line=i, severity="info", category="style",
                    message=f"Line too long ({len(line)} chars)",
                    suggestion="Consider breaking this line into multiple lines (< 120 chars)."
                ))

            # Check for trailing whitespace
            if line.rstrip() != line:
                self.issues.append(CodeIssue(
                    line=i, severity="info", category="style",
                    message="Trailing whitespace",
                    suggestion="Remove trailing whitespace."
                ))

    def _check_security(self):
        dangerous = [
            (r'eval\s*\(', "Use of eval() is dangerous - can execute arbitrary code",
             "Use ast.literal_eval() for safe evaluation or redesign the logic."),
            (r'exec\s*\(', "Use of exec() is dangerous - can execute arbitrary code",
             "Avoid exec() entirely; redesign using safer alternatives."),
            (r'os\.system\s*\(', "os.system() is vulnerable to shell injection",
             "Use subprocess.run() with a list of arguments instead."),
            (r'subprocess\.call\s*\(', "subprocess.call() can be vulnerable to shell injection",
             "Use subprocess.run() with shell=False."),
            (r'password\s*=\s*["\'][^"\']+["\']', "Hardcoded password detected",
             "Use environment variables or a secrets manager."),
            (r'api[_-]?key\s*=\s*["\'][^"\']+["\']', "Hardcoded API key detected",
             "Use environment variables or a secrets manager."),
            (r'\.decode\([^)]*["\']utf-8["\'][^)]*\)\s*(==|!=)\s*True',
             "Redundant decode comparison",
             "Just use the bytes object directly as a boolean."),
        ]
        for i, line in enumerate(self.lines, 1):
            for pattern, msg, suggestion in dangerous:
                if re.search(pattern, line, re.IGNORECASE):
                    self.issues.append(CodeIssue(
                        line=i, severity="warning", category="security",
                        message=msg, suggestion=suggestion
                    ))

    def _check_best_practices(self):
        try:
            tree = ast.parse(self.content)
        except SyntaxError:
            return

        for node in ast.walk(tree):
            # Check for bare except
            if isinstance(node, ast.ExceptHandler) and node.type is None:
                self.issues.append(CodeIssue(
                    line=node.lineno, severity="warning", category="best-practice",
                    message="Bare except clause - catches all exceptions",
                    suggestion="Specify exception types (e.g., except ValueError:)."
                ))

            # Check for empty except
            if isinstance(node, ast.ExceptHandler) and not node.body:
                self.issues.append(CodeIssue(
                    line=node.lineno, severity="warning", category="best-practice",
                    message="Empty except clause",
                    suggestion="Remove empty except clauses or add error handling."
                ))

            # Check for mutable default arguments
            if isinstance(node, ast.FunctionDef):
                for arg in node.args.args:
                    if arg.annotation is None:
                        continue
                for default in node.args.defaults:
                    if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                        self.issues.append(CodeIssue(
                            line=node.lineno, severity="warning", category="best-practice",
                            message="Mutable default argument",
                            suggestion="Use None as default and initialize inside the function."
                        ))

    def _check_performance(self):
        for i, line in enumerate(self.lines, 1):
            # Check for string concatenation in loop
            if '+ ' in line and i > 0:
                # Heuristic: inside a for/while block
                context = '\n'.join(self.lines[max(0, i-3):i+1])
                if re.search(r'(for|while).*:', context):
                    if re.search(r'\+\s*=.*\+\s*["\']', line):
                        self.issues.append(CodeIssue(
                            line=i, severity="info", category="performance",
                            message="String concatenation in loop",
                            suggestion="Use a list and ''.join() or f-strings instead."
                        ))

    def report(self):
        if not self.issues:
            print("✅ No issues found!")
            return

        by_severity = {"error": [], "warning": [], "info": [], "style": []}
        for issue in self.issues:
            by_severity.get(issue.severity, by_severity["info"]).append(issue)

        print(f"\n{'='*60}")
        print(f"📋 CODE REVIEW REPORT: {self.file_path.name}")
        print(f"{'='*60}")
        for severity in ["error", "warning", "info", "style"]:
            issues = by_severity.get(severity, [])
            if issues:
                label = {"error": "🔴 ERRORS", "warning": "🟡 WARNINGS",
                         "info": "🔵 INFO", "style": "🟢 STYLE"}[severity]
                print(f"\n{label} ({len(issues)})")
                for issue in issues:
                    print(f"  {issue}")
        print(f"\n{'='*60}")
        print(f"Total: {len(self.issues)} issue(s)")


def main():
    if len(sys.argv) < 2:
        print("AI Code Reviewer - Automatically analyze code and suggest fixes")
        print("Usage: python ai_code_reviewer.py <file.py>")
        print("       python ai_code_reviewer.py <directory>")
        sys.exit(1)

    target = sys.argv[1]
    path = Path(target)

    if path.is_dir():
        files = list(path.rglob("*.py"))
    else:
        files = [path]

    for f in files:
        reviewer = AICodeReviewer(str(f))
        if reviewer.load():
            print(f"\n🔍 Analyzing: {f}")
            reviewer.review()
            reviewer.report()

    # Return exit code based on errors
    all_issues = []
    for f in files:
        r = AICodeReviewer(str(f))
        if r.load():
            all_issues.extend(r.review())
    has_errors = any(i.severity == "error" for i in all_issues)
    sys.exit(1 if has_errors else 0)


if __name__ == "__main__":
    main()
