---
fdd: true
type: workflow
name: ADR Validate
version: 1.0
purpose: Validate Architecture Decision Records document
---

# Validate Architecture Decision Records

**Type**: Validation  
**Role**: Architect  
**Artifact**: Validation report (output to chat)

---

## Prerequisite Checklist

- [ ] Agent has read execution-protocol.md
- [ ] Agent has read workflow-execution.md
- [ ] Agent understands this workflow's purpose

---

## Overview

This workflow guides the execution of the specified task.

---

ALWAYS open and follow `../requirements/workflow-execution.md` WHEN executing this workflow

## ⚠️ PRE-FLIGHT CHECKLIST (ALWAYS Complete Before Proceeding)

**Agent ALWAYS verifies before starting this workflow**:

**Navigation Rules Compliance**:
- [ ] ✅ Open and follow `../requirements/execution-protocol.md` (MANDATORY BASE)
- [ ] ✅ Open and follow `../requirements/workflow-execution.md` (General execution)
- [ ] ✅ Open and follow `../requirements/workflow-execution-validations.md` (Validation specifics)

**Workflow-Specific Requirements**:
- [ ] ✅ Open and follow `../requirements/adr-structure.md` (This workflow's requirements)
- [ ] ✅ Check adapter initialization (FDD-Adapter/AGENTS.md exists)
- [ ] ✅ Validate all prerequisites from Prerequisites section below

**Self-Check**:
- [ ] ✅ I have read ALL files listed above
- [ ] ✅ I understand "Maximum Attention to Detail" requirement
- [ ] ✅ I am ready to check EVERY validation criterion individually
- [ ] ✅ I will verify `**ADR ID**:` field in EACH ADR header
- [ ] ✅ I will run grep searches for systematic verification
- [ ] ✅ I will complete self-test before reporting results

**⚠️ If ANY checkbox is unchecked → STOP and read missing files first**

---

## Requirements

**ALWAYS open and follow**: `../requirements/adr-structure.md`

Extract:
- MADR format requirements
- FDD extensions (Related Design Elements)
- ADR numbering rules
- Validation criteria (100 points breakdown)
- Pass threshold (≥90/100)

---

## Prerequisites

**MUST validate**:
- [ ] ADR directory exists - validate: Check ADR directory from `{adapter-dir}/artifacts.json` (default: `architecture/ADR/`)
- [ ] DESIGN artifact exists - validate: Check file at DESIGN path from `{adapter-dir}/artifacts.json` (default: `architecture/DESIGN.md`)
- [ ] PRD artifact exists - validate: Check file at PRD path from `{adapter-dir}/artifacts.json` (default: `architecture/PRD.md`)

**If missing**: Ask the user whether to:
- Create/validate prerequisites via the corresponding workflows
- Provide inputs in another form (path, link, or pasted text in any format)
- Proceed anyway (reduce scope to content-only checks and report missing cross-references)

---

## Steps

### 1. Run Deterministic Gate (FDD Structure + IDs)

Run `fdd validate` for the ADR directory.

If the ADR artifact is registered in `{adapter-dir}/artifacts.json` and `format: FDD`, this gate performs structural validation.

If the ADR artifact is not registered or registered with a non-FDD format, the gate is expected to return `PASS` with `skipped: true`.

If the output includes `skipped: true`, do NOT execute Step 3 (FDD-format-only scoring). Report `Status: SKIPPED` for structural validation and continue to Step 5 (Semantic Expert Review) as a content-only review.

**Meaning**: This ADR artifact is not a registered `format: FDD` artifact, so structure/ID validation MUST NOT be executed by this workflow.

**Fix**: Register the ADR artifact in `{adapter-dir}/artifacts.json` with `format: FDD`, then re-run `adr-validate`.

### 2. Read Dependencies

Open the PRD and DESIGN artifacts (paths resolved via `{adapter-dir}/artifacts.json`; defaults: `architecture/PRD.md`, `architecture/DESIGN.md`)

Extract:
- All actor IDs (from PRD.md Section B)
- All capability IDs (from PRD.md Section C)
- All requirement IDs (from DESIGN.md Section B)
- All principle IDs (from DESIGN.md Section B)

### 3. Execute Validation (FDD Format Only)

ONLY execute this step if Step 1 did NOT return `skipped: true`. If Step 1 returned `skipped: true`, skip to Step 5.

Follow validation criteria from `adr-structure.md`:
- File Structure (15 pts): ADR directory exists, ADR-0001 exists
- ADR Numbering (15 pts): Sequential, no gaps, proper format (ADR-NNNN)
- Required Sections (30 pts): Context, Drivers, Options, Outcome, Related Elements
- Content Quality (25 pts): Clear context, ≥2 options, rationale, consequences
- FDD Integration (15 pts): Related Design Elements with valid IDs

Calculate total score

### 4. Output Results to Chat

**Format**:
```markdown
## Validation Report: ADR/

### Summary
- **Status**: **PASS** ✅ | **FAIL** ❌
- **Score**: **{X}/100**
- **Threshold**: **≥90/100**

---

### Findings

#### 1) File Structure — **{X}/15**
- ✅ | ❌ {item}

#### 2) ADR Numbering — **{X}/15**
- ✅ | ❌ {item}

#### 3) Required Sections — **{X}/30**
- ✅ | ❌ {item}

#### 4) Content Quality — **{X}/25**
- ✅ | ❌ {item}

#### 5) FDD Integration — **{X}/15**
- ✅ | ❌ {item}

---

### Recommendations

#### High Priority
1. **{Fix}**

---

### Next Steps

- **If PASS**: ✅ ADRs validated, proceed with feature development
- **If FAIL**: ❌ Fix issues above, then re-run `adr-validate`
```

### 5. Semantic Expert Review (Always)

Run an expert panel review of ADR content after producing the validation output.

**Critical requirement**: This step MUST produce an explicit section in chat titled `### Semantic Expert Review` that confirms the review was executed.

**Experts**:
- Architect
- Security Expert
- Developer
- Performance Expert
- QA Expert

**Instructions (MANDATORY)**:
- [ ] Execute this checklist for EACH expert listed above (do not skip any expert)
- [ ] Adopt the role of the current expert (write: `Role assumed: {expert}`)
- [ ] Review the entire ADR set (read each ADR file, not only filenames)
- [ ] Enforce semantic boundaries:
  - [ ] ADRs record decisions and rationale, not broad system design
  - [ ] Each ADR MUST include alternatives and consequences
  - [ ] ADRs MUST NOT restate PRD requirements as decisions
- [ ] Identify issues (list each item explicitly):
  - [ ] Contradictions between ADRs and DESIGN/PRD
  - [ ] Missing decision rationale
  - [ ] Missing alternatives
  - [ ] Missing consequences
  - [ ] Misplaced content (belongs in DESIGN)
- [ ] Provide concrete proposals:
  - [ ] What to remove (quote the exact fragment)
  - [ ] What to add (provide the missing content)
  - [ ] What to rewrite (provide suggested phrasing)
- [ ] Propose the corrective workflow: `adr` (UPDATE mode)

**Required output format** (append to chat):
```markdown
### Semantic Expert Review

**Review status**: **COMPLETED** ✅  
**Reviewed artifact**: `ADR/`  
**Experts reviewed**: *Architect, Security Expert, Developer*

*Rule*: For EACH expert listed in the workflow, include a `#### Expert: {expert}` section below. Do not omit any expert.

#### Expert: {expert}
- **Role assumed**: {expert}
- **Checklist completed**: **YES** ✅
- **Findings**:
  - **Contradictions**: ...
  - **Missing decision rationale**: ...
  - **Missing alternatives**: ...
  - **Missing consequences**: ...
  - **Misplaced content**: ...
- **Proposed edits**:
  - **Remove**: "..." → **Reason**: ...
  - **Add**: ...
  - **Rewrite**: "..." → "..."

*Repeat the `#### Expert: {expert}` block for each expert above.*

---
 
**Recommended corrective workflow**: `adr` *(UPDATE mode)*
```

---

## Validation

Self-validating workflow

---

## Validation Criteria

- [ ] All workflow steps completed
- [ ] Output artifacts are valid

---

## Validation Checklist

- [ ] All prerequisites were met
- [ ] All steps were executed in order

---

## Next Steps

**If PASS**: ADRs validated, architecture documentation complete

**If FAIL**: Fix ADR files under ADR/, re-validate
