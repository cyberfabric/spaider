---
fdd: true
type: requirement
name: Features Manifest Structure
version: 1.1
purpose: Define validation rules for FEATURES.md files
---

# Features Manifest Structure Requirements

---

## Agent Instructions

**ALWAYS open and follow**: `../workflows/features.md` WHEN executing workflow

**ALWAYS open and follow**: `../templates/FEATURES.template.md` WHEN generating content

**ALWAYS open**: `../examples/requirements/features-manifest/valid.md` WHEN reviewing valid artifact structure

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

---

## File Overview

**Purpose**: Central manifest tracking all features in the project

**Location**: `architecture/features/FEATURES.md`

---

## Validation Criteria

### File Validation

1. **File exists**: `architecture/features/FEATURES.md` exists
2. **Header present**: Project name in title, status overview present

### Structure Validation

1. **Feature list present**
   - ≥1 feature defined
   - All features have required fields

2. **Feature entry format**
   - Heading: `### N. [fdd-{project}-feature-{slug}](feature-{slug}/) EMOJI PRIORITY`
   - Status emoji valid (⏳📝📘🔄✅)
   - Slug is kebab-case
   - Sequential numbering (1, 2, 3, ...)

### Required Fields Per Feature

| Field | Format | Required |
|-------|--------|----------|
| **Purpose** | One-line description | YES |
| **Status** | NOT_STARTED, IN_DESIGN, DESIGN_READY, IN_DEVELOPMENT, IMPLEMENTED | YES |
| **Depends On** | None or feature links | YES |
| **Blocks** | None or feature links | YES |
| **Scope** | Bulleted list | YES |
| **Requirements Covered** | FDD IDs from DESIGN.md | YES |
| **Principles Covered** | FDD IDs from DESIGN.md | Optional |
| **Constraints Affected** | FDD IDs from DESIGN.md | Optional |
| **Phases** | Phase list with status | YES |

### Phase Format

**Phase ID Format**: `ph-{N}` (N = integer: 1, 2, 3, ...)

**Format**:
```
**Phases**:
  - `ph-1`: ✅ IMPLEMENTED — {meaning}
  - `ph-2`: 🔄 IN_DEVELOPMENT — {meaning}
  - `ph-3`: ⏳ NOT_STARTED — {meaning}
```

**Phase dependencies** (optional):
```
  - `ph-2`: 🔄 IN_DEVELOPMENT — {meaning}
    - **Depends On**:
      - [feature-a](feature-a/) `ph-1`
```

**Rules**:
- Every feature MUST define at least `ph-1`
- IMPLEMENTED feature MUST have ALL phases marked ✅
- Phase marked ✅ MUST NOT depend on IN_PROGRESS or NOT_STARTED phases

### Content Validation

1. **Feature directories exist**
   - Each feature has: `architecture/features/feature-{slug}/`
   - DESIGN.md exists if status ≠ NOT_STARTED

2. **Dependencies valid**
   - All dependency slugs reference existing features
   - No circular dependencies (DAG structure)
   - Phase dependencies satisfiable

3. **Status consistency**
   - Status matches DESIGN.md existence
   - IMPLEMENTED features have complete DESIGN.md
   - IMPLEMENTED features have ALL phases ✅

---

## Cross-Validation with DESIGN.md

### Traceability Rules

1. **Requirements Coverage (MANDATORY)**
   - All requirement IDs from DESIGN.md Section B.1 (FR) MUST appear in at least one feature
   - All requirement IDs from DESIGN.md Section B.2 (NFR) MUST appear in at least one feature
   - No orphaned requirements

2. **Principles Coverage (RECOMMENDED)**
   - Principle IDs from DESIGN.md Section B.3 SHOULD appear in features that implement them

3. **Constraints Coverage (RECOMMENDED)**
   - Constraint IDs from DESIGN.md Section B.4 SHOULD appear in affected features

### ID Format Validation

- All IDs follow format: `fdd-{project}-{type}-{name}`
- FEATURES.md must use exact IDs from DESIGN.md
- No capability/usecase IDs in FEATURES.md (those belong in DESIGN.md)

### Scoring

| Issue | Penalty |
|-------|---------|
| Orphaned requirement | -10 points |
| Invalid ID reference | -5 points |
| Format violation | -2 points |

---

## Status Lifecycle

| Status | Emoji | Meaning |
|--------|-------|---------|
| NOT_STARTED | ⏳ | Planned, no DESIGN.md |
| IN_DESIGN | 📝 | Being designed |
| DESIGN_READY | 📘 | Design complete |
| IN_DEVELOPMENT | 🔄 | Implementation in progress |
| IMPLEMENTED | ✅ | Complete and validated |

---

## Dependency Rules

1. **Acyclic**: No circular dependencies
2. **Valid references**: All dependencies must exist
3. **Implementation order**: Dependencies implemented before dependents
4. **Foundation first**: Core features have no dependencies

---

## Common Issues

- Missing required header (`# Features: {PROJECT_NAME}`)
- Missing `**Status Overview**:` and `**Meaning**:` blocks
- Invalid feature entry format or numbering
- Orphaned requirements (not covered by any feature)
- Phase format violations

---

## Validation Checklist (Final)

- [ ] Document follows required structure
- [ ] All validation criteria pass
- [ ] All DESIGN.md requirements covered
- [ ] Agent used template for generation
- [ ] Agent referenced example for validation

---

## References

**Template**: `../templates/FEATURES.template.md`

**Example**: `../examples/requirements/features-manifest/valid.md`

**Related**:
- `overall-design-structure.md` — Source of requirements
- `feature-design-structure.md` — Feature DESIGN.md structure
