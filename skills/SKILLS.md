# Skills System Specification

**Version**: 1.0  
**Purpose**: Define how agents discover, select, and use Claude-compatible skills in this repository  
**Scope**: All agent work in this repository (all FDD workflows and non-FDD tasks)

---

## Core Rules

**MUST**:
- Treat every directory under `skills/` (except this file) as an Agent Skills skill.
- Require each skill directory to contain `SKILL.md` with valid YAML frontmatter.
- Use progressive disclosure:
  - Read only `name` + `description` for discovery.
  - Read SKILL.md body only after selecting a skill.
  - Read `references/` files only when explicitly needed.

**MUST NOT**:
- Load multiple full SKILL bodies into context during discovery.
- Invent skill behavior that is not defined in the skill’s `SKILL.md`.

---

## Toolchain Preflight (MANDATORY)

**Before doing any work that relies on skill scripts, agent MUST verify**:
- `python` OR `python3` is available and runnable

**Minimum checks**:
- `python --version` OR `python3 --version`

**If ANY tool is missing**:
- STOP.
- Do NOT proceed with the workflow/task.
- Propose an installation approach.
- The agent chooses how to install (method is not prescribed here).
- The user must approve any commands that modify the system.

---

## Skill Discovery Protocol (MANDATORY)

When executing an FDD workflow, agent MUST follow `requirements/execution-protocol.md` for workflow-driven skill usage.

### Step 1: Enumerate skills

Agent MUST enumerate candidate skills by locating:
- `skills/*/SKILL.md`

Agent MUST ignore:
- `skills/SKILLS.md`

### Step 2: Read metadata only

Agent MUST read only the YAML frontmatter for each candidate:
- `name`
- `description`

Agent MUST use `description` keywords to match the current task.

### Step 3: Select skill(s)

Agent MUST:
- Select 1 primary skill.
- Optionally select up to 2 supporting skills if composition is required.

Agent MUST prefer skills that:
- Mention the user’s artifacts (FDD, DESIGN.md, CHANGES.md, FEATURES.md)
- Mention the user’s required operations (validate, generate, search, edit)
- Declare compatibility constraints that match the environment

### Step 4: Activate

After selecting a skill, agent MUST:
- Open the selected skill’s `SKILL.md` body
- Follow its instructions exactly

If the skill references files under:
- `references/` → open only the referenced file(s)
- `scripts/` → run only as instructed by the skill
- `assets/` → use only as instructed by the skill

---

## Adding a New Skill (Repository Policy)

A new skill directory under `skills/` MUST:
- Contain `SKILL.md`
- Use a `name` that matches the directory name
- Keep SKILL.md body concise and use `references/` for detailed material

If a skill contains `scripts/`, it MUST:
- Contain `tests/` with unit tests for the scripts
- Use Python standard library `unittest` (no external test dependencies)
- Be deterministic (no network access, no time-based assertions, no random data)
- Avoid modifying repository state (use temporary files/directories for test artifacts)
- Cover both PASS and FAIL cases for every supported artifact kind/branch in the script

To run tests:
- `python3 -m unittest discover -s guidelines/FDD/skills/<skill>/tests -p 'test_*.py'`

---

## References

- Agent Skills specification: https://agentskills.io/specification
- Anthropic reference skills: https://github.com/anthropics/skills
