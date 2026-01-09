---
description: Implement specific change from implementation plan
---

# Implement Feature Change

**Type**: Operation  
**Role**: Developer  
**Artifact**: Code files, tests

---

## Requirements

**ALWAYS open and follow**: 
- `../requirements/feature-changes-structure.md` (change structure)
- `{adapter-directory}/FDD-Adapter/AGENTS.md` (code conventions)

Extract:
- Task format and execution model
- Code conventions from adapter
- Testing requirements from adapter

---

## Prerequisites

**MUST validate**:
- [ ] CHANGES.md validated - validate: Score ≥90/100
- [ ] Adapter exists - validate: Check adapter AGENTS.md (REQUIRED for development)

**If adapter missing**: STOP, run `adapter` workflow first

---

## Steps

### 1. Select Change

Ask user: Which change to implement?

Options: List NOT_STARTED or IN_PROGRESS changes from CHANGES.md

Store change ID

### 2. Read Change Specification

Open CHANGES.md

Extract for selected change:
- Objective
- Requirements implemented
- Task list with files and validation

### 3. Read Adapter Conventions

Open `{adapter-directory}/FDD-Adapter/AGENTS.md`

Follow MUST WHEN instructions for:
- Code conventions
- Testing requirements
- Build requirements

### 3.1 Code Tagging Requirements

**MUST tag all code with IDs from both CHANGES and DESIGN**:

- Change ID: `@fdd-change:fdd-{project}-{feature}-change-{slug}` (from CHANGES source)
- Flow ID: `@fdd-flow:{flow-id}` (Section B of DESIGN)  
  _Example_: `@fdd-flow:fdd-analytics-feature-gts-core-flow-route-crud-operations`
- Algorithm ID: `@fdd-algo:{algo-id}` (Section C of DESIGN)  
  _Example_: `@fdd-algo:fdd-analytics-feature-gts-core-algo-routing-logic`
- State ID: `@fdd-state:{state-id}` (Section D of DESIGN, if present)  
  _Example_: `@fdd-state:fdd-analytics-feature-gts-core-state-entity-lifecycle`
- Requirement ID: `@fdd-req:{req-id}` (Section F of DESIGN)  
  _Example_: `@fdd-req:fdd-analytics-feature-gts-core-req-routing`
- Test scenario ID: `@fdd-test:{test-id}` (Section F of DESIGN)  
  _Example_: `@fdd-test:fdd-analytics-feature-gts-core-test-routing-table-lookup`

**Tag placement**:
- At the beginning of new/modified functions, methods, structs, or complex blocks implementing the logic
- At the beginning of test modules/functions that implement test scenarios
- Prefer multiple tags when a block covers multiple IDs (e.g., change + req + algo)

**Examples (multiple IDs allowed)**:
```rust
// @fdd-change:fdd-analytics-feature-schema-query-returns-change-gts-schema-types
// @fdd-req:fdd-analytics-feature-schema-query-returns-req-routing
// @fdd-algo:fdd-analytics-feature-schema-query-returns-algo-routing-logic
pub struct SchemaV1 {
    pub schema_id: String,
    pub version: String,
}
```

```typescript
// @fdd-change:fdd-analytics-feature-schema-query-returns-change-api-rest-endpoints
export async function handleSchemaQuery(
    req: Request
): Promise<SchemaResponse> {
    // Implementation
}
```

**Multiple changes/IDs in same file**:
```python
# @fdd-change:fdd-analytics-feature-schema-query-returns-change-schema-validation
# @fdd-req:fdd-analytics-feature-schema-query-returns-req-validation
def validate_schema_structure(schema: dict):
    pass

# @fdd-change:fdd-analytics-feature-schema-query-returns-change-type-conversion
def convert_gts_to_json_schema(gts_schema):
    pass
```

### 3.2 Tag Verification (agent checklist)

**ALWAYS verify** (before finishing implementation):
- Grep/search code for ALL IDs from CHANGES (change IDs) and DESIGN (flow/algo/state/req/test)
- Confirm tags exist in the files that implement corresponding logic/tests
- If any DESIGN ID has no code tag → report as gap and/or add tag

**Suggested searches**:
- `@fdd-change:` to list change-tagged files
- `@fdd-flow:`, `@fdd-algo:`, `@fdd-state:`, `@fdd-req:`, `@fdd-test:` to confirm DESIGN coverage

### 4. Implement Tasks

**For each task in change**:
1. Read task specification from CHANGES.md (hierarchical format: `1.1.1`, `1.2.1`, etc.)
2. Implement according to adapter conventions
3. Run task validation
4. **Update CHANGES.md**: Change task checkbox from `- [ ]` to `- [x]`
   - Example: `- [ ] 1.1.1 Task description` → `- [x] 1.1.1 Task description`
5. Proceed to next task

**After each task**:
- Show progress: Task {X}/{total} complete
- Ask: Continue to next task? [yes/pause]

### 5. Mark Change Complete

After all tasks done:
1. **Update change status in CHANGES.md**:
   - Change header: `**Status**: 🔄 IN_PROGRESS` → `**Status**: ✅ COMPLETED`
2. **Update summary section**:
   - Increment "Completed" count
   - Decrement "In Progress" or "Not Started" count
3. Verify all task checkboxes marked `- [x]`

---

## Validation

After implementing all changes, run: `feature-code-validate`

**Note**: Validation is now done at feature level (not per-change)

Expected:
- All feature code compiles/runs
- All tests pass (including test scenarios from DESIGN.md)
- All requirements implemented
- No TODO/FIXME in business logic

---

## Next Steps

**After implementing all changes**: 
- Run `feature-code-validate` to validate entire feature
- If validation passes: mark feature as COMPLETE in FEATURES.md
- If validation fails: Fix code, re-validate
