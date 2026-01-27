---
fdd: true
type: workflow
name: Design Validate
version: 1.0
purpose: Validate overall design document
---

# Validate Overall Design

**Type**: Validation  
**Role**: Architect, Product Manager (for PRD alignment)  
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
- [ ] ✅ Open and follow `../requirements/overall-design-structure.md` (This workflow's requirements)
- [ ] ✅ Check adapter initialization (FDD-Adapter/AGENTS.md exists)
- [ ] ✅ Validate all prerequisites from Prerequisites section below

**Self-Check**:
- [ ] ✅ I have read ALL files listed above
- [ ] ✅ I understand "Maximum Attention to Detail" requirement
- [ ] ✅ I am ready to check EVERY validation criterion individually
- [ ] ✅ I will run grep searches for systematic verification
- [ ] ✅ I will complete self-test before reporting results

**⚠️ If ANY checkbox is unchecked → STOP and read missing files first**

---

## Requirements

**ALWAYS open and follow**: `../requirements/overall-design-structure.md`

Extract:
- Required sections structure
- Validation criteria (100 points breakdown)
- Pass threshold (≥90/100)

---

## Prerequisites

**MUST validate**:
- [ ] DESIGN artifact exists - validate: Check file at DESIGN path from `{adapter-dir}/artifacts.json` (default: `architecture/DESIGN.md`)
- [ ] PRD artifact exists - validate: Check file at PRD path from `{adapter-dir}/artifacts.json` (default: `architecture/PRD.md`)
- [ ] PRD.md validated - validate: Score ≥90/100

**If missing**: Ask the user whether to:
- Create/validate prerequisites via the corresponding workflows
- Provide inputs in another form (path, link, or pasted text in any format)
- Proceed anyway (reduce scope to content-only checks and report missing cross-references)

---

## Steps

### 1. Run Deterministic Gate (FDD Structure + IDs)

Run `fdd validate` for the DESIGN artifact.

If the artifact is registered in `{adapter-dir}/artifacts.json` and `format: FDD`, this gate performs structural validation.

If the artifact is not registered or registered with a non-FDD format, the gate is expected to return `PASS` with `skipped: true`.

If the output includes `skipped: true`, do NOT execute Step 3 (FDD-format-only scoring). Report `Status: SKIPPED` for structural validation and continue to Step 6 (Semantic Expert Review) as a content-only review.

**Meaning**: This DESIGN is not a registered `format: FDD` artifact, so structure/ID validation MUST NOT be executed by this workflow.

**Fix**: Register the DESIGN in `{adapter-dir}/artifacts.json` with `format: FDD`, then re-run `design-validate`.

### 2. Read Dependencies

Open the PRD artifact (path resolved via `{adapter-dir}/artifacts.json`; default: `architecture/PRD.md`)

Extract:
- All actor IDs
- All use case IDs
- Vision statement

### 3. Execute Validation (FDD Format Only)

ONLY execute this step if Step 1 did NOT return `skipped: true`. If Step 1 returned `skipped: true`, skip to Step 6.

Follow validation criteria from `overall-design-structure.md`:
- Structure: Required sections/subsections present, correct order
- Completeness: No placeholders, required ID payload blocks present
- Cross-References: All referenced actor/use case/ADR IDs exist
- Domain Model & API Contracts: Links/locations present as required

Calculate total score

### 4. Output Results to Chat

**Format**:
```markdown
## Validation Report: DESIGN.md

### Summary
- **Status**: **PASS** ✅ | **FAIL** ❌
- **Score**: **{X}/100**
- **Threshold**: **≥90/100**

---

### Findings

#### 1) Structure — **{X}/20**
- ✅ | ❌ {item}

#### 2) Completeness — **{X}/25**
- ✅ | ❌ {item}

#### 3) Cross-References — **{X}/{points}**
- ✅ | ❌ {item}

#### 4) Domain Model & API Contracts — **{X}/{points}**
- ✅ | ❌ {item}

---

### Recommendations

#### High Priority
1. **{Fix}**

---

### Next Steps

- **If PASS**: ✅ Run `adr-validate`, then proceed to `features`
- **If FAIL**: ❌ Fix issues above, then re-run `design-validate`
```

### 5. Validate ADR directory (If DESIGN.md passed)

**If DESIGN.md validation score ≥90**:
- Check if ADR directory from `{adapter-dir}/artifacts.json` exists (default: `architecture/ADR/`)
- If exists: Run `adr-validate` workflow
- If missing: Suggest running `adr` workflow first

**Output**:
```markdown
---
 
## ADR Validation
 
{If ADR directory exists}: Running adr-validate...
{If ADR directory missing}: ⚠️ ADR directory not found (default: `architecture/ADR/`). Run `adr` workflow to create Architecture Decision Records.
```

### 6. Semantic Expert Review (Always)

Run an expert panel review of the DESIGN content after producing the validation output.

**Critical requirement**: This step MUST produce an explicit section in chat titled `### Semantic Expert Review` that confirms the review was executed.

**Experts**:
- Architect
- Database Architect
- Performance Engineer
- Security Expert
- QA Engineer
- Developer
- DCO Engineer
- DevOps Engineer
- Monitoring Engineer

**Instructions (MANDATORY)**:
- [ ] Execute this checklist for EACH expert listed above (do not skip any expert)
- [ ] Adopt the role of the current expert (write: `Role assumed: {expert}`)
- [ ] Review the entire artifact content (not only headings)
- [ ] Enforce semantic boundaries:
  - [ ] PRD answers **WHAT**, overall design answers **HOW**
  - [ ] ADR decisions MUST NOT be rewritten as normative requirements in DESIGN.md
  - [ ] Feature-level details MUST NOT dominate overall design
- [ ] Identify issues (list each item explicitly):
  - [ ] Contradictions
  - [ ] Missing information
  - [ ] Unclear/ambiguous statements
  - [ ] Misplaced content (belongs in PRD/ADR/feature designs)
- [ ] Provide concrete proposals:
  - [ ] What to remove (quote the exact fragment)
  - [ ] What to add (provide the missing content)
  - [ ] What to rewrite (provide suggested phrasing)
- [ ] Propose the corrective workflow: `design` (UPDATE mode)

**Required output format** (append to chat):
```markdown
### Semantic Expert Review

**Review status**: **COMPLETED** ✅  
**Reviewed artifact**: `DESIGN.md`  
**Experts reviewed**: *Architect, Database Architect, Performance Engineer, Security Expert, QA Engineer, Developer, DCO Engineer, DevOps Engineer, Monitoring Engineer*

*Rule*: For EACH expert listed in the workflow, include a `#### Expert: {expert}` section below. Do not omit any expert.

#### Expert: {expert}
- **Role assumed**: {expert}
- **Checklist completed**: **YES** ✅
- **Findings**:
  - **Contradictions**: ...
  - **Missing information**: ...
  - **Unclear statements**: ...
  - **Misplaced content**: ...
- **Proposed edits**:
  - **Remove**: "..." → **Reason**: ...
  - **Add**: ...
  - **Rewrite**: "..." → "..."

*Repeat the `#### Expert: {expert}` block for each expert above.*

---
 
**Recommended corrective workflow**: `design` *(UPDATE mode)*
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

**If DESIGN.md PASS and ADR PASS**: `features` workflow

**If DESIGN.md PASS but ADR directory missing**: `adr` workflow to create ADRs

**If DESIGN.md FAIL**: Fix DESIGN.md, re-validate
