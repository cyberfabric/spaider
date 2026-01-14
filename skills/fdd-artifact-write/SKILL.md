---
name: fdd-artifact-write
description: Write (create/update) an FDD artifact from provided content and auto-run fdd-artifact-validate.
---

## Purpose

Write an FDD artifact to disk (create or update) using content prepared by the agent, then run `fdd-artifact-validate` on the written file.

## Preconditions

- `python3` is available.
- You have the artifact content ready in a UTF-8 text file.
- You confirmed the paths to be written.

## Command

```bash
python3 scripts/write_artifact.py \
  --artifact {path-to-artifact} \
  --content-file {path-to-content-file} \
  --mode {create|update}
```

## Options

- `--skip-fs-checks`
  - Passes `--skip-fs-checks` to the validator.
  - Use for deterministic tests or when filesystem cross-checks are not available.

## Behavior

- `--mode create`
  - Fails if the target artifact already exists.
- `--mode update`
  - Fails if the target artifact does not exist.
- Always writes the file first, then runs the validator.
- Always prints the validator JSON report to stdout.
- Exit code:
  - `0` when validation status is PASS.
  - `2` when validation status is FAIL.
  - `1` for usage or IO errors.

## Notes

- The script does not rollback file changes if validation fails.
- The validator output is authoritative.
