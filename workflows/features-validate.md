---
fdd: true
type: workflow
name: Features Validate
version: 1.0
purpose: Validate features manifest
---

# Validate Features Manifest

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
- [ ] ✅ Open and follow `../requirements/features-manifest-structure.md` (This workflow's requirements)
- [ ] ✅ Check adapter initialization (`.fdd-config.json` exists and adapter directory exists per `fdd adapter-info`)
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

**ALWAYS open and follow**: `../requirements/features-manifest-structure.md`

Extract:
- Required structure
- Validation criteria (100 points breakdown)
- Pass threshold (≥95/100)

---

## Prerequisites

**MUST validate**:
- [ ] Artifacts registry exists - validate: `{adapter-dir}/artifacts.json` exists and is readable
- [ ] FEATURES manifest is registered - validate: `artifacts.json` contains a `kind: FEATURES` entry for the target system
- [ ] Overall DESIGN is registered - validate: `artifacts.json` contains a `kind: DESIGN` entry for the same system

**If missing**: Ask the user whether to:
- Register/create missing artifacts via the corresponding workflows
- Provide inputs in another form (path, link, or pasted text in any format)
- Proceed anyway (reduce scope to content-only checks and report missing cross-references)

---

## Steps

### 1. Read Dependencies

Open:
- `{adapter-dir}/artifacts.json`
- The `kind: DESIGN` artifact path for the target system

Extract:
- All requirement IDs (Section B)

### 2. Run Deterministic Gate

Run the deterministic validator for prerequisites and the target artifact.

If the artifact is registered in `{adapter-dir}/artifacts.json` and `format: FDD`, this gate performs structural validation.

If the artifact is not registered or registered with a non-FDD format, the gate is expected to return `PASS` with `skipped: true`.

**Commands** (run from repo root):
```bash
python3 skills/fdd/scripts/fdd.py validate --artifact {features_manifest_path}

# Optional: validate all registered artifacts (all systems) in one shot
python3 skills/fdd/scripts/fdd.py validate --artifact .
```

**MUST** include the raw JSON output of these commands in the chat under a "Deterministic Gate Output" subsection.

**If FAIL**: Stop and report workflow FAIL.

**If PASS with `skipped: true`**: do NOT execute Step 3 (FDD-format-only scoring). Report `Status: SKIPPED` for structural validation and continue to Step 5 (Semantic Expert Review) as a content-only review.

**Meaning**: This FEATURES manifest is not a registered `format: FDD` artifact, so structure/ID validation MUST NOT be executed by this workflow.

**Fix**: Register the FEATURES manifest in `{adapter-dir}/artifacts.json` with `format: FDD`, then re-run `features-validate`.

**If PASS**: Continue. Deterministic PASS is NOT workflow completion.

### 3. Execute Validation (FDD Format Only)

ONLY execute this step if Step 2 did NOT return `skipped: true`. If Step 2 returned `skipped: true`, skip to Step 5.

Follow validation criteria from `features-manifest-structure.md`:
- Structure (20 pts): Required sections present
- Feature Definitions (30 pts): All features have ID, name, purpose, scope
- Coverage (30 pts): All DESIGN.md requirements covered by features
- Dependencies (20 pts): Valid, no circular dependencies

Calculate total score

### 4. Output Results to Chat

**Format**:
```markdown
## Validation Report: FEATURES.md

### Summary
- **Status**: **PASS** ✅ | **FAIL** ❌
- **Score**: **{X}/100**
- **Threshold**: **≥95/100**

---

### Findings

#### 1) Structure — **{X}/20**
- ✅ | ❌ {item}

#### 2) Feature Definitions — **{X}/30**
- ✅ | ❌ {item}

#### 3) Coverage — **{X}/30**
- ✅ | ❌ {item}

#### 4) Dependencies — **{X}/20**
- ✅ | ❌ {item}

---

### Coverage Analysis
- **Requirements covered**: **{X}/{total}** (**{percentage}%**)
- **Orphaned requirements**: {list if any}

---

### Recommendations

#### High Priority
1. **{Fix}**

---

### Next Steps

- **If PASS**: ✅ Proceed to `feature` (design first feature from FEATURES.md)
- **If FAIL**: ❌ Fix issues above, then re-run `features-validate`
```

### 5. Semantic Expert Review (Always)

Run an expert panel review of the FEATURES manifest content after producing the validation output.

**Critical requirement**: This step MUST produce an explicit section in chat titled `### Semantic Expert Review` that confirms the review was executed.

**Experts**:
- Product Manager
- Architect
- QA Engineer

**Instructions (MANDATORY)**:
- [ ] Execute this checklist for EACH expert listed above (do not skip any expert)
- [ ] Adopt the role of the current expert (write: `Role assumed: {expert}`)
- [ ] Review the entire artifact content (not only headings)
- [ ] Enforce semantic boundaries:
  - [ ] FEATURES answers "What features exist and how they relate", not detailed architecture
  - [ ] Feature requirements MUST be traceable to overall DESIGN requirements
- [ ] Identify issues (list each item explicitly):
  - [ ] Contradictions
  - [ ] Missing features or missing metadata
  - [ ] Unclear feature scopes or acceptance criteria
  - [ ] Misplaced content (belongs in feature design / DESIGN)
- [ ] Provide concrete proposals:
  - [ ] What to remove (quote the exact fragment)
  - [ ] What to add (provide the missing content)
  - [ ] What to rewrite (provide suggested phrasing)
- [ ] Propose the corrective workflow: `features` (UPDATE mode)

**Required output format** (append to chat):
```markdown
### Semantic Expert Review

**Review status**: **COMPLETED** ✅
**Reviewed artifact**: `FEATURES.md`  
**Experts reviewed**: *Product Manager, Architect, QA Engineer*

*Rule*: For EACH expert listed in the workflow, include a `#### Expert: {expert}` section below. Do not omit any expert.

#### Expert: {expert}
- **Role assumed**: {expert}
- **Checklist completed**: **YES** ✅
- **Findings**:
  - **Contradictions**: ...
  - **Missing metadata**: ...
  - **Unclear scopes**: ...
  - **Misplaced content**: ...
- **Proposed edits**:
  - **Remove**: "..." → **Reason**: ...
  - **Add**: ...
  - **Rewrite**: "..." → "..."

*Repeat the `#### Expert: {expert}` block for each expert above.*

---
 
**Recommended corrective workflow**: `features` *(UPDATE mode)*
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

**If PASS**: `feature` workflow (design first feature from FEATURES.md)

**If FAIL**: Fix FEATURES.md issues, re-run `features-validate`
