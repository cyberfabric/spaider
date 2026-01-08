# Feature Changes (Implementation Plan) Structure Requirements

**MUST read and follow**: `../workflows/feature-changes.md`

**This file defines**: Structure only (WHAT to create)  
**Workflow defines**: Process (HOW to create)

⚠️ **Do NOT use this file alone. Execute the workflow, not just the structure.**

---

**Version**: 1.0  
**Purpose**: Define structure for feature implementation plan (replaces OpenSpec)

**Scope**: Implementation plan for feature requirements

---

## Overview

**Feature CHANGES.md** - Implementation plan breaking down feature requirements into atomic changes

**Purpose**: Define granular implementation plan for feature
- List of atomic changes implementing feature requirements
- Each change = 1-5 requirements
- Each change = one deployable unit
- Task breakdown for each change

**Location**: `architecture/features/feature-{slug}/CHANGES.md`

**Prerequisites**: Feature DESIGN.md validated (100/100 + 100%)

---

## File Structure

### Document Header

```markdown
# Implementation Plan: {Feature Name}

**Feature**: `{feature-slug}`  
**Version**: {version}  
**Last Updated**: YYYY-MM-DD  
**Status**: {Overall status}

**Feature DESIGN**: `@/architecture/features/feature-{slug}/DESIGN.md`

---

## Summary

**Total Changes**: {count}  
**Completed**: {count}  
**In Progress**: {count}  
**Not Started**: {count}

**Estimated Effort**: {total story points/hours}

---
```

### Change Entries

**Format**: One change per section

```markdown
## Change {Number}: {Change Name}

**ID**: `change-{slug}`  
**Status**: ⏳ NOT_STARTED | 🔄 IN_PROGRESS | ✅ COMPLETED  
**Priority**: HIGH | MEDIUM | LOW  
**Effort**: {story points or hours}  
**Implements**: `fdd-{project}-{feature}-req-{id}`, `fdd-{project}-{feature}-req-{id}`

---

### Objective

{Clear objective of this change - what will be achieved}

### Requirements Coverage

**Implements**:
- **`fdd-{project}-{feature}-req-{id}`**: {Requirement description}
- **`fdd-{project}-{feature}-req-{id}`**: {Requirement description}

**References**:
- Actor Flow: {Section B reference from feature DESIGN.md}
- Algorithm: {Section C reference from feature DESIGN.md}
- State: {Section D reference from feature DESIGN.md}
- Technical Detail: {Section E reference from feature DESIGN.md}

### Tasks

{Hierarchical task breakdown with numbered sections}

## 1. Implementation

### 1.1 {Task Group Name}
- [ ] 1.1.1 {Task description with file path and action}
- [ ] 1.1.2 {Task description with file path and action}
- [ ] 1.1.3 {Task description with file path and action}

### 1.2 {Task Group Name}
- [ ] 1.2.1 {Task description with file path and action}
- [ ] 1.2.2 {Task description with file path and action}

## 2. Testing

### 2.1 {Test Group Name}
- [ ] 2.1.1 {Test description and validation}
- [ ] 2.1.2 {Test description and validation}

{Continue with all task groups}

**Format**: Hierarchical numbering with checkboxes (`- [ ]` incomplete, `- [x]` completed)

### Specification

{Detailed implementation specification}

**Domain Model Changes**:
- Type: `{type identifier}`
- Fields: {field specifications}
- Relationships: {relationship specifications}

**API Changes**:
- Endpoint: `{endpoint path}`
- Method: GET | POST | PUT | DELETE | PATCH
- Request: {request specification}
- Response: {response specification}

**Database Changes**:
- Table/Collection: `{name}`
- Schema: {schema specification}
- Migrations: {migration steps}

**Code Changes**:
- Module: `{module path}`
- Functions: {function signatures}
- Implementation: {high-level implementation approach}

### Dependencies

**Depends on**:
- Change {Number}: {change name} (MUST be completed first)
- External: {external dependencies}

**Blocks**:
- Change {Number}: {change name} (this MUST be completed first)

### Testing

**Unit Tests**:
- Test: {test description}
- File: `{test file path}`
- Validates: {what is validated}

**Integration Tests**:
- Test: {test description}
- File: `{test file path}`
- Validates: {what is validated}

**E2E Tests**:
- Scenario: {scenario from Section F of feature DESIGN.md}
- File: `{test file path}`
- Validates: {what is validated}

### Validation Criteria

**Code validation** (MUST pass):
- All tasks completed
- All tests pass
- Code follows adapter conventions
- No linter errors
- Documentation updated
- Implements all referenced requirements

---
```

---

## Change Directory Structure

**Each change MUST have directory**: `architecture/features/feature-{slug}/changes/change-{slug}/`

**Directory contents**:
```
changes/change-{slug}/
├── tasks.md              # Task breakdown with status
├── specification.md      # Detailed implementation spec
├── notes.md              # Implementation notes (optional)
└── validation.md         # Validation checklist
```

### tasks.md

```markdown
# Tasks: {Change Name}

**Change**: `change-{slug}`  
**Status**: {status}

---

## Task List

## 1. Implementation

### 1.1 {Task Group Name}
- [ ] 1.1.1 {Task description including action and file path}
- [ ] 1.1.2 {Task description including action and file path}

## 2. Testing

### 2.1 {Test Group Name}
- [ ] 2.1.1 {Test description and validation criteria}
- [ ] 2.1.2 {Test description and validation criteria}

{Continue for all tasks}

---

## Progress

**Total Tasks**: {count}  
**Completed**: {count}  
**In Progress**: {count}  
**Remaining**: {count}

**Current Task**: {current task number and description}
```

### specification.md

```markdown
# Implementation Specification: {Change Name}

**Change**: `change-{slug}`

---

## Domain Model

{Complete domain model specification}

## API Contracts

{Complete API contract specification}

## Database Schema

{Complete database schema specification}

## Code Structure

{Complete code structure specification}

## Implementation Approach

{Step-by-step implementation approach}
```

### validation.md

```markdown
# Validation Checklist: {Change Name}

**Change**: `change-{slug}`

---

## Code Validation

- [ ] All tasks completed
- [ ] All files created/modified
- [ ] Code follows adapter conventions
- [ ] Type definitions match domain model
- [ ] API contracts implemented correctly

## Testing Validation

- [ ] Unit tests written
- [ ] Unit tests pass
- [ ] Integration tests written
- [ ] Integration tests pass
- [ ] E2E tests written
- [ ] E2E tests pass
- [ ] Test coverage ≥{threshold}%

## Documentation Validation

- [ ] Code documented
- [ ] API endpoints documented
- [ ] Database schema documented
- [ ] README updated

## Quality Validation

- [ ] No linter errors
- [ ] No linter warnings
- [ ] Build succeeds
- [ ] No type errors
- [ ] No security vulnerabilities

## Requirements Validation

- [ ] All referenced requirements implemented
- [ ] Implementation matches feature DESIGN.md
- [ ] No contradictions with parent artifacts
- [ ] All edge cases handled
```

---

## Validation Criteria

### File Structure Validation

1. **CHANGES.md exists**
   - File at `architecture/features/feature-{slug}/CHANGES.md`
   - File is not empty
   - Contains required sections

2. **Document header present**
   - Feature reference
   - Version
   - Status
   - Summary with counts

3. **Change entries valid**
   - All changes numbered sequentially
   - All changes have unique IDs
   - All changes have status
   - All changes have priority
   - All changes reference feature requirements

4. **Change directories exist**
   - Directory for each change at `changes/change-{slug}/`
   - All required files present (tasks.md, specification.md, validation.md)

### Content Validation

1. **Change structure**
   - Objective clear and specific
   - Requirements coverage lists all implemented requirements
   - All requirement IDs exist in feature DESIGN.md Section F
   - Tasks are granular and actionable
   - Specification is complete
   - Testing plan covers all scenarios

2. **Task breakdown**
   - Each task has clear action
   - Each task specifies affected files
   - Each task has validation criteria
   - Tasks in logical order
   - No placeholders

3. **Specification completeness**
   - Domain model changes specified
   - API changes specified
   - Database changes specified
   - Code changes specified
   - All specifications follow adapter format

4. **Dependency tracking**
   - Dependencies listed
   - No circular dependencies
   - Dependency graph is acyclic (DAG)

5. **Testing coverage**
   - Unit tests for all code changes
   - Integration tests for API/DB changes
   - E2E tests for user scenarios
   - All tests reference feature DESIGN.md Section F scenarios

### Consistency Validation

1. **Feature DESIGN.md consistency**
   - All changes implement feature requirements
   - No changes implement non-existent requirements
   - All feature requirements covered by at least one change
   - References to actor flows, algorithms, states are valid

2. **Adapter consistency**
   - Domain model uses adapter format
   - API contracts use adapter format
   - Database schema uses adapter conventions
   - Code structure follows adapter conventions

3. **Parent artifact consistency**
   - No contradictions with DESIGN.md
   - No contradictions with BUSINESS.md
   - Types reference Overall Design domain model
   - No type redefinitions

### Completeness Validation

1. **All requirements covered**
   - Every requirement from feature DESIGN.md Section F has implementing change
   - Coverage map shows 100% coverage
   - No requirements orphaned

2. **No placeholders**
   - No `[TODO]` markers
   - No `[TBD]` markers
   - No empty specifications
   - All tasks have clear actions

3. **Change atomicity**
   - Each change implements 1-5 requirements
   - Each change is deployable independently (after dependencies)
   - No change too large (>10 tasks)
   - No change too small (<1 requirement)

### Validation Scoring

**Total**: 100 points

**Breakdown**:
- File structure (10 points): CHANGES.md + change directories
- Change structure (20 points): All required sections, no placeholders
- Task breakdown (15 points): Granular, actionable, validated
- Specification (20 points): Complete domain/API/DB/code specs
- Testing (15 points): Unit/integration/E2E coverage
- Consistency (10 points): No contradictions with parent artifacts
- Completeness (10 points): All requirements covered, 100% coverage

**Pass threshold**: ≥90/100

---

## Examples

### Valid CHANGES.md Entry

```markdown
# Implementation Plan: Analytics Event Tracking

**Feature**: `analytics-event-tracking`  
**Version**: 1.0  
**Last Updated**: 2025-01-07  
**Status**: 🔄 IN_PROGRESS

**Feature DESIGN**: `@/architecture/features/feature-analytics-event-tracking/DESIGN.md`

---

## Summary

**Total Changes**: 3  
**Completed**: 1  
**In Progress**: 1  
**Not Started**: 1

**Estimated Effort**: 13 story points

---

## Change 1: Event Schema Definition

**ID**: `change-event-schema`  
**Status**: ✅ COMPLETED  
**Priority**: HIGH  
**Effort**: 3 story points  
**Implements**: `fdd-analytics-event-req-domain-model`

---

### Objective

Define domain model for analytics events including event types, properties, and metadata.

### Requirements Coverage

**Implements**:
- **`fdd-analytics-event-req-domain-model`**: System MUST define event schema with type, properties, timestamp, user context

**References**:
- Actor Flow: Section B.1 - User triggers event
- Technical Detail: Section E.1 - Domain model specification

### Tasks

## 1. Implementation

### 1.1 Define Type Schemas
- [x] 1.1.1 Create GTS type definition for Event at `gts/analytics/event.v1.gts`
- [x] 1.1.2 Create GTS type for EventProperties at `gts/analytics/event_properties.v1.gts`
- [x] 1.1.3 Create GTS type for EventMetadata at `gts/analytics/event_metadata.v1.gts`

## 2. Testing

### 2.1 Schema Validation
- [x] 2.1.1 Verify all types compile and export valid JSON Schema
- [x] 2.1.2 Verify EventProperties supports arbitrary key-value pairs
- [x] 2.1.3 Verify EventMetadata includes timestamp and user context

### Specification

**Domain Model Changes**:
- Type: `gts.analytics.event.v1`
- Fields:
  - `id: string` - Unique event identifier
  - `type: string` - Event type (e.g., "page_view", "click")
  - `properties: EventProperties` - Event-specific properties
  - `metadata: EventMetadata` - Timestamp, user context
- Relationships: None

**API Changes**: None (domain model only)

**Database Changes**: None (domain model only)

**Code Changes**:
- Module: `domain/analytics/`
- Functions: Type definitions only
- Implementation: GTS schema compilation

### Dependencies

**Depends on**: None (first change)

**Blocks**: Change 2, Change 3

### Testing

**Unit Tests**:
- Test: Event schema validation
- File: `tests/domain/analytics/event_test.rs`
- Validates: Schema compiles, all fields present

### Validation Criteria

**Code validation**:
- ✅ All tasks completed
- ✅ GTS types compile
- ✅ JSON Schema output valid
- ✅ No linter errors
- ✅ Implements `fdd-analytics-event-req-domain-model`

---

## Change 2: Event Ingestion API

**ID**: `change-event-api`  
**Status**: 🔄 IN_PROGRESS  
**Priority**: HIGH  
**Effort**: 5 story points  
**Implements**: `fdd-analytics-event-req-ingest-api`, `fdd-analytics-event-req-validation`

---

{Similar structure for Change 2}

---

## Change 3: Event Storage

**ID**: `change-event-storage`  
**Status**: ⏳ NOT_STARTED  
**Priority**: MEDIUM  
**Effort**: 5 story points  
**Implements**: `fdd-analytics-event-req-persistence`

---

{Similar structure for Change 3}
```

### Valid Change Directory

```
changes/change-event-schema/
├── tasks.md              # 3 tasks listed with status
├── specification.md      # GTS schema specification
├── notes.md              # Implementation notes
└── validation.md         # Validation checklist (all checked)
```

---

## Workflow Integration

**Feature changes workflows**:
- `feature-changes` - Create/edit implementation plan
- `feature-changes-validate` - Validate plan structure and completeness
- `feature-change-implement` - Implement specific change task-by-task
- `feature-change-validate` - Validate implemented change against requirements

**Prerequisites**:
- Feature DESIGN.md validated (100/100 + 100%)
- All feature requirements finalized

**Validation frequency**:
- After creating CHANGES.md
- After modifying CHANGES.md
- Before starting implementation
- After completing each change

---

## Change Status Lifecycle

```
⏳ NOT_STARTED
    ↓ (start implementation)
🔄 IN_PROGRESS
    ↓ (complete all tasks + validation passes)
✅ COMPLETED
    ↓ (all changes completed - optional)
📦 ARCHIVED
```

**Status transitions**:
- NOT_STARTED → IN_PROGRESS: When first task started
- IN_PROGRESS → COMPLETED: When all tasks done AND validation passes
- IN_PROGRESS → NOT_STARTED: Rollback if needed
- COMPLETED → IN_PROGRESS: If issues found, reopen change
- COMPLETED → ARCHIVED: When all changes in CHANGES.md are completed (optional)

---

## Archiving Completed CHANGES.md

**When to archive**:
- All changes in CHANGES.md have status `✅ COMPLETED`
- Summary section: `**Completed**: {N}` equals `**Total Changes**: {N}`
- Feature implementation fully complete

**Archive location**:
```
architecture/features/feature-{slug}/archive/YYYY-MM-DD-CHANGES.md
```

**Archive process**:
1. Verify all changes completed
2. Create archive directory if not exists: `architecture/features/feature-{slug}/archive/`
3. Generate timestamp filename: `YYYY-MM-DD-CHANGES.md` (current date)
4. Move CHANGES.md to archive location
5. Confirm archiving complete

**Purpose**:
- Preserve historical implementation records
- Allow new CHANGES.md for future feature enhancements
- Maintain clean feature directory structure
- Document completed implementation milestones

**When NOT to archive**:
- Changes still in progress or not started
- Feature may need revisions or fixes
- User prefers to keep active CHANGES.md for reference

**Archive trigger workflows**:
- `feature-changes` workflow (Step 7) - Manual archive option in UPDATE mode
- `feature-changes-validate` workflow - Suggests archiving when all completed

---

## References

**Replaces**: OpenSpec integration

**Used by workflows**:
- `feature-changes` - Creates/edits CHANGES.md
- `feature-changes-validate` - Validates CHANGES.md
- `feature-change-implement` - Implements change
- `feature-change-validate` - Validates implementation

**Related requirements**:
- `feature-design-structure.md` - Feature DESIGN.md structure
- `adapter-structure.md` - Adapter conventions
- `overall-design-structure.md` - Domain model reference
