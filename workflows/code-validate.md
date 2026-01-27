---
fdd: true
type: workflow
name: Code Validate
version: 1.0
purpose: Validate code implementation against an FDD artifact
---

# Validate Code

**Type**: Validation  
**Role**: Developer, QA  
**Artifact**: Validation report (output to chat)

---

## Prerequisite Checklist

- [ ] Agent has read execution-protocol.md
- [ ] Agent has read workflow-execution.md
- [ ] Agent understands this workflow's purpose

---


ALWAYS open and follow `../requirements/workflow-execution.md` WHEN executing this workflow

## ⚠️ PRE-FLIGHT CHECKLIST (ALWAYS Complete Before Proceeding)

**Agent ALWAYS verifies before starting this workflow**:

**Navigation Rules Compliance**:
- [ ] ✅ Open and follow `../requirements/execution-protocol.md` (MANDATORY BASE)
- [ ] ✅ Open and follow `../requirements/workflow-execution.md` (General execution)
- [ ] ✅ Open and follow `../requirements/workflow-execution-validations.md` (Validation specifics)

**Workflow-Specific Requirements**:
- [ ] ✅ Open and follow the requirements file for the selected artifact kind (when `format: FDD`)
- [ ] ✅ Check adapter initialization (FDD-Adapter/AGENTS.md exists)
- [ ] ✅ Validate all prerequisites from Prerequisites section below

**Self-Check**:
- [ ] ✅ I have read ALL files listed above
- [ ] ✅ I understand "Maximum Attention to Detail" requirement
- [ ] ✅ I am ready to check EVERY validation criterion individually
- [ ] ✅ I will verify tests pass and build succeeds
- [ ] ✅ I will complete self-test before reporting results
- [ ] ✅ I will validate adherence to engineering best practices required by `code.md` (TDD, SOLID, DRY, KISS, YAGNI)

**⚠️ If ANY checkbox is unchecked → STOP and read missing files first**

---

## Overview

**Purpose**: Validate implementation against an FDD artifact

**Scope**:
- Code and tests relevant to the selected artifact scope

**Key Principle**: Validate implementation against the selected artifact input and report gaps deterministically

---

## Requirements

Extract:
- The artifact IDs and checkboxes/statuses that represent "implemented" scope (when applicable)
- Adapter build and test commands
- Code quality requirements

---

## Prerequisites

**MUST validate**:
- [ ] Adapter exists - validate: Required for validation

**If missing**: Ask the user whether to:
- Create/validate prerequisites via the corresponding workflows
- Provide inputs in another form (path, link, or pasted text in any format)
- Proceed anyway (reduce scope to content-only checks and report missing cross-references)

---

## Steps

### 1. Identify Validation Scope

Ask the user for the artifact input as one of:
- Registered artifact path (preferred)
- Link
- Pasted text

If the artifact cannot be validated as an FDD artifact (registry says `format != "FDD"` or user provides non-FDD input):
- Perform content-only checks
- Suggest converting to FDD via the appropriate workflow

### 2. Build Codebase Map

Locate relevant code by IDs/tags (when available):
- If the selected artifact is an FDD artifact with IDs: search for matching `@fdd-*` tags in the codebase scope defined by the adapter
- Otherwise: ask the user for target directories/files to validate

### 3. Validate Implementation Coverage

For each selected ID/scope marked as implemented (when applicable):

**Verify code exists**:
- Verify code is not placeholder/stub (no TODO/FIXME/unimplemented!)

**Validation**:
- ✅ Code files exist and contain implementation
- ✅ No TODO/FIXME in implementation code
- ✅ No unimplemented!() in business logic

### 4. Validate Conformance (When IDs Exist)

Collect artifact IDs (when present) and validate that they are represented in code and tests.

**Check implementation and non-deviation**:
- Search the codebase for all `@fdd-` tags and verify EVERY occurrence includes a phase postfix `:ph-{N}` (N is an integer).
- For each Flow ID: locate code tagged with `@fdd-flow:{id}:ph-{N}` and verify the control flow matches the described steps (no skipped/extra steps that change behavior).
- For each Algorithm ID: locate code tagged with `@fdd-algo:{id}:ph-{N}` and verify logic matches described algorithm; no TODO/unimplemented!/panic/unwrap stubs; performance/complexity expectations respected.
- For each State ID (if any): locate code tagged with `@fdd-state:{id}:ph-{N}` and verify state transitions match the design; forbidden states/transitions absent.
- Technical details (Section E): verify endpoints, security, error handling, OData parameters, and delegation points align with design and adapter specs (`modkit-rest-integration.md`, `patterns.md`, `conventions.md`); ensure OperationBuilder usage and api_gateway integration are intact (no direct axum routes, no custom middleware).

**Validation**:
- ✅ All `@fdd-*` code tags include mandatory phase postfix `:ph-{N}`
- ✅ All design IDs (flows/algorithms/states/requirements/tests) found in code and mapped to implementations
- ✅ Implementations follow design steps/logic; no divergent behavior
- ✅ No missing or extra endpoints/paths versus design Section E
- ✅ No placeholder/stub code in mapped implementations

### 5. Validate Test Scenarios (When Present)

If the selected artifact defines test scenarios, verify they are implemented.

**Check test exists**:
1. Extract testing scenario ID(s) from the selected artifact
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

### 6. Execute Build Validation

**Run build**:
- Execute the build command from `{adapter-directory}/specs/build-deploy.md`.

**Check**:
- ✅ Build succeeds
- ✅ No compilation errors
- ✅ No compiler warnings (or acceptable per adapter)

**Score**: 15 points

### 7. Execute Linter Validation

**Run linters**:
- Execute the lint command(s) from `{adapter-directory}/specs/conventions.md` or `{adapter-directory}/specs/build-deploy.md`.

**Check**:
- ✅ Linter passes
- ✅ No linter errors
- ✅ No linter warnings (or acceptable per adapter)

**Score**: 10 points

### 8. Execute Test Validation

**Run all tests**:
- Execute the test command(s) from `{adapter-directory}/specs/testing.md`.

**Check**:
- All unit tests pass
- All integration tests pass
- All e2e tests pass (if applicable)
- No ignored tests without justification
- Coverage meets adapter threshold

**Score**: 30 points

### 9. Code Quality Validation

**Check for incomplete work**:
- Search the relevant code set for incomplete work markers: `TODO`, `FIXME`, `XXX`, `HACK`.
- Search business logic code (domain/service layers per adapter) for incomplete implementation markers: `unimplemented!`, `todo!`.
- Search test code for ignored tests (e.g. `#[ignore]`) and validate justification per adapter rules.

**Check per adapter conventions.md**:
- No TODO/FIXME in domain/service layers
- No unimplemented!() in business logic
- No bare unwrap() or panic in production code
- Error handling complete
- No ignored tests without documented reason
- No placeholder tests (assert!(true))

**Engineering best practices (required by `code.md`)**:
- TDD: New/changed behavior is covered by tests, and tests meaningfully assert the expected outcomes.
- SOLID: Responsibilities are separated; no single function/module mixes unrelated concerns; dependencies are injectable where appropriate.
- DRY: No copy-paste duplication across feature code and tests without clear justification.
- KISS: No unnecessary complexity introduced to satisfy the design.
- YAGNI: No speculative abstractions, configuration, or extension points beyond the validated design scope.

**Score**: 15 points

### 10. Validate Code Logic Consistency with Design

**Purpose**: Verify code logic does not contradict design specifications

**After all technical checks pass (build/lint/tests), perform deep design-code consistency check**:

**For each requirement in DESIGN.md Section F marked IMPLEMENTED**:
1. Read requirement specification carefully
2. Locate implementing code via @fdd-req tags (or @fdd-flow/@fdd-algo/@fdd-state tags when relevant).
3. Analyze code logic and compare with requirement description
4. Check for contradictions:
   - ❌ Code does opposite of what design specifies
   - ❌ Code skips mandatory steps from design
   - ❌ Code adds behavior not in design that changes semantics
   - ❌ Code uses different algorithm/approach that violates design constraints
   - ❌ Error handling contradicts design error specifications

**For each flow in DESIGN.md Section B marked implemented**:
1. Read flow steps and control logic
2. Locate flow implementation via @fdd-flow tags
3. Trace execution path through code
4. Verify:
   - ✅ All flow steps executed in correct order
   - ✅ No steps bypassed that would change behavior
   - ✅ Conditional logic matches design conditions
   - ✅ Error paths match design error handling

**For each algorithm in DESIGN.md Section C marked implemented**:
1. Read algorithm specification and complexity requirements
2. Locate algorithm implementation via @fdd-algo tags
3. Analyze implementation logic
4. Verify:
   - ✅ Algorithm logic matches design specification
   - ✅ Performance characteristics match design (O(n), O(1), etc.)
   - ✅ Edge cases handled as designed
   - ✅ No logic shortcuts that violate design constraints

**For technical details in DESIGN.md Section E**:
1. Read endpoint specifications, security requirements, OData parameters
2. Verify code implementation matches specifications:
   - ✅ Endpoints match paths/methods from design
   - ✅ Security checks match design requirements
   - ✅ Query parameters match OData specifications
   - ✅ Response formats match design schemas
   - ✅ Delegation points implemented as designed

**Validation**:
- ✅ No contradictions found between code logic and design
- ✅ All requirements implemented as specified (not diverged)
- ✅ Flows execute exactly as designed
- ✅ Algorithms match design specifications
- ✅ Technical implementation matches Section E specs

**Documentation**:
- List any logic divergences found
- Categorize: CRITICAL (contradicts design) vs MINOR (style deviation)
- CRITICAL divergences = validation FAIL

**Score**: 20 points

### 11. Calculate Score

**Scoring breakdown**:
- Requirements Implementation (30 pts): All requirements marked IMPLEMENTED actually implemented
- Design Conformance (20 pts): Flows/algorithms/states/technical details from DESIGN implemented without deviation
- Test Scenarios Implementation (20 pts): All test scenarios from DESIGN.md implemented
- Build Success (15 pts): Build succeeds without errors
- Linter Pass (10 pts): Linter succeeds without errors
- Test Pass (30 pts): All tests pass, coverage meets threshold
- Code Quality (15 pts): No TODO/FIXME/unimplemented in business logic
- Code Logic Consistency (20 pts): Code logic does not contradict design specifications
- Code Tagging (10 pts): Feature code tagged with relevant feature DESIGN.md IDs (`@fdd-flow`, `@fdd-algo`, `@fdd-state`, `@fdd-req`, `@fdd-test`)

**Total**: 150 points
**Pass threshold**: ≥128/150 (≈85%)

### 12. Output Results to Chat

**Format**:
```markdown
## Validation Report: Code ({artifact-scope})

### Summary
- **Status**: **PASS** ✅ | **FAIL** ❌
- **Score**: **{X}/150**
- **Threshold**: **≥128/150**

---

### Findings

#### 1) Requirements Implementation — **{X}/30**
- ✅ | ❌ Requirement {req-id}: {status} (Change {change-id}: {change-status})

#### 2) Test Scenarios Implementation — **{X}/20**
- ✅ | ❌ Test scenario {test-id}: {implemented | NOT IMPLEMENTED}
  - Test file: {path} or NOT FOUND
  - Test status: {pass | fail | ignored | placeholder}

#### 3) Build Status — **{X}/15**
- ✅ | ❌ Build: {success | failed}
- ✅ | ❌ Compiler warnings: {count}

#### 4) Linter Status — **{X}/10**
- ✅ | ❌ Linter: {success | failed}
- ✅ | ❌ Linter warnings: {count}

#### 5) Test Execution — **{X}/30**
- ✅ | ❌ Unit tests: {X}/{total} passed
- ✅ | ❌ Integration tests: {X}/{total} passed
- ✅ | ❌ E2E tests: {X}/{total} passed
- ✅ | ❌ Coverage: {X}% (threshold: {Y}%)

#### 6) Code Quality — **{X}/15**
- ✅ | ❌ No TODO/FIXME in domain/service: {found count}
- ✅ | ❌ No unimplemented! in business logic: {found count}
- ✅ | ❌ No ignored tests without reason: {found count}
- ✅ | ❌ Error handling complete
- ✅ | ❌ Engineering best practices followed *(TDD, SOLID, DRY, KISS, YAGNI)*

#### 7) Code Logic Consistency — **{X}/20**
- ✅ | ❌ Requirements logic matches design specifications
- ✅ | ❌ Flow execution matches design steps
- ✅ | ❌ Algorithm implementation matches design specifications
- ✅ | ❌ Technical details match Section E specifications
- ✅ | ❌ No **CRITICAL** divergences found
  - List of divergences: {CRITICAL: [...] | MINOR: [...]}

#### 8) Code Tagging — **{X}/10**
- ✅ | ❌ All relevant code tagged with artifact IDs when applicable (phase is always a postfix, no standalone phase tags):
  - @fdd-flow:{flow-id}:ph-{N}, @fdd-algo:{algo-id}:ph-{N}, @fdd-state:{state-id}:ph-{N}, @fdd-req:{req-id}:ph-{N}, @fdd-test:{test-id}:ph-{N}

---

### Recommendations

#### Critical
1. **{Fix}**

#### High Priority
1. **{Fix}**

#### Medium Priority
1. **{Fix}**

---

### Next Steps

#### If PASS
- ✅ Feature code validated! Update feature status as COMPLETE in FEATURES.md
- ✅ Proceed to next feature

#### If FAIL
- ❌ Fix issues above, then re-run `code-validate`

---

### Self-Test Confirmation

**Agent confirms**:
- ✅ Read execution-protocol.md before starting
- ✅ Read all required files from pre-flight checklist
- ✅ Checked EVERY requirement individually

Self-test passed: YES

---
```

### 13. Semantic Expert Review (Always)

Run an expert panel review of the codebase changes and implementation quality after producing the validation output.

If a design artifact is available (registered `format: FDD` artifact path, or provided as a path/link/text by the user), experts MUST also evaluate design-to-code alignment.

**Critical requirement**: This step MUST produce an explicit section in chat titled `### Semantic Expert Review` that confirms the review was executed.

**Experts**:
- Developer
- QA Engineer
- Security Expert
- Performance Engineer
- DevOps Engineer
- Architect
- DCO Engineer
- Monitoring Engineer
- UX Engineer
- Product Manager
- Legal Counsel
- Compliance Engineer
- Data Engineer
- Cloud Engineer
- Infrastructure Engineer
- Database Architect
- Data Engineer
- Legal Counsel
- Compliance Engineer
- UX Engineer

**Instructions (MANDATORY)**:
- [ ] Execute this checklist for EACH expert listed above (do not skip any expert)
- [ ] Adopt the role of the current expert (write: `Role assumed: {expert}`)
- [ ] Review the actual code and tests changed/added in this validation scope
- [ ] If a design artifact was provided or is available:
  - [ ] Evaluate design-to-code alignment (no invented semantics)
  - [ ] If design is missing/insufficient for current behavior, propose updating design before changing behavior
- [ ] Identify issues (list each item explicitly):
  - [ ] Contradictions vs design intent (when design exists)
  - [ ] Missing behavior (requirements/tests)
  - [ ] Unclear intent (naming/structure)
  - [ ] Unnecessary complexity (YAGNI, premature abstraction)
  - [ ] Missing non-functional concerns (security/perf/observability) when required by design/adapter specs
- [ ] Provide concrete proposals:
  - [ ] What to remove (dead code, unused abstractions)
  - [ ] What to add (tests, error handling, validation, observability)
  - [ ] What to rewrite (simpler structure, clearer naming, separation of concerns)
- [ ] Propose the corrective workflow:
  - [ ] If design must change: `feature` or `design` (UPDATE mode)
  - [ ] If only code must change: `code` (continue implementation)

**Required output format** (append to chat):
```markdown
### Semantic Expert Review

**Review status**: **COMPLETED** ✅  
**Reviewed artifact**: `Code ({artifact-scope})`  
**Experts reviewed**: *Developer, QA Engineer, Security Expert, Performance Engineer, DevOps Engineer*

*Rule*: For EACH expert listed in the workflow, include a `#### Expert: {expert}` section below. Do not omit any expert.

#### Expert: {expert}
- **Role assumed**: {expert}
- **Checklist completed**: **YES** ✅
- **Findings**:
  - **Contradictions**: ...
  - **Missing behavior**: ...
  - **Unclear intent**: ...
  - **Unnecessary complexity**: ...
- **Proposed edits**:
  - **Remove**: "..." → **Reason**: ...
  - **Add**: ...
  - **Rewrite**: "..." → "..."
 
*Repeat the `#### Expert: {expert}` block for each expert above.*

---
 
**Recommended corrective workflow**: `{feature | design | code}` *(choose per findings)*
```

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
- Re-run `code-validate`
- Do NOT mark feature as COMPLETE until PASS

---

## Validation Criteria

- [ ] All workflow steps completed
- [ ] Output artifacts are valid

---


## Validation Checklist

- [ ] All prerequisites were met
- [ ] All steps were executed in order
- [ ] Engineering best practices adherence was validated (TDD, SOLID, DRY, KISS, YAGNI)

---

## References

None