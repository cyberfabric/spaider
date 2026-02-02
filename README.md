# **Spider**

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.0-green.svg)]()
[![Status](https://img.shields.io/badge/status-active-brightgreen.svg)]()
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)]()

**Version**: 2.0 | **Status**: Active | **Language**: English

**Audience**: Prompt engineers, AI developers, software architects, engineering teams

**Spider** is a platform for weaving agentic systems: its threads (like prompts, templates, DSL, rules) run through the whole project, turning intent into consistent artifacts. **Spider** focuses on four principles — **feedback**, **transformation**, **determinism**, and **quality** — so you can derive documents from documents, code from documents, or documents from code while keeping everything aligned. Each transformation is a controlled step in a pipeline: feedback tightens the web, deterministic validation removes LLM variability, and traceability keeps every derived piece connected and reviewable.

As an **extensible platform**, **Spider** can be "trained" by registering thread packages called **Weavers**. Each **Weaver** bundles templates, rules, checklists and examples for a specific domain or use case. 

**Spider** comes with a built-in **SDLC Weaver** that implements a full Software Development Life Cycle (SDLC) pipeline from Product Requirements Document (PRD) to code, with traceability and validation at every step.

---

## Table of Contents

- [**Spider**](#spider)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Project Setup (Spider + Agents)](#project-setup-spider--agents)
  - [**Spider SDLC** Overview](#spider-sdlc-overview)
  - [Contributing](#contributing)

---

## Prerequisites

Before using **Spider**, ensure you have:

- **Python 3.8+** — Required for `spider` tool execution
- **Git** — For version control and submodule installation (recommended)
- **AI Agent** — Claude Code, Windsurf, Cursor, GH Copilot, or similar LLM-powered coding assistant integrated with your IDE

---

## Project Setup (Spider + Agents)

Add Spider to your repo, then initialize and generate agent proxy files.

```bash
# Option A: git submodule (recommended)
git submodule add https://github.com/cyberfabric/spider spider
git submodule update --init --recursive

# Option B: plain clone
git clone https://github.com/cyberfabric/spider spider
```

```bash
# Agent-safe invocation (recommended)
python3 spider/skills/spider/scripts/spider.py init
python3 spider/skills/spider/scripts/spider.py agents --agent windsurf
```

Supported agents: `windsurf`, `cursor`, `claude`, `copilot`.

If you update the Spider submodule later, re-run:

```bash
python3 spider/skills/spider/scripts/spider.py agents --agent windsurf
```

## **Spider SDLC** Overview

**Spider SDLC** is a production-ready software development life cycle (SDLC) SDD built on **Spider**. It fully leverages Spider’s capabilities — identifier-based **traceability**, reliable **workflows** that follow a strict protocol, and Weaver-defined rules and tasks, structured templates and quality checklists. Each Weaver can both generate (transform/derive) content and evaluate it: scoring semantic quality, validating artifact-to-artifact alignment (e.g., requirements → design → implementation), and enforcing structure against the templates defined in the weave.

See the [SDLC Pipeline](weavers/sdlc/README.md) for a detailed overview of the **Spider SDLC** pipeline, artifact kinds, generation and validation processes, and references to related documentation.

---

## Contributing

We welcome contributions to **Spider**.

**How to contribute**:

1. **Report issues**: Use GitHub Issues for bugs, feature requests, or questions
2. **Submit pull requests**: Fork the repository, create a branch, submit PR with description
3. **Follow** **Spider** **methodology**: Use **Spider** workflows when making changes to **Spider** itself
4. **Update documentation**: Include doc updates for any user-facing changes

**Guidelines**:
- Follow existing code style and conventions
- Update workflows with real-world examples when possible
- Maintain backward compatibility
- Document breaking changes in version history
- Add tests for new functionality

**Development setup**:
```bash
git clone <spider-repo-url>
cd spider
make test-coverage
make self-check
make validate
```