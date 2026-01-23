# Technical Design: {PROJECT_NAME}

## A. Architecture Overview

### Architectural Vision

{2-3 paragraphs describing the technical approach, key architectural decisions, and design philosophy}

### Architecture Layers

<!-- TODO: Add architecture diagram (draw.io, Mermaid, or embedded image) -->

| Layer | Responsibility | Technology |
|-------|---------------|------------|
| Presentation | {description} | {tech} |
| Application | {description} | {tech} |
| Domain | {description} | {tech} |
| Infrastructure | {description} | {tech} |

## B. Requirements & Principles

### B.1 Functional Requirements

#### FR-{NNN}: {Requirement Title}

**ID**: `fdd-{project-name}-req-{requirement-slug}`

<!-- fdd-id-content -->
**Priority**: {HIGH | MEDIUM | LOW}
**Capabilities**: `fdd-{project-name}-capability-{cap1}`, `fdd-{project-name}-capability-{cap2}`
**Use Cases**: `fdd-{project-name}-usecase-{uc1}`
**Actors**: `fdd-{project-name}-actor-{actor1}`, `fdd-{project-name}-actor-{actor2}`

{Description of what the system must do}
<!-- fdd-id-content -->

<!-- TODO: Add more functional requirements as needed -->

### B.2 Non-Functional Requirements

#### NFR: {NFR Category}

**ID**: `fdd-{project-name}-nfr-{category-slug}`

<!-- fdd-id-content -->
- {Specific requirement 1}
- {Specific requirement 2}
<!-- fdd-id-content -->

<!-- TODO: Add more NFR categories: performance, scalability, reliability, security, etc. -->

### B.3 Design Principles

#### {Principle Name}

**ID**: `fdd-{project-name}-principle-{principle-slug}`

<!-- fdd-id-content -->
**ADRs**: `fdd-{project-name}-adr-{adr-slug}`

{Description of the principle and why it matters}
<!-- fdd-id-content -->

<!-- TODO: Add more design principles as needed -->

### B.4 Constraints

#### {Constraint Name}

**ID**: `fdd-{project-name}-constraint-{constraint-slug}`

<!-- fdd-id-content -->
**ADRs**: `fdd-{project-name}-adr-{adr-slug}`

{Description of the constraint and its impact}
<!-- fdd-id-content -->

<!-- TODO: Add more constraints as needed -->

## C. Technical Architecture

### C.1 Component Model

<!-- TODO: Add component diagram (draw.io, Mermaid, or ASCII) -->

**Components**:
- **{Component 1}**: {Purpose and responsibility}
- **{Component 2}**: {Purpose and responsibility}

**Interactions**:
- {Component 1} → {Component 2}: {Description of interaction}

### C.2 Domain Model

**Technology**: {GTS | JSON Schema | OpenAPI | TypeScript}
**Location**: [{domain-model-file}]({path/to/domain-model})

**Core Entities**:
- [{EntityName}]({path/to/entity.schema}) - {Description}

**Relationships**:
- {Entity1} → {Entity2}: {Relationship description}

### C.3 API Contracts

**Technology**: {REST/OpenAPI | GraphQL | gRPC | CLISPEC}
**Location**: [{api-spec-file}]({path/to/api-spec})

**Endpoints Overview**:
- `{METHOD} {/path}` - {Description}

### C.4 Security Model

**Authentication**: {Approach description}
**Authorization**: {Approach description}
**Data Protection**: {Approach description}
**Security Boundaries**: {Description}

### C.5 Non-Functional Requirements

**Performance**:
- {Performance requirement 1}

**Scalability**:
- {Scalability requirement 1}

**Reliability**:
- {Reliability requirement 1}

## D. Additional Context

<!-- TODO: Add any additional technical context, architect notes, rationale, etc. -->
<!-- This section is optional and not validated by FDD -->
