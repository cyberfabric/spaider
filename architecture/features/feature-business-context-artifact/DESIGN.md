# Feature: Business Context Artifact

## A. Feature Context

**Feature ID**: `fdd-fdd-feature-business-context-artifact`
**Status**: IN_DESIGN

### 1. Overview
This feature defines the lifecycle of the Business Context artifact (`architecture/BUSINESS.md`) by standardizing how it is created, updated, and validated through executable workflows and deterministic validation.

### 2. Purpose
Ensure business requirements are captured in a consistent, machine-readable format and can be validated deterministically before downstream architecture and implementation workflows proceed.

### 3. Actors
- `fdd-fdd-actor-product-manager`
- `fdd-fdd-actor-architect`
- `fdd-fdd-actor-ai-assistant`

### 4. References
- Overall Design: [DESIGN](../../DESIGN.md)
- Feature Manifest: [FEATURES](../FEATURES.md)
- Business Context Artifact: [BUSINESS](../../BUSINESS.md)
- Operation Workflow: [business-context](../../../workflows/business-context.md)
- Validation Workflow: [business-validate](../../../workflows/business-validate.md)
- Artifact Structure Requirements: [business-context-structure](../../../requirements/business-context-structure.md)

## B. Actor Flows (FDL)

### Business context update flow

- [ ] **ID**: `fdd-fdd-feature-business-context-artifact-flow-business-context-update`

<!-- fdd-id-content -->
1. [ ] - `ph-1` - Product Manager initiates a change to `architecture/BUSINESS.md` via the `business-context` operation workflow - `inst-initiate-business-context-change`
2. [ ] - `ph-1` - AI assistant gathers required inputs section-by-section and proposes content updates - `inst-collect-inputs`
3. [ ] - `ph-1` - **IF** user confirms changes: - `inst-if-user-confirms`
   1. [ ] - `ph-1` - Apply the change to `architecture/BUSINESS.md` - `inst-apply-change`
4. [ ] - `ph-1` - Run the `business-validate` validation workflow - `inst-run-business-validate`
5. [ ] - `ph-1` - **RETURN** validation result (PASS or FAIL) - `inst-return-validation-result`
<!-- fdd-id-content -->

## C. Algorithms (FDL)

### Validate business context artifact

- [ ] **ID**: `fdd-fdd-feature-business-context-artifact-algo-validate-business-context`

<!-- fdd-id-content -->
Input: business_md_path, requirements_path  
Output: validation_report

1. [ ] - `ph-1` - Parse `architecture/BUSINESS.md` into sections and items - `inst-parse-business-md`
2. [ ] - `ph-1` - Verify required sections exist per `business-context-structure.md` - `inst-verify-required-sections`
3. [ ] - `ph-1` - Verify all actor IDs are well-formed and unique - `inst-verify-actor-ids`
4. [ ] - `ph-1` - Verify all capability IDs are well-formed and unique - `inst-verify-capability-ids`
5. [ ] - `ph-1` - **IF** any structural issue exists: - `inst-if-structural-issue`
   1. [ ] - `ph-1` - **RETURN** FAIL report - `inst-return-fail`
6. [ ] - `ph-1` - **RETURN** PASS report - `inst-return-pass`
<!-- fdd-id-content -->

## D. States (FDL)

### Business context lifecycle state

- [ ] **ID**: `fdd-fdd-feature-business-context-artifact-state-business-context-lifecycle`

<!-- fdd-id-content -->
1. [ ] - `ph-1` - **FROM** DRAFT **TO** VALIDATED **WHEN** `business-validate` passes - `inst-draft-to-validated`
2. [ ] - `ph-1` - **FROM** VALIDATED **TO** DRAFT **WHEN** a new edit is proposed - `inst-validated-to-draft`
<!-- fdd-id-content -->

## E. Technical Details

### 1. Database Schema
This feature does not introduce a database schema.

### 2. API Endpoints
This feature does not define API endpoints. It relies on local file operations and deterministic validation.

### 3. Security
- Only repository contributors should modify `architecture/BUSINESS.md`.
- Validation must be deterministic and must not execute untrusted code.

### 4. Error Handling
- If `architecture/BUSINESS.md` is missing or unreadable, validation must fail with a clear file-system error.
- If required sections or IDs are missing/invalid, validation must fail and list all issues.

## F. Requirements

### Business context structure requirements are defined

- [ ] **ID**: `fdd-fdd-feature-business-context-artifact-req-structure-requirements-defined`

<!-- fdd-id-content -->
**Status**: ✅ IMPLEMENTED
**Description**: The system MUST define the required and optional structure of `architecture/BUSINESS.md` in `requirements/business-context-structure.md`, including required sections, optional sections, ID formats, ID placement rules, and validation rules.
**References**:
- [business-context-structure](../../../requirements/business-context-structure.md)
**Implements**:
- `fdd-fdd-feature-business-context-artifact-algo-validate-business-context`
**Phases**:
- [ ] `ph-1`: Provide structure requirements for `architecture/BUSINESS.md`
**Tests Covered**:
- `fdd-fdd-feature-business-context-artifact-test-structure-requirements-present`
**Acceptance Criteria**:
- A dedicated requirements file exists at `requirements/business-context-structure.md`.
- The requirements file explicitly states required sections (A: Vision, B: Actors, C: Capabilities).
- The requirements file explicitly states optional sections (D: Use Cases, E: Additional Context) and which are validated.
- The requirements file defines required identifiers and where they appear:
  - Actor IDs (`fdd-{project}-actor-{name}`) in the ID line immediately after `####` actor headings.
  - Capability IDs (`fdd-{project}-capability-{name}`) in the ID line immediately after `####` capability headings.
  - Use case IDs (`fdd-{project}-usecase-{name}`) if Section D is present.
- The requirements file defines how to validate `architecture/BUSINESS.md` deterministically.
<!-- fdd-id-content -->

### Business context operation workflow exists

- [ ] **ID**: `fdd-fdd-feature-business-context-artifact-req-operation-workflow-exists`

<!-- fdd-id-content -->
**Status**: ✅ IMPLEMENTED
**Description**: The system MUST provide an operation workflow to create or update `architecture/BUSINESS.md`.
**References**:
- [business-context workflow](../../../workflows/business-context.md)
**Implements**:
- `fdd-fdd-feature-business-context-artifact-flow-business-context-update`
**Phases**:
- [ ] `ph-1`: Provide operation workflow for `architecture/BUSINESS.md`
**Tests Covered**:
- `fdd-fdd-feature-business-context-artifact-test-operation-workflow-present`
**Acceptance Criteria**:
- There is an operation workflow file at `workflows/business-context.md`.
- The workflow references `requirements/business-context-structure.md`.
<!-- fdd-id-content -->

### Business context validation workflow exists

- [ ] **ID**: `fdd-fdd-feature-business-context-artifact-req-validation-workflow-exists`

<!-- fdd-id-content -->
**Status**: ✅ IMPLEMENTED
**Description**: The system MUST provide a validation workflow for `architecture/BUSINESS.md`.
**References**:
- [business-validate workflow](../../../workflows/business-validate.md)
**Implements**:
- `fdd-fdd-feature-business-context-artifact-algo-validate-business-context`
**Phases**:
- [ ] `ph-1`: Provide validation workflow for `architecture/BUSINESS.md`
**Tests Covered**:
- `fdd-fdd-feature-business-context-artifact-test-validation-workflow-present`
**Acceptance Criteria**:
- There is a validation workflow file at `workflows/business-validate.md`.
- The workflow references `requirements/business-context-structure.md`.
<!-- fdd-id-content -->

## G. Testing Scenarios

### Structure requirements file is present

- [ ] **ID**: `fdd-fdd-feature-business-context-artifact-test-structure-requirements-present`

<!-- fdd-id-content -->
**Validates**: `fdd-fdd-feature-business-context-artifact-req-structure-requirements-defined`
1. [ ] - `ph-1` - Confirm `requirements/business-context-structure.md` exists in the repository - `inst-confirm-structure-requirements-exists`
2. [ ] - `ph-1` - Confirm the file explicitly marks required sections and optional sections for `architecture/BUSINESS.md` - `inst-confirm-structure-required-optional-sections`
3. [ ] - `ph-1` - Confirm the file defines ID formats and ID placement rules for actors, capabilities, and use cases - `inst-confirm-structure-id-rules`
4. [ ] - `ph-1` - Confirm the file describes how to validate `architecture/BUSINESS.md` - `inst-confirm-structure-validation-rules`
5. [ ] - `ph-1` - Verify the requirement is satisfied - `inst-verify-structure-requirements-satisfied`
<!-- fdd-id-content -->

### Operation workflow file is present

- [ ] **ID**: `fdd-fdd-feature-business-context-artifact-test-operation-workflow-present`

<!-- fdd-id-content -->
**Validates**: `fdd-fdd-feature-business-context-artifact-req-operation-workflow-exists`
1. [ ] - `ph-1` - Confirm `workflows/business-context.md` exists in the repository - `inst-confirm-operation-workflow-exists`
2. [ ] - `ph-1` - Confirm the workflow references `requirements/business-context-structure.md` - `inst-confirm-operation-workflow-references-requirements`
3. [ ] - `ph-1` - Verify the requirement is satisfied - `inst-verify-operation-workflow-satisfied`
<!-- fdd-id-content -->

### Validation workflow file is present

- [ ] **ID**: `fdd-fdd-feature-business-context-artifact-test-validation-workflow-present`

<!-- fdd-id-content -->
**Validates**: `fdd-fdd-feature-business-context-artifact-req-validation-workflow-exists`
1. [ ] - `ph-1` - Confirm `workflows/business-validate.md` exists in the repository - `inst-confirm-validation-workflow-exists`
2. [ ] - `ph-1` - Confirm the workflow references `requirements/business-context-structure.md` - `inst-confirm-validation-workflow-references-requirements`
3. [ ] - `ph-1` - Verify the requirement is satisfied - `inst-verify-validation-workflow-satisfied`
<!-- fdd-id-content -->
