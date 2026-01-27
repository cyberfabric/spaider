---
fdd: true
type: workflow
name: PRD Validate
version: 1.0
purpose: Validate PRD document
---

# Validate PRD

**Type**: Validation  
**Role**: Product Manager, Business Analyst  
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
- [ ] ✅ Open and follow `../requirements/prd-structure.md` (This workflow's requirements)
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

**ALWAYS open and follow**: `../requirements/prd-structure.md`

Extract:
- Required sections structure
- ID format requirements
- Validation criteria (100 points breakdown)
- Pass threshold (≥90/100)

---

## Prerequisites

**MUST validate**:
- [ ] PRD artifact exists - validate: Check file at PRD path from `{adapter-dir}/artifacts.json` (default: `architecture/PRD.md`)

**If missing**: Ask the user whether to:
- Create PRD via `prd`
- Provide PRD input in another form (path, link, or pasted text in any format)

---

## Steps

### 1. Run Deterministic Gate (FDD Structure + IDs)

Run `fdd validate` for the PRD artifact.

If the artifact is registered in `{adapter-dir}/artifacts.json` and `format: FDD`, this gate performs structural validation.

If the artifact is not registered or registered with a non-FDD format, the gate is expected to return `PASS` with `skipped: true`.

If the output includes `skipped: true`, do NOT execute Step 2 (FDD-format-only scoring). Report `Status: SKIPPED` for structural validation and continue to Step 4 (Semantic Expert Review) as a content-only review.

**Meaning**: This PRD is not a registered `format: FDD` artifact, so structure/ID validation MUST NOT be executed by this workflow.

**Fix**: Register the PRD in `{adapter-dir}/artifacts.json` with `format: FDD`, then re-run `prd-validate`.

### 2. Execute Detailed Validation (FDD Format Only)

**⚠️ CRITICAL**: ALWAYS open and follow `../requirements/workflow-execution-validations.md` for detailed validation requirements

**⚠️ ALWAYS** perform validation with **MAXIMUM ATTENTION TO DETAIL**

ONLY execute this step if Step 1 did NOT return `skipped: true`. If Step 1 returned `skipped: true`, skip to Step 4.

Follow validation criteria from `prd-structure.md`:

#### Structure Validation (25 pts)
**ALWAYS verify EACH item**:
- [ ] Section A: VISION present with exact heading
- [ ] Section B: Actors present with exact heading
- [ ] Section C: Functional Requirements present with exact heading
- [ ] Section D: Use Cases present with exact heading
- [ ] Section E: Non-functional requirements present with exact heading
- [ ] Section F: Additional context (optional) - if present, verify exact heading
- [ ] Section numbering follows A, B, C, D, E, F format
- [ ] Section order is correct (A → B → C → D → E → [F])
- [ ] Headers use ## for sections, #### for actors/requirements/use cases/NFRs
- [ ] No prohibited sections present

#### Completeness Validation (30 pts)
**ALWAYS check EVERY line**:
- [ ] Section A contains: Purpose, Target Users, Key Problems Solved, Success Criteria
- [ ] Section A contains: Capabilities list
- [ ] Success criteria are measurable (specific numbers/percentages)
- [ ] At least 2 paragraphs in Section A
- [ ] At least 1 actor defined in Section B
- [ ] Each actor has: #### heading, **ID**: line, **Role**: line
- [ ] Actors grouped by Human Actors and System Actors
- [ ] At least 1 functional requirement defined in Section C
- [ ] Each functional requirement has: #### heading, **ID**: line, description, **Actors**: line
- [ ] At least 1 use case defined in Section D
- [ ] At least 1 NFR defined in Section E
- [ ] NO placeholders (TODO, TBD, [Description], etc.)
- [ ] NO empty sections or sections with only HTML comments
- [ ] All content is substantive, not placeholder text

#### ID Formats Validation (25 pts)
**ALWAYS verify EACH ID individually**:
- [ ] ALL actor IDs follow format: `fdd-{project}-actor-{name}` in kebab-case
- [ ] ALL functional requirement IDs follow format: `fdd-{project}-fr-{name}` in kebab-case
- [ ] ALL use case IDs follow format: `fdd-{project}-usecase-{name}`
- [ ] ALL NFR IDs follow format: `fdd-{project}-nfr-{name}`
- [ ] If Section F present and contains IDs: ALL context IDs follow format: `fdd-{project}-prd-context-{name}`
- [ ] ALL IDs are wrapped in backticks
- [ ] ALL IDs appear immediately after heading with format: `**ID**: \`fdd-...\``
- [ ] ALL IDs are unique (no duplicates across entire document)
- [ ] Project name is consistent across all IDs

#### Consistency Validation (20 pts)
**ALWAYS verify EVERY reference**:
- [ ] Build index of ALL actor IDs from Section B
- [ ] For EACH functional requirement in Section C:
  - [ ] Verify **Actors**: line exists
  - [ ] Verify at least 1 actor ID listed
  - [ ] Verify EACH actor ID in backticks
  - [ ] Verify EACH actor ID exists in Section B index
- [ ] For EACH use case in Section D, verify EACH **Actor**: line references valid actor IDs
- [ ] Count and report: X/Y actor references validated
- [ ] NO invalid or non-existent actor references

Calculate total score

### 3. Output Detailed Results to Chat

**Format**:
```markdown
## Validation Report: PRD.md ({module-name})

### Summary
- **Status**: **PASS** ✅ | **FAIL** ❌
- **Score**: **{X}/100**
- **Threshold**: **≥90/100**

---

### Findings

#### 1) Structure — **{X}/25**
- ✅ Section A: VISION present and correctly named
- ✅ | ❌ Section B: Actors present and correctly named
- ✅ | ❌ Section C: Capabilities present and correctly named
- ✅ | ❌ Section D: Use Cases (optional) - check if present and correctly named
- ✅ | ❌ Section E: Additional Context (optional) - check if present and correctly named
- ✅ | ❌ Section numbering follows A, B, C, D, E
- ✅ | ❌ Section order correct
- ✅ | ❌ Headers formatted correctly
- ❌ **CRITICAL**: Section D incorrectly named "Additional Context" (should be "Use Cases" or absent)

#### 2) Completeness — **{X}/30**
- ✅ | ❌ Section A contains all required components
- ✅ | ❌ Success criteria measurable (**{count}** criteria)
- ✅ | ❌ **{count}** actors defined
- ✅ | ❌ **{count}** capabilities defined
- ✅ | ❌ No placeholders found
- ✅ | ❌ All sections have substantive content

#### 3) ID Formats — **{X}/25**
- ✅ | ❌ All **{count}** actor IDs follow format `fdd-{project}-actor-{name}`
- ✅ | ❌ All **{count}** capability IDs follow format `fdd-{project}-capability-{name}`
- ✅ | ❌ All IDs unique (checked **{total}** IDs)
- ✅ | ❌ All IDs wrapped in backticks
- ✅ | ❌ All IDs appear immediately after headings

#### 4) Consistency — **{X}/20**
- ✅ | ❌ All capability actor references validated (checked **{count}** references)
- ✅ | ❌ All referenced actor IDs exist in Section B
- ✅ | ❌ All actor IDs in backticks
- ✅ | ❌ No orphaned references

---

### Recommendations

#### High Priority *(must fix to pass)*
1. **{Specific fix}** (include file location and *expected vs actual*)
2. **{Another specific fix}**

---

### Next Steps

- **If PASS**: ✅ Proceed to `design`
- **If FAIL**: ❌ Fix the **{count}** issues above, then re-run `prd-validate`
```

### 4. Semantic Expert Review (Always)

Run an expert panel review of the PRD content after producing the validation output.

**Critical requirement**: This step MUST produce an explicit section in chat titled `### Semantic Expert Review` that confirms the review was executed.

 **Experts**:
 - Product Manager
 - Architect
 - Security Engineer
 - QA Engineer
 - UX Engineer
 - Legal Counsel
 - Compliance Engineer
 - Data Engineer
 - DevOps Engineer
 - Cloud Engineer
 - Infrastructure Engineer
 
 **Instructions (MANDATORY)**:
 - [ ] Execute this checklist for EACH expert listed above (do not skip any expert)
 - [ ] Adopt the role of the current expert (write: `Role assumed: {expert}`)
 - [ ] Review the entire artifact content (not only headings)
 - [ ] Enforce semantic boundaries:
   - [ ] PRD answers **WHAT** and **WHY**, not **HOW**
   - [ ] Architecture decisions, implementation details, and low-level technical choices MUST NOT dominate PRD
- [ ] Identify issues (list each item explicitly):
  - [ ] Contradictions
  - [ ] Missing information
  - [ ] Unclear/ambiguous statements
  - [ ] Misplaced content (belongs in DESIGN/ADR)
- [ ] Provide concrete proposals:
  - [ ] What to remove (quote the exact fragment)
  - [ ] What to add (provide the missing content)
  - [ ] What to rewrite (provide suggested phrasing)
- [ ] Propose the corrective workflow: `prd` (UPDATE mode)

**Required output format** (append to chat):
```markdown
### Semantic Expert Review

**Review status**: **COMPLETED** ✅
**Reviewed artifact**: `PRD.md`  
**Experts reviewed**: *Product Manager, Architect*

*Rule*: For EACH expert listed in the workflow, include a `#### Expert: {expert}` section below. Do not omit any expert.

#### Expert: Product Manager
- **Role assumed**: Product Manager
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

#### Expert: Architect
- **Role assumed**: Architect
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

---
 
**Recommended corrective workflow**: `prd` *(UPDATE mode)*
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

**If PASS**: `design` workflow

**If FAIL**: Fix PRD.md, re-validate
