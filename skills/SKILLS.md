# Skills System Specification

**Version**: 1.1  
**Purpose**: Define how agents discover, select, and use Claude-compatible skills in this repository  
**Scope**: All agent work in this repository (all FDD workflows and non-FDD tasks)

**Path base**: All paths in this document are relative to the FDD repository root (the directory containing `AGENTS.md`).

**How to locate the path base in a monorepo**: The FDD repository root is the directory that contains `AGENTS.md` and is the parent directory of `skills/` (this file is `skills/SKILLS.md`).

**Skill root directory**: `skills/`

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
- Enumerate skills from any other repository root (e.g., monorepo root) instead of the path base defined above.

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

 Agent MUST apply Skill Discovery Protocol for:
 - FDD workflow execution (per `requirements/execution-protocol.md`)
 - Non-workflow requests involving FDD artifacts or FDD ID traceability

 Non-workflow requests that trigger Skill Discovery include:
 - Reading/searching/editing FDD artifacts (BUSINESS.md, DESIGN.md, ADR.md, FEATURES.md, feature DESIGN.md, feature CHANGES.md)
 - Answering questions like "where is {id} defined" / "where is {id} used" (FDD IDs, ADR IDs, qualified IDs)

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

### Skill Selection Report (MANDATORY)

Before proceeding with any task work (including non-skill tooling), agent MUST output a Skill Selection Report that includes:
- `trigger`: which Skill Discovery trigger matched
- `candidates`: list of candidate skill `name` values with a brief selection rationale based on `description` keywords
- `primary`: selected primary skill `name`
- `supporting`: optional list of supporting skill `name` values (max 2)

The report MUST be based only on SKILL YAML frontmatter (`name`, `description`).

If agent cannot select a primary skill:
- STOP.
- Do NOT proceed with ad-hoc approaches.
- Ask the user to fix skill navigation (add a missing skill, or improve skill `description` keywords / discovery triggers).

### Step 4: Activate

After selecting a skill, agent MUST:
- Open the selected skill’s `SKILL.md` body
- Follow its instructions exactly

### Skill Lock (MANDATORY)

Once the agent outputs the Skill Selection Report and selects a `primary` skill, the agent MUST enter **Skill Lock**.

While in Skill Lock, the agent MUST NOT do any task work (including any non-skill tooling) until the primary skill is activated and followed.

**Allowed actions while in Skill Lock**:
- Open and read the selected primary skill `SKILL.md` body.
- Perform the `Toolchain Preflight` checks required by `skills/SKILLS.md` and/or the selected skill.
- Ask only the minimum clarifying question(s) required to execute the selected skill.

**Forbidden actions while in Skill Lock**:
- Running ad-hoc searches (e.g. grep/ripgrep-style searches) when the skill provides an authoritative command.
- Using generic repo tooling to perform the task when the selected skill defines how to perform it.

**Violation handling**:
- If the agent performs any forbidden action while in Skill Lock, the agent MUST declare the output invalid, discard it, and restart from `Skill Discovery Protocol` Step 1.

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
