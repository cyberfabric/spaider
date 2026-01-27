---
fdd: true
type: workflow
name: Feature
version: 1.0
purpose: Create or update feature design document
---

# Create or Update Feature Design

**Type**: Operation  
**Role**: Solution Architect  
**Artifact**: Path resolved via `{adapter-dir}/artifacts.json` (kind: `FEATURE`; default: `architecture/features/feature-{slug}/DESIGN.md`)

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

## Requirements

**ALWAYS open and follow**: `../requirements/feature-design-structure.md`

**ALWAYS open and follow**: `../templates/feature-DESIGN.template.md` WHEN generating content

Extract:
- Required sections (A-G)
- FDL requirements for behavioral sections
- Validation criteria

---

## Prerequisites

**MUST validate**:
- [ ] FEATURES manifest exists - validate: Check file at FEATURES path from `{adapter-dir}/artifacts.json` (default: `architecture/features/FEATURES.md`)
- [ ] FEATURES.md validated - validate: Score ≥90/100
- [ ] Feature exists in FEATURES.md - validate: Feature ID present

**If missing**: Ask the user whether to:
- Create/validate FEATURES via `features` + `features-validate`
- Provide the feature list/manifest in another form (path, link, or pasted text in any format)
- Proceed anyway (design a feature with minimal dependencies; record assumptions and missing links)

---

## Steps

Identify Feature.
 
### 1. Identify Feature

Ask user: Which feature to design/update?

Options: List from FEATURES.md

Store feature ID and slug

### 2. Detect Mode

Check if the feature design artifact exists (path resolved via `{adapter-dir}/artifacts.json`; default: `architecture/features/feature-{slug}/DESIGN.md`):
- **If exists**: UPDATE mode - Read and propose changes
- **If NOT exists**: CREATE mode - Generate from scratch

### 3. Read Context

Open the DESIGN artifact and FEATURES manifest (paths resolved via `{adapter-dir}/artifacts.json`; defaults: `architecture/DESIGN.md`, `architecture/features/FEATURES.md`)

Extract:
- Requirements assigned to this feature
- Actors relevant to feature
- Dependencies on other features

### 3. Design Feature

**Interactive questions per section** (following feature-design-structure.md):

**Section A: Overview**
- Feature purpose
- Scope boundaries

**Section B: Actor Flows** (use FDL)
- For each actor: Main flow, alternative flows
- Use FDL format from requirements

**Section C: Algorithms** (use FDL)
- Key business logic
- State transitions
- Use FDL format

**Section D: State Machines** (if applicable)
- States and transitions
- Use FDL format

**Section E: Technical Details**
- Database schemas (if adapter available)
- API endpoints (if adapter available)
- Integration points

**Section F: Requirements**
- Map requirements from DESIGN.md
- Generate requirement IDs

**Section G: Test Scenarios**
- Acceptance criteria per requirement
- Edge cases

### 4. Create feature/DESIGN.md

Generate content following `feature-design-structure.md`

Ensure:
- No contradictions with overall DESIGN.md
- No type redefinitions
- FDL used correctly
- All requirement IDs valid

### 5. Summary and Confirmation

Show:
- File path
- Sections included
- Requirements count
- Actor flows count

Ask: Create file? [yes/no/modify]

### 6. Create File

After confirmation:
- Create/update the feature design artifact (path resolved via `{adapter-dir}/artifacts.json`; default: `architecture/features/feature-{slug}/DESIGN.md`)
- Verify creation

---

## Validation

Run: `feature-validate`

Expected:
- Score: 100/100
- Completeness: 100%
- Status: PASS

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

**If validation passes**: `implement` workflow

**If validation fails**: Fix feature DESIGN.md, re-validate
