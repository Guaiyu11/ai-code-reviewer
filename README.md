# AI Code Reviewer

[![CI](https://github.com/Guaiyu11/ai-code-reviewer/actions/workflows/ci.yml/badge.svg)](https://github.com/Guaiyu11/ai-code-reviewer/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)

A curated collection of 100+ Python CLI productivity tools for developers, generated and maintained by AI.

**100+ tools across 7 categories** | **100% Python** | **MIT License**

[**中文版**](./README_zh-CN.md)

## Contents

| Directory | Description | Count |
|-----------|-------------|-------|
| `code/` | Code quality, API docs, testing, static analysis | ~9 |
| `git/` | Git commit helpers, gitignore generation | ~3 |
| `devops/` | System monitoring, Docker, cron, environment tools | ~17 |
| `data/` | JSON, CSV, YAML, XML format converters and validators | ~14 |
| `net/` | HTTP debugging, URL tools, network analysis | ~16 |
| `text/` | Text manipulation, formatting, search, statistics | ~55 |
| `util/` | Passwords, UUIDs, QR codes, screenshots, and more | ~27 |

## Quick Start

```bash
# Clone
git clone https://github.com/Guaiyu11/ai-code-reviewer.git
cd ai-code-reviewer

# Install dependencies
pip install -r requirements.txt

# Run any tool directly
python code/code-explainer.py your_code.py
python text/regex-tester.py
python net/port-scan.py 192.168.1.1

# Or make executable
chmod +x code/code-explainer.py
./code/code-explainer.py your_code.py
```

## Directory Structure

```
ai-code-reviewer/
├── README.md
├── CONTRIBUTING.md
├── setup.py              # pip installable
├── requirements.txt
├── .gitignore
├── LICENSE
├── code/                 # Code quality tools
│   ├── code-explainer.py
│   ├── test-generator.py
│   ├── dependency-audit.py
│   ├── api-docs-gen.py
│   ├── dockerfile-linter.py
│   └── ...
├── git/                  # Git tools
│   ├── commit_gen.py
│   └── gitignore-gen.py
├── devops/               # DevOps tools
│   ├── cron-parser.py
│   ├── watch-process.py
│   ├── kill-port.py
│   └── ...
├── data/                 # Data format tools
│   ├── json-schema-validator.py
│   ├── csv2json.py
│   ├── json2csv.py
│   └── ...
├── net/                  # Network tools
│   ├── http-headers.py
│   ├── url-decode-all.py
│   ├── port-scan.py
│   └── ...
├── text/                 # Text processing
│   ├── regex-tester.py
│   ├── sort-lines.py
│   ├── extract-emails.py
│   └── ...
└── util/                 # Utilities
    ├── password-gen.py
    ├── uuid-generator.py
    └── ...
```

## Install as Package

```bash
pip install .
```

## Highlights

- **Zero dependencies** for most tools (pure Python stdlib)
- **Single-file** each tool, easy to copy/paste
- **MIT License** — free to use, modify, distribute
- **AI-generated** and maintained
- **CI tested** on Python 3.9, 3.10, 3.11, 3.12

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md). All contributions welcome!

## Donate

If you find this useful:

Nano: `nano_cix84h3anhf4xqxkro63x6go5onmoe8fh6qkqaoie8ddw8eyasuhigttg`

## License

MIT
