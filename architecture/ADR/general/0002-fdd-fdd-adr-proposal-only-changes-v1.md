# ADR-0002: Proposal-Only Changes to Approved Artifacts

**Date**: 2026-01-20

**Status**: Accepted

**ADR ID**: `fdd-fdd-adr-proposal-only-changes-v1`

## Context and Problem Statement

FDD workflows and AI agents may need to update approved artifacts under `architecture/` (e.g., `BUSINESS.md`, `DESIGN.md`, `ADR/`, `FEATURES.md`, feature `DESIGN.md`, feature `CHANGES.md`). Direct edits by automated tooling can cause accidental loss of content, non-deterministic diffs, and unreviewed changes to the authoritative state.

We need a single deterministic process for changing approved artifacts that supports review, conflict detection, auditability, and automated validation.

## Decision Drivers

1. **Determinism**
   - Changes must be representable as deterministic operations over precise selectors.

2. **Reviewability**
   - Human review must be possible before applying changes to approved artifacts.

3. **Traceability and Auditability**
   - The repository must preserve what was proposed, what was approved, and what was merged.

4. **AI Safety**
   - AI agents must not directly mutate approved artifacts.

## Considered Options

* Allow direct writes to approved artifacts
* Proposal-only workflow outputs (chosen)

## Pros and Cons of the Options

### Option 1: Allow Direct Writes to Approved Artifacts

**Description**: Operation workflows directly edit files under `architecture/`.

**Pros**:
* Simple implementation

**Cons**:
* High risk of accidental content loss
* Non-deterministic edits (agent rewriting formatting)
* Weak review story for automated changes

**Rejected**.

### Option 2: Proposal-Only Workflow Outputs (SELECTED)

**Description**: Operation workflows output deterministic proposals under `architecture/changes/` and never directly modify approved artifacts.

**Pros**:
* Deterministic, reviewable changes
* Enables automated proposal validation before merge
* Preserves audit trail

**Cons**:
* Requires proposal tooling (`fdd` merge/archive) and conventions

**Selected**.

## Decision Outcome

Chosen option: "Proposal-only workflow outputs", because it is the safest way to preserve approved artifact integrity while enabling automation, review, and deterministic validation before changes are applied.

All operation workflows MUST produce proposals under `architecture/changes/`.

Workflows MUST NOT directly modify approved artifacts under `architecture/` and `architecture/features/`.

Approved artifacts MUST be updated only by applying approved proposals via `fdd` merge/archive operations.

### Consequences

* Good, because approved artifacts become stable, reviewable, and changes become auditable and deterministic.
* Bad, because additional tooling and process is required to propose, review, and apply changes.

## Related Design Elements

**Requirements**:
* `fdd-fdd-req-artifact-change-management` - Defines how approved artifacts are changed
* `fdd-fdd-req-proposal-validation` - Requires deterministic validation of proposals
* `fdd-fdd-req-core-artifact-status` - Defines authoritative state and approvals

**Capabilities**:
* `fdd-fdd-capability-change-management` - Enables proposal workflow for artifact updates

**ADRs**:
* `fdd-fdd-adr-initial-architecture-v1` - Foundational architecture decision

This decision is directly tied to:

* Requirements:
  * `fdd-fdd-req-artifact-change-management`
  * `fdd-fdd-req-proposal-validation`
  * `fdd-fdd-req-core-artifact-status`
* Capabilities:
  * `fdd-fdd-capability-change-management`

## More Information

**Supersedes**: None

**Superseded by**: None

**Related ADRs**: `fdd-fdd-adr-initial-architecture-v1`
