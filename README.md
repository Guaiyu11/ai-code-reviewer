# AI Code Reviewer Toolkit

🤖 A collection of pure CLI tools for code analysis, generation, and developer productivity. No browser, no API keys, no cloud required.

## 🧰 Tools

### Code Quality & Review

| Tool | Description |
|------|-------------|
| `ai_code_reviewer.py` | Analyze Python code for issues, security risks, and style problems |
| `code-explainer.py` | Explain code structure, functions, and dependencies |
| `dependency-audit.py` | Scan Python/Node projects for known vulnerabilities |
| `test-generator.py` | Auto-generate pytest unit tests from Python source |

### Git & Version Control

| Tool | Description |
|------|-------------|
| `commit_gen.py` | Generate Conventional Commits messages from git diff |
| `gitmoji_commits.py` | Generate gitmoji-based commit messages from git diff |
| `git-history-analysis.py` | Analyze commit patterns, contributors, and code churn |
| `diff-highlight.py` | Highlight git diffs in terminal |

### Development Utilities

| Tool | Description |
|------|-------------|
| `readme_gen.py` | Auto-generate README.md from source code structure |
| `api-docs-gen.py` | Generate Markdown API docs from Python docstrings |
| `code-timer.py` | Profile code execution time |
| `log-analyzer.py` | Parse and summarize log files |
| `env-validator.py` | Validate .env files and detect issues |

### Data & Format Tools

| Tool | Description |
|------|-------------|
| `json-formatter.py` | Format, minify, and validate JSON |
| `json-schema-validator.py` | Validate JSON against JSON Schema |
| `csv-viewer.py` | Preview and analyze CSV files in terminal |
| `sql-formatter.py` | Format and analyze SQL queries |

### Web & Network

| Tool | Description |
|------|-------------|
| `http-debug.py` | Debug HTTP requests and responses |
| `secret-scan.py` | Scan for exposed API keys and secrets |

### DevOps & Infrastructure

| Tool | Description |
|------|-------------|
| `dockerfile-linter.py` | Lint Dockerfiles for security and best practices |
| `cron-parser.py` | Parse, explain, and preview cron expressions |

---

## Quick Demo

```bash
$ python3 ai_code_reviewer.py example.py

🔍 Analyzing: example.py

============================================================
📋 CODE REVIEW REPORT: example.py
============================================================

🔴 ERRORS (1)
  🔴 [ERROR] Line 5: Syntax error: invalid syntax

🟡 WARNINGS (2)
  🟡 [WARNING] Line 12: Hardcoded password detected
  🟡 [WARNING] Line 23: Bare except clause

🔵 INFO (1)
  🔵 [INFO] Line 45: Line too long (145 chars)

============================================================
Total: 4 issue(s)
============================================================

$ echo $?
1
```

## Features

- 🔍 **Syntax checking** - Catches syntax errors before runtime
- 🔒 **Security scanning** - Detects hardcoded passwords, API keys, dangerous functions
- 🎨 **Style checks** - Line length, trailing whitespace, TODO without description
- ⚡ **Best practices** - Bare except, mutable defaults, empty except clauses
- 🚀 **Performance hints** - String concatenation in loops

## Installation

```bash
git clone https://github.com/Guaiyu11/ai-code-reviewer.git
cd ai-code-reviewer
pip install -r requirements.txt  # if needed
```

## Usage Examples

```bash
# Code review
python3 ai_code_reviewer.py script.py

# Generate tests
python3 test-generator.py my_module.py

# Audit dependencies
python3 dependency-audit.py requirements.txt

# Analyze git history
python3 git-history-analysis.py --repo ./ --max 100

# Format SQL
python3 sql-formatter.py "SELECT id,name FROM users WHERE active=1" --analyze

# Lint Dockerfile
python3 dockerfile-linter.py Dockerfile

# Parse cron
python3 cron-parser.py "0 9 * * 1-5" --next 5

# Generate API docs
python3 api-docs-gen.py my_module.py --output API.md
```

## GitHub Actions Integration

```yaml
name: Code Review

on: [push, pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Run AI Code Reviewer
        run: |
          pip install -q .
          python ai_code_reviewer.py ./src/ || true
```

---

## ❤️ Support This Project

Nano (XNO) - fast, feeless, green:

```
nano_cix84h3anhf4xqxkro63x6go5onmoe8fh6qkqaoie8ddw8eyasuhigttg
```

## License

MIT License
