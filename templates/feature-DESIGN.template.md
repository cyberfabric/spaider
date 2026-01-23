# Feature: {Feature Name}

## A. Feature Context

**Feature ID**: `fdd-{project-name}-feature-{feature-slug}`
**Status**: NOT_STARTED

### 1. Overview

{Brief overview of what this feature does}

### 2. Purpose

{Why this feature exists, what problem it solves}

### 3. Actors

- `fdd-{project-name}-actor-{actor-slug}` - {Role in this feature}

### 4. References

- Overall Design: [DESIGN.md](../../DESIGN.md)
- Dependencies: {List feature dependencies or "None"}

## B. Actor Flows (FDL)

### {Flow Name}

- [ ] **ID**: `fdd-{project-name}-feature-{feature-slug}-flow-{flow-slug}`

<!-- fdd-id-content -->
**Actor**: `fdd-{project-name}-actor-{actor-slug}`

**Success Scenarios**:
- {Scenario 1}

**Error Scenarios**:
- {Error scenario 1}

**Steps**:
1. [ ] - `ph-1` - {Step description} - `inst-{step-id}`
2. [ ] - `ph-1` - **IF** {condition} - `inst-{step-id}`
   1. [ ] - `ph-1` - {Action if true} - `inst-{step-id}`
3. [ ] - `ph-1` - **ELSE** - `inst-{step-id}`
   1. [ ] - `ph-1` - {Action if false} - `inst-{step-id}`
4. [ ] - `ph-1` - **RETURN** {result} - `inst-{step-id}`
<!-- fdd-id-content -->

<!-- TODO: Add more flows as needed -->

## C. Algorithms (FDL)

### {Algorithm Name}

- [ ] **ID**: `fdd-{project-name}-feature-{feature-slug}-algo-{algo-slug}`

<!-- fdd-id-content -->
**Input**: {Input description}
**Output**: {Output description}

**Steps**:
1. [ ] - `ph-1` - {Step description} - `inst-{step-id}`
2. [ ] - `ph-1` - **FOR EACH** {item} in {collection} - `inst-{step-id}`
   1. [ ] - `ph-1` - {Process item} - `inst-{step-id}`
3. [ ] - `ph-1` - **TRY** - `inst-{step-id}`
   1. [ ] - `ph-1` - {Risky operation} - `inst-{step-id}`
4. [ ] - `ph-1` - **CATCH** {error} - `inst-{step-id}`
   1. [ ] - `ph-1` - {Handle error} - `inst-{step-id}`
5. [ ] - `ph-1` - **RETURN** {result} - `inst-{step-id}`
<!-- fdd-id-content -->

<!-- TODO: Add more algorithms as needed -->

## D. States (FDL)

### {Entity Name} State Machine

- [ ] **ID**: `fdd-{project-name}-feature-{feature-slug}-state-{entity-slug}`

<!-- fdd-id-content -->
**States**: {State1}, {State2}, {State3}
**Initial State**: {State1}

**Transitions**:
1. [ ] - `ph-1` - **FROM** {State1} **TO** {State2} **WHEN** {condition} - `inst-{step-id}`
2. [ ] - `ph-1` - **FROM** {State2} **TO** {State3} **WHEN** {condition} - `inst-{step-id}`
<!-- fdd-id-content -->

<!-- TODO: Add more state machines as needed -->
<!-- Note: This section is optional if feature has no state management -->

## E. Technical Details

### Database Schema

<!-- TODO: Add tables/entities if applicable -->
{Tables, columns, relationships or "Not applicable"}

### API Endpoints

<!-- TODO: Reference API specification from Overall Design -->
- See [API Spec]({path/to/api-spec})

### Security

**Authorization**: {Authorization rules}
**Access Control**: {Access control description}

### Error Handling

| Error Type | Handling Approach |
|------------|-------------------|
| {Error 1} | {How to handle} |

## F. Requirements

### {Requirement Title}

- [ ] **ID**: `fdd-{project-name}-feature-{feature-slug}-req-{req-slug}`

<!-- fdd-id-content -->
**Status**: ⏳ NOT_STARTED
**Description**: {Clear description with SHALL/MUST statements}

**References**:
- [{Flow Name}](#{flow-name})
- [{Algorithm Name}](#{algorithm-name})

**Implements**:
- `fdd-{project-name}-feature-{feature-slug}-flow-{flow-slug}`
- `fdd-{project-name}-feature-{feature-slug}-algo-{algo-slug}`

**Phases**:
- [ ] `ph-1`: {What is implemented in this phase}

**Tests Covered**:
- `fdd-{project-name}-feature-{feature-slug}-test-{test-slug}`

**Acceptance Criteria**:
- {Criterion 1}
- {Criterion 2}
<!-- fdd-id-content -->

<!-- TODO: Add more requirements as needed -->

## G. Testing Scenarios

### {Test Scenario Title}

- [ ] **ID**: `fdd-{project-name}-feature-{feature-slug}-test-{test-slug}`

<!-- fdd-id-content -->
**Validates**: `fdd-{project-name}-feature-{feature-slug}-req-{req-slug}`

**Steps**:
1. [ ] - `ph-1` - {Setup step} - `inst-{step-id}`
2. [ ] - `ph-1` - {Action step} - `inst-{step-id}`
3. [ ] - `ph-1` - {Verification step} - `inst-{step-id}`
<!-- fdd-id-content -->

<!-- TODO: Add more testing scenarios as needed -->

## H. Additional Context

<!-- TODO: Add dependencies, references, notes, diagrams if needed -->
<!-- This section is optional -->
