# AI Code Reviewer

🤖 A pure CLI tool that automatically analyzes Python code and provides fix suggestions. No browser, no API keys, no cloud required.

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

## Roadmap

- [ ] Support for JavaScript/TypeScript
- [ ] Support for Go and Rust
- [ ] JSON/SARIF output format
- [ ] CI/CD integration
- [ ] Config file for custom rules

## Donate

If this tool is useful, consider donating Nano:

```
nano_cix84h3anhf4xqxkro63x6go5onmoe8fh6qkqaoie8ddw8eyasuhigttg
```

![Nano](https://img.shields.io/badge/Nano-NANO-blue)

## License

MIT License - feel free to use, modify, and distribute.
