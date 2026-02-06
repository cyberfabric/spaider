# Spaider AI Agent Navigation

**Version**: 1.1

---

## ⚠️ MUST Instruction Semantics ⚠️

**MUST** = **MANDATORY**. NOT optional. NOT recommended. NOT suggested.

**ALWAYS** = **MANDATORY**. Equivalent to MUST. Used for action-gated instructions.

**If you skip ANY MUST instruction**:
- 🚫 Your execution is **INVALID**
- 🚫 Output must be **DISCARDED**
- 🚫 You are **NOT following Spaider**

**One skipped MUST = entire workflow FAILED**

**All MUST instructions are CRITICAL without exception.**

## ⚠️ SCOPE LIMITATION (OPT-IN) ⚠️

**MUST** treat Spaider as opt-in.

**MUST NOT** apply Spaider navigation rules unless the user explicitly enables Spaider.

Spaider is considered disabled ONLY when at least one is true:
- User explicitly requests disabling Spaider (for example: `/spaider off`)

Spaider disable MUST take precedence over Spaider enable.

Spaider is considered enabled ONLY when at least one is true:
- User explicitly asks to use Spaider (mentions `spaider` or `Spaider`) and confirms intent
- User explicitly requests executing an Spaider workflow (for example: `spaider analyze`, `spaider generate`, `spaider rules`, `spaider adapter`)
- User explicitly requests the `spaider` entrypoint workflow (`/spaider`)

**If Spaider intent is unclear** (user mentions "spaider" but doesn't explicitly request workflow):
- Ask for clarification: "Would you like to enable Spaider mode?"
- Do NOT assume enabled without confirmation
- Continue as normal assistant until confirmed

If Spaider is disabled OR NOT enabled:
- **MUST** ignore the rest of this file
- **MUST** behave as a normal coding assistant


---

## Agent Acknowledgment

**Before proceeding with ANY Spaider work, confirm you understand**:

- [ ] MUST = MANDATORY, not optional
- [ ] Skipping ANY MUST instruction = INVALID execution
- [ ] INVALID execution = output must be DISCARDED
- [ ] I will read ALL required files BEFORE proceeding
- [ ] I will follow workflows step-by-step WITHOUT shortcuts
- [ ] I will NOT create files without user confirmation (operation workflows)
- [ ] I will end EVERY response with a list of Spaider files read while producing the response, why each file was read, and which initial instruction triggered opening each file

**By proceeding with Spaider work, I acknowledge and accept these requirements.**

---

## Variables

**While Spaider is enabled**, remember these variables:

| Variable | Value | Description |
|----------|-------|-------------|
| `{spaider_path}` | Directory containing this AGENTS.md | Project root for Spaider navigation |
| `{spaider_mode}` | `on` or `off` | Current Spaider mode state |

**Setting `{spaider_mode}`**:
- Explicit command: `spaider on` / `spaider off`
- Spaider prompts that activate/deactivate Spaider workflows

Use `{spaider_path}` as the base path for all relative Spaider file references.

---

## Navigation Rules

ALWAYS open and follow `requirements/extension.md` WHEN you see **Extends**: {file}

ALWAYS open and follow `{adapter-directory}/AGENTS.md` WHEN starting any Spaider work

ALWAYS open and follow `skills/spaider/SKILL.md` WHEN you see `spaider` in the prompt

## Skill registration

<available_skills>
  <skill>
    <name>spaider</name>
    <description>Framework for Documentation and Development - AI agent toolkit. Use when user works with PRD, DESIGN, DECOMPOSITION, ADR, spec specs, architecture documentation, requirements, or mentions Spaider/workflow/artifact/adapter/traceability. Provides structured artifact templates, validation, design-to-code traceability, and guided code implementation with traceability markers. Opt-in - suggest enabling when design/architecture activities detected.</description>
    <location>skills/spaider/SKILL.md</location>
  </skill>
</available_skills>

### Dependency Error Handling

**If referenced file not found**:
- Log warning to user: "Spaider dependency not found: {path}"
- Continue with available files — do NOT fail silently
- If critical dependency missing (SKILL.md, workflow), inform user and suggest `/spaider` to reinitialize

---

## Execution Logging

ALWAYS provide execution visibility WHEN Spaider is enabled.

ALWAYS notify the user WHEN entering a major section (H2 heading `##`) of any Spaider prompt (workflow, rules, requirements).

ALWAYS notify the user WHEN completing a checklist task (a Markdown task line starting with `- [ ]`).

ALWAYS use this notification format WHEN emitting execution logs:

```
📟 [CONTEXT]: MESSAGE
```

ALWAYS set **CONTEXT** to the file or section being executed WHEN emitting execution logs (e.g., `workflows/generate.md`, `DESIGN rules`, `execution-protocol`).

ALWAYS set **MESSAGE** to what Spaider is doing and why WHEN emitting execution logs.

ALWAYS ensure execution logging supports these goals WHEN Spaider is enabled:
- Help the user understand which Spaider prompts are being followed
- Help the user track decision points and branching logic
- Help the user debug unexpected behavior
- Help the user learn the Spaider workflow

ALWAYS consider these examples as valid execution logs WHEN Spaider is enabled:

```
📟 [execution-protocol]: Entering "Load Rules" — target is CODE, loading codebase/rules.md
📟 [DESIGN rules]: Completing "Validate structure" — all required sections present
📟 [workflows/generate.md]: Entering "Determine Target" — user requested code implementation
```