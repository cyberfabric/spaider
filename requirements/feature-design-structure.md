---
fdd: true
type: requirement
name: Feature Design Structure
version: 1.1
purpose: Define validation rules for feature DESIGN.md files
---

# Feature Design Structure Requirements

---

## Agent Instructions

**ALWAYS open and follow**: `../workflows/feature.md` WHEN executing workflow

**ALWAYS open and follow**: `../templates/feature-DESIGN.template.md` WHEN generating content

**ALWAYS open**: `../examples/requirements/feature-design/valid.md` WHEN reviewing valid artifact structure

**ALWAYS open and follow**: `requirements.md` WHEN extracting shared requirements

**ALWAYS open and follow**: `FDL.md` WHEN writing flows, algorithms, or states

---

## Prerequisite Checklist

- [ ] Agent has read and understood this requirement
- [ ] Agent will follow the rules defined here
- [ ] Agent will use template for generation
- [ ] Agent will reference example for structure validation
- [ ] Agent will follow FDL syntax for behavioral sections

---

## Overview

**This file defines**: Validation rules (WHAT must be valid)  
**Template defines**: Structure for generation (HOW to create)  
**Workflow defines**: Process (STEP by STEP)

**Location**: `architecture/features/feature-{slug}/DESIGN.md`

**Size limits**:
- Recommended: ≤3000 lines
- Hard limit: ≤4000 lines

---

## Required Sections

| Section | Purpose | Required |
|---------|---------|----------|
| A | Feature Context | YES |
| B | Actor Flows (FDL) | YES |
| C | Algorithms (FDL) | YES |
| D | States (FDL) | YES (can be minimal) |
| E | Technical Details | YES |
| F | Requirements | YES |
| G | Testing Scenarios | YES |
| H | Additional Context | Optional |

**Order**: A → B → C → D → E → F → G → [H]

---

## Validation Criteria

### File Validation

- File exists at `architecture/features/feature-{slug}/DESIGN.md`
- File ≤4000 lines (warning if >3000)

### Structure Validation

- All required sections A-G present
- Correct section order
- No duplicate sections

### Section Requirements

| Section | Min Lines | Key Requirement |
|---------|-----------|-----------------|
| A | — | Feature ID, Status, Actors from BUSINESS.md |
| B | 50 | FDL syntax, flow IDs, checkboxes |
| C | 100 | FDL syntax, algo IDs, no code blocks |
| D | — | FDL syntax with **WHEN** keyword |
| E | 200 | DB, API, Security, Error Handling |
| F | — | ≥1 requirement with all fields |
| G | — | ≥1 test with FDL steps |

---

## FDD ID Formats

| ID Type | Format |
|---------|--------|
| Flow | `fdd-{project}-feature-{slug}-flow-{name}` |
| Algorithm | `fdd-{project}-feature-{slug}-algo-{name}` |
| State | `fdd-{project}-feature-{slug}-state-{name}` |
| Requirement | `fdd-{project}-feature-{slug}-req-{name}` |
| Test | `fdd-{project}-feature-{slug}-test-{name}` |

**ID Rules**:
- All IDs wrapped in backticks
- Names in kebab-case (2-4 words)
- Unique within their section
- Must include checkbox: `- [ ] **ID**: {id}` or `- [x] **ID**: {id}`

---

## FDL Requirements

### Mandatory for Sections B, C, D, G

**Step format**:
```
1. [ ] - `ph-1` - {instruction} - `inst-{short-id}`
```

**Required elements per step**:
- Checkbox: `[ ]` or `[x]`
- Phase token: `ph-{N}`
- Instruction ID: `inst-{short-id}` (unique within section)

### FDL Keywords

**Allowed**:
- Control: **IF**, **ELSE IF**, **ELSE**, **FOR EACH**, **WHILE**
- Error: **TRY**, **CATCH**
- Flow: **RETURN**, **PARALLEL**, **GO TO**, **SKIP TO**
- Pattern: **MATCH**, **CASE**
- State: **FROM**, **TO**, **WHEN** (states only)

**Prohibited** (as bold keywords):
- **WHEN** (except in states), **THEN**, **SET**, **VALIDATE**, **CHECK**
- **LOAD**, **READ**, **WRITE**, **CREATE**, **ADD**, **AND**
- Gherkin: **GIVEN**, **WHEN**, **THEN** (in tests)

---

## Section F: Requirements Validation

**Required fields per requirement**:

| Field | Description |
|-------|-------------|
| **ID** | Unique requirement ID with checkbox |
| **Status** | ⏳ NOT_STARTED, 🔄 IN_PROGRESS, ✅ IMPLEMENTED |
| **Description** | SHALL/MUST statements |
| **References** | Anchors to sections B-E |
| **Implements** | Flow/algo/state IDs |
| **Phases** | Phase decomposition with checkboxes |
| **Tests Covered** | Test IDs from Section G |
| **Acceptance Criteria** | ≥2 testable criteria |

---

## Section G: Testing Validation

**Required fields per test**:

| Field | Description |
|-------|-------------|
| **ID** | Unique test ID with checkbox |
| **Validates** | Requirement IDs from Section F |
| **Steps** | FDL syntax (NOT Gherkin) |

---

## Cross-Validation with Overall Design

### Type References
- ✅ Reference types from Overall Design Section C
- ❌ No new type definitions in feature DESIGN.md

### API References
- ✅ Reference endpoints from Overall Design
- ❌ No new endpoint definitions

### Actor Alignment
- ✅ Only actors from BUSINESS.md
- Actor IDs must match

---

## Scoring

| Category | Points |
|----------|--------|
| Structure (A-G present) | 15 |
| FDL Compliance (B, C, D, G) | 30 |
| Technical Details (E) | 20 |
| Requirements (F) | 20 |
| Testing Scenarios (G) | 15 |
| **Total** | **100** |

---

## Common Issues

- Missing required sections (A-G)
- Invalid section order
- Missing or invalid FDL step format
- Missing required requirement fields
- Missing `<!-- fdd-id-content -->` payload blocks
- Using Gherkin keywords instead of FDL
- Type redefinitions instead of references

---

## Validation Checklist (Final)

- [ ] Document follows required structure (A-G)
- [ ] All validation criteria pass
- [ ] FDL syntax correct in B, C, D, G
- [ ] Cross-validation with Overall Design passes
- [ ] Agent used template for generation
- [ ] Agent referenced example for validation
- [ ] Agent followed FDL.md for behavioral sections

---

## References

**Template**: `../templates/feature-DESIGN.template.md`

**Example**: `../examples/requirements/feature-design/valid.md`

**Related**:
- `FDL.md` — FDL syntax specification
- `overall-design-structure.md` — Overall Design structure
- `feature-changes-structure.md` — CHANGES.md structure
