# ADR-0001: Use deterministic validation

**Date**: 2025-01-01

**Status**: Accepted

**ADR ID**: `fdd-demo-adr-deterministic-validation`

## Context and Problem Statement

We need consistent validation across artifacts and workflows.

## Considered Options

* Deterministic validation via `fdd validate`
* Manual validation only

## Decision Outcome

Chosen option: "Deterministic validation via fdd validate", because it provides a fast, repeatable gate that prevents structural drift.

## Related Design Elements

* `fdd-demo-req-validate-artifacts`
