---
name: fdd-artifact-validate
description: Validate FDD artifacts (BUSINESS.md, DESIGN.md, ADR.md, FEATURES.md, feature DESIGN.md, feature CHANGES.md) against FDD requirements/*-structure.md by checking required sections and placeholder markers (TODO/TBD). Use before running any FDD validation workflow or when reviewing changes to FDD artifacts.
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

Optional:
- `python3 scripts/validate_artifact.py --artifact {path} --requirements {path}`
- `python3 scripts/validate_artifact.py --artifact {path} --output {path}`

## What this validates

- Required sections (derived from the relevant `requirements/*-structure.md` file)
- Placeholder markers: `TODO`, `TBD`

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
