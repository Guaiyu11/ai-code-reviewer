# AI Code Reviewer - AI 代码审查工具箱

[![CI](https://github.com/Guaiyu11/ai-code-reviewer/actions/workflows/ci.yml/badge.svg)](https://github.com/Guaiyu11/ai-code-reviewer/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![中文](https://img.shields.io/badge/-中文-red.svg)](./README_zh-CN.md)

精心整理的 120+ Python CLI 开发效率工具集合，由 AI 生成并维护。

**涵盖 7 大分类** | **纯 Python** | **MIT 许可证**

[**English**](./README.md)

## 目录

| 目录 | 说明 | 数量 |
|------|------|------|
| `code/` | 代码质量、API 文档、测试、静态分析 | ~9 |
| `git/` | Git 提交助手、gitignore 生成 | ~3 |
| `devops/` | 系统监控、Docker、cron、环境工具 | ~17 |
| `data/` | JSON、CSV、YAML、XML 格式转换与验证 | ~14 |
| `net/` | HTTP 调试、URL 工具、网络分析 | ~16 |
| `text/` | 文本处理、格式化、搜索、统计 | ~55 |
| `util/` | 密码生成、UUID、QR码、截图等 | ~27 |

## 快速开始

```bash
# 克隆
git clone https://github.com/Guaiyu11/ai-code-reviewer.git
cd ai-code-reviewer

# 安装依赖
pip install -r requirements.txt

# 直接运行任意工具
python code/code-explainer.py your_code.py
python text/regex-tester.py
python net/port-scan.py 192.168.1.1

# 或赋予执行权限
chmod +x code/code-explainer.py
./code/code-explainer.py your_code.py
```

## 目录结构

```
ai-code-reviewer/
├── README.md              # 英文说明
├── README_zh-CN.md        # 中文说明
├── CONTRIBUTING.md        # 贡献指南
├── setup.py               # pip 安装包
├── requirements.txt
├── .gitignore
├── LICENSE
├── code/                  # 代码质量工具
├── git/                   # Git 工具
├── devops/                # DevOps 工具
├── data/                  # 数据格式工具
├── net/                   # 网络工具
├── text/                  # 文本处理
└── util/                  # 通用工具
```

## 作为包安装

```bash
pip install .
```

## 亮点

- **零依赖** 大部分工具仅使用 Python 标准库
- **单文件** 每个工具独立，方便复制粘贴
- **MIT 许可证** 可自由使用、修改、分发
- **CI 自动化测试** 支持 Python 3.9 / 3.10 / 3.11 / 3.12

## 贡献代码

参见 [CONTRIBUTING.md](./CONTRIBUTING.md)。

## 捐赠

如果觉得有用，欢迎捐赠 Nano：

`nano_cix84h3anhf4xqxkro63x6go5onmoe8fh6qkqaoie8ddw8eyasuhigttg`

## 许可证

MIT
