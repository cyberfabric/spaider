---
description: Validate feature code implementation against feature design
---

# Validate Feature Code

**Type**: Validation  
**Role**: Developer, QA  
**Artifact**: Validation report (output to chat)

---

## ⚠️ PRE-FLIGHT CHECKLIST (ALWAYS Complete Before Proceeding)

**Agent ALWAYS verifies before starting this workflow**:

**Navigation Rules Compliance**:
- [ ] ✅ Open and follow `../requirements/execution-protocol.md` (MANDATORY BASE)
- [ ] ✅ Open and follow `../requirements/workflow-execution.md` (General execution)
- [ ] ✅ Open and follow `../requirements/workflow-execution-validations.md` (Validation specifics)

**Workflow-Specific Requirements**:
- [ ] ✅ Open and follow `../requirements/feature-design-structure.md` (Feature design requirements)
- [ ] ✅ Open and follow `../requirements/feature-changes-structure.md` (Changes structure)
- [ ] ✅ Open and follow adapter specs/testing.md (Test requirements)
- [ ] ✅ Open and follow adapter specs/feature-status-validation.md (Status validation)
- [ ] ✅ Check adapter initialization (FDD-Adapter/AGENTS.md exists)
- [ ] ✅ Validate all prerequisites from Prerequisites section below

**Self-Check**:
- [ ] ✅ I have read ALL files listed above
- [ ] ✅ I understand "Maximum Attention to Detail" requirement
- [ ] ✅ I am ready to check EVERY validation criterion individually
- [ ] ✅ I will verify tests pass and build succeeds
- [ ] ✅ I will complete self-test before reporting results

**⚠️ If ANY checkbox is unchecked → STOP and read missing files first**

---

## Overview

**Purpose**: Validate complete feature implementation against feature design using changes for code identification

**Scope**: 
- All code implementing requirements marked as implemented in CHANGES.md
- All test scenarios from feature DESIGN.md Section F
- Complete feature codebase quality

**Key Principle**: Validate the ENTIRE feature code against the feature design, not individual changes

---

## Requirements

**ALWAYS open and follow**:
- `../requirements/feature-design-structure.md` (feature design structure)
- `../requirements/feature-changes-structure.md` (changes structure)
- `{adapter-directory}/FDD-Adapter/specs/testing.md` (test requirements)
- `{adapter-directory}/FDD-Adapter/specs/feature-status-validation.md` (status validation)

Extract:
- Testing scenario requirements from feature DESIGN.md
- Requirements marked as implemented in CHANGES.md
- Adapter build and test commands
- Code quality requirements

---

## Prerequisites

**MUST validate**:
- [ ] Feature DESIGN.md exists and validated (100/100 + 100%)
- [ ] CHANGES source exists and validated (active or archived)
- [ ] At least one change with status IN_PROGRESS or COMPLETED
- [ ] Adapter exists - validate: Required for validation

 **CHANGES source selection**:
 - **Preferred**: Use active `CHANGES.md` in the feature directory.
 - **Fallback**: If active `CHANGES.md` does not exist, use the most recent archived changes file in `archive/`.
   - Choose the newest `YYYY-MM-DD-CHANGES.md` (lexicographically latest date).

---

## Steps

### 1. Identify Feature Scope

**Read feature artifacts**:
1. Open feature DESIGN.md
2. Open feature CHANGES source (active `CHANGES.md` or latest archived `archive/YYYY-MM-DD-CHANGES.md`)
3. Extract feature slug from paths

**Extract validation scope**:
- All requirements from DESIGN.md Section F
- All testing scenarios from DESIGN.md Section F
- All changes from CHANGES source (to identify code locations)

### 2. Build Codebase Map

**Use CHANGES.md to identify code**:
1. Extract all file paths from all changes (tasks section)
2. Extract all @fdd-change tags used
3. Build list of files implementing feature requirements

**Locate feature code by tags**:
- Search for `@fdd-change:fdd-{project}-{feature}-change-` across the codebase scope defined by the adapter.
- Collect all files containing these tags.

**Result**: Complete list of files implementing this feature

### 3. Validate Requirements Implementation

**For each requirement in DESIGN.md Section F marked as IMPLEMENTED**:

**Check requirement status in CHANGES.md**:
- Find which change(s) implement this requirement (via **Implements**: field)
- Verify change status is COMPLETED
- If any implementing change is NOT_STARTED or IN_PROGRESS → requirement is NOT implemented

**Verify code exists**:
- Check that files specified in change tasks exist
- Check that @fdd-change tags exist in code
- Verify code is not placeholder/stub (no TODO/FIXME/unimplemented!)

**Validation**:
- ✅ Requirement ID found in CHANGES.md **Implements**: field
- ✅ All implementing changes have status COMPLETED
- ✅ Code files exist and contain implementation
- ✅ No TODO/FIXME in implementation code
- ✅ No unimplemented!() in business logic

### 4. Validate Test Scenarios Implementation

**CRITICAL**: All testing scenarios from DESIGN.md Section F MUST be implemented

**For each testing scenario in DESIGN.md Section F**:

**Check test exists**:
1. Extract testing scenario ID: `fdd-{project}-feature-{feature-slug}-test-{scenario-name}`
2. Search for test referencing this scenario ID:
    - Search within test locations defined by the adapter (unit, integration, e2e).

**Verify test implementation**:
- ✅ Test file exists (unit/integration/e2e per adapter)
- ✅ Test contains scenario ID in comment for traceability
- ✅ Test is NOT #[ignore] without justification
- ✅ Test actually validates scenario behavior (not placeholder)
- ✅ Test follows adapter testing conventions

**Validation**:
- ✅ Test scenario ID found in test file
- ✅ Test implements scenario logic
- ✅ Test is not ignored or placeholder
- ✅ Test can be executed

### 5. Execute Build Validation

**Run build**:
- Execute the build command from `{adapter-directory}/FDD-Adapter/specs/build-deploy.md`.

**Check**:
- ✅ Build succeeds
- ✅ No compilation errors
- ✅ No compiler warnings (or acceptable per adapter)

**Score**: 15 points

### 6. Execute Linter Validation

**Run linters**:
- Execute the lint command(s) from `{adapter-directory}/FDD-Adapter/specs/conventions.md` or `{adapter-directory}/FDD-Adapter/specs/build-deploy.md`.

**Check**:
- ✅ Linter passes
- ✅ No linter errors
- ✅ No linter warnings (or acceptable per adapter)

**Score**: 10 points

### 7. Execute Test Validation

**Run all tests**:
- Execute the test command(s) from `{adapter-directory}/FDD-Adapter/specs/testing.md`.

**Check**:
- ✅ All unit tests pass
- ✅ All integration tests pass
- ✅ All e2e tests pass (if applicable)
- ✅ No ignored tests without justification
- ✅ Coverage meets adapter threshold

**Score**: 30 points

### 8. Code Quality Validation

**Check for incomplete work**:
- Search the feature code set (identified via `@fdd-change` tags) for incomplete work markers: `TODO`, `FIXME`, `XXX`, `HACK`.
- Search feature business logic code (domain/service layers per adapter) for incomplete implementation markers: `unimplemented!`, `todo!`.
- Search test code for ignored tests (e.g., `#[ignore]`) and validate justification per adapter rules.

**Check per adapter feature-status-validation.md**:
- ✅ No TODO/FIXME in domain/service layers
- ✅ No unimplemented!() in business logic
- ✅ No bare unwrap() or panic in production code
- ✅ Error handling complete
- ✅ No ignored tests without documented reason
- ✅ No placeholder tests (assert!(true))

**Score**: 15 points

### 9. Calculate Score

**Scoring breakdown**:
- Requirements Implementation (30 pts): All requirements marked IMPLEMENTED actually implemented
- Test Scenarios Implementation (20 pts): All test scenarios from DESIGN.md implemented
- Build Success (15 pts): Build succeeds without errors
- Linter Pass (10 pts): Linter succeeds without errors
- Test Pass (30 pts): All tests pass, coverage meets threshold
- Code Quality (15 pts): No TODO/FIXME/unimplemented in business logic
- Code Tagging (10 pts): All feature code tagged with @fdd-change

**Total**: 130 points
**Pass threshold**: ≥110/130 (≈85%)

### 10. Output Results to Chat

**Format**:
```markdown
## Validation: Feature Code ({feature-slug})

**Score**: {X}/130  
**Status**: PASS | FAIL  
**Threshold**: ≥110/130

---

### Findings

**Requirements Implementation** ({X}/30):
✅ | ❌ Requirement {req-id}: {status} (Change {change-id}: {change-status})

**Test Scenarios Implementation** ({X}/20):
✅ | ❌ Test scenario {test-id}: {implemented | NOT IMPLEMENTED}
  - Test file: {path} or NOT FOUND
  - Test status: {pass | fail | ignored | placeholder}

**Build Status** ({X}/15):
✅ | ❌ Build: {success | failed}
✅ | ❌ Compiler warnings: {count}

**Linter Status** ({X}/10):
✅ | ❌ Linter: {success | failed}
✅ | ❌ Linter warnings: {count}

**Test Execution** ({X}/30):
✅ | ❌ Unit tests: {X}/{total} passed
✅ | ❌ Integration tests: {X}/{total} passed
✅ | ❌ E2E tests: {X}/{total} passed
✅ | ❌ Coverage: {X}% (threshold: {Y}%)

**Code Quality** ({X}/15):
✅ | ❌ No TODO/FIXME in domain/service: {found count}
✅ | ❌ No unimplemented! in business logic: {found count}
✅ | ❌ No ignored tests without reason: {found count}
✅ | ❌ Error handling complete

**Code Tagging** ({X}/10):
✅ | ❌ All feature code tagged with:
   - @fdd-change:{change-id} (from CHANGES source)
   - @fdd-flow:{flow-id}, @fdd-algo:{algo-id}, @fdd-state:{state-id}, @fdd-req:{req-id}, @fdd-test:{test-id} (from feature DESIGN.md)
✅ | ❌ Validator searched code for ALL IDs from DESIGN.md (Sections B/C/D/F) and CHANGES source

---

### Recommendations

**Critical**:
1. {Fix}

**High Priority**:
1. {Fix}

**Medium Priority**:
1. {Fix}

---

### Next Steps

**If PASS**:
✅ Feature code validated! Update feature status as COMPLETE in FEATURES.md
✅ Proceed to next feature

**If FAIL**: Fix issues above, re-run `feature-code-validate`

---

### Self-Test Confirmation

**Agent confirms**:
✅ Read execution-protocol.md before starting
✅ Read all required files from pre-flight checklist
✅ Checked EVERY requirement individually
✅ Checked EVERY test scenario individually
✅ Ran build, lint, and test commands
✅ Checked for TODO/FIXME/unimplemented systematically
✅ Used adapter commands for systematic verification
✅ Completed self-test before reporting

Self-test passed: YES

---

## Validation

Self-validating workflow

---

## Next Steps

**If PASS**:
- Update FEATURES.md: Mark feature status as COMPLETE
- If more features exist: Design next feature
- If all features complete: Project complete 

**If FAIL**: 
- Fix code issues
- Re-run `feature-code-validate`
- Do NOT mark feature as COMPLETE until PASS

---

## Difference from Previous Per-Change Validation

**OLD**: Validated individual change implementations  
**NEW**: Validates ENTIRE feature code against feature design

**Key differences**:
1. **Scope**: Entire feature vs single change
2. **Test scenarios**: ALL scenarios from DESIGN.md must be implemented
3. **Requirements**: ALL requirements marked IMPLEMENTED must be coded
4. **Code identification**: Uses CHANGES.md to find feature code
5. **Quality**: Complete feature quality checks (build, lint, tests, TODO/FIXME)

**Why better**:
- Validates feature as a whole (not fragmented)
- Ensures test scenarios are implemented (not just specified)
- Catches cross-change integration issues
- Validates complete feature quality before completion
- Single validation for entire feature code

---

## References

**Related workflows**:
- `feature-validate.md` - Validates feature DESIGN.md
- `feature-changes-validate.md` - Validates CHANGES.md structure
- `feature-change-implement.md` - Implement specific change

**Related requirements**:
- `feature-design-structure.md` - Feature design structure
- `feature-changes-structure.md` - Changes structure
- Adapter specs/testing.md - Test requirements
- Adapter specs/feature-status-validation.md - Status validation rules
