# AI Code Reviewer

A curated collection of Python CLI productivity tools for developers, generated and maintained by AI.

**100+ tools across 6 categories** | **100% Python** | **MIT License**

## Contents

| Directory | Description |
|-----------|-------------|
| `code/` | Code quality, API docs, testing, static analysis |
| `git/` | Git commit helpers, gitignore generation |
| `devops/` | System monitoring, Docker, cron, environment tools |
| `data/` | JSON, CSV, YAML, XML format converters and validators |
| `net/` | HTTP debugging, URL tools, network analysis |
| `text/` | Text manipulation, formatting, search, statistics |
| `util/` | Passwords, UUIDs, QR codes, screenshots, and more |

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run any tool directly with Python
python code/code-explainer.py your_code.py

# Or make them executable
chmod +x code/code-explainer.py
./code/code-explainer.py your_code.py
```

## Directory Structure

```
ai-code-reviewer/
├── README.md
├── requirements.txt
├── code/            # Code quality tools (9 tools)
│   ├── code-explainer.py
│   ├── test-generator.py
│   ├── dependency-audit.py
│   └── ...
├── git/             # Git tools (3 tools)
│   ├── commit_gen.py
│   └── ...
├── devops/          # DevOps tools (17 tools)
│   ├── dockerfile-linter.py
│   ├── cron-parser.py
│   └── ...
├── data/            # Data format tools (14 tools)
│   ├── json-schema-validator.py
│   ├── csv2json.py
│   └── ...
├── net/             # Network tools (15 tools)
│   ├── http-headers.py
│   ├── url-decode-all.py
│   └── ...
├── text/            # Text processing (53 tools)
│   ├── regex-tester.py
│   ├── sort-lines.py
│   └── ...
└── util/            # Utilities (27 tools)
    ├── password-gen.py
    ├── uuid-generator.py
    └── ...
```

## Tools Overview

### Code Quality (`code/`)
- `code-explainer.py` - Explain code structure and dependencies
- `test-generator.py` - Auto-generate pytest tests from Python code
- `dependency-audit.py` - Scan for known vulnerabilities in dependencies
- `api-docs-gen.py` - Generate Markdown API documentation from docstrings
- `dockerfile-linter.py` - Dockerfile security and best practice checks
- `git-history-analysis.py` - Analyze commit patterns and contributors
- And more...

### Git Tools (`git/`)
- `commit_gen.py` - Generate conventional commit messages
- `gitignore-gen.py` - Generate .gitignore files for any project
- `gitmoji_commits.py` - Emoji-enhanced git commits

### DevOps (`devops/`)
- `cron-parser.py` - Parse, explain, and preview cron expressions
- `watch-process.py` - Monitor process CPU and memory in real-time
- `kill-port.py` - Find and kill processes using specific ports
- `env-exec.py` - Run commands with environment from .env files
- And more...

### Data Formats (`data/`)
- `json-schema-validator.py` - Validate JSON against schemas
- `csv2json.py` / `json2csv.py` - Convert between CSV and JSON
- `json2yaml.py` - JSON to YAML conversion
- `pretty-xml.py` - Format and indent XML
- `sql-formatter.py` - SQL formatting with performance analysis
- And more...

### Network (`net/`)
- `http-headers.py` - Show HTTP response headers
- `url-decode-all.py` - Recursively decode URL-encoded text
- `port-scan.py` - Scan common ports on remote hosts
- `domain-info.py` - DNS and WHOIS lookup
- `mac-vendor.py` - MAC address vendor/OUI lookup
- And more...

### Text Processing (`text/`)
- `regex-tester.py` - Live regex matching and testing
- `sort-lines.py` - Sort lines by various criteria
- `extract-emails.py` / `extract-urls.py` - Extract from text
- `word-count.py` / `char-count.py` - Text statistics
- `slug.py` - Convert text to URL-friendly slugs
- And more...

### Utilities (`util/`)
- `password-gen.py` / `uuid-generator.py` - Generate secure passwords and UUIDs
- `qrcode-gen.py` - Generate QR codes
- `screenshot.py` - Take screenshots from CLI
- `calc.py` - Expression calculator
- `weather-cli.py` - Weather from CLI
- And more...

## Requirements

- Python 3.7+
- See `requirements.txt` for additional dependencies

## Contributing

This repo is AI-generated and maintained. Tools are organized by category.

## Donate

If you find this useful, consider donating Nano:

```
nano_cix84h3anhf4xqxkro63x6go5onmoe8fh6qkqaoie8ddw8eyasuhigttg
```

## License

MIT
