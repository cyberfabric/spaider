# Cypilot AI Agent Navigation

**Version**: 1.1

---

## Variables

**While Cypilot is enabled**, remember these variables:

| Variable | Value | Description |
|----------|-------|-------------|
| `{cypilot_path}` | Directory containing this AGENTS.md | Project root for Cypilot navigation |
| `{cypilot_mode}` | `on` or `off` | Current Cypilot mode state |

**Setting `{cypilot_mode}`**:
- Explicit command: `cypilot on` / `cypilot off`
- Cypilot prompts that activate/deactivate Cypilot workflows

Use `{cypilot_path}` as the base path for all relative Cypilot file references.

---

## Navigation Rules

ALWAYS open and follow `{cypilot_path}/requirements/extension.md` WHEN you see **Extends**: {file}

ALWAYS open and follow `{adapter-directory}/AGENTS.md` WHEN starting any Cypilot work

### Dependency Error Handling

**If referenced file not found**:
- Log warning to user: "Cypilot dependency not found: {path}"
- Continue with available files — do NOT fail silently
- If critical dependency missing (SKILL.md, workflow), inform user and suggest `/cypilot` to reinitialize
