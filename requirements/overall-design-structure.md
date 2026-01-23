---
fdd: true
type: requirement
name: Overall Design Structure
version: 1.1
purpose: Define validation rules for DESIGN.md files
---

# Overall Design Structure Requirements

---

## Agent Instructions

**ALWAYS open and follow**: `../workflows/design.md` WHEN executing workflow

**ALWAYS open and follow**: `../templates/DESIGN.template.md` WHEN generating content

**ALWAYS open**: `../examples/requirements/overall-design/valid.md` WHEN reviewing valid artifact structure

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

**Size limits**:
- Recommended: ≤1500 lines
- Hard limit: ≤2000 lines

**Related**:
- `business-context-structure.md` — BUSINESS.md structure
- `adr-structure.md` — ADR directory structure

---

## File Overview

**Purpose**: Technical requirements, principles, and architecture

**Location**: `architecture/DESIGN.md`

**Contains**: 
- Section A: Architecture Overview
- Section B: Requirements & Principles
- Section C: Technical Architecture (C.1-C.5)
- Section D: Additional Context (optional)

---

## Validation Criteria

### File Validation

1. **File exists**
   - File `architecture/DESIGN.md` exists
   - File contains ≥200 lines (recommended: 500-2000 lines)

### Structure Validation

1. **All required sections present**
   - Section A: Architecture Overview
   - Section B: Requirements & Principles (B.1-B.4)
   - Section C: Technical Architecture (C.1-C.5)
   - Section D: Additional Context (optional)

2. **Section order correct**: A → B → C → D

3. **No prohibited sections**
   - Only A-D allowed at top level
   - Section C has exactly 5 subsections (C.1-C.5)

4. **Headers use proper levels**
   - `##` for sections A-D
   - `###` for subsections B.1-B.4, C.1-C.5

### Section B Subsections

| Subsection | Content |
|------------|---------|
| B.1 | Functional Requirements |
| B.2 | Non-Functional Requirements |
| B.3 | Design Principles |
| B.4 | Constraints |

### Section C Subsections

| Subsection | Content |
|------------|---------|
| C.1 | Component Model |
| C.2 | Domain Model |
| C.3 | API Contracts |
| C.4 | Security Model |
| C.5 | Non-Functional Requirements |

### Content Validation

1. **Domain Model accessible**
   - Files at specified location exist
   - Files are in machine-readable format (GTS, JSON Schema, OpenAPI, TypeScript)
   - References are clickable Markdown links

2. **API Contracts accessible**
   - Files at specified location exist
   - Files are in machine-readable format (OpenAPI, GraphQL, CLISPEC, proto)
   - References are clickable Markdown links

3. **Component diagram present**
   - At least one diagram in Section C.1
   - Can be embedded image, Mermaid code, or ASCII art

---

## FDD ID Format Validation

| ID Type | Format | Example |
|---------|--------|---------|
| Requirement | `fdd-{project}-req-{name}` | `fdd-analytics-req-multi-tenant` |
| NFR | `fdd-{project}-nfr-{name}` | `fdd-analytics-nfr-performance` |
| Principle | `fdd-{project}-principle-{name}` | `fdd-analytics-principle-plugin-based` |
| Constraint | `fdd-{project}-constraint-{name}` | `fdd-analytics-constraint-api-dep` |
| ADR | `fdd-{project}-adr-{name}` | `fdd-analytics-adr-event-sourcing` |

**ID Rules**:
- All IDs wrapped in backticks
- Names in kebab-case (2-4 words)
- Unique within their section
- `**ID**:` line MUST be first non-empty line after heading

---

## Traceability Field Requirements

Each Functional Requirement (FR) MUST include:

| Field | Format | Mandatory |
|-------|--------|-----------|
| **Capabilities** | `**Capabilities**: \`{cap-id}\`` | YES |
| **Actors** | `**Actors**: \`{actor-id}\`` | YES |
| **Use Cases** | `**Use Cases**: \`{uc-id}\`` | If applicable |
| **ADRs** | `**ADRs**: \`{adr-id}\`` | If applicable |

---

## Cross-Reference Validation

### BUSINESS.md → DESIGN.md Traceability

1. **Capability Coverage (MANDATORY)**
   - Every capability ID from BUSINESS.md Section C MUST be referenced
   - No orphaned capabilities

2. **Use Case Coverage (MANDATORY)**
   - Every use case ID from BUSINESS.md Section D MUST be referenced
   - No orphaned use cases

3. **Actor References (MANDATORY)**
   - Every FR MUST have `**Actors**:` field
   - Actor IDs MUST match capability actors from BUSINESS.md

4. **ADR Coverage (MANDATORY)**
   - All ADRs from `architecture/ADR/` MUST appear in at least one DESIGN.md requirement
   - No orphaned ADRs

### Validation Checks

- Every capability ID from BUSINESS.md appears in FR `**Capabilities**` field
- Every use case ID from BUSINESS.md appears in FR `**Use Cases**` field
- Every FR has Capabilities and Actors fields
- All referenced IDs are valid (exist in source documents)
- All ADRs from `architecture/ADR/` are referenced

---

## Scoring

| Category | Points |
|----------|--------|
| Structure | 30 |
| Domain Model | 25 |
| API Contracts | 25 |
| Content Quality | 20 |
| **Total** | **100** |

**Penalties**:
- Missing capability coverage: **-15 points** per orphaned capability
- Missing use case coverage: **-15 points** per orphaned use case
- Orphaned ADR: **-15 points** per ADR
- Missing Capabilities/Actors field: **-10 points** per FR
- Invalid ID reference: **-5 points** per invalid ID

---

## Common Issues

- Missing required top-level sections (A/B/C)
- Missing required C.1-C.5 subsections
- Missing functional requirement IDs
- Orphaned capabilities/use cases (not referenced in DESIGN.md)
- Domain model/API references not clickable links

---

## Validation Checklist (Final)

- [ ] Document follows required structure
- [ ] All validation criteria pass
- [ ] All traceability rules satisfied
- [ ] Agent used template for generation
- [ ] Agent referenced example for validation

---

## References

**Template**: `../templates/DESIGN.template.md`

**Example**: `../examples/requirements/overall-design/valid.md`

**Related**:
- `business-context-structure.md` — BUSINESS.md structure
- `adr-structure.md` — ADR directory structure
- `feature-design-structure.md` — Feature DESIGN.md structure
