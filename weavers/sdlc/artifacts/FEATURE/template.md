---
spider-template:
  version:
    major: 1
    minor: 0
  kind: FEATURE
  unknown_sections: warn
---

<!-- spd:#:feature-design -->
# Feature: {Feature Name}

<!-- spd:id-ref:feature has="task" -->
[ ] - `spd-{system}-feature-{feature-slug}`
<!-- spd:id-ref:feature -->

<!-- spd:##:context -->
## 1. Feature Context

<!-- spd:overview -->
### 1. Overview
{1-2 paragraphs summarizing what this feature does and why it exists.}

{Include:
- Problem statement
- Primary user value
- Key assumptions}
<!-- spd:overview -->

<!-- spd:paragraph:purpose -->
### 2. Purpose
{1-3 sentences describing the intended outcome of this feature.}

{Optionally include measurable success criteria.}
<!-- spd:paragraph:purpose -->

### 3. Actors
<!-- spd:id-ref:actor -->
- `spd-{system}-actor-{slug}`
- `spd-{system}-actor-{slug}`
<!-- spd:id-ref:actor -->

<!-- spd:list:references -->
### 4. References
- Overall Design: [DESIGN.md](../../DESIGN.md)
- ADRs: `spd-{system}-adr-{slug}`
- Related feature: `spd-{system}-feature-{slug}`
<!-- spd:list:references -->
<!-- spd:##:context -->

<!-- spd:##:flows -->
## 2. Actor Flows

<!-- spd:###:flow-title repeat="many" -->
### {Flow Name}

<!-- spd:id:flow has="task" to_code="true" -->
- [ ] **ID**: `spd-{system}-feature-{feature}-flow-{slug}`

**Actors**:
<!-- spd:id-ref:actor -->
- `spd-{system}-actor-{slug}`
<!-- spd:id-ref:actor -->

<!-- spd:fdl:flow-steps -->
1. [ ] - `p1` - Actor fills form (field1, field2) - `inst-fill-form`
2. [ ] - `p1` - API: POST /api/{resource} (body: field1, field2) - `inst-api-call`
3. [ ] - `p2` - Algorithm: validate input using <!-- spd:id-ref:algo has="task" required="false" -->[ ] - `spd-{system}-feature-{feature}-algo-{slug}`<!-- spd:id-ref:algo --> - `inst-run-algo`
4. [ ] - `p1` - DB: INSERT {table}(field1, field2, status) - `inst-db-insert`
5. [ ] - `p1` - DB: SELECT * FROM {table} WHERE condition - `inst-db-query`
6. [ ] - `p1` - File: READ config from {path} - `inst-file-read`
7. [ ] - `p1` - CLI: run `command --flag value` - `inst-cli-exec`
8. [ ] - `p1` - State: transition using <!-- spd:id-ref:state has="task" required="false" --> [ ] - `spd-{system}-feature-{feature}-state-{slug}`<!-- spd:id-ref:state --> - `inst-state-ref`
9. [ ] - `p2` - **IF** {condition}: - `inst-if`
   1. [ ] - `p2` - {nested step} - `inst-if-nested`
10. [ ] - `p1` - API: RETURN 201 Created (id, status) - `inst-return`
<!-- spd:fdl:flow-steps -->
<!-- spd:id:flow -->
<!-- spd:###:flow-title repeat="many" -->
<!-- spd:##:flows -->

<!-- spd:##:algorithms -->
## 3. Algorithms

<!-- spd:###:algo-title repeat="many" -->
### {Algorithm Name}

<!-- spd:id:algo has="task" to_code="true" -->
- [ ] **ID**: `spd-{system}-feature-{feature}-algo-{slug}`

<!-- spd:fdl:algo-steps -->
1. [ ] - `p1` - **IF** {field} is empty **RETURN** error "{validation message}" - `inst-validate`
2. [ ] - `p1` - retrieve {entity} from repository by {criteria} - `inst-fetch`
3. [ ] - `p1` - calculate {result} based on {business rule description} - `inst-calc`
4. [ ] - `p1` - transform {source data} into {target format} - `inst-transform`
5. [ ] - `p1` - **FOR EACH** {item} in {collection}: - `inst-loop`
   1. [ ] - `p1` - apply {operation} to {item} - `inst-loop-body`
6. [ ] - `p1` - normalize {data} according to {domain rules} - `inst-normalize`
7. [ ] - `p1` - **RETURN** {result description} - `inst-return`
<!-- spd:fdl:algo-steps -->
<!-- spd:id:algo -->
<!-- spd:###:algo-title repeat="many" -->
<!-- spd:##:algorithms -->

<!-- spd:##:states -->
## 4. States

<!-- spd:###:state-title repeat="many" -->
### {State Machine Name}

<!-- spd:id:state has="task" to_code="true" -->
- [ ] **ID**: `spd-{system}-feature-{feature}-state-{slug}`

<!-- spd:fdl:state-transitions -->
1. [ ] - `p1` - **FROM** {STATE} **TO** {STATE} **WHEN** {trigger} - `inst-transition-1`
2. [ ] - `p1` - **FROM** {STATE} **TO** {STATE} **WHEN** {trigger} - `inst-transition-2`
<!-- spd:fdl:state-transitions -->
<!-- spd:id:state -->
<!-- spd:###:state-title repeat="many" -->
<!-- spd:##:states -->

<!-- spd:##:requirements -->
## 5. Definition of Done

<!-- spd:###:req-title repeat="many" -->
### {Requirement Name}

<!-- spd:id:req has="priority,task" to_code="true" -->
- [ ] `p1` - **ID**: `spd-{system}-feature-{feature}-req-{slug}`

<!-- spd:paragraph:req-body -->
{Describe what must be true when this requirement is satisfied.}
<!-- spd:paragraph:req-body -->

<!-- spd:list:req-impl -->
**Implementation details**:
- API: {endpoints}
- DB: {tables/queries}
- Domain: {entities}
<!-- spd:list:req-impl -->

**Implements**:
<!-- spd:id-ref:flow has="priority" -->
- `p1` - `spd-{system}-feature-{feature}-flow-{slug}`
<!-- spd:id-ref:flow -->

<!-- spd:id-ref:algo has="priority" -->
- `p1` - `spd-{system}-feature-{feature}-algo-{slug}`
<!-- spd:id-ref:algo -->

**Covers (PRD)**:
<!-- spd:id-ref:fr -->
- `spd-{system}-fr-{slug}`
<!-- spd:id-ref:fr -->

<!-- spd:id-ref:nfr -->
- `spd-{system}-nfr-{slug}`
<!-- spd:id-ref:nfr -->

**Covers (DESIGN)**:
<!-- spd:id-ref:principle -->
- `spd-{system}-principle-{slug}`
<!-- spd:id-ref:principle -->

<!-- spd:id-ref:constraint -->
- `spd-{system}-constraint-{slug}`
<!-- spd:id-ref:constraint -->

<!-- spd:id-ref:component -->
- `spd-{system}-component-{slug}`
<!-- spd:id-ref:component -->

<!-- spd:id-ref:seq -->
- `spd-{system}-seq-{slug}`
<!-- spd:id-ref:seq -->

<!-- spd:id-ref:dbtable -->
- `spd-{system}-dbtable-{slug}`
<!-- spd:id-ref:dbtable -->

<!-- spd:id:req -->
<!-- spd:###:req-title repeat="many" -->
<!-- spd:##:requirements -->

<!-- spd:##:additional-context -->
## 6. Additional Context (optional)

<!-- spd:free:context-notes -->
{Optional notes, decisions, constraints, links, and rationale.}
<!-- spd:free:context-notes -->
<!-- spd:##:additional-context -->

<!-- spd:#:feature-design -->
