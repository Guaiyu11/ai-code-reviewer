#!/usr/bin/env python3
"""
AI README Generator
Auto-generates README.md from source code structure and docstrings.
"""

import ast
import os
import sys
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple


class READMEAnalyzer:
    """Analyzes source code and generates README content."""

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.files: Dict[str, dict] = {}
        self.project_name = self.project_path.name
        self.description = ""
        self.installation = ""
        self.usage = ""

    def scan(self) -> None:
        """Scan project and extract metadata."""
        # Get project description from README or main file
        readme = self.project_path / "README.md"
        if readme.exists():
            content = readme.read_text(encoding="utf-8")
            # Extract first paragraph
            paras = content.split("\n\n")
            for p in paras:
                p = p.strip()
                if p and not p.startswith("#") and len(p) > 50:
                    self.description = p[:200]
                    break

        # Scan Python files
        for py_file in self.project_path.rglob("*.py"):
            if ".git" in py_file.parts or "__pycache__" in py_file.parts:
                continue
            self._analyze_py_file(py_file)

        # Detect project type
        self._detect_project_type()

    def _detect_project_type(self) -> None:
        """Detect what kind of project this is."""
        has_fastapi = any("fastapi" in str(f) for f in self.files.values())
        has_flask = any("flask" in str(f) for f in self.files.values())
        has_django = any("django" in str(f) for f in self.files.values())
        has_cli = any("argparse" in str(f) or "click" in str(f) for f in self.files.values())
        has_tests = any("test" in f for f in self.files.keys())
        has_readme = (self.project_path / "README.md").exists()
        has_requirements = (self.project_path / "requirements.txt").exists()
        has_pyproject = (self.project_path / "pyproject.toml").exists()
        has_setup = (self.project_path / "setup.py").exists()

        self._project_type = {
            "web": has_fastapi or has_flask or has_django,
            "cli": has_cli,
            "test": has_tests,
            "has_deps": has_requirements or has_pyproject or has_setup,
        }

    def _analyze_py_file(self, file_path: Path) -> None:
        """Analyze a Python file and extract info."""
        try:
            content = file_path.read_text(encoding="utf-8")
            tree = ast.parse(content, filename=str(file_path))
        except Exception:
            return

        info = {
            "path": str(file_path.relative_to(self.project_path)),
            "classes": [],
            "functions": [],
            "docstring": ast.get_docstring(tree) or "",
            "has_main": False,
            "line_count": len(content.splitlines()),
        }

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                doc = ast.get_docstring(node) or ""
                info["classes"].append({
                    "name": node.name,
                    "doc": doc.split(".")[0] if doc else "",
                    "methods": [n.name for n in node.body if isinstance(n, ast.FunctionDef)],
                })
            elif isinstance(node, ast.FunctionDef):
                if node.name == "main" or node.name == "__main__":
                    info["has_main"] = True
                doc = ast.get_docstring(node) or ""
                info["functions"].append({
                    "name": node.name,
                    "doc": doc.split(".")[0] if doc else "",
                    "args": [a.arg for a in node.args.args],
                })

        self.files[str(file_path)] = info

    def _get_main_files(self) -> List[Tuple[str, dict]]:
        """Get main source files sorted by importance."""
        result = []
        for path, info in self.files.items():
            if info["classes"] or info["functions"] or info["has_main"]:
                result.append((path, info))
        result.sort(key=lambda x: (
            "main" in x[0].lower(),
            -x[1]["line_count"],
            x[0]
        ))
        return result

    def generate(self) -> str:
        """Generate README content."""
        lines = []

        # Title
        name = self.project_name.replace("-", " ").replace("_", " ").title()
        lines.append(f"# {name}\n")
        if self.description:
            lines.append(f"{self.description}\n")

        # Badges placeholder
        lines.append("[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)]")
        lines.append("[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)]\n")

        # Features
        features = self._extract_features()
        if features:
            lines.append("## ✨ Features\n")
            for f in features:
                lines.append(f"- {f}")
            lines.append("")

        # Quick Start
        lines.append("## 🚀 Quick Start\n")
        lines.append("```bash")
        if self._project_type.get("has_deps"):
            lines.append("pip install -r requirements.txt")
        if any(info["has_main"] for _, info in self.files.items()):
            lines.append(f"python {list(self.files.keys())[0]}")
        elif self._project_type.get("cli"):
            lines.append(f"python -m {self.project_name} --help")
        lines.append("```\n")

        # Project Structure
        lines.append("## 📁 Project Structure\n")
        lines.append("```\n" + self._generate_tree() + "```\n")

        # Main Modules
        main_files = self._get_main_files()
        if main_files:
            lines.append("## 📦 Modules\n")
            for path, info in main_files[:5]:
                rel = Path(path)
                lines.append(f"### `{path}`\n")
                if info["docstring"]:
                    lines.append(f"{info['docstring'][:150]}...\n")
                if info["classes"]:
                    lines.append("**Classes:** ")
                    lines.append(", ".join(f"`{c['name']}`" for c in info["classes"]) + "\n")
                if info["functions"]:
                    funcs = [f["name"] for f in info["functions"] if not f["name"].startswith("_")]
                    if funcs:
                        lines.append("**Functions:** ")
                        lines.append(", ".join(f"`{fn}`" for fn in funcs[:10]) + "\n")
                lines.append("")

        # Usage
        lines.append("## 💡 Usage\n")
        for path, info in main_files[:3]:
            if info["has_main"]:
                lines.append("```bash")
                lines.append(f"python {path} --help")
                lines.append("```\n")
                break

        # Contributing
        lines.append("## 🤝 Contributing\n")
        lines.append("1. Fork the repository")
        lines.append("2. Create a feature branch (`git checkout -b feature/amazing-feature`)")
        lines.append("3. Commit changes (`git commit -m '✨ feat: add amazing feature'`)")
        lines.append("4. Push to branch (`git push origin feature/amazing-feature`)")
        lines.append("5. Open a Pull Request\n")

        # License
        lines.append("## 📄 License\n")
        lines.append("Distributed under the MIT License.\n")

        return "\n".join(lines)

    def _extract_features(self) -> List[str]:
        """Extract features from docstrings."""
        features = set()
        keywords = [
            "analyze", "scan", "check", "detect", "find", "search",
            "generate", "create", "build", "make",
            "parse", "extract", "read", "write", "load", "save",
            "format", "validate", "verify", "test",
        ]
        for info in self.files.values():
            doc = info.get("docstring", "").lower()
            for kw in keywords:
                if kw in doc:
                    # Capitalize and clean up
                    feat = doc[doc.find(kw):].split(".")[0].strip()
                    feat = feat[:60].capitalize()
                    if len(feat) > 10:
                        features.add(feat)
        return sorted(list(features))[:10]

    def _generate_tree(self, prefix: str = "", path: Optional[Path] = None) -> str:
        """Generate a simple directory tree."""
        if path is None:
            path = self.project_path

        lines = []
        try:
            items = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name))
            dirs = [i for i in items if i.is_dir() and not i.name.startswith(".")]
            files = [i for i in items if i.is_file() and i.suffix in (".py", ".md", ".txt", ".yml", ".yaml", ".json", ".toml")]

            for i, item in enumerate(dirs + files):
                is_last = i == len(dirs + files) - 1
                connector = "└── " if is_last else "├── "
                lines.append(f"{prefix}{connector}{item.name}")

                if item.is_dir() and item.name not in (".git", "__pycache__"):
                    extension = "    " if is_last else "│   "
                    lines.append(self._generate_tree(prefix + extension, item))
        except PermissionError:
            pass

        return "\n".join(lines)


def main():
    """Main entry point."""
    import argparse
    parser = argparse.ArgumentParser(description="AI README Generator")
    parser.add_argument("path", nargs="?", default=".", help="Project path (default: current)")
    parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    parser.add_argument("-f", "--force", action="store_true", help="Overwrite existing README")
    args = parser.parse_args()

    project_path = Path(args.path).resolve()
    if not project_path.exists():
        print(f"Error: Path does not exist: {project_path}", file=sys.stderr)
        return 1

    readme_path = project_path / "README.md"
    if readme_path.exists() and not args.force:
        print(f"README.md already exists. Use --force to overwrite.", file=sys.stderr)
        return 1

    analyzer = READMEAnalyzer(str(project_path))
    analyzer.scan()
    content = analyzer.generate()

    if args.output:
        Path(args.output).write_text(content, encoding="utf-8")
        print(f"✅ README written to {args.output}")
    else:
        print(content)

    return 0


if __name__ == "__main__":
    sys.exit(main())
