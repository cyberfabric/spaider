<!-- spd:#:decomposition -->
# Decomposition: Spider

<!-- spd:##:overview -->
## 1. Overview

Spider specs are organized around **architectural components** with explicit dependencies. Foundation specs (Methodology Core, Adapter System) enable higher-level specs (Weaver Packages, CLI Tool, Workflows). The decomposition follows the component model from DESIGN.md, ensuring each spec maps to one or more components and covers related functional requirements.

<!-- spd:##:overview -->

<!-- spd:##:entries -->
## 2. Entries

**Overall implementation status:**
<!-- spd:id:status has="priority,task" -->
- [x] `p1` - **ID**: `spd-spider-status-overall`

<!-- spd:###:spec-title repeat="many" -->
### 1. [Methodology Core](spec-methodology-core/) ✅ HIGH

<!-- spd:id:spec has="priority,task" -->
- [x] `p1` - **ID**: `spd-spider-spec-methodology-core`

<!-- spd:paragraph:spec-purpose required="true" -->
- **Purpose**: Provide universal Spider specifications including requirements, SDSL language, and base template syntax that all projects share.
<!-- spd:paragraph:spec-purpose -->

<!-- spd:paragraph:spec-depends -->
- **Depends On**: None
<!-- spd:paragraph:spec-depends -->

<!-- spd:list:spec-scope -->
- **Scope**:
  - Requirements specifications (`requirements/*.md`)
  - SDSL (Spider Description Language) specification
  - Template marker syntax specification
  - Execution protocol definition
<!-- spd:list:spec-scope -->

<!-- spd:list:spec-out-scope -->
- **Out of scope**:
  - Project-specific customization
  - Concrete templates for artifact kinds
<!-- spd:list:spec-out-scope -->

- **Requirements Covered**:
<!-- spd:id-ref:fr has="priority,task" -->
  - [x] `p1` - `spd-spider-fr-artifact-templates`
  - [x] `p2` - `spd-spider-fr-artifact-examples`
  - [x] `p1` - `spd-spider-fr-sdsl`
<!-- spd:id-ref:fr -->

- **Design Principles Covered**:
<!-- spd:id-ref:principle has="priority,task" -->
  - [x] `p1` - `spd-spider-principle-tech-agnostic`
  - [x] `p1` - `spd-spider-principle-machine-readable`
  - [x] `p1` - `spd-spider-principle-machine-readable-artifacts`
<!-- spd:id-ref:principle -->

- **Design Constraints Covered**:
<!-- spd:id-ref:constraint has="priority,task" -->
  - [x] `p1` - `spd-spider-constraint-markdown`
  - [x] `p1` - `spd-spider-constraint-no-forced-tools`
<!-- spd:id-ref:constraint -->

<!-- spd:list:spec-domain-entities -->
- **Domain Model Entities**:
  - Artifact
  - Workflow
  - SDSL
<!-- spd:list:spec-domain-entities -->

- **Design Components**:
<!-- spd:id-ref:component has="priority,task" -->
  - [x] `p1` - `spd-spider-component-methodology-core`
<!-- spd:id-ref:component -->

<!-- spd:list:spec-api -->
- **API**:
  - Specifications only, no CLI commands
<!-- spd:list:spec-api -->

- **Sequences**:
<!-- spd:id-ref:seq has="priority,task" -->
  - [x] `p1` - `spd-spider-seq-intent-to-workflow`
<!-- spd:id-ref:seq -->

- **Data**:
<!-- spd:id-ref:dbtable has="priority,task" -->
  - [x] `p3` - `spd-spider-dbtable-na`
<!-- spd:id-ref:dbtable -->

<!-- spd:id:spec -->
<!-- spd:###:spec-title repeat="many" -->

<!-- spd:###:spec-title repeat="many" -->
### 2. [Adapter System](spec-adapter-system/) ✅ HIGH

<!-- spd:id:spec has="priority,task" -->
- [x] `p1` - **ID**: `spd-spider-spec-adapter-system`

<!-- spd:paragraph:spec-purpose required="true" -->
- **Purpose**: Enable project-specific customization without modifying core methodology through adapter configuration and hierarchical artifact registry.
<!-- spd:paragraph:spec-purpose -->

<!-- spd:paragraph:spec-depends -->
- **Depends On**: None
<!-- spd:paragraph:spec-depends -->

<!-- spd:list:spec-scope -->
- **Scope**:
  - Adapter discovery (`adapter-info` command)
  - `artifacts.json` registry with hierarchical systems
  - `.spider-adapter/` directory structure
  - Spec files (tech-stack, conventions, etc.)
<!-- spd:list:spec-scope -->

<!-- spd:list:spec-out-scope -->
- **Out of scope**:
  - Actual project artifacts
  - Weaver packages
<!-- spd:list:spec-out-scope -->

- **Requirements Covered**:
<!-- spd:id-ref:fr has="priority,task" -->
  - [x] `p1` - `spd-spider-fr-adapter-config`
  - [x] `p2` - `spd-spider-fr-hierarchical-registry`
  - [x] `p2` - `spd-spider-fr-brownfield-support`
<!-- spd:id-ref:fr -->

- **Design Principles Covered**:
<!-- spd:id-ref:principle has="priority,task" -->
  - [x] `p1` - `spd-spider-principle-tech-agnostic`
  - [x] `p1` - `spd-spider-principle-adapter-variability-boundary`
<!-- spd:id-ref:principle -->

- **Design Constraints Covered**:
<!-- spd:id-ref:constraint has="priority,task" -->
  - [x] `p1` - `spd-spider-constraint-git`
<!-- spd:id-ref:constraint -->

<!-- spd:list:spec-domain-entities -->
- **Domain Model Entities**:
  - Adapter
  - ArtifactRegistry
  - System
<!-- spd:list:spec-domain-entities -->

- **Design Components**:
<!-- spd:id-ref:component has="priority,task" -->
  - [x] `p1` - `spd-spider-component-adapter-system`
<!-- spd:id-ref:component -->

<!-- spd:list:spec-api -->
- **API**:
  - `spider adapter-info`
  - `spider init`
<!-- spd:list:spec-api -->

- **Sequences**:
<!-- spd:id-ref:seq has="priority,task" -->
  - [x] `p1` - `spd-spider-seq-adapter-discovery`
<!-- spd:id-ref:seq -->

- **Data**:
<!-- spd:id-ref:dbtable has="priority,task" -->
  - [x] `p3` - `spd-spider-dbtable-na`
<!-- spd:id-ref:dbtable -->

<!-- spd:id:spec -->
<!-- spd:###:spec-title repeat="many" -->

<!-- spd:###:spec-title repeat="many" -->
### 3. [Weaver Packages](spec-rules-packages/) ✅ HIGH

<!-- spd:id:spec has="priority,task" -->
- [x] `p1` - **ID**: `spd-spider-spec-rules-packages`

<!-- spd:paragraph:spec-purpose required="true" -->
- **Purpose**: Provide templates, checklists, rules, and examples for each artifact kind with validation and self-check capabilities.
<!-- spd:paragraph:spec-purpose -->

<!-- spd:paragraph:spec-depends -->
- **Depends On**: `spd-spider-spec-methodology-core`
<!-- spd:paragraph:spec-depends -->

<!-- spd:list:spec-scope -->
- **Scope**:
  - Template definitions (`template.md` per kind)
  - Semantic checklists (`checklist.md` per kind)
  - Generation rules (`rules.md` per kind)
  - Canonical examples (`weavers/sdlc/artifacts/{KIND}/examples/example.md`)
  - Weaver validation (`validate-weavers`)
  - Template QA (`self-check`)
<!-- spd:list:spec-scope -->

<!-- spd:list:spec-out-scope -->
- **Out of scope**:
  - Custom project rules
  - Code generation rules
<!-- spd:list:spec-out-scope -->

- **Requirements Covered**:
<!-- spd:id-ref:fr has="priority,task" -->
  - [x] `p1` - `spd-spider-fr-rules-packages`
  - [x] `p2` - `spd-spider-fr-template-qa`
  - [x] `p1` - `spd-spider-fr-artifact-templates`
<!-- spd:id-ref:fr -->

- **Design Principles Covered**:
<!-- spd:id-ref:principle has="priority,task" -->
  - [x] `p1` - `spd-spider-principle-machine-readable`
  - [x] `p1` - `spd-spider-principle-deterministic-gate`
<!-- spd:id-ref:principle -->

- **Design Constraints Covered**:
<!-- spd:id-ref:constraint has="priority,task" -->
  - [x] `p1` - `spd-spider-constraint-markdown`
<!-- spd:id-ref:constraint -->

<!-- spd:list:spec-domain-entities -->
- **Domain Model Entities**:
  - Template
  - Checklist
  - Rules
<!-- spd:list:spec-domain-entities -->

- **Design Components**:
<!-- spd:id-ref:component has="priority,task" -->
  - [x] `p1` - `spd-spider-component-rules-packages`
<!-- spd:id-ref:component -->

<!-- spd:list:spec-api -->
- **API**:
  - `spider validate-weavers`
  - `spider self-check`
<!-- spd:list:spec-api -->

- **Sequences**:
<!-- spd:id-ref:seq has="priority,task" -->
  - [x] `p1` - `spd-spider-seq-validate-overall-design`
<!-- spd:id-ref:seq -->

- **Data**:
<!-- spd:id-ref:dbtable has="priority,task" -->
  - [x] `p3` - `spd-spider-dbtable-na`
<!-- spd:id-ref:dbtable -->

<!-- spd:id:spec -->
<!-- spd:###:spec-title repeat="many" -->

<!-- spd:###:spec-title repeat="many" -->
### 4. [Spider CLI Tool](spec-spider-cli/) ✅ HIGH

<!-- spd:id:spec has="priority,task" -->
- [x] `p1` - **ID**: `spd-spider-spec-spider-cli`

<!-- spd:paragraph:spec-purpose required="true" -->
- **Purpose**: Provide deterministic validation, ID management, and traceability commands via a Python stdlib-only CLI tool.
<!-- spd:paragraph:spec-purpose -->

<!-- spd:paragraph:spec-depends -->
- **Depends On**: `spd-spider-spec-adapter-system`, `spd-spider-spec-rules-packages`
<!-- spd:paragraph:spec-depends -->

<!-- spd:list:spec-scope -->
- **Scope**:
  - Artifact validation (`validate --artifact`)
  - Code validation (`validate-code`)
  - Cross-artifact validation
  - ID management (`list-ids`, `where-defined`, `where-used`)
  - JSON output for machine consumption
<!-- spd:list:spec-scope -->

<!-- spd:list:spec-out-scope -->
- **Out of scope**:
  - IDE-specific integrations
  - Interactive workflows
<!-- spd:list:spec-out-scope -->

- **Requirements Covered**:
<!-- spd:id-ref:fr has="priority,task" -->
  - [x] `p1` - `spd-spider-fr-validation`
  - [x] `p1` - `spd-spider-fr-traceability`
  - [x] `p1` - `spd-spider-fr-cross-artifact-validation`
<!-- spd:id-ref:fr -->

- **Design Principles Covered**:
<!-- spd:id-ref:principle has="priority,task" -->
  - [x] `p1` - `spd-spider-principle-deterministic-gate`
  - [x] `p1` - `spd-spider-principle-traceability`
  - [x] `p1` - `spd-spider-principle-cli-json-composability`
<!-- spd:id-ref:principle -->

- **Design Constraints Covered**:
<!-- spd:id-ref:constraint has="priority,task" -->
  - [x] `p1` - `spd-spider-constraint-stdlib-only`
  - [x] `p1` - `spd-spider-constraint-no-forced-tools`
<!-- spd:id-ref:constraint -->

<!-- spd:list:spec-domain-entities -->
- **Domain Model Entities**:
  - ValidationResult
  - SpiderId
  - CrossReference
<!-- spd:list:spec-domain-entities -->

- **Design Components**:
<!-- spd:id-ref:component has="priority,task" -->
  - [x] `p1` - `spd-spider-component-spider-skill`
<!-- spd:id-ref:component -->

<!-- spd:list:spec-api -->
- **API**:
  - `spider validate`
  - `spider list-ids`
  - `spider where-defined`
  - `spider where-used`
<!-- spd:list:spec-api -->

- **Sequences**:
<!-- spd:id-ref:seq has="priority,task" -->
  - [x] `p1` - `spd-spider-seq-validate-overall-design`
  - [x] `p1` - `spd-spider-seq-traceability-query`
<!-- spd:id-ref:seq -->

- **Data**:
<!-- spd:id-ref:dbtable has="priority,task" -->
  - [x] `p3` - `spd-spider-dbtable-na`
<!-- spd:id-ref:dbtable -->

<!-- spd:id:spec -->
<!-- spd:###:spec-title repeat="many" -->

<!-- spd:###:spec-title repeat="many" -->
### 5. [Workflow Engine](spec-workflow-engine/) ✅ HIGH

<!-- spd:id:spec has="priority,task" -->
- [x] `p1` - **ID**: `spd-spider-spec-workflow-engine`

<!-- spd:paragraph:spec-purpose required="true" -->
- **Purpose**: Provide interactive artifact creation/update workflows and validation workflows with execution protocol.
<!-- spd:paragraph:spec-purpose -->

<!-- spd:paragraph:spec-depends -->
- **Depends On**: `spd-spider-spec-spider-cli`, `spd-spider-spec-rules-packages`
<!-- spd:paragraph:spec-depends -->

<!-- spd:list:spec-scope -->
- **Scope**:
  - Generate workflow (`../workflows/generate.md`)
  - Validate workflow (`../workflows/analyze.md`)
  - Execution protocol
  - Artifact management (PRD, DESIGN, ADR, DECOMPOSITION, SPEC)
  - Question-answer flow with proposals
<!-- spd:list:spec-scope -->

<!-- spd:list:spec-out-scope -->
- **Out of scope**:
  - Code generation
  - IDE integrations
<!-- spd:list:spec-out-scope -->

- **Requirements Covered**:
<!-- spd:id-ref:fr has="priority,task" -->
  - [x] `p1` - `spd-spider-fr-workflow-execution`
  - [x] `p1` - `spd-spider-fr-design-first`
  - [x] `p1` - `spd-spider-fr-prd-mgmt`
  - [x] `p1` - `spd-spider-fr-overall-design-mgmt`
  - [x] `p1` - `spd-spider-fr-spec-design-mgmt`
<!-- spd:id-ref:fr -->

- **Design Principles Covered**:
<!-- spd:id-ref:principle has="priority,task" -->
  - [x] `p1` - `spd-spider-principle-design-first`
  - [x] `p1` - `spd-spider-principle-deterministic-gate`
<!-- spd:id-ref:principle -->

- **Design Constraints Covered**:
<!-- spd:id-ref:constraint has="priority,task" -->
  - [x] `p1` - `spd-spider-constraint-git`
  - [x] `p1` - `spd-spider-constraint-markdown`
<!-- spd:id-ref:constraint -->

<!-- spd:list:spec-domain-entities -->
- **Domain Model Entities**:
  - Workflow
  - ExecutionProtocol
  - WorkflowPhase
<!-- spd:list:spec-domain-entities -->

- **Design Components**:
<!-- spd:id-ref:component has="priority,task" -->
  - [x] `p1` - `spd-spider-component-workflows`
<!-- spd:id-ref:component -->

<!-- spd:list:spec-api -->
- **API**:
  - `/spider`
  - `/spider-generate`
  - `/spider-analyze`
<!-- spd:list:spec-api -->

- **Sequences**:
<!-- spd:id-ref:seq has="priority,task" -->
  - [x] `p1` - `spd-spider-seq-intent-to-workflow`
<!-- spd:id-ref:seq -->

- **Data**:
<!-- spd:id-ref:dbtable has="priority,task" -->
  - [x] `p3` - `spd-spider-dbtable-na`
<!-- spd:id-ref:dbtable -->

<!-- spd:id:spec -->
<!-- spd:###:spec-title repeat="many" -->

<!-- spd:###:spec-title repeat="many" -->
### 6. [Agent Compliance](spec-agent-compliance/) ✅ MEDIUM

<!-- spd:id:spec has="priority,task" -->
- [x] `p2` - **ID**: `spd-spider-spec-agent-compliance`

<!-- spd:paragraph:spec-purpose required="true" -->
- **Purpose**: Enforce workflow quality through anti-pattern detection, evidence requirements, and STRICT/RELAXED mode.
<!-- spd:paragraph:spec-purpose -->

<!-- spd:paragraph:spec-depends -->
- **Depends On**: `spd-spider-spec-workflow-engine`
<!-- spd:paragraph:spec-depends -->

<!-- spd:list:spec-scope -->
- **Scope**:
  - Anti-patterns documentation (8 patterns)
  - Evidence requirements for validation
  - STRICT vs RELAXED mode
  - Agent self-test protocol (6 questions)
  - Agent compliance protocol
<!-- spd:list:spec-scope -->

<!-- spd:list:spec-out-scope -->
- **Out of scope**:
  - Specific AI agent implementations
  - Automated enforcement
<!-- spd:list:spec-out-scope -->

- **Requirements Covered**:
<!-- spd:id-ref:fr has="priority,task" -->
  - [x] `p2` - `spd-spider-fr-multi-agent-integration`
  - [x] `p1` - `spd-spider-nfr-security-integrity`
  - [x] `p1` - `spd-spider-nfr-reliability-recoverability`
<!-- spd:id-ref:fr -->

- **Design Principles Covered**:
<!-- spd:id-ref:principle has="priority,task" -->
  - [x] `p1` - `spd-spider-principle-deterministic-gate`
  - [x] `p1` - `spd-spider-principle-traceability`
<!-- spd:id-ref:principle -->

- **Design Constraints Covered**:
<!-- spd:id-ref:constraint has="priority,task" -->
  - [x] `p1` - `spd-spider-constraint-no-forced-tools`
<!-- spd:id-ref:constraint -->

<!-- spd:list:spec-domain-entities -->
- **Domain Model Entities**:
  - AntiPattern
  - EvidenceRequirement
  - RulesMode
<!-- spd:list:spec-domain-entities -->

- **Design Components**:
<!-- spd:id-ref:component has="priority,task" -->
  - [x] `p1` - `spd-spider-component-agent`
<!-- spd:id-ref:component -->

<!-- spd:list:spec-api -->
- **API**:
  - `spider agent-workflows`
  - `spider agent-skills`
<!-- spd:list:spec-api -->

- **Sequences**:
<!-- spd:id-ref:seq has="priority,task" -->
  - [x] `p1` - `spd-spider-seq-intent-to-workflow`
<!-- spd:id-ref:seq -->

- **Data**:
<!-- spd:id-ref:dbtable has="priority,task" -->
  - [x] `p3` - `spd-spider-dbtable-na`
<!-- spd:id-ref:dbtable -->

<!-- spd:id:spec -->
<!-- spd:###:spec-title repeat="many" -->

<!-- spd:###:spec-title repeat="many" -->
### 7. [Template System](specs/template-system.md) ✅ HIGH

<!-- spd:id:spec has="priority,task" -->
- [x] `p1` - **ID**: `spd-spider-spec-template-system`

<!-- spd:paragraph:spec-purpose required="true" -->
- **Purpose**: Provide marker-based template parsing and validation engine for deterministic artifact structure validation.
<!-- spd:paragraph:spec-purpose -->

<!-- spd:paragraph:spec-depends -->
- **Depends On**: `spd-spider-spec-methodology-core`
<!-- spd:paragraph:spec-depends -->

<!-- spd:list:spec-scope -->
- **Scope**:
  - Template parsing with Spider markers (spd:type:name format)
  - Artifact validation against templates
  - ID extraction and validation
  - Cross-artifact reference validation
  - Block content type validation (paragraph, list, table, sdsl, etc.)
<!-- spd:list:spec-scope -->

<!-- spd:list:spec-out-scope -->
- **Out of scope**:
  - Semantic validation (handled by checklists)
  - Code traceability (handled by codebase module)
<!-- spd:list:spec-out-scope -->

- **Requirements Covered**:
<!-- spd:id-ref:fr has="priority,task" -->
  - [ ] `p1` - `spd-spider-fr-artifact-templates`
  - [ ] `p1` - `spd-spider-fr-validation`
  - [ ] `p1` - `spd-spider-fr-cross-artifact-validation`
  - [ ] `p2` - `spd-spider-fr-template-qa`
<!-- spd:id-ref:fr -->

- **Design Principles Covered**:
<!-- spd:id-ref:principle has="priority,task" -->
  - [ ] `p1` - `spd-spider-principle-machine-readable`
  - [ ] `p1` - `spd-spider-principle-deterministic-gate`
  - [ ] `p1` - `spd-spider-principle-machine-readable-artifacts`
<!-- spd:id-ref:principle -->

- **Design Constraints Covered**:
<!-- spd:id-ref:constraint has="priority,task" -->
  - [ ] `p1` - `spd-spider-constraint-markdown`
  - [ ] `p1` - `spd-spider-constraint-stdlib-only`
<!-- spd:id-ref:constraint -->

<!-- spd:list:spec-domain-entities -->
- **Domain Model Entities**:
  - Template
  - TemplateBlock
  - Artifact
  - ArtifactBlock
  - IdDefinition
  - IdReference
<!-- spd:list:spec-domain-entities -->

- **Design Components**:
<!-- spd:id-ref:component has="priority,task" -->
  - [ ] `p1` - `spd-spider-component-spider-skill`
<!-- spd:id-ref:component -->

<!-- spd:list:spec-api -->
- **API**:
  - `Template.from_path(path)`
  - `Template.validate(artifact_path)`
  - `Artifact.validate()`
  - `cross_validate_artifacts()`
<!-- spd:list:spec-api -->

- **Sequences**:
<!-- spd:id-ref:seq has="priority,task" -->
  - [ ] `p1` - `spd-spider-seq-validate-overall-design`
  - [ ] `p1` - `spd-spider-seq-traceability-query`
<!-- spd:id-ref:seq -->

- **Data**:
<!-- spd:id-ref:dbtable has="priority,task" -->
  - [ ] `p3` - `spd-spider-dbtable-na`
<!-- spd:id-ref:dbtable -->

<!-- spd:id:spec -->
<!-- spd:###:spec-title repeat="many" -->

<!-- spd:id:status -->
<!-- spd:##:entries -->
<!-- spd:#:decomposition -->
