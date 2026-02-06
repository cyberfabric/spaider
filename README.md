# <img src="spaider.png" alt="Spaider" width="256" /> 
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.0-green.svg)]()
[![Status](https://img.shields.io/badge/status-active-brightgreen.svg)]()
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)]()

**Version**: 2.0 | **Status**: Active | **Language**: English

**Audience**: Prompt engineers, AI developers, software architects, engineering teams

<p align="center">
  <img src="spaider-cover.png" alt="Spaider Banner" width="100%" />
</p>

**Spaider** helps you build agentic systems that don’t drift.

It turns intent into a deterministic, reviewable pipeline of artifacts — prompts, templates, rules, checklists, specs, and code — so teams can ship agent-driven changes with confidence.

**What you get**
- **Less drift** — keep prompts, docs, and code aligned as the project evolves
- **More determinism** — validation gates reduce “LLM randomness” in outputs
- **End-to-end traceability** — link PRD → design → tasks → code for easier reviews
- **Reusable building blocks** — standardize workflows via curated domain packs

**How it works**
Spaider is extensible: you register thread packages called **Weavers**. A Weaver bundles templates, rules, checklists, and examples for a specific domain or use case.

Spaider ships with a built-in **SDLC Weaver** that runs a full PRD → code pipeline, with traceability and validation at every step.

---

## Table of Contents

- [](#)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Project Setup (Spaider + Agents)](#project-setup-spaider--agents)
  - [Using Spaider](#using-spaider)
    - [Real Conversation (Prompt Excerpt)](#real-conversation-prompt-excerpt)
      - [1) Enable Spaider mode](#1-enable-spaider-mode)
      - [2) Ask what Spaider can do](#2-ask-what-spaider-can-do)
      - [3) Ask what Spaider can generate](#3-ask-what-spaider-can-generate)
    - [Example Prompts](#example-prompts)
    - [Agent Skill](#agent-skill)
    - [Workflow Commands](#workflow-commands)
    - [Checklists and Quality Gates](#checklists-and-quality-gates)
  - [Weaver: **Spaider SDLC**](#weaver-spaider-sdlc)
  - [Contributing](#contributing)

---

## Prerequisites

Before using **Spaider**, ensure you have:

- **Python 3.8+** — Required for `spaider` tool execution
- **Git** — For version control and submodule installation (recommended)
- **AI Agent** — OpenAI Codex, Claude Code, Windsurf, Cursor, GH Copilot, or similar LLM-powered coding assistant integrated with your IDE

---

## Project Setup (Spaider + Agents)

Add Spaider to your repo, then initialize and generate agent proxy files.

```bash
# Option A: git submodule (recommended)
git submodule add https://github.com/cyberfabric/spaider spaider
git submodule update --init --recursive

# Option B: plain clone
git clone https://github.com/cyberfabric/spaider spaider
```

```bash
# Agent-safe invocation (recommended)
python3 spaider/skills/spaider/scripts/spaider.py init
python3 spaider/skills/spaider/scripts/spaider.py agents --agent windsurf
```

Supported agents: `windsurf`, `cursor`, `claude`, `copilot`, `openai`.

If you update the Spaider submodule later, re-run:

```bash
python3 spaider/skills/spaider/scripts/spaider.py agents --agent windsurf
```

## Using Spaider

To use Spaider, run your IDE with an AI agent (or run an agent in a terminal), and then start your requests with `spaider`.

That prefix switches the agent into Spaider mode: it loads the adapter + required rules, routes the request to the right workflow (analyze vs generate), and gates any file writes behind explicit confirmation.

### Real Conversation (Prompt Excerpt)

Below are a few real prompts from the story (with outcomes summarized). The full, screenshot-based conversation is in `guides/STORY.md`.

#### 1) Enable Spaider mode

Prompt: `spaider on`

![Enabling Spaider mode](images/intro-0000.png)

Outcome: The agent discovers the project adapter, loads required context deterministically, and prints a clear status block.

#### 2) Ask what Spaider can do

Prompt: `spaider how can you help me?`

![How Spaider can help](images/intro-0100.png)

Outcome: The agent explains the two workflows (read-only analyze vs write generate), gives example prompts, and asks for the minimum information needed to proceed.

#### 3) Ask what Spaider can generate

Prompt: `spaider what can I generate with you?`

![What Spaider can generate](images/intro-0200.png)

Outcome: The agent explains what “generate” can create/update (adapter context, architecture artifacts, or code), what it will not do blindly, and asks you to pick the target so it can start the right write workflow.

End result of the full story: A working example application (“Overwork Alert”) with CLI + daemon wiring, deterministic validations, unit tests, and a successful manual macOS smoke test.

[Continue reading the story](guides/STORY.md#part-2-analyze-vs-generate)

### Example Prompts

**Enable / Disable**

| Prompt | What the agent does |
|--------|---------------------|
| `spaider on` | Enables Spaider mode — discovers adapter, loads project context, shows available workflows |
| `spaider off` | Disables Spaider mode — returns to normal assistant behavior |

**Setup & Adapter Configuration**

| Prompt | What the agent does |
|--------|---------------------|
| `spaider configure adapter for Python monorepo with FastAPI` | Generates adapter with tech-stack specs, testing conventions, and codebase mappings |
| `spaider add src/api/ to tracked codebase` | Updates `artifacts.json` to include directory in traceability scanning |
| `spaider register SPEC at docs/specs/payments.md` | Adds artifact entry to `artifacts.json` with kind, path, and system mapping |
| `spaider add tech-stack spec for PostgreSQL + Redis` | Creates `specs/tech-stack.md` with database and caching conventions |
| `spaider update testing conventions` | Modifies `specs/testing.md` with project-specific test patterns |
| `spaider show adapter config` | Displays `artifacts.json` structure, registered artifacts, and codebase mappings |
| `spaider regenerate AGENTS.md` | Rebuilds navigation rules based on current artifact registry |

**Artifact Generation**

| Prompt | What the agent does |
|--------|---------------------|
| `spaider make PRD for user authentication system` | Generates PRD with actors, capabilities, requirements, flows, and constraints following the template |
| `spaider make DESIGN from PRD.md` | Transforms PRD into architecture design with components, interfaces, data models, and full traceability |
| `spaider decompose auth spec into tasks` | Creates DECOMPOSITION artifact breaking the spec into ordered, dependency-mapped implementation units |
| `spaider make SPEC spec for login flow` | Produces detailed spec design with acceptance criteria, edge cases, and code implementation instructions |

**Validation & Quality**

| Prompt | What the agent does |
|--------|---------------------|
| `spaider validate PRD.md` | Runs deterministic template validation + semantic quality scoring against PRD checklist (50+ criteria) |
| `spaider validate all` | Validates entire artifact hierarchy, checks cross-references, reports broken links and missing IDs |
| `spaider validate code for auth module` | Scans code for `@spaider-*` markers, verifies coverage against SPEC specs, reports unimplemented items |
| `spaider review DESIGN.md with consistency-checklist` | Performs multi-phase consistency analysis detecting contradictions and alignment issues |

**With Checklists (Deep Review)**

| Prompt | What the agent does |
|--------|---------------------|
| `spaider review PRD with PRD checklist, focus on requirements` | Applies 50+ expert criteria: completeness, testability, atomicity, no implementation leakage |
| `spaider review SPEC spec with code-checklist` | Checks implementation readiness: error handling, security, edge cases, testing strategy |
| `spaider validate codebase with reverse-engineering checklist` | Systematic code archaeology: identifies patterns, dependencies, undocumented behaviors |
| `spaider improve this prompt with prompt-engineering checklist` | Applies prompt design guidelines: clarity, constraints, examples, output format |

**Traceability & Search**

| Prompt | What the agent does |
|--------|---------------------|
| `spaider find requirements related to authentication` | Searches artifacts for IDs matching pattern, returns definitions and all references |
| `spaider trace REQ-AUTH-001` | Traces requirement through DESIGN → SPEC → code, shows implementation locations |
| `spaider list unimplemented specs` | Cross-references SPEC specs with code markers, reports items without `@spaider-*` tags |

**Code Review & Pull Requests**

| Prompt | What the agent does |
|--------|---------------------|
| `spaider review PR https://github.com/org/repo/pull/123` | Fetches PR diff, validates changes against design specs, checks traceability markers, reports coverage gaps |
| `spaider review PR #59` | Reviews local PR by number — checks code quality, design alignment, and Spaider marker consistency |
| `spaider review PR with code-checklist` | Deep PR review applying code quality criteria: error handling, security, edge cases, testing |
| `spaider analyze PR against SPEC spec` | Verifies PR implements all items from linked SPEC spec, reports missing or extra changes |
| `spaider check PR traceability` | Scans PR diff for `@spaider-*` markers, validates they reference existing design IDs |

**Weavers & Extensions**

| Prompt | What the agent does |
|--------|---------------------|
| `spaider make weaver for API documentation` | Scaffolds weaver directory with template, rules, checklist, and examples for custom artifact kind |
| `spaider register weaver at weavers/api-docs` | Adds weaver entry with format and path to artifact registry |
| `spaider add ENDPOINT kind to api-docs weaver` | Creates template structure for new artifact kind with markers and validation rules |
| `spaider show weaver SDLC` | Displays weaver directory layout, available artifact kinds, and their templates |
| `spaider analyze weavers` | Checks template marker pairing, frontmatter, and rule syntax across all weavers |

### Agent Skill

Spaider provides a single **Agent Skill** (`spaider`) following the [Agent Skills specification](https://agentskills.io/specification). The skill is defined in `skills/spaider/SKILL.md` and gets loaded into the agent's context when invoked.

The skill provides:
- Artifact validation and search capabilities
- ID lookup and traceability across documents and code
- Protocol guard for consistent context loading
- Integration with project adapter

When the skill is loaded, the agent gains access to Spaider's CLI commands and workflow triggers.

### Workflow Commands

For agents that don't support the Agent Skills specification, Spaider provides **workflow commands** — slash commands that load structured prompts guiding the agent through deterministic pipelines:

| Command | Workflow | Description |
|---------|----------|-------------|
| `/spaider` | — | Enable Spaider mode, discover adapter, show available workflows |
| `/spaider-generate` | `workflows/generate.md` | Create/update artifacts (PRD, DESIGN, DECOMPOSITION, ADR, SPEC) or implement code with traceability markers |
| `/spaider-analyze` | `workflows/analyze.md` | Validate artifacts against templates or code against design (deterministic + semantic) |
| `/spaider-adapter` | `workflows/adapter.md` | Create/update project adapter — scan structure, configure rules, generate `AGENTS.md` and `artifacts.json` |

Each workflow includes feedback loops, quality gates, and references to relevant checklists and rules.

### Checklists and Quality Gates

Spaider provides **expert-level checklists** for validation at each stage.

**Artifact checklists** in `weavers/sdlc/artifacts/{KIND}/`:
- [**PRD checklist**](weavers/sdlc/artifacts/PRD/checklist.md) — 300+ criteria for requirements completeness, stakeholder coverage, constraint clarity
- [**DESIGN checklist**](weavers/sdlc/artifacts/DESIGN/checklist.md) — 380+ criteria for architecture validation, component boundaries, integration points
- [**DECOMPOSITION checklist**](weavers/sdlc/artifacts/DECOMPOSITION/checklist.md) — 130+ criteria for spec breakdown quality, dependency mapping
- [**SPEC checklist**](weavers/sdlc/artifacts/SPEC/checklist.md) — 380+ criteria for implementation readiness, acceptance criteria, edge cases
- [**ADR checklist**](weavers/sdlc/artifacts/ADR/checklist.md) — 270+ criteria for decision rationale, alternatives analysis, consequences

**Generic checklists** in `requirements/`:
- [**Code checklist**](requirements/code-checklist.md) — 200+ criteria for code quality, security, error handling, testing
- [**Consistency checklist**](requirements/consistency-checklist.md) — 45+ criteria for cross-artifact consistency and contradiction detection
- [**Reverse engineering**](requirements/reverse-engineering.md) — 270+ criteria for legacy code analysis methodology
- [**Prompt engineering**](requirements/prompt-engineering.md) — 220+ criteria for AI prompt design guidelines

Use checklists by referencing them in `/spaider-analyze` or manually during review.

---

## Weaver: **Spaider SDLC**

**Spaider SDLC** is a production-ready software development life cycle (SDLC) SDD built on **Spaider**. It fully leverages Spaider’s capabilities — identifier-based **traceability**, reliable **workflows** that follow a strict protocol, and Weaver-defined rules and tasks, structured templates and quality checklists. Each Weaver can both generate (transform/derive) content and evaluate it: scoring semantic quality, validating artifact-to-artifact alignment (e.g., requirements → design → implementation), and enforcing structure against the templates defined in the weaver.

See the [SDLC Pipeline](weavers/sdlc/README.md) for a detailed overview of the **Spaider SDLC** pipeline, artifact kinds, generation and validation processes, and references to related documentation.

---

## Contributing

We welcome contributions to **Spaider**.

**How to contribute**:

1. **Report issues**: Use GitHub Issues for bugs, spec requests, or questions
2. **Submit pull requests**: Fork the repository, create a branch, submit PR with description
3. **Follow** **Spaider** **methodology**: Use **Spaider** workflows when making changes to **Spaider** itself
4. **Update documentation**: Include doc updates for any user-facing changes

**Guidelines**:
- Follow existing code style and conventions
- Update workflows with real-world examples when possible
- Maintain backward compatibility
- Document breaking changes in version history
- Add tests for new functionality

**Development setup**:
```bash
git clone <spaider-repo-url>
cd spaider
make test-coverage
make self-check
make validate
```
