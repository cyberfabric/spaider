---
fdd: true
type: requirement
name: Feature Changes Structure
version: 1.1
purpose: Define validation rules for feature CHANGES.md files
---

# Feature Changes Structure Requirements

---

## Agent Instructions

**ALWAYS open and follow**: `../workflows/feature-changes.md` WHEN executing workflow

**ALWAYS open and follow**: `../templates/feature-CHANGES.template.md` WHEN generating content

**ALWAYS open**: `../examples/requirements/feature-changes/valid.md` WHEN reviewing valid artifact structure

**ALWAYS open and follow**: `requirements.md` WHEN extracting shared requirements

---

## Prerequisite Checklist

- [ ] Agent has read and understood this requirement
- [ ] Agent will follow the rules defined here
- [ ] Agent will use template for generation
- [ ] Agent will reference example for structure validation

---

## Overview

**This file defines**: Validation rules (WHAT must be valid)  
**Template defines**: Structure for generation (HOW to create)  
**Workflow defines**: Process (STEP by STEP)

**Purpose**: Implementation plan breaking down feature requirements into atomic changes

**Location**: `architecture/features/feature-{slug}/CHANGES.md`

**Archived**: `architecture/features/feature-{slug}/archive/YYYY-MM-DD-CHANGES.md`

**Prerequisites**: Feature DESIGN.md validated (100/100 + 100%)

---

## Validation Criteria

### File Structure Validation

1. **CHANGES source exists**
   - Active: `architecture/features/feature-{slug}/CHANGES.md` OR
   - Archived: `architecture/features/feature-{slug}/archive/YYYY-MM-DD-CHANGES.md`

2. **Document header present**
   - Feature reference, Version, Status
   - Summary with counts (Total, Completed, In Progress, Not Started)

3. **Change entries valid**
   - Sequential numbering
   - Unique IDs per change
   - All changes have: Status, Priority, Phases

### Change Entry Required Fields

| Field | Description |
|-------|-------------|
| **ID** | `fdd-{project}-{feature}-change-{slug}` |
| **Status** | ⏳ NOT_STARTED, 🔄 IN_PROGRESS, ✅ COMPLETED |
| **Priority** | HIGH, MEDIUM, LOW |
| **Effort** | Story points or hours |
| **Implements** | Requirement IDs from DESIGN.md Section F |
| **Phases** | `ph-1` or `ph-{N}, ph-{N}` |

### Change Entry Required Sections

| Section | Description |
|---------|-------------|
| Objective | Clear goal of this change |
| Requirements Coverage | Implements + References |
| Tasks | Hierarchical breakdown with checkboxes |
| Specification | Domain/API/DB/Code changes |
| Dependencies | Depends on + Blocks |
| Testing | Unit/Integration/E2E tests |
| Validation Criteria | All completion checks |

### Content Validation

1. **Task breakdown**
   - Each task has clear action
   - Each task specifies affected files
   - Each task has validation criteria
   - Tasks in logical order

2. **Specification completeness**
   - Domain model changes specified
   - API changes specified
   - Database changes specified
   - Code changes specified (including tagging)

3. **Testing coverage**
   - All testing scenarios from DESIGN.md Section G have tests
   - Each test includes scenario ID: `// @fdd-test:{scenario-id}:ph-{N}`

---

## Code Tagging Requirements

**Format** (paired fdd-begin/fdd-end blocks):
```
<!-- fdd-begin {change-id}:ph-{N}:inst-{id} -->
... code ...
<!-- fdd-end   {change-id}:ph-{N}:inst-{id} -->
```

**Rules**:
- Tags MUST wrap non-empty code (no single-line markers)
- All feature-scoped tags include `:ph-{N}` postfix
- Standalone phase tags MUST NOT exist
- Phase values in code MUST match `**Phases**` in change

**Language-specific**:
- **Rust/TS/JS/Go/Java/C#**: `// fdd-begin ...`
- **Python**: `# fdd-begin ...`
- **SQL**: `-- fdd-begin ...`
- **Markdown**: `<!-- fdd-begin ... -->`

---

## Consistency Validation

1. **Feature DESIGN.md consistency**
   - All changes implement feature requirements
   - All feature requirements covered by changes
   - References to flows/algos/states/TDs are valid

2. **Code tagging consistency**
   - No standalone phase tags
   - All tags include `:ph-{N}` postfix
   - Phases match declared values

3. **Parent artifact consistency**
   - No contradictions with DESIGN.md or BUSINESS.md
   - Types reference Overall Design (no redefinitions)

---

## Completeness Validation

1. **Requirements coverage**
   - Every requirement from DESIGN.md Section F has implementing change
   - 100% coverage required
   - No orphaned requirements

2. **Change atomicity**
   - Each change implements 1-5 requirements
   - Each change deployable independently
   - No change >10 tasks or <1 requirement

---

## Scoring

| Category | Points |
|----------|--------|
| File structure | 10 |
| Change structure | 20 |
| Task breakdown | 15 |
| Specification | 15 |
| Code tagging | 5 |
| Testing | 15 |
| Consistency | 10 |
| Completeness | 10 |
| **Total** | **100** |

**Pass threshold**: ≥90/100

---

## Status Lifecycle

```
⏳ NOT_STARTED → 🔄 IN_PROGRESS → ✅ COMPLETED → 📦 ARCHIVED
```

| Transition | When |
|------------|------|
| NOT_STARTED → IN_PROGRESS | First task started |
| IN_PROGRESS → COMPLETED | All tasks done + validation passes |
| COMPLETED → ARCHIVED | All changes completed (optional) |

---

## Archiving

**When to archive**:
- All changes have status ✅ COMPLETED
- Summary: `**Completed**: {N}` equals `**Total Changes**: {N}`

**Archive location**: `architecture/features/feature-{slug}/archive/YYYY-MM-DD-CHANGES.md`

---

## Common Issues

- Missing required header fields
- Missing or invalid summary counts
- Missing change entries or invalid numbering
- Missing `<!-- fdd-id-content -->` payload blocks
- Standalone phase tags in code
- Missing test scenario ID references

---

## Validation Checklist (Final)

- [ ] Document follows required structure
- [ ] All validation criteria pass
- [ ] 100% requirements coverage
- [ ] Code tagging format correct
- [ ] Agent used template for generation
- [ ] Agent referenced example for validation

---

## References

**Template**: `../templates/feature-CHANGES.template.md`

**Example**: `../examples/requirements/feature-changes/valid.md`

**Related**:
- `feature-design-structure.md` — Feature DESIGN.md structure
- `adapter-structure.md` — Adapter conventions
- `overall-design-structure.md` — Domain model reference
