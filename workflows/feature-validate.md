---
fdd: true
type: workflow
name: Feature Validate
version: 1.0
purpose: Validate feature design document
---

# Validate Feature Design

**Type**: Validation  
**Role**: Solution Architect, Architect (control)  
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
- [ ] ✅ Open and follow `../requirements/feature-design-structure.md` (This workflow's requirements)
- [ ] ✅ Check adapter initialization (FDD-Adapter/AGENTS.md exists)
- [ ] ✅ Validate all prerequisites from Prerequisites section below

**Self-Check**:
- [ ] ✅ I have read ALL files listed above
- [ ] ✅ I understand "Maximum Attention to Detail" requirement
- [ ] ✅ I am ready to check EVERY validation criterion individually
- [ ] ✅ I will validate FDL syntax and completeness
- [ ] ✅ I will run grep searches for systematic verification
- [ ] ✅ I will complete self-test before reporting results

**⚠️ If ANY checkbox is unchecked → STOP and read missing files first**

---

## Requirements

**ALWAYS open and follow**: `../requirements/feature-design-structure.md`

Extract:
- Required sections structure
- FDL validation requirements
- Validation criteria (100 points breakdown)
- Pass threshold (100/100 + 100% completeness)

---

## Prerequisites

**MUST validate**:
- [ ] Feature design artifact exists - validate: Check file at feature design path from `{adapter-dir}/artifacts.json` (default: `architecture/features/feature-{slug}/DESIGN.md`)
- [ ] DESIGN artifact exists and validated (path from `{adapter-dir}/artifacts.json`; default: `architecture/DESIGN.md`)
- [ ] FEATURES manifest exists and validated (path from `{adapter-dir}/artifacts.json`; default: `architecture/features/FEATURES.md`)

**If missing**: Ask the user whether to:
- Create/validate prerequisites via the corresponding workflows
- Provide inputs in another form (path, link, or pasted text in any format)
- Proceed anyway (reduce scope to content-only checks and report missing cross-references)

---

## Steps

### 1. Run Deterministic Gate (FDD Structure + IDs)

Run `fdd validate` for the feature design artifact.

If the artifact is registered in `{adapter-dir}/artifacts.json` and `format: FDD`, this gate performs structural validation.

If the artifact is not registered or registered with a non-FDD format, the gate is expected to return `PASS` with `skipped: true`.

If the output includes `skipped: true`, do NOT execute Step 3 (FDD-format-only scoring). Report `Status: SKIPPED` for structural validation and continue to Step 6 (Semantic Expert Review) as a content-only review.

**Meaning**: This feature design is not a registered `format: FDD` artifact, so structure/ID validation MUST NOT be executed by this workflow.

**Fix**: Register the feature design in `{adapter-dir}/artifacts.json` with `format: FDD`, then re-run `feature-validate`.

### 2. Read Dependencies

Open:
- DESIGN artifact (path from `{adapter-dir}/artifacts.json`; default: `architecture/DESIGN.md`) - Extract all types, requirements
- FEATURES manifest (path from `{adapter-dir}/artifacts.json`; default: `architecture/features/FEATURES.md`) - Extract feature requirements

### 3. Execute Validation (FDD Format Only)

ONLY execute this step if Step 1 did NOT return `skipped: true`. If Step 1 returned `skipped: true`, skip to Step 6.

Follow validation criteria from `feature-design-structure.md`:
- Structure (20 pts)
- Completeness (30 pts)
- FDL Correctness (25 pts)
- Non-Contradiction (25 pts)

Calculate total score

### 4. Check Completeness

- No placeholders
- All sections present
- 100% completeness required

### 5. Output Results to Chat

**Format**:
```markdown
## Validation Report: Feature DESIGN.md ({feature-slug})

### Summary
- **Status**: **PASS** ✅ | **FAIL** ❌
- **Score**: **{X}/100**
- **Completeness**: **{X}%**
- **Threshold**: **100/100 + 100%**

---

### Findings

#### 1) Structure — **{X}/20**
- ✅ | ❌ {item}

#### 2) Completeness — **{X}/30**
- ✅ | ❌ {item}

#### 3) FDL Correctness — **{X}/25**
- ✅ | ❌ {item}

#### 4) Non-Contradiction — **{X}/25**
- ✅ | ❌ {item}

---

### Recommendations

#### Critical *(must fix to pass)*
1. **{Fix}**

---

### Next Steps

- **If PASS**: ✅ Proceed to `implement`
- **If FAIL**: ❌ Fix issues above, then re-run `feature-validate`
```

### 6. Semantic Expert Review (Always)

Run an expert panel review of the feature design content after producing the validation output.

**Critical requirement**: This step MUST produce an explicit section in chat titled `### Semantic Expert Review` that confirms the review was executed.

**Experts**:
- Architect
- Developer
- QA Engineer
- Security Expert
- Database Architect
- Performance Engineer
- DCO Engineer
- Monitoring Engineer
- DevOps Engineer
- Cloud Engineer
- Infrastructure Engineer
- Data Engineer
- Legal Counsel
- Compliance Engineer
- UX Engineer
- Product Manager

**Instructions (MANDATORY)**:
- [ ] Execute this checklist for EACH expert listed above (do not skip any expert)
- [ ] Adopt the role of the current expert (write: `Role assumed: {expert}`)
- [ ] Review the entire artifact content (not only headings)
- [ ] Enforce semantic boundaries:
  - [ ] Feature design answers "How this feature works" and MUST remain consistent with overall DESIGN and FEATURES
  - [ ] Non-feature architecture decisions MUST NOT be introduced here
- [ ] Identify issues (list each item explicitly):
  - [ ] Contradictions vs overall DESIGN and FEATURES
  - [ ] Missing information (flows, edge cases, data)
  - [ ] Unclear statements or under-specified behavior
  - [ ] Misplaced content (belongs in overall DESIGN/ADR)
- [ ] Provide concrete proposals:
  - [ ] What to remove (quote the exact fragment)
  - [ ] What to add (provide the missing content)
  - [ ] What to rewrite (provide suggested phrasing)
- [ ] Propose the corrective workflow: `feature` (UPDATE mode)

**Required output format** (append to chat):
```markdown
### Semantic Expert Review

**Review status**: **COMPLETED** ✅  
**Reviewed artifact**: `Feature DESIGN.md ({feature-slug})`  
**Experts reviewed**: *Architect, Developer, QA Engineer, Security Expert, Database Architect, Performance Engineer, DCO Engineer, Monitoring Engineer, DevOps Engineer, Cloud Engineer, Infrastructure Engineer, Data Engineer, Legal Counsel, Compliance Engineer, UX Engineer, Product Manager*

*Rule*: For EACH expert listed in the workflow, include a `#### Expert: {expert}` section below. Do not omit any expert.

#### Expert: Architect
- **Role assumed**: Architect
- **Checklist completed**: **YES** ✅
- **Findings**:
  - **Contradictions vs overall DESIGN and FEATURES**: ...
  - **Missing information (flows, edge cases, data)**: ...
  - **Unclear statements**: ...
  - **Misplaced content**: ...
- **Proposed edits**:
  - **Remove**: "..." → **Reason**: ...
  - **Add**: ...
  - **Rewrite**: "..." → "..."

#### Expert: Developer
- **Role assumed**: Developer
- **Checklist completed**: **YES** ✅
- **Findings**: ...
- **Proposed edits**: ...

#### Expert: QA Engineer
- **Role assumed**: QA Engineer
- **Checklist completed**: **YES** ✅
- **Findings**: ...
- **Proposed edits**: ...

#### Expert: Security Expert
- **Role assumed**: Security Expert
- **Checklist completed**: **YES** ✅
- **Findings**: ...
- **Proposed edits**: ...

#### Expert: Database Architect
- **Role assumed**: Database Architect
- **Checklist completed**: **YES** ✅
- **Findings**: ...
- **Proposed edits**: ...

#### Expert: Performance Engineer
- **Role assumed**: Performance Engineer
- **Checklist completed**: **YES** ✅
- **Findings**: ...
- **Proposed edits**: ...

#### Expert: DCO Engineer
- **Role assumed**: DCO Engineer
- **Checklist completed**: **YES** ✅
- **Findings**: ...
- **Proposed edits**: ...

#### Expert: Monitoring Engineer
- **Role assumed**: Monitoring Engineer
- **Checklist completed**: **YES** ✅
- **Findings**: ...
- **Proposed edits**: ...

#### Expert: DevOps Engineer
- **Role assumed**: DevOps Engineer
- **Checklist completed**: **YES** ✅
- **Findings**: ...
- **Proposed edits**: ...

#### Expert: Cloud Engineer
- **Role assumed**: Cloud Engineer
- **Checklist completed**: **YES** ✅
- **Findings**: ...
- **Proposed edits**: ...

#### Expert: Infrastructure Engineer
- **Role assumed**: Infrastructure Engineer
- **Checklist completed**: **YES** ✅
- **Findings**: ...
- **Proposed edits**: ...

#### Expert: Data Engineer
- **Role assumed**: Data Engineer
- **Checklist completed**: **YES** ✅
- **Findings**: ...
- **Proposed edits**: ...

#### Expert: Legal Counsel
- **Role assumed**: Legal Counsel
- **Checklist completed**: **YES** ✅
- **Findings**: ...
- **Proposed edits**: ...

#### Expert: Compliance Engineer
- **Role assumed**: Compliance Engineer
- **Checklist completed**: **YES** ✅
- **Findings**: ...
- **Proposed edits**: ...

#### Expert: UX Engineer
- **Role assumed**: UX Engineer
- **Checklist completed**: **YES** ✅
- **Findings**: ...
- **Proposed edits**: ...

#### Expert: Product Manager
- **Role assumed**: Product Manager
- **Checklist completed**: **YES** ✅
- **Findings**: ...
- **Proposed edits**: ...

---

**Recommended corrective workflow**: `feature` *(UPDATE mode)*
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

**If PASS**: `implement` workflow

**If FAIL**: Fix feature DESIGN.md issues, re-run `feature-validate`
