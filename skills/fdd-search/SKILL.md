---
name: fdd-search
description: Read-only search and traceability for FDD artifacts and FDD/ADR IDs. Supports listing sections/IDs/items, reading blocks by section/heading/id, text search, and repo-wide traceability (scan-ids, where-defined, where-used incl. :ph/:inst).
---

## Purpose

Read and search FDD artifacts deterministically, and perform repo-wide FDD/ADR ID traceability.
This skill is **read-only** and MUST NOT write or edit any artifact.

## When to use

Use this skill whenever you need to interact with FDD artifacts or FDD ID traceability:

- **Read/inspect** an artifact deterministically (list sections/IDs/items, get a structured block).
- **Traceability** across repo: enumerate IDs (`scan-ids`), resolve normative definitions (`where-defined`), and find usages excluding definitions (`where-used`).

All commands print JSON to stdout and are intended to be machine-consumed (stable ordering).

## Preconditions

- ALWAYS follow `../SKILLS.md` Toolchain Preflight.
- `python3` is available.
- Target paths exist and are readable.

## Command

This skill exposes read-only operations via subcommands.
The first argv is the subcommand name.

## Subcommands

### Read/Search

```bash
python3 scripts/fdd-search.py list-sections --artifact {path}
python3 scripts/fdd-search.py list-sections --artifact {path} --under-heading "{Exact Heading}"

python3 scripts/fdd-search.py list-ids --artifact {path}
python3 scripts/fdd-search.py list-ids --artifact {path} --pattern "{substring}"
python3 scripts/fdd-search.py list-ids --artifact {path} --pattern "{regex}" --regex
python3 scripts/fdd-search.py list-ids --artifact {path} --under-heading "{Exact Heading}"

python3 scripts/fdd-search.py read-section --artifact {path} --section {A|B|C}
python3 scripts/fdd-search.py read-section --artifact {path} --heading "{Exact Heading}"
python3 scripts/fdd-search.py read-section --artifact {path-to-FEATURES.md} --feature-id {fdd-...-feature-...}
python3 scripts/fdd-search.py read-section --artifact {path-to-CHANGES.md} --change {N}
python3 scripts/fdd-search.py read-section --artifact {path} --id {any-id-substring}

python3 scripts/fdd-search.py list-items --artifact {path}
python3 scripts/fdd-search.py list-items --artifact {path} --type {actor|capability|usecase|requirement|feature|flow|algo|state|test|change|adr}
python3 scripts/fdd-search.py list-items --artifact {path} --lod {id|summary}
python3 scripts/fdd-search.py list-items --artifact {path} --pattern "{substring}"
python3 scripts/fdd-search.py list-items --artifact {path} --pattern "{regex}" --regex
python3 scripts/fdd-search.py list-items --artifact {path} --under-heading "{Exact Heading}"

python3 scripts/fdd-search.py get-item --artifact {path} --id {any-id-substring}
python3 scripts/fdd-search.py get-item --artifact {path} --heading "{Exact Heading}"
python3 scripts/fdd-search.py get-item --artifact {path} --section {A|B|C}
python3 scripts/fdd-search.py get-item --artifact {path-to-FEATURES.md} --feature-id {fdd-...-feature-...}
python3 scripts/fdd-search.py get-item --artifact {path-to-CHANGES.md} --change {N}

python3 scripts/fdd-search.py find-id --artifact {path} --id {any-id-substring}

python3 scripts/fdd-search.py search --artifact {path} --query "{literal}"
python3 scripts/fdd-search.py search --artifact {path} --query "{regex}" --regex

# Traceability (Cross-reference)

# Scan IDs under a root (file or directory)
python3 scripts/fdd-search.py scan-ids --root {file-or-dir}
python3 scripts/fdd-search.py scan-ids --root {file-or-dir} --pattern "{substring}"
python3 scripts/fdd-search.py scan-ids --root {file-or-dir} --pattern "{regex}" --regex

# Scan options
python3 scripts/fdd-search.py scan-ids --root {file-or-dir} --kind {all|fdd|adr}
python3 scripts/fdd-search.py scan-ids --root {file-or-dir} --all
python3 scripts/fdd-search.py scan-ids --root {file-or-dir} --include "**/*.rs" --include "**/*.md"
python3 scripts/fdd-search.py scan-ids --root {file-or-dir} --exclude "target/**" --exclude "node_modules/**"
python3 scripts/fdd-search.py scan-ids --root {file-or-dir} --max-bytes 5000000

# IMPORTANT: if pattern starts with '-', use '=' form:
python3 scripts/fdd-search.py scan-ids --root {file-or-dir} --pattern=-actor-

# Find where an ID is DEFINED (normative)
python3 scripts/fdd-search.py where-defined --root {repo-root} --id {fdd-id-or-ADR-0001}

# Qualified IDs (phase/instruction): base -> ph -> inst
python3 scripts/fdd-search.py where-defined --root {repo-root} --id {base-id}:ph-1
python3 scripts/fdd-search.py where-defined --root {repo-root} --id {base-id}:ph-1:inst-some-job

# Optionally treat @fdd-* code tags as definitions too
python3 scripts/fdd-search.py where-defined --root {repo-root} --id {base-id}:ph-1 --include-tags

# Definition lookup options
python3 scripts/fdd-search.py where-defined --root {repo-root} --id {id} --include "modules/**" --include "**/architecture/**"
python3 scripts/fdd-search.py where-defined --root {repo-root} --id {id} --exclude "target/**" --exclude "node_modules/**"
python3 scripts/fdd-search.py where-defined --root {repo-root} --id {id} --max-bytes 5000000

# Find where an ID is USED (all occurrences EXCEPT normative definitions)
python3 scripts/fdd-search.py where-used --root {repo-root} --id {fdd-id-or-qualified-id}

# Filtering for repo-wide commands
python3 scripts/fdd-search.py where-used --root {repo-root} --id {id} --include "**/*.rs" --include "**/*.md"
python3 scripts/fdd-search.py where-used --root {repo-root} --id {id} --exclude "target/**" --exclude "node_modules/**"
python3 scripts/fdd-search.py where-used --root {repo-root} --id {id} --max-bytes 5000000
```

### Traceability semantics

- `where-defined`
  - Resolves **normative** definition location based on ID type and searches only in expected artifacts by default.
  - Supports both root-level `architecture/...` and module-local `modules/*/architecture/...` layouts.
  - Supports qualified queries `{base-id}:ph-{N}:inst-{name}`:
    - Finds the base `**ID**:` line.
    - Then searches inside the corresponding feature-design block for `ph-*` and `inst-*` tokens.
  - Output fields:
    - `status` (`FOUND`/`AMBIGUOUS`/`NOT_FOUND`)
    - `definitions` (matches; for qualified queries this is typically an `fdl_phase`/`fdl_inst` line)
    - `context_definitions` (base `**ID**:` line(s) for qualified queries)
    - `base_id`, `phase`, `inst`
  - Exit codes:
    - `0` if exactly one definition.
    - `2` if ambiguous (multiple definitions).
    - `1` if not found.

- `where-used`
  - Returns all occurrences of the query **excluding** normative definition lines.
  - Output fields:
    - `hits`
    - `base_id`, `phase`, `inst`
