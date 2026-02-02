# Spider AI Agent Navigation

**Version**: 1.1

---

## ⚠️ SCOPE LIMITATION (OPT-IN) ⚠️

**MUST** treat Spider as opt-in.

**MUST NOT** apply Spider navigation rules unless the user explicitly enables Spider.

Spider is considered disabled ONLY when at least one is true:
- User explicitly requests disabling Spider (for example: `/spider off`)

Spider disable MUST take precedence over Spider enable.

Spider is considered enabled ONLY when at least one is true:
- User explicitly asks to use Spider (mentions `spider` or `Spider`) and confirms intent
- User explicitly requests executing an Spider workflow (for example: `spider validate`, `spider generate`, `spider rules`, `spider adapter`)
- User explicitly requests the `spider` entrypoint workflow (`/spider`)

**If Spider intent is unclear** (user mentions "spider" but doesn't explicitly request workflow):
- Ask for clarification: "Would you like to enable Spider mode?"
- Do NOT assume enabled without confirmation
- Continue as normal assistant until confirmed

If Spider is disabled OR NOT enabled:
- **MUST** ignore the rest of this file
- **MUST** behave as a normal coding assistant

## ⚠️ MUST Instruction Semantics ⚠️

**MUST** = **MANDATORY**. NOT optional. NOT recommended. NOT suggested.

**ALWAYS** = **MANDATORY**. Equivalent to MUST. Used for action-gated instructions.

**If you skip ANY MUST instruction**:
- 🚫 Your execution is **INVALID**
- 🚫 Output must be **DISCARDED**
- 🚫 You are **NOT following Spider**

**One skipped MUST = entire workflow FAILED**

**All MUST instructions are CRITICAL without exception.**

---

## Agent Acknowledgment

**Before proceeding with ANY Spider work, confirm you understand**:

- [ ] MUST = MANDATORY, not optional
- [ ] Skipping ANY MUST instruction = INVALID execution
- [ ] INVALID execution = output must be DISCARDED
- [ ] I will read ALL required files BEFORE proceeding
- [ ] I will follow workflows step-by-step WITHOUT shortcuts
- [ ] I will NOT create files without user confirmation (operation workflows)
- [ ] I will end EVERY response with a list of Spider files read while producing the response, why each file was read, and which initial instruction triggered opening each file

**By proceeding with Spider work, I acknowledge and accept these requirements.**

---

## Navigation Rules

ALWAYS open and follow `requirements/extension.md` WHEN you see **Extends**: {file}

ALWAYS open and follow `{adapter-directory}/AGENTS.md` WHEN starting any Spider work

ALWAYS open and follow `skills/spider/SKILL.md` WHEN you see `spider` in the prompt

### Dependency Error Handling

**If referenced file not found**:
- Log warning to user: "Spider dependency not found: {path}"
- Continue with available files — do NOT fail silently
- If critical dependency missing (SKILL.md, workflow), inform user and suggest `/spider` to reinitialize