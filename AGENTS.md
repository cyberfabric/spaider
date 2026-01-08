# FDD AI Agent Navigation

**Version**: 1.0

---

## ⚠️ MUST Instruction Semantics ⚠️

**MUST** = **MANDATORY**. NOT optional. NOT recommended. NOT suggested.

**If you skip ANY MUST instruction**:
- 🚫 Your execution is **INVALID**
- 🚫 Output must be **DISCARDED**
- 🚫 You are **NOT following FDD**

**One skipped MUST = entire workflow FAILED**

**All MUST instructions are CRITICAL without exception.**

---

## Agent Acknowledgment

**Before proceeding with ANY FDD work, confirm you understand**:

- [ ] MUST = MANDATORY, not optional
- [ ] Skipping ANY MUST instruction = INVALID execution
- [ ] INVALID execution = output must be DISCARDED
- [ ] I will read ALL required files BEFORE proceeding
- [ ] I will follow workflows step-by-step WITHOUT shortcuts
- [ ] I will NOT create files without user confirmation (operation workflows)

**By proceeding with FDD work, I acknowledge and accept these requirements.**

---

## Navigation Rules

MUST check for relevant workflow in `workflows/` directory WHEN receiving any task request

MUST read `requirements/extension.md` WHEN you see **Extends**: {file}

MUST read `requirements/core.md` WHEN modifying any FDD core files

MUST read `{adapter-directory}/FDD-Adapter/AGENTS.md` WHEN starting any FDD work

MUST read `requirements/FDL.md` WHEN you see FDL

MUST read `requirements/workflow-selection.md` WHEN selecting which workflow to execute

MUST read `requirements/execution-protocol.md` WHEN executing any workflow (FIRST)

MUST read `requirements/workflow-execution.md` WHEN executing any workflow

MUST read `requirements/core-workflows.md` WHEN creating or modifying workflow files

MUST read `requirements/core-requirements.md` WHEN creating or modifying requirements files

MUST read `requirements/core-agents.md` WHEN creating or modifying AGENTS.md files

MUST read `requirements/business-context-structure.md` WHEN working with BUSINESS.md

MUST read `requirements/overall-design-structure.md` WHEN working with DESIGN.md

MUST read `requirements/adr-structure.md` WHEN working with ADR.md

MUST read `requirements/features-manifest-structure.md` WHEN working with FEATURES.md

MUST read `requirements/feature-design-structure.md` WHEN working with feature DESIGN.md

MUST read `requirements/feature-changes-structure.md` WHEN working with feature CHANGES.md

MUST read `requirements/adapter-structure.md` WHEN creating or configuring FDD adapter

---

## ⚠️ Execution Protocol Violations

**If agent skips execution-protocol.md**:
- Workflow execution is AUTOMATICALLY INVALID
- All output must be DISCARDED
- User should point out violation
- Agent must restart with protocol compliance

**Common protocol violations**:
1. ❌ **Not reading execution-protocol.md** before starting workflow
2. ❌ **Not reading workflow-execution.md** before executing workflow
3. ❌ **Not reading workflow-execution-validations.md** for validation workflows
4. ❌ **Not completing pre-flight checklist** in workflow files
5. ❌ **Not running self-test** before reporting validation results
6. ❌ **Not checking EVERY validation criterion individually**
7. ❌ **Not using grep for systematic verification**
8. ❌ **Not cross-referencing EVERY ID**

**One violation = entire workflow execution FAILED**

**Agent responsibility**:
- Follow execution-protocol.md for EVERY workflow
- Complete all checklist items
- Run self-test before reporting
- Include protocol compliance report in output
- Self-identify violations if discovered

**User responsibility**:
- Point out violations when detected
- Request protocol compliance report
- Ask agent to restart with full compliance

**Recovery from violation**:
1. Acknowledge the violation
2. Identify what was skipped
3. Explain why (honest answer)
4. Discard invalid output
5. Restart workflow with full protocol compliance
6. Show protocol compliance report in new output