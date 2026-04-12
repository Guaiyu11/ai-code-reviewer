#!/usr/bin/env python3
"""
AI Gitmoji Commits Generator
Analyzes git diff and generates gitmoji-based commit messages.
"""

import subprocess
import sys
import re
from typing import List, Tuple, Optional

# Gitmoji map - https://gitmoji.dev/
GITMOJIS = {
    "feat": "✨",
    "fix": "🐛",
    "docs": "📝",
    "style": "🎨",
    "refactor": "♻️",
    "perf": "⚡️",
    "test": "✅",
    "build": "📦️",
    "ci": "🔧",
    "chore": "🔨",
    "rev": "🔄",
    "del": "🗑️",
    "move": "🚚",
    "code": "💻",
    "merge": "🔀",
    "break": "🚨",
    "security": "🔒",
    "deps": "⬆️",
    "init": "🎉",
}


def get_git_diff(staged_only: bool = False) -> str:
    """Get the current git diff."""
    try:
        if staged_only:
            result = subprocess.run(
                ["git", "diff", "--cached"],
                capture_output=True, text=True
            )
            if result.returncode != 0 or not result.stdout.strip():
                result = subprocess.run(["git", "diff"], capture_output=True, text=True)
        else:
            result = subprocess.run(["git", "diff"], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        print(f"Error getting git diff: {e}", file=sys.stderr)
        return ""


def get_gitmoji_for_type(commit_type: str) -> str:
    """Get the gitmoji for a commit type."""
    return GITMOJIS.get(commit_type.lower(), "📝")


def analyze_diff(diff_text: str) -> Tuple[str, List[str], int, int]:
    """Analyze git diff and return (type, files, added, removed)."""
    if not diff_text.strip():
        return "chore", [], 0, 0

    files_changed = re.findall(r'^\+\+\+ b/(.+)$', diff_text, re.MULTILINE)
    added_lines = len(re.findall(r'^\+[^+]', diff_text, re.MULTILINE))
    removed_lines = len(re.findall(r'^-[^-]', diff_text, re.MULTILINE))

    commit_type = "chore"
    is_new = "[new file]" in diff_text
    is_delete = "[deleted]" in diff_text.lower()

    # Detect patterns
    has_tests = any("test" in f or "spec" in f for f in files_changed)
    has_docs = any("readme" in f.lower() or "docs" in f.lower() or f.endswith(".md") for f in files_changed)
    has_config = any("config" in f.lower() or f.endswith((".yml", ".yaml", ".json", ".toml")) for f in files_changed)

    new_funcs = re.findall(
        r'^\+.*(?:def|class|async\s+def|function|const|let|func|interface|type\s+\w+\s*=)\s+(\w+)',
        diff_text, re.MULTILINE
    )

    has_fixes = bool(re.search(r'\b(fix|bug|error|wrong|incorrect|broken)\b', diff_text, re.IGNORECASE))
    has_refactor = bool(re.search(r'\b(refactor|rename|restructure)\b', diff_text, re.IGNORECASE))
    has_perf = bool(re.search(r'\b(perf|optim|speed|faster|latency)\b', diff_text, re.IGNORECASE))
    has_security = bool(re.search(r'\b(security|vulnerable|injection|xss|csurf)\b', diff_text, re.IGNORECASE))
    has_deps = bool(re.search(r'\b(depend|upgrade|bump|packet|npm|pip|包)\b', diff_text, re.IGNORECASE))
    has_ci = bool(re.search(r'\b(ci|cd|pipeline|github|gitlab|action|workflow)\b', diff_text, re.IGNORECASE))
    has_build = bool(re.search(r'\b(build|compile|webpack|vite|rollup|tsc)\b', diff_text, re.IGNORECASE))
    has_style = bool(re.search(r'\b(style|format|prettier|eslint|indent)\b', diff_text, re.IGNORECASE))
    has_merge = "[merge]" in diff_text.lower() or "Merge branch" in diff_text

    # Determine type
    if has_merge:
        commit_type = "merge"
    elif is_delete and not is_new:
        commit_type = "del"
    elif has_security:
        commit_type = "security"
    elif has_fixes and new_funcs:
        commit_type = "fix"
    elif has_fixes:
        commit_type = "fix"
    elif has_perf:
        commit_type = "perf"
    elif has_refactor:
        commit_type = "refactor"
    elif is_new and new_funcs:
        commit_type = "feat"
    elif has_tests:
        commit_type = "test"
    elif has_docs:
        commit_type = "docs"
    elif has_ci:
        commit_type = "ci"
    elif has_build:
        commit_type = "build"
    elif has_deps:
        commit_type = "deps"
    elif has_style:
        commit_type = "style"
    elif new_funcs:
        commit_type = "feat"
    else:
        commit_type = "chore"

    return commit_type, files_changed, added_lines, removed_lines


def generate_short_description(diff_text: str, commit_type: str, files: List[str]) -> str:
    """Generate a short commit description."""
    new_funcs = re.findall(
        r'^\+.*(?:def|class|async\s+def|function|const|let|func)\s+(\w+)',
        diff_text, re.MULTILINE
    )
    file_names = [f.split('/')[-1].split('.')[0] for f in files[:3]] if files else []

    if new_funcs:
        main_func = new_funcs[0].replace('_', ' ')
        if len(new_funcs) == 1:
            return f"add {main_func}"
        return f"add {len(new_funcs)} {commit_type}s"
    elif file_names:
        if len(file_names) == 1:
            return f"update {file_names[0]}"
        return f"update {len(file_names)} files"
    return f"update {commit_type}"


def format_gitmoji(commit_type: str, description: str) -> str:
    """Format a gitmoji commit message."""
    emoji = get_gitmoji_for_type(commit_type)
    return f"{emoji} {commit_type}: {description}"


def format_gitmoji_verbose(commit_type: str, description: str, files: List[str],
                            added: int, removed: int) -> str:
    """Format a verbose gitmoji commit message with stats."""
    emoji = get_gitmoji_for_type(commit_type)
    stats = f"+{added} -{removed}" if (added or removed) else ""
    if stats:
        return f"{emoji} {commit_type}: {description} ({stats})"
    return f"{emoji} {commit_type}: {description}"


def main():
    """Main entry point."""
    import argparse
    parser = argparse.ArgumentParser(description="AI Gitmoji Commits Generator")
    parser.add_argument("-s", "--staged", action="store_true", help="Use staged changes only")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show file stats")
    parser.add_argument("-n", "--dry-run", action="store_true", help="Show analysis without commit")
    parser.add_argument("-l", "--list", action="store_true", help="List all available gitmojis")
    args = parser.parse_args()

    if args.list:
        print("📜 Available Gitmojis:")
        for t, e in GITMOJIS.items():
            print(f"  {e} {t}")
        return 0

    diff = get_git_diff(staged_only=args.staged)

    if not diff.strip():
        print("No changes detected.")
        return 1

    commit_type, files, added, removed = analyze_diff(diff)
    description = generate_short_description(diff, commit_type, files)

    if args.verbose or args.dry_run:
        print(f"📊 Analysis:")
        print(f"   Type: {get_gitmoji_for_type(commit_type)} {commit_type}")
        print(f"   Files: {len(files)}")
        if files:
            for f in files[:5]:
                print(f"     - {f}")
            if len(files) > 5:
                print(f"     ... and {len(files) - 5} more")
        print(f"   Changes: +{added} -{removed}")
        print()

    commit_msg = format_gitmoji_verbose(commit_type, description, files, added, removed) if args.verbose \
                 else format_gitmoji(commit_type, description)

    print(commit_msg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
