# FDD Adapter Structure Requirements

**MUST read and follow**: `../workflows/adapter.md`

**This file defines**: Structure only (WHAT to create)  
**Workflow defines**: Process (HOW to create)

⚠️ **Do NOT use this file alone. Execute the workflow, not just the structure.**

---

**Version**: 1.0  
**Purpose**: Define structure and validation criteria for FDD Adapter

**Scope**: Project-specific adapter configuration that extends FDD core methodology

---

## Overview

**FDD Adapter** - OPTIONAL project-specific configuration extending FDD core methodology

**Purpose**: Define project-specific implementations for:
- Domain model technology and format
- API contract format and conventions
- Testing framework and tools
- Build and deployment tools
- Behavior description language (optional FDL override)
- Project structure and conventions

**When Required**:
- OPTIONAL for Product Manager workflows (business context is generic)
- OPTIONAL for Architect workflows (can use defaults)
- RECOMMENDED for Solution Architect workflows (technical formats)
- REQUIRED for Developer workflows (code conventions mandatory)

**Auto-Trigger**: Agent MUST stop and run `adapter` workflow WHEN:
- User specifies domain model format/location
- User specifies API contract format/location
- User specifies custom file structures
- User specifies project-specific conventions
- Implementation workflows started without adapter

**Location**: `{adapter-directory}/FDD-Adapter/` where `{adapter-directory}` is one of:
- `spec/FDD-Adapter/`
- `guidelines/FDD-Adapter/`
- `docs/FDD-Adapter/`

**Status**: MUST be marked as COMPLETE or INCOMPLETE

---

## Required Files

### AGENTS.md

**Location**: `{adapter-directory}/FDD-Adapter/AGENTS.md`

**Purpose**: Adapter-specific navigation for AI agents (MUST WHEN format)

**Primary Content**: MUST WHEN instructions pointing to detailed specification files

**Structure**:
1. Header with extension declaration
2. MUST WHEN instructions (navigation to specs)
3. Adapter status

**MUST contain WHEN-based navigation** to:
- Domain model specification file
- API contract specification file
- Testing specification file
- Build/deployment specification file
- Project structure specification file

**Format**:
```markdown
# FDD Adapter: {Project Name}

**Extends**: `../../FDD/AGENTS.md`

**Version**: {version}  
**Status**: COMPLETE | INCOMPLETE  
**Last Updated**: YYYY-MM-DD

---

MUST read `specs/domain-model.md` WHEN working with domain types

MUST read `specs/api-contracts.md` WHEN working with API endpoints

MUST read `specs/testing.md` WHEN writing or running tests

MUST read `specs/build-deploy.md` WHEN building or deploying

MUST read `specs/project-structure.md` WHEN creating files or directories

MUST read `specs/conventions.md` WHEN writing code or documentation
```

**Detailed Specification Files** (in `{adapter-directory}/FDD-Adapter/specs/`):

- `domain-model.md` - Domain model technology, location, format, examples
- `api-contracts.md` - API contract technology, location, format, examples
- `testing.md` - Testing frameworks, commands, coverage requirements
- `build-deploy.md` - Build commands, deployment process, CI/CD
- `project-structure.md` - Directory structure, file locations
- `conventions.md` - Coding standards, naming conventions, patterns

---

## Validation Criteria

### File Structure Validation

1. **AGENTS.md exists**
   - File located at `{adapter-directory}/FDD-Adapter/AGENTS.md`
   - File is not empty
   - File contains required sections

2. **Extension declaration present**
   - Contains `**Extends**: ../../FDD/AGENTS.md` or relative path to FDD AGENTS.md
   - Extension path is valid
   - Points to FDD core AGENTS.md

3. **Status declared**
   - Status field present
   - Status is COMPLETE or INCOMPLETE
   - If INCOMPLETE, missing specifications listed

### Content Validation

1. **Project identification**
   - Project name specified
   - Project root path specified
   - Architecture root path specified
   - All paths are valid and accessible

2. **Domain model specification**
   - Technology name specified
   - Location path specified (relative to project root)
   - Format described in detail
   - Type identifier format defined with examples
   - Location is accessible and contains domain model files

3. **API contracts specification**
   - Technology name specified
   - Location path specified (relative to project root)
   - Format described in detail
   - Endpoint format defined with examples
   - Location is accessible and contains API contract files

4. **Testing framework specification**
   - Unit test framework specified
   - Integration test framework specified
   - E2E test framework specified
   - Test location specified
   - Test command specified and executable
   - Coverage command specified (if applicable)

5. **Build tools specification**
   - Build command specified and executable
   - Clean command specified and executable
   - Lint command specified and executable

6. **Behavior description language**
   - Uses FDL or custom BDL specified
   - Specification path provided
   - If custom BDL, specification file exists and is valid

7. **Project structure defined**
   - Architecture files structure shown
   - Source code structure shown
   - All paths are consistent with project identification

### Completeness Validation

1. **All required sections present**
   - Project Identification
   - Technology Stack (Domain Model, API Contracts, Testing, Build Tools, BDL)
   - Project Structure

2. **No placeholders**
   - No `[TODO]` markers
   - No `[TBD]` markers
   - No `{fill this}` placeholders
   - No empty sections

3. **Commands are OS agnostic**
   - No OS-specific path separators (use `/` or cross-platform notation)
   - No OS-specific commands (no `ls`, `cat`, `grep`, etc.)
   - Commands work on Windows, macOS, Linux

### Validation Scoring

**Total**: 100 points

**Breakdown**:
- File structure (10 points): File exists, extends correctly, status declared
- Project identification (10 points): Name, paths specified and valid
- Domain model (20 points): Complete specification with examples
- API contracts (20 points): Complete specification with examples
- Testing framework (15 points): All frameworks and commands specified
- Build tools (10 points): All commands specified and executable
- BDL specification (5 points): Valid specification path
- Project structure (10 points): Complete structure definition
- Completeness (10 points): No placeholders, OS agnostic

**Pass threshold**: ≥90/100

---

## Examples

### Valid Adapter (Rust + GTS + OpenAPI)

```markdown
# FDD Adapter: Hyperspot

**Extends**: `../../FDD/AGENTS.md`

**Version**: 1.0  
**Status**: COMPLETE  
**Last Updated**: 2025-01-07

---

## Project Identification

**Project Name**: Hyperspot  
**Project Root**: `/project/root`  
**Architecture Root**: `/project/root/architecture`

---

## Technology Stack

### Domain Model

**Technology**: GTS (Global Type System)  
**Location**: `gts/`  
**Format**: TypeScript-like syntax with JSON Schema output

**Type Identifier Format**: `gts.{namespace}.{type}.v{version}`

**Example**:
```
gts.analytics.event.v1
```

### API Contracts

**Technology**: OpenAPI 3.1  
**Location**: `docs/api/`  
**Format**: YAML files per service

**Endpoint Format**: `/{version}/{service}/{resource}`

**Example**:
```
/v1/analytics/events
```

### Testing Framework

**Unit Tests**: cargo test  
**Integration Tests**: cargo test --test '*'  
**E2E Tests**: pytest testing/e2e/

**Test Location**: `tests/`, `testing/e2e/`  
**Test Command**: `make test`  
**Coverage Command**: `make coverage`

### Build Tools

**Build Command**: `cargo build --release`  
**Clean Command**: `cargo clean`  
**Lint Command**: `cargo clippy -- -D warnings`

### Behavior Description Language

**Uses**: FDL  
**Specification**: `../FDL.md`

---

## Project Structure

### Architecture Files

```
architecture/
├── BUSINESS.md
├── DESIGN.md
├── ADR.md
└── features/
    ├── FEATURES.md
    └── feature-{slug}/
        ├── DESIGN.md
        └── CHANGES.md
```

### Source Code

```
src/
├── domain/      # Domain models (from gts/)
├── api/         # API implementations
├── core/        # Core business logic
└── infra/       # Infrastructure
```
```

### Invalid Adapter (Missing Specifications)

```markdown
# FDD Adapter: MyProject

**Extends**: `../../FDD/AGENTS.md`

**Status**: INCOMPLETE

Missing specifications:
- Domain model technology
- API contracts format
- Testing framework
```
❌ Missing required sections, marked as INCOMPLETE

---

## Workflow Integration

**Adapter workflows**:
- `adapter` - Create adapter from scratch or from existing codebase
- `adapter-validate` - Validate adapter against these requirements

**Prerequisites for other workflows**:
- ALL FDD workflows REQUIRE valid adapter (≥90/100)
- Adapter MUST be validated before any other workflow runs
- If adapter INCOMPLETE, must complete before proceeding

**Validation command**:
```
Run workflow: adapter-validate
```

**Expected output**:
- Score: X/100
- Status: PASS (≥90) | FAIL (<90)
- Issues: List of missing/invalid items
- Recommendations: What to fix

---

## References

**Used by workflows**:
- All FDD workflows (prerequisite check)
- `adapter` - Creates adapter
- `adapter-validate` - Validates adapter

**Related requirements**:
- `../AGENTS.md` - Core FDD requirements
- `workflow-requirements.md` - Workflow structure requirements
