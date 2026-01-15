---
name: fdd-artifact-validate
description: Validate FDD artifacts (BUSINESS.md, DESIGN.md, ADR.md, FEATURES.md, feature DESIGN.md, feature CHANGES.md) against FDD requirements/*-structure.md. Also supports codebase traceability scan for a feature directory to verify implemented DESIGN/CHANGES items are tagged in code.
---

# FDD Artifact Validate

## Goal

Produce a deterministic validation report for an FDD artifact using the relevant `requirements/*-structure.md` file as the source of truth.

## Preconditions

1. ALWAYS follow `../SKILLS.md` Toolchain Preflight.
2. The target artifact file MUST exist.

## How to run

Run the validator script:

- `python3 scripts/validate_artifact.py --artifact {path}`

Codebase traceability scan (directory-mode):

- Code-root mode (recommended):
  - `python3 scripts/validate_artifact.py --artifact {code-root}`
  - `{code-root}` MUST contain `architecture/features/feature-*/DESIGN.md`
  - Optional filtering:
    - `python3 scripts/validate_artifact.py --artifact {code-root} --features gts-core,init-module`

- Feature-dir mode (backwards compatible):
  - `python3 scripts/validate_artifact.py --artifact {feature-dir}`
  - Expects `{feature-dir}/DESIGN.md`
  - Uses `{feature-dir}/CHANGES.md` (or `{feature-dir}/archive/YYYY-MM-DD-CHANGES.md` if CHANGES.md is missing)
  - Scans code files under `{feature-dir}` (with an automatic fallback to scan the module root when code is not located under the feature directory)

Optional:
- `python3 scripts/validate_artifact.py --artifact {path} --requirements {path}`
- `python3 scripts/validate_artifact.py --artifact {path} --output {path}`

## What this validates

- Required sections (derived from the relevant `requirements/*-structure.md` file)
- Placeholder markers: `TODO`, `TBD`

For directory-mode traceability scan:
- The validator MUST validate the relevant `DESIGN.md` and `CHANGES.md` first.
- If feature artifacts are invalid, the traceability scan MUST fail early (do not validate code markers against invalid artifacts).
- For each implemented scope in DESIGN (`- [x] **ID**: ...`), expects a corresponding `@fdd-{kind}:...:ph-{N}` tag in code (flow/algo/state/req/test)
- For each implemented FDL step line in DESIGN (`[x] ... - `inst-...``), expects an instruction-level marker in code:
  - `fdd-...-(flow|algo|state|test)-...:ph-{N}:inst-{local}`
- For each completed change in CHANGES (`**Status**: ✅ COMPLETED`), expects a corresponding `@fdd-change:...:ph-{N}` tag in code

## Artifact type detection

If `--requirements` is not provided, the script selects a requirements file by artifact path:

- `BUSINESS.md` -> `requirements/business-context-structure.md`
- `ADR.md` -> `requirements/adr-structure.md`
- `FEATURES.md` -> `requirements/features-manifest-structure.md`
- `DESIGN.md` (feature scope) -> `requirements/feature-design-structure.md`
- `CHANGES.md` -> `requirements/feature-changes-structure.md`
- `DESIGN.md` (non-feature scope) -> `requirements/overall-design-structure.md`

## Output

The script outputs JSON suitable for:
- pasting into chat
- attaching to CI logs
- feeding into follow-up decisions

## Progressive disclosure

- Use this skill to generate the machine report.
- Use the referenced `requirements/*-structure.md` file only for deeper manual inspection.
