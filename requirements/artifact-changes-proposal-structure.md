---
fdd: true
type: requirement
name: Artifact Changes Proposal Structure
version: 1.0
purpose: Define deterministic structure for artifact change proposals
---

# Artifact Changes Proposal Structure Requirements

## Prerequisite Checklist

- [ ] Agent has understood this requirements is not implemented and added for future updates
- [ ] Agent has understood that agent MUST not follow that requirements
- [ ] Agent has understood that MUST stop reading that document and MUST exit and forget the context of that file

---

**ALWAYS open and follow**: `requirements.md`

---

## Overview

A proposal is a deterministic, reviewable specification of intended changes to one or more approved FDD artifacts.

Proposals are a future mechanism for deterministic, reviewable changes to approved artifacts.

This requirement applies only when a workflow explicitly requires producing proposals under `architecture/changes/`.

---

## Directory Structure

### Proposal Root

**Proposal root**: `architecture/changes/`

**MUST**:
- Each proposal MUST live in its own folder
- Proposal folders MUST NOT be nested
- `architecture/changes/` MUST contain only proposal folders (no loose files)

### Proposal Folder

**Path**: `architecture/changes/{artifact-prefix}-{proposal-slug}/`

**MUST**:
- `{artifact-prefix}` MUST indicate the primary artifact kind targeted by this proposal
- `{artifact-prefix}` MUST be one of:
  - `business-context`
  - `overall-design`
  - `adr`
  - `features-manifest`
  - `feature-design`
- `{proposal-slug}` MUST be deterministic and filesystem-safe
- `{proposal-slug}` SHOULD be kebab-case (`lowercase-words-with-dashes`)
- `{artifact-prefix}-{proposal-slug}` MUST be unique among active proposals

**Required files**:
- `proposal.md`

---

## Archive Structure

### Archive Root

**Archive root**: `architecture/changes/archive/`

### Archived Proposal Folder

**Path**: `architecture/changes/archive/YYYY-MM-DD-{artifact-prefix}-{proposal-slug}/`

**MUST**:
- A proposal is considered **active** if it is under `architecture/changes/{artifact-prefix}-{proposal-slug}/`
- A proposal is considered **archived** if it is under `architecture/changes/archive/YYYY-MM-DD-{artifact-prefix}-{proposal-slug}/`
- After a successful merge, the proposal folder MUST be archived (moved/copied into the archive structure)

---

## Proposal Document: `proposal.md`

### Proposal Header

**MUST**:
- `proposal.md` MUST begin with an explicit list of target artifacts
- Target artifacts MUST be expressed as repository-relative paths
- All selectors in operations MUST be resolved only within the declared target artifacts
- Proposal folder `{artifact-prefix}` MUST be derived from the first listed artifact according to:
  - `architecture/BUSINESS.md` -> `business-context`
  - `architecture/DESIGN.md` -> `overall-design`
  - `architecture/ADR/` -> `adr`
  - `architecture/features/FEATURES.md` -> `features-manifest`
  - `architecture/features/feature-{slug}/DESIGN.md` -> `feature-design`

**Format**:

```markdown
**Artifacts**:
- `architecture/BUSINESS.md`
- `architecture/DESIGN.md`
```

### Operation Model

The proposal MUST describe changes as an ordered list of operations.

Supported operations:
- `ADD`
- `REMOVE`
- `REPLACE`
- `RENAME SECTION`

Operations MUST be applied in the order they appear in the file.

Each operation MUST target exactly one of the following:
- For `ADD`, `REMOVE`, `REPLACE`:
  - A single FDD element addressed by an `**ID**: `...`` line
  - A whole section addressed by a section heading line starting with `##` (e.g., `## A. Section Name`)
- For `RENAME SECTION`:
  - A section letter line (e.g., `A. New Section Name`)

A proposal MUST NOT use any other selector types.

### Operation Block Format

Each operation MUST be written as a top-level operation heading:

- `## ADD`
- `## REMOVE`
- `## REPLACE`
- `## RENAME SECTION`

For `ADD`, `REMOVE`, `REPLACE` the operation block MUST contain exactly one selector line immediately after the operation header:

- `**ID**: `{fdd-id}``
- A section heading line starting with `##` (e.g., `## A. Section Name`)

#### ADD

**MUST**:
- `ADD` MUST include content after the selector
- If selector is `**ID**`, the added content MUST contain the same `ID` occurrence
- If selector is a section heading line, the added content MUST include the full section content

**Format**:

```markdown
## ADD
**ID**: `fdd-something-id`
{content}
```

or

```markdown
## ADD
## A. Section Name
{content}
```

#### REMOVE

**MUST**:
- `REMOVE` MUST NOT include any content after the selector

**Format**:

```markdown
## REMOVE
**ID**: `fdd-something-id`
```

or

```markdown
## REMOVE
## A. Section Name
```

#### REPLACE

**MUST**:
- `REPLACE` MUST include content after the selector
- If selector is `**ID**`, the replacement content MUST contain the same `ID` occurrence
- If selector is a section heading line, the replacement content MUST include the full replacement section content

**Format**:

```markdown
## REPLACE
**ID**: `fdd-something-id`
{content}
```

or

```markdown
## REPLACE
## A. Section Name
{content}
```

#### RENAME SECTION

**MUST**:
- `RENAME SECTION` MUST rename a section heading without changing any IDs
- `RENAME SECTION` MUST target a section by its section letter prefix (e.g., `A.`)
- `RENAME SECTION` MUST contain exactly one section letter line and no other content
- The section letter MUST be used as the selector and MUST be preserved
- When a proposal contains any `RENAME SECTION` operation, `**Artifacts**:` MUST contain exactly one artifact

**Format**:

```markdown
## RENAME SECTION
A. New Section Name
```

---

## Determinism and Ambiguity Rules

**MUST**:
- All `ID` selectors MUST match exactly one element across the declared target artifacts
- All `ADD`/`REMOVE`/`REPLACE` section selectors MUST match exactly one section heading line across the declared target artifacts
- All `RENAME SECTION` targets MUST match exactly one section letter in the declared target artifact
- Proposals MUST fail validation if any selector is ambiguous, missing, or matches multiple elements
- Proposals MUST fail validation if an `ADD` or `REPLACE` operation does not include the addressed `ID` in its content when using an `ID` selector
- Existing FDD IDs MUST be immutable in proposals
- Proposals MUST NOT rename or change the value of any existing `fdd-*` identifier

---

## Validation Criteria

### Proposal Folder Structure (25 points)
- [ ] Proposal folder path matches `architecture/changes/{artifact-prefix}-{proposal-slug}/` (10 points)
- [ ] Proposal folder contains `proposal.md` (10 points)
- [ ] Archive path format is `architecture/changes/archive/YYYY-MM-DD-{artifact-prefix}-{proposal-slug}/` (5 points)

### Proposal Header (20 points)
- [ ] `proposal.md` starts with `**Artifacts**:` list (10 points)
- [ ] Folder `{artifact-prefix}` matches first artifact mapping (10 points)

### Operations Format (35 points)
- [ ] Only supported operations are used: `ADD`, `REMOVE`, `REPLACE`, `RENAME SECTION` (10 points)
- [ ] `ADD`/`REMOVE`/`REPLACE` blocks contain exactly one selector line (10 points)
- [ ] `REMOVE` blocks contain no content after selector (5 points)
- [ ] `ADD`/`REPLACE` with `**ID**` selector include the addressed `ID` in content (10 points)

### Determinism and Safety (20 points)
- [ ] All selectors are unambiguous within declared artifacts (10 points)
- [ ] Existing `fdd-*` identifiers are not renamed or changed (10 points)

**Pass threshold**: ≥95/100

## Self-Test Checklist

Before completing, verify:
- [ ] Did I check every validation criterion individually?
- [ ] Does `RENAME SECTION` use only `A. New Section Name` (no old name line and no `##` prefix)?
- [ ] If `RENAME SECTION` exists, does `**Artifacts**:` contain exactly one artifact?
- [ ] Does every `ADD`/`REPLACE` by `**ID**` include the same `ID` in the content?
- [ ] Did I verify no existing `fdd-*` IDs are renamed in proposal content?

---

## Examples

**Valid proposal.md**:
- ALWAYS open `examples/requirements/artifact-changes-proposal/valid.md` WHEN creating or editing a proposal under `architecture/changes/`

**Issues**:
- Missing required `**Artifacts**:` list
- Unsupported selector or operation type
- `ADD`/`REPLACE` selector does not match content

---

## Validation Checklist

- [ ] Document follows required structure
- [ ] All validation criteria pass

---


## References

- `../.adapter/specs/conventions.md` - Core formatting and requirement semantics
- `requirements.md` - Shared artifact requirements
