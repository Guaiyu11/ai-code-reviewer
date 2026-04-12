#!/usr/bin/env python3
"""
AI Conventional Commits Generator
Analyzes git diff and generates Conventional Commits messages.
"""

import subprocess
import sys
import re


def get_git_diff():
    """Get the current git diff."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            # No staged changes, try unstaged
            result = subprocess.run(
                ["git", "diff"],
                capture_output=True,
                text=True
            )
        return result.stdout
    except Exception as e:
        print(f"Error getting git diff: {e}", file=sys.stderr)
        return ""


def analyze_diff(diff_text):
    """Analyze git diff and determine commit type and scope."""
    if not diff_text.strip():
        return None, None, "No changes to commit"

    files_changed = re.findall(r'^\+\+\+ b/(.+)$', diff_text, re.MULTILINE)
    added_lines = len(re.findall(r'^\+[^+]', diff_text, re.MULTILINE))
    removed_lines = len(re.findall(r'^-[^-]', diff_text, re.MULTILINE))
    
    # Determine type
    commit_type = "chore"
    scope = None
    
    # Check for specific patterns
    has_tests = any("test" in f or "spec" in f for f in files_changed)
    has_docs = any("readme" in f.lower() or "docs" in f.lower() or ".md" in f for f in files_changed)
    has_config = any("config" in f.lower() or ".yml" in f or ".yaml" in f or ".json" in f for f in files_changed)
    has_src = any("src/" in f or "lib/" in f or "app/" in f for f in files_changed)
    
    # Check for new files vs modifications
    is_new = "[new file]" in diff_text
    is_delete = "[deleted]" in diff_text.lower()
    
    # Detect feature additions
    feature_patterns = [
        r'def\s+\w+', r'class\s+\w+', r'async\s+def', r'function\s+\w+',
        r'const\s+\w+\s*=', r'let\s+\w+\s*=', r'func\s+\w+',
        r'interface\s+\w+', r'type\s+\w+\s*='
    ]
    has_new_functions = any(re.search(p, diff_text) for p in feature_patterns)
    
    # Check for bug fixes / refactoring
    has_fixes = "fix" in diff_text.lower() or "bug" in diff_text.lower() or "error" in diff_text.lower()
    has_refactor = "refactor" in diff_text.lower() or "rename" in diff_text.lower()
    
    # Determine scope from files
    if files_changed:
        scopes = set()
        for f in files_changed:
            parts = f.split('/')
            if len(parts) > 1:
                scopes.add(parts[0])
            elif len(parts) == 1 and '.' in f:
                scopes.add(parts[0].split('.')[0])
        
        if len(scopes) == 1:
            scope = list(scopes)[0]
        elif "src" in scopes:
            scope = "src"
        elif "lib" in scopes:
            scope = "lib"
    
    # Determine commit type
    if has_tests and not has_src:
        commit_type = "test"
    elif has_docs and not has_src:
        commit_type = "docs"
    elif has_config and not has_src:
        commit_type = "chore"
    elif is_new and has_new_functions:
        commit_type = "feat"
    elif has_fixes and not has_new_functions:
        commit_type = "fix"
    elif has_refactor:
        commit_type = "refactor"
    elif added_lines > removed_lines * 2 and has_new_functions:
        commit_type = "feat"
    else:
        commit_type = "feat" if has_src else "chore"
    
    return commit_type, scope, files_changed


def generate_description(diff_text, commit_type, files_changed):
    """Generate a concise commit description from the diff."""
    if not diff_text.strip():
        return "no changes"
    
    # Extract function/class names being added or modified
    new_funcs = re.findall(r'^\+.*(?:def|class|async\s+def|function|const|let|func)\s+(\w+)', diff_text, re.MULTILINE)
    
    # Get file names for context
    file_names = [f.split('/')[-1].split('.')[0] for f in files_changed[:3]] if files_changed else []
    
    # Build description
    if new_funcs:
        main_func = new_funcs[0].replace('_', ' ')
        if len(new_funcs) == 1:
            desc = f"add {commit_type} {main_func}"
        else:
            desc = f"add {len(new_funcs)} new {commit_type}s"
    elif file_names:
        if len(file_names) == 1:
            desc = f"update {file_names[0]}"
        else:
            desc = f"update {len(file_names)} files"
    else:
        desc = f"update {commit_type}"
    
    return desc


def generate_conventional_commit(diff_text):
    """Generate a full conventional commit message."""
    commit_type, scope, files_changed = analyze_diff(diff_text)
    
    if isinstance(files_changed, str):  # Error message
        return files_changed
    
    description = generate_description(diff_text, commit_type, files_changed)
    
    if scope:
        return f"{commit_type}({scope}): {description}"
    return f"{commit_type}: {description}"


def main():
    """Main entry point."""
    diff = get_git_diff()
    
    if "--dry-run" in sys.argv or "-n" in sys.argv:
        print("📊 Analyzing git diff...")
        files = re.findall(r'^\+\+\+ b/(.+)$', diff, re.MULTILINE) if diff else []
        print(f"   Files changed: {len(files)}")
        if files:
            for f in files[:5]:
                print(f"   - {f}")
            if len(files) > 5:
                print(f"   ... and {len(files) - 5} more")
        print()
    
    commit_msg = generate_conventional_commit(diff)
    print(commit_msg)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
