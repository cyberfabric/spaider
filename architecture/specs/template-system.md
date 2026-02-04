<!-- spd:#:spec -->
# Spec: Template System

<!-- spd:id-ref:spec has="task" -->
- [x] - `spd-spider-spec-template-system`
<!-- spd:id-ref:spec -->

<!-- spd:##:context -->
## 1. Spec Context

<!-- spd:overview -->
### 1. Overview
The Template System provides marker-based parsing and validation for Spider artifacts. It enables deterministic structural validation by parsing templates with Spider markers (`spd:type:name` format), matching artifact content against template structure, and extracting/validating Spider IDs.

Problem: AI agents need deterministic validation of artifacts to ensure consistent quality.
Primary value: Enables machine-readable artifact structure with automated validation.
Key assumptions: Templates use Spider marker syntax; artifacts follow template structure.
<!-- spd:overview -->

<!-- spd:paragraph:purpose -->
### 2. Purpose
Enable deterministic parsing and validation of Spider artifacts against marker-based templates, ensuring structural compliance and ID integrity across the artifact hierarchy.

Success criteria: All artifacts validate in <100ms; marker parsing handles all valid template syntax; cross-validation detects orphaned and missing references.
<!-- spd:paragraph:purpose -->

### 3. Actors
<!-- spd:id-ref:actor -->
- `spd-spider-actor-developer`
- `spd-spider-actor-architect`
- `spd-spider-actor-ai-assistant`
<!-- spd:id-ref:actor -->

### 4. References
<!-- spd:list:references -->
- Overall Design: [DESIGN.md](../DESIGN.md)
- ADRs: `spd-spider-adr-template-centric-architecture-v1`
- Related spec: [Rules Packages](./rules-packages.md)
- Implementation: `skills/spider/scripts/spider/utils/template.py`
<!-- spd:list:references -->
<!-- spd:##:context -->

<!-- spd:##:flows -->
## 2. Actor Flows

<!-- spd:###:flow-title repeat="many" -->
### Load Template

<!-- spd:id:flow has="task" to_code="true" -->
- [x] **ID**: `spd-spider-spec-template-system-flow-load`

**Actors**:
<!-- spd:id-ref:actor -->
- `spd-spider-actor-ai-assistant`
<!-- spd:id-ref:actor -->

<!-- spd:sdsl:flow-steps -->
1. [x] - `p1` - CLI receives template path from weaver package - `inst-receive-path`
2. [x] - `p1` - File: READ template content from `{weaver}/artifacts/{KIND}/template.md` - `inst-read-file`
3. [x] - `p1` - Parse YAML frontmatter (version, kind, policy) - `inst-parse-frontmatter`
4. [x] - `p1` - **IF** frontmatter missing or invalid **RETURN** error "Invalid template frontmatter" - `inst-check-frontmatter`
5. [x] - `p1` - Algorithm: parse marker blocks using `spd-spider-spec-template-system-algo-parse-markers` - `inst-parse-markers`
6. [x] - `p1` - State: transition template to LOADED using `spd-spider-spec-template-system-state-lifecycle` - `inst-set-loaded`
7. [x] - `p1` - **RETURN** Template object with blocks, version, policy - `inst-return-template`
<!-- spd:sdsl:flow-steps -->
<!-- spd:id:flow -->
<!-- spd:###:flow-title repeat="many" -->

<!-- spd:###:flow-title repeat="many" -->
### Validate Artifact

<!-- spd:id:flow has="task" to_code="true" -->
- [x] **ID**: `spd-spider-spec-template-system-flow-validate`

**Actors**:
<!-- spd:id-ref:actor -->
- `spd-spider-actor-developer`
- `spd-spider-actor-ai-assistant`
<!-- spd:id-ref:actor -->

<!-- spd:sdsl:flow-steps -->
1. [x] - `p1` - CLI receives artifact path and resolves template from registry - `inst-resolve-template`
2. [x] - `p1` - File: READ artifact content from path - `inst-read-artifact`
3. [x] - `p1` - Algorithm: parse artifact blocks using `spd-spider-spec-template-system-algo-parse-markers` - `inst-parse-artifact`
4. [x] - `p1` - Algorithm: match artifact blocks to template using `spd-spider-spec-template-system-algo-match-blocks` - `inst-match-blocks`
5. [x] - `p1` - **FOR EACH** matched block pair (template, artifact): - `inst-loop-blocks`
   1. [x] - `p1` - Algorithm: validate content using `spd-spider-spec-template-system-algo-validate-content` - `inst-validate-content`
6. [x] - `p1` - Algorithm: extract and validate IDs using `spd-spider-spec-template-system-algo-extract-ids` - `inst-extract-ids`
7. [x] - `p1` - **IF** kind="SPEC": validate filename matches main spec ID slug - `inst-validate-filename`
8. [x] - `p1` - **IF** errors exist **RETURN** ValidationResult(status=FAIL, errors) - `inst-return-fail`
9. [x] - `p1` - **RETURN** ValidationResult(status=PASS, ids, refs) - `inst-return-pass`
<!-- spd:sdsl:flow-steps -->
<!-- spd:id:flow -->
<!-- spd:###:flow-title repeat="many" -->

<!-- spd:###:flow-title repeat="many" -->
### Cross-Validate Artifacts

<!-- spd:id:flow has="task" to_code="true" -->
- [x] **ID**: `spd-spider-spec-template-system-flow-cross-validate`

**Actors**:
<!-- spd:id-ref:actor -->
- `spd-spider-actor-architect`
- `spd-spider-actor-ai-assistant`
<!-- spd:id-ref:actor -->

<!-- spd:sdsl:flow-steps -->
1. [x] - `p1` - CLI loads all artifacts from registry - `inst-load-all`
2. [x] - `p1` - **FOR EACH** artifact in registry: - `inst-loop-artifacts`
   1. [x] - `p1` - Flow: validate artifact using `spd-spider-spec-template-system-flow-validate` - `inst-validate-each`
   2. [x] - `p1` - Collect all defined IDs into global set - `inst-collect-ids`
   3. [x] - `p1` - Collect all referenced IDs into global set - `inst-collect-refs`
3. [x] - `p1` - **FOR EACH** reference in all refs: - `inst-loop-refs`
   1. [x] - `p1` - **IF** reference not in defined IDs AND not external **RETURN** error "Orphaned reference" - `inst-check-orphan`
4. [x] - `p1` - **RETURN** CrossValidationResult(artifacts, orphaned_refs, coverage) - `inst-return-cross`
<!-- spd:sdsl:flow-steps -->
<!-- spd:id:flow -->
<!-- spd:###:flow-title repeat="many" -->
<!-- spd:##:flows -->

<!-- spd:##:algorithms -->
## 3. Algorithms

<!-- spd:###:algo-title repeat="many" -->
### Parse Marker Blocks

<!-- spd:id:algo has="task" to_code="true" -->
- [x] **ID**: `spd-spider-spec-template-system-algo-parse-markers`

<!-- spd:sdsl:algo-steps -->
1. [x] - `p1` - Split content into lines - `inst-split-lines`
2. [x] - `p1` - Initialize empty block stack and results list - `inst-init-stack`
3. [x] - `p1` - **FOR EACH** line with index: - `inst-loop-lines`
   1. [x] - `p1` - **IF** line matches Spider marker pattern: - `inst-check-marker`
      1. [x] - `p1` - Parse marker type, name, and attributes using regex - `inst-parse-marker`
      2. [x] - `p1` - **IF** opening marker: push to stack with line number - `inst-push-open`
      3. [x] - `p1` - **IF** closing marker: pop from stack, create TemplateBlock - `inst-pop-close`
4. [x] - `p1` - **IF** stack not empty **RETURN** error "Unclosed markers" - `inst-check-unclosed`
5. [x] - `p1` - **RETURN** list of TemplateBlock objects - `inst-return-blocks`
<!-- spd:sdsl:algo-steps -->
<!-- spd:id:algo -->
<!-- spd:###:algo-title repeat="many" -->

<!-- spd:###:algo-title repeat="many" -->
### Match Blocks

<!-- spd:id:algo has="task" to_code="true" -->
- [x] **ID**: `spd-spider-spec-template-system-algo-match-blocks`

<!-- spd:sdsl:algo-steps -->
1. [x] - `p1` - Initialize matched pairs list and unmatched template blocks - `inst-init-match`
2. [x] - `p1` - **FOR EACH** template block: - `inst-loop-template`
   1. [x] - `p1` - Find corresponding artifact block by type and name - `inst-find-artifact`
   2. [x] - `p1` - **IF** found: add to matched pairs - `inst-add-matched`
   3. [x] - `p1` - **IF** not found AND block.required=true: add to errors - `inst-missing-required`
3. [x] - `p1` - **FOR EACH** artifact block not in matched: - `inst-loop-extra`
   1. [x] - `p1` - **IF** template.policy.unknown_sections="error": add to errors - `inst-unknown-error`
   2. [x] - `p1` - **IF** template.policy.unknown_sections="warn": add to warnings - `inst-unknown-warn`
4. [x] - `p1` - **RETURN** MatchResult(pairs, errors, warnings) - `inst-return-match`
<!-- spd:sdsl:algo-steps -->
<!-- spd:id:algo -->
<!-- spd:###:algo-title repeat="many" -->

<!-- spd:###:algo-title repeat="many" -->
### Extract IDs

<!-- spd:id:algo has="task" to_code="true" -->
- [x] **ID**: `spd-spider-spec-template-system-algo-extract-ids`

<!-- spd:sdsl:algo-steps -->
1. [x] - `p1` - Initialize definitions list and references list - `inst-init-lists`
2. [x] - `p1` - **FOR EACH** block with type="id": - `inst-loop-id-blocks`
   1. [x] - `p1` - Extract ID value using `_ID_DEF_RE` pattern - `inst-extract-def`
   2. [x] - `p1` - **IF** ID matches `spd-{system}-{kind}-{slug}` format: add to definitions - `inst-add-def`
   3. [x] - `p1` - **IF** ID invalid format: add to errors - `inst-invalid-id`
3. [x] - `p1` - **FOR EACH** block with type="id-ref": - `inst-loop-ref-blocks`
   1. [x] - `p1` - Extract referenced IDs using `_BACKTICK_ID_RE` pattern - `inst-extract-ref`
   2. [x] - `p1` - Add each reference to references list with source location - `inst-add-ref`
4. [x] - `p1` - Check for duplicate definitions - `inst-check-duplicates`
5. [x] - `p1` - **RETURN** IdResult(definitions, references, errors) - `inst-return-ids`
<!-- spd:sdsl:algo-steps -->
<!-- spd:id:algo -->
<!-- spd:###:algo-title repeat="many" -->

<!-- spd:###:algo-title repeat="many" -->
### Validate Block Content

<!-- spd:id:algo has="task" to_code="true" -->
- [x] **ID**: `spd-spider-spec-template-system-algo-validate-content`

<!-- spd:sdsl:algo-steps -->
1. [x] - `p1` - Dispatch based on block type from `VALID_MARKER_TYPES` - `inst-dispatch`
2. [x] - `p1` - **IF** type="paragraph": validate non-empty text content - `inst-validate-paragraph`
3. [x] - `p1` - **IF** type="list": validate bullet or numbered list format - `inst-validate-list`
4. [x] - `p1` - **IF** type="table": validate markdown table structure - `inst-validate-table`
5. [x] - `p1` - **IF** type="sdsl": validate SDSL instruction format with priorities - `inst-validate-sdsl`
6. [x] - `p1` - **IF** type starts with "#": validate heading level matches - `inst-validate-heading`
7. [x] - `p1` - **IF** type="code": validate fenced code block present - `inst-validate-code`
8. [x] - `p1` - **IF** type="free": skip validation (any content allowed) - `inst-validate-free`
9. [x] - `p1` - **IF** type="id": validate **ID**: format, priority if required - `inst-validate-id`
   1. [x] - `p1` - **IF** line has checkbox (`[ ]`/`[x]`) AND not list item **RETURN** error "Task checkbox must be in a list item" - `inst-validate-id-task-list`
10. [x] - `p1` - **IF** type="id-ref": validate ID reference format, priority if required - `inst-validate-id-ref`
    1. [x] - `p1` - **IF** line has checkbox (`[ ]`/`[x]`) AND not list item **RETURN** error "Task checkbox must be in a list item" - `inst-validate-id-ref-task-list`
11. [x] - `p1` - **RETURN** list of content errors - `inst-return-content-errors`
<!-- spd:sdsl:algo-steps -->
<!-- spd:id:algo -->
<!-- spd:###:algo-title repeat="many" -->
<!-- spd:##:algorithms -->

<!-- spd:##:states -->
## 4. States

<!-- spd:###:state-title repeat="many" -->
### Template Loading Lifecycle

<!-- spd:id:state has="task" to_code="true" -->
- [x] **ID**: `spd-spider-spec-template-system-state-lifecycle`

<!-- spd:sdsl:state-transitions -->
1. [x] - `p1` - **FROM** UNINITIALIZED **TO** LOADING **WHEN** from_path() called - `inst-start-load`
2. [x] - `p1` - **FROM** LOADING **TO** LOADED **WHEN** parsing succeeds - `inst-load-success`
3. [x] - `p1` - **FROM** LOADING **TO** ERROR **WHEN** parsing fails - `inst-load-error`
4. [x] - `p1` - **FROM** LOADED **TO** VALIDATING **WHEN** validate() called - `inst-start-validate`
5. [x] - `p1` - **FROM** VALIDATING **TO** LOADED **WHEN** validation completes - `inst-validate-complete`
<!-- spd:sdsl:state-transitions -->
<!-- spd:id:state -->
<!-- spd:###:state-title repeat="many" -->
<!-- spd:##:states -->

<!-- spd:##:requirements -->
## 5. Definition of Done

<!-- spd:###:req-title repeat="many" -->
### Template Parsing

<!-- spd:id:req has="priority,task" to_code="true" -->
- [x] `p1` - **ID**: `spd-spider-spec-template-system-req-parsing`

<!-- spd:paragraph:req-body -->
Templates with Spider markers are parsed into structured TemplateBlock objects with type, name, attributes, and line ranges. Supports all marker types in VALID_MARKER_TYPES including id, id-ref, list, paragraph, table, sdsl, headings, and free.
<!-- spd:paragraph:req-body -->

**Implementation details**:
<!-- spd:list:req-impl -->
- API: `Template.from_path(path)` returns `(Template, errors)`
- Module: `skills/spider/scripts/spider/utils/template.py`
- Domain: `Template`, `TemplateBlock`, `TemplateVersion`, `TemplatePolicy`
<!-- spd:list:req-impl -->

**Implements**:
<!-- spd:id-ref:flow has="priority" -->
- `p1` - `spd-spider-spec-template-system-flow-load`
<!-- spd:id-ref:flow -->

<!-- spd:id-ref:algo has="priority" -->
- `p1` - `spd-spider-spec-template-system-algo-parse-markers`
<!-- spd:id-ref:algo -->

**Covers (PRD)**:
<!-- spd:id-ref:fr -->
- `spd-spider-fr-artifact-templates`
- `spd-spider-fr-validation`
<!-- spd:id-ref:fr -->

<!-- spd:id-ref:nfr -->
- `spd-spider-nfr-validation-performance`
<!-- spd:id-ref:nfr -->

**Covers (DESIGN)**:
<!-- spd:id-ref:principle -->
- `spd-spider-principle-machine-readable`
- `spd-spider-principle-deterministic-gate`
<!-- spd:id-ref:principle -->

<!-- spd:id-ref:constraint -->
- `spd-spider-constraint-markdown`
- `spd-spider-constraint-stdlib-only`
<!-- spd:id-ref:constraint -->

<!-- spd:id-ref:component -->
- `spd-spider-component-spider-skill`
<!-- spd:id-ref:component -->

<!-- spd:id-ref:seq -->
- `spd-spider-seq-validate-overall-design`
<!-- spd:id-ref:seq -->

<!-- spd:id-ref:dbtable -->
- `spd-spider-dbtable-na`
<!-- spd:id-ref:dbtable -->
<!-- spd:id:req -->
<!-- spd:###:req-title repeat="many" -->

<!-- spd:###:req-title repeat="many" -->
### Artifact Validation

<!-- spd:id:req has="priority,task" to_code="true" -->
- [x] `p1` - **ID**: `spd-spider-spec-template-system-req-validation`

<!-- spd:paragraph:req-body -->
Artifacts are validated against their templates with block matching, content validation per type, and ID extraction. Returns structured ValidationResult with PASS/FAIL status, errors list, and extracted IDs/references.
<!-- spd:paragraph:req-body -->

**Implementation details**:
<!-- spd:list:req-impl -->
- API: `Template.validate(artifact_path)` returns `Dict[str, List[errors]]`
- API: `Artifact.validate()` returns validation result
- Module: `skills/spider/scripts/spider/utils/template.py`
- Domain: `Artifact`, `ArtifactBlock`, `IdDefinition`, `IdReference`
<!-- spd:list:req-impl -->

**Implements**:
<!-- spd:id-ref:flow has="priority" -->
- `p1` - `spd-spider-spec-template-system-flow-validate`
<!-- spd:id-ref:flow -->

<!-- spd:id-ref:algo has="priority" -->
- `p1` - `spd-spider-spec-template-system-algo-match-blocks`
- `p1` - `spd-spider-spec-template-system-algo-extract-ids`
- `p1` - `spd-spider-spec-template-system-algo-validate-content`
<!-- spd:id-ref:algo -->

**Covers (PRD)**:
<!-- spd:id-ref:fr -->
- `spd-spider-fr-validation`
- `spd-spider-fr-template-qa`
<!-- spd:id-ref:fr -->

<!-- spd:id-ref:nfr -->
- `spd-spider-nfr-validation-performance`
<!-- spd:id-ref:nfr -->

**Covers (DESIGN)**:
<!-- spd:id-ref:principle -->
- `spd-spider-principle-deterministic-gate`
- `spd-spider-principle-machine-readable-artifacts`
<!-- spd:id-ref:principle -->

<!-- spd:id-ref:constraint -->
- `spd-spider-constraint-markdown`
<!-- spd:id-ref:constraint -->

<!-- spd:id-ref:component -->
- `spd-spider-component-spider-skill`
<!-- spd:id-ref:component -->

<!-- spd:id-ref:seq -->
- `spd-spider-seq-validate-overall-design`
<!-- spd:id-ref:seq -->

<!-- spd:id-ref:dbtable -->
- `spd-spider-dbtable-na`
<!-- spd:id-ref:dbtable -->
<!-- spd:id:req -->
<!-- spd:###:req-title repeat="many" -->

<!-- spd:###:req-title repeat="many" -->
### Cross-Artifact Validation

<!-- spd:id:req has="priority,task" to_code="true" -->
- [x] `p1` - **ID**: `spd-spider-spec-template-system-req-cross-validation`

<!-- spd:paragraph:req-body -->
Multiple artifacts are validated together to detect orphaned references (refs pointing to undefined IDs) and missing references. Supports external system references via prefix detection.
<!-- spd:paragraph:req-body -->

**Implementation details**:
<!-- spd:list:req-impl -->
- API: `cross_validate_artifacts(artifacts, project_root)` returns cross-validation result
- Module: `skills/spider/scripts/spider/utils/template.py`
- Domain: Uses Artifact.list_ids(), Artifact.list_refs()
<!-- spd:list:req-impl -->

**Implements**:
<!-- spd:id-ref:flow has="priority" -->
- `p1` - `spd-spider-spec-template-system-flow-cross-validate`
<!-- spd:id-ref:flow -->

<!-- spd:id-ref:algo has="priority" -->
- `p1` - `spd-spider-spec-template-system-algo-extract-ids`
<!-- spd:id-ref:algo -->

**Covers (PRD)**:
<!-- spd:id-ref:fr -->
- `spd-spider-fr-cross-artifact-validation`
- `spd-spider-fr-traceability`
<!-- spd:id-ref:fr -->

<!-- spd:id-ref:nfr -->
- `spd-spider-nfr-validation-performance`
<!-- spd:id-ref:nfr -->

**Covers (DESIGN)**:
<!-- spd:id-ref:principle -->
- `spd-spider-principle-traceability`
- `spd-spider-principle-deterministic-gate`
<!-- spd:id-ref:principle -->

<!-- spd:id-ref:constraint -->
- `spd-spider-constraint-stdlib-only`
<!-- spd:id-ref:constraint -->

<!-- spd:id-ref:component -->
- `spd-spider-component-spider-skill`
<!-- spd:id-ref:component -->

<!-- spd:id-ref:seq -->
- `spd-spider-seq-traceability-query`
<!-- spd:id-ref:seq -->

<!-- spd:id-ref:dbtable -->
- `spd-spider-dbtable-na`
<!-- spd:id-ref:dbtable -->
<!-- spd:id:req -->
<!-- spd:###:req-title repeat="many" -->
<!-- spd:##:requirements -->

<!-- spd:##:additional-context -->
## 6. Additional Context (optional)

<!-- spd:free:context-notes -->
**Implementation Notes**:

The Template System is implemented in `skills/spider/scripts/spider/utils/template.py` (~1200 LOC) with:
- `Template` class: Parses and holds template structure
- `Artifact` class: Parses artifacts against templates
- `TemplateBlock` dataclass: Represents a marker block span
- Key regex patterns: `_MARKER_RE`, `_ID_DEF_RE`, `_ID_REF_RE`, `_BACKTICK_ID_RE`

**Marker Types Supported** (`VALID_MARKER_TYPES`):
- Content: `free`, `paragraph`, `list`, `numbered-list`, `task-list`, `table`, `code`
- Identity: `id`, `id-ref`
- Structure: `#`, `##`, `###`, `####`, `#####`, `######`
- Special: `link`, `image`, `sdsl`

**SDSL (Spider DSL)** format:
```
N. [ ] - `pN` - Description - `inst-slug`
```

**Dependencies**: None (Python stdlib only per `spd-spider-constraint-stdlib-only`)
<!-- spd:free:context-notes -->
<!-- spd:##:additional-context -->

<!-- spd:#:spec -->
