# Contributing to AI Code Reviewer

Welcome! This repo is AI-generated and AI-maintained. Contributions welcome.

## How to Contribute

### Adding a New Tool

1. Pick the right directory for your tool:
   - `code/` — code quality, testing, analysis
   - `git/` — git helpers
   - `devops/` — system, Docker, cron
   - `data/` — JSON, CSV, YAML, XML converters
   - `net/` — HTTP, URL, network tools
   - `text/` — text manipulation, search
   - `util/` — misc utilities

2. Create the tool file. Requirements:
   - Single-file Python script
   - Use `#!/usr/bin/env python3` header
   - Add `--help` support with argparse
   - Keep dependencies minimal (prefer stdlib)
   - Include docstring at top

3. Update `README.md` table with your new tool

### Style Guide

```python
#!/usr/bin/env python3
"""Short description of what the tool does.

Usage:
    python your-tool.py [args]
"""

import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description='What it does')
    parser.add_argument('input', help='Input file or value')
    parser.add_argument('-o', '--output', help='Output file')
    args = parser.parse_args()
    # your code here

if __name__ == '__main__':
    main()
```

### Pull Request Process

1. Fork the repo
2. Add your tool in the appropriate directory
3. Update README.md table
4. Open PR with: `feat: add <tool-name> in <dir>/`
5. Link any related issue

### Code Review Standards

- No external dependencies unless absolutely necessary
- Works on Python 3.8+
- Includes usage examples in docstring
- Handles errors gracefully
- Has `if __name__ == '__main__':` guard
