---
fdd: true
type: requirement
name: Business Context Structure
version: 1.1
purpose: Define validation rules for BUSINESS.md files
---

# Business Context Structure Requirements

---

## Agent Instructions

**ALWAYS open and follow**: `../workflows/business-context.md` WHEN executing workflow

**ALWAYS open and follow**: `../templates/BUSINESS.template.md` WHEN generating content

**ALWAYS open**: `../examples/requirements/business-context/valid.md` WHEN reviewing valid artifact structure

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
- Recommended: ≤500 lines
- Hard limit: ≤1000 lines

---

## File Overview

**Purpose**: Business context, actors, and system capabilities

**Location**: `architecture/BUSINESS.md`

**Contains**: 
- Section A: Vision
- Section B: Actors
- Section C: Capabilities
- Section D: Use Cases (optional)
- Section E: Additional Context (optional)

---

## Validation Criteria

### File Validation

1. **File exists**
   - File `architecture/BUSINESS.md` exists
   - File contains ≥50 lines (recommended: 200-500 lines)

### Structure Validation

1. **All required sections present**
   - Section A: VISION
   - Section B: Actors
   - Section C: Capabilities
   - Section D: Use Cases (optional, but if present must be validated)
   - Section E: Additional Context (optional, not validated)

2. **Section order correct**
   - A → B → C → D → E
   - Section D may be omitted
   - If Section D not present, Section E can follow Section C

3. **No prohibited sections**
   - Only A-E allowed at top level (D and E are optional)

4. **Headers use proper levels**
   - `##` for sections A-E
   - `####` for actors/capabilities/use cases

### Content Validation

1. **Section A: VISION**
   - Contains: Purpose, Target Users, Key Problems Solved, Success Criteria
   - Success criteria are measurable
   - ≥2 paragraphs of content

2. **Section B: Actors**
   - ≥1 actor defined
   - Grouped by Human Actors and System Actors
   - Each actor has:
     - `####` heading with actor name
     - `**ID**:` line with valid actor ID
     - `**Role**:` line with description

3. **Section C: Capabilities**
   - ≥1 capability defined
   - Each capability has:
     - `####` heading with capability name
     - `**ID**:` line with valid capability ID
     - Bulleted list of features
     - `**Actors**:` line listing actor IDs
   - All referenced actor IDs exist in Section B

4. **Section D: Use Cases** (if present)
   - ≥1 use case defined
   - Each use case has:
     - `####` heading with "UC-XXX: Use Case Name" format
     - `**ID**:` line with valid use case ID
     - `**Actor**:` line listing actor IDs
     - `**Preconditions**:` description
     - `**Flow**:` numbered list of steps
     - `**Postconditions**:` description
   - All referenced actor IDs exist in Section B
   - Flow steps MAY reference capability IDs from Section C

### FDD ID Format Validation

| ID Type | Format | Example |
|---------|--------|---------|
| Actor | `fdd-{project}-actor-{name}` | `fdd-analytics-actor-admin` |
| Capability | `fdd-{project}-capability-{name}` | `fdd-analytics-capability-data-viz` |
| Use Case | `fdd-{project}-usecase-{name}` | `fdd-analytics-usecase-create-report` |

**ID Rules**:
- All IDs wrapped in backticks
- Names in kebab-case (2-4 words)
- Unique within their section

### Cross-Reference Validation

1. **Capability → Actor**
   - All actor IDs in `**Actors**:` lines must exist in Section B
   - At least one actor per capability

2. **Use Case → Actor** (if Section D present)
   - All actor IDs in `**Actor**:` lines must exist in Section B

3. **Use Case → Capability** (if Section D present)
   - Capability IDs referenced in Flow must exist in Section C (optional)

---

## Best Practices

1. **Business-focused content** — no technical implementation details
2. **Actor definitions** — distinguish human vs system, concise roles
3. **Capability scope** — broad but coherent, group related features
4. **Success criteria** — measurable, quantitative targets
5. **ID naming** — descriptive, domain language, kebab-case

---

## Common Issues

- Missing required section structure (A/B/C headings)
- Actor headings not `####` or not grouped by Human/System
- Actor IDs wrong format or not wrapped in backticks
- Capabilities missing actor references
- Use case actors using names instead of IDs

---

## Validation Checklist (Final)

- [ ] Document follows required structure
- [ ] All validation criteria pass
- [ ] Agent used template for generation
- [ ] Agent referenced example for validation

---

## References

**Template**: `../templates/BUSINESS.template.md`

**Example**: `../examples/requirements/business-context/valid.md`

**Related**:
- `overall-design-structure.md` — DESIGN.md references BUSINESS.md
- `../.adapter/specs/conventions.md` — Core FDD principles
