# AI Code Reviewer Toolkit

🤖 A collection of pure CLI tools for code analysis and generation. No browser, no API keys, no cloud required.

## 🧰 Tools

| Tool | Description |
|------|-------------|
| `ai_code_reviewer.py` | Analyze Python code for issues, security risks, and style problems |
| `commit_gen.py` | Generate Conventional Commits messages from git diff |
| `gitmoji_commits.py` | Generate gitmoji-based commit messages from git diff |
| `readme_gen.py` | Auto-generate README.md from source code structure |

## Quick Demo

```bash
$ python3 ai_code_reviewer.py example.py

🔍 Analyzing: example.py

============================================================
📋 CODE REVIEW REPORT: example.py
============================================================

🔴 ERRORS (1)
  🔴 [ERROR] Line 5: Syntax error: invalid syntax
   💡 Suggestion: Fix the syntax error and ensure proper Python formatting.

🟡 WARNINGS (2)
  🟡 [WARNING] Line 12: Hardcoded password detected
   💡 Suggestion: Use environment variables or a secrets manager.
  🟡 [WARNING] Line 23: Bare except clause - catches all exceptions
   💡 Suggestion: Specify exception types (e.g., except ValueError:).

🔵 INFO (1)
  🔵 [INFO] Line 45: Line too long (145 chars)
   💡 Suggestion: Consider breaking this line into multiple lines (< 120 chars).

============================================================
Total: 4 issue(s)  |  Errors: 1  |  Warnings: 2  |  Info: 1
============================================================

$ echo $?
1
```

## Features

- 🔍 **Syntax checking** - Catches syntax errors before runtime
- 🔒 **Security scanning** - Detects hardcoded passwords, API keys, dangerous functions (eval, os.system)
- 🎨 **Style checks** - Line length, trailing whitespace, TODO without description
- ⚡ **Best practices** - Bare except, mutable defaults, empty except clauses
- 🚀 **Performance hints** - String concatenation in loops

## Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/ai-code-reviewer.git
cd ai-code-reviewer

# Run directly
python3 ai_code_reviewer.py your_code.py

# Or make it executable
chmod +x ai_code_reviewer.py
./ai_code_reviewer.py your_code.py
```

## Usage

### Review a single file
```bash
python3 ai_code_reviewer.py script.py
```

### Review a directory (recursive)
```bash
python3 ai_code_reviewer.py ./src/
```

### Exit codes
- `0` - No errors found
- `1` - Errors detected

## Common Scenarios

### GitHub Actions Integration

Add this to `.github/workflows/code-review.yml` to run on every pull request:

```yaml
name: AI Code Review

on:
  pull_request:
    paths:
      - '**.py'

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Run AI Code Reviewer
        run: |
          pip install -q .
          python ai_code_reviewer.py ./src/ || true
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Pre-commit Hook

Add to `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: ai-code-reviewer
        name: AI Code Review
        entry: python ai_code_reviewer.py
        language: system
        types: [python]
        pass_filenames: true
```

Or as a shell hook in `.git/hooks/pre-commit`:

```bash
#!/bin/sh
# .git/hooks/pre-commit

echo "Running AI Code Reviewer..."
python3 ai_code_reviewer.py $(git diff --name-only --diff-filter=ACM | grep '\.py$')

if [ $? -ne 0 ]; then
  echo "⚠️  Code review found issues. Review above or use --no-verify to skip."
fi
```

### CI/CD Pipeline (generic)

```yaml
# Example: GitLab CI (.gitlab-ci.yml)
code-review:
  stage: test
  script:
    - pip install -q .
    - python ai_code_reviewer.py ./app/ || true  # allow pipeline to continue
  allow_failure: true  # don't block merge, just report

# Example: CircleCI (.circleci/config.yml)
- run:
    name: AI Code Review
    command: |
      pip install -q .
      python ai_code_reviewer.py ./src/
```

## Example Output

```
🔍 Analyzing: example.py

============================================================
📋 CODE REVIEW REPORT: example.py
============================================================

🔴 ERRORS (1)
  🔴 [ERROR] Line 5: Syntax error: invalid syntax
   💡 Suggestion: Fix the syntax error and ensure proper Python formatting.

🟡 WARNINGS (2)
  🟡 [WARNING] Line 12: Hardcoded password detected
   💡 Suggestion: Use environment variables or a secrets manager.
  🟡 [WARNING] Line 23: Bare except clause - catches all exceptions
   💡 Suggestion: Specify exception types (e.g., except ValueError:).

🔵 INFO (1)
  🔵 [INFO] Line 45: Line too long (145 chars)
   💡 Suggestion: Consider breaking this line into multiple lines (< 120 chars).

============================================================
Total: 4 issue(s)
```

## Supported Checks

| Category | Checks |
|----------|--------|
| Security | eval(), exec(), os.system(), hardcoded passwords/keys |
| Best Practices | Bare except, empty except, mutable default args |
| Style | Line length > 120, trailing whitespace, bare TODO |
| Performance | String concatenation in loops |
| Syntax | AST parse errors |

## 🧩 Additional Tools

### Gitmoji Commits (`gitmoji_commits.py`)

Generate expressive gitmoji commit messages:

```bash
python gitmoji_commits.py                 # Generate from diff
python gitmoji_commits.py -v              # Verbose with stats
python gitmoji_commits.py -s              # Use staged changes
python gitmoji_commits.py --list          # List all gitmojis
```

Output example: `✨ feat: add authentication (/+45 -12)`

### README Generator (`readme_gen.py`)

Auto-generate README.md from your source code:

```bash
python readme_gen.py .                    # Scan current directory
python readme_gen.py . -o README.md       # Write to file
python readme_gen.py . --force            # Overwrite existing
```

Generates: project structure tree, feature list, module documentation, usage examples.

## Roadmap

- [ ] Support for JavaScript/TypeScript
- [ ] Support for Go and Rust
- [ ] JSON/SARIF output format
- [ ] Config file for custom rules

---

## ❤️ Support This Project

If `ai-code-reviewer` saves you time and headaches, consider buying the maintainer a coffee:

```
nano_cix84h3anhf4xqxkro63x6go5onmoe8fh6qkqaoie8ddw8eyasuhigttg
```

Nano is fast, feeless, and green — the perfect tip token. Every donation is appreciated!

---

## License

MIT License - feel free to use, modify, and distribute.
