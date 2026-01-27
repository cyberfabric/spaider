"""Tests for cascading validation module."""

import tempfile
import unittest
from pathlib import Path

from skills.fdd.scripts.fdd.validation.cascade import (
    ARTIFACT_DEPENDENCIES,
    resolve_dependencies,
    validate_all_artifacts,
    validate_with_dependencies,
)


def _write_registry(*, project_root: Path, adapter_dir: Path, entries: list) -> None:
    (project_root / ".fdd-config.json").write_text(
        '{\n  "fddAdapterPath": "adapter"\n}\n',
        encoding="utf-8",
    )
    adapter_dir.mkdir(parents=True, exist_ok=True)
    (adapter_dir / "AGENTS.md").write_text("# FDD Adapter: Test\n\n**Extends**: `../AGENTS.md`\n", encoding="utf-8")
    (adapter_dir / "artifacts.json").write_text(
        (
            "{\n"
            "  \"version\": \"1.0\",\n"
            "  \"artifacts\": "
            + __import__("json").dumps(entries, indent=2)
            + "\n"
            "}\n"
        ),
        encoding="utf-8",
    )


class TestArtifactDependencies(unittest.TestCase):
    """Test artifact dependency graph."""

    def test_dependency_graph_structure(self):
        """Verify dependency graph has expected structure."""
        self.assertEqual(ARTIFACT_DEPENDENCIES["feature-design"], ["features-manifest", "overall-design"])
        self.assertEqual(ARTIFACT_DEPENDENCIES["features-manifest"], ["overall-design"])
        self.assertEqual(ARTIFACT_DEPENDENCIES["overall-design"], ["prd", "adr"])
        self.assertEqual(ARTIFACT_DEPENDENCIES["adr"], ["prd"])
        self.assertEqual(ARTIFACT_DEPENDENCIES["prd"], [])

    def test_unknown_artifact_has_no_dependencies(self):
        """Unknown artifact kind returns empty list."""
        self.assertEqual(ARTIFACT_DEPENDENCIES.get("unknown", []), [])


class TestResolveDependencies(unittest.TestCase):
    """Test dependency resolution."""

    def test_resolve_no_dependencies(self):
        """prd has no dependencies."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)

            (tmp_path / ".git").mkdir()
            adapter_dir = tmp_path / "adapter"
            arch = tmp_path / "architecture"
            arch.mkdir()
            prd = arch / "PRD.md"
            prd.write_text("# PRD", encoding="utf-8")

            _write_registry(
                project_root=tmp_path,
                adapter_dir=adapter_dir,
                entries=[
                    {"kind": "PRD", "system": "Test", "path": "architecture/PRD.md", "format": "FDD"},
                ],
            )

            result = resolve_dependencies("prd", prd)
            self.assertEqual(result, {})

    def test_resolve_adr_depends_on_prd(self):
        """ADR depends on prd."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)

            (tmp_path / ".git").mkdir()
            adapter_dir = tmp_path / "adapter"
            arch = tmp_path / "architecture"
            arch.mkdir()
            adr = arch / "ADR"
            prd = arch / "PRD.md"
            adr.mkdir()
            prd.write_text("# PRD", encoding="utf-8")

            _write_registry(
                project_root=tmp_path,
                adapter_dir=adapter_dir,
                entries=[
                    {"kind": "PRD", "system": "Test", "path": "architecture/PRD.md", "format": "FDD"},
                    {"kind": "ADR", "system": "Test", "path": "architecture/ADR", "format": "FDD"},
                ],
            )

            result = resolve_dependencies("adr", adr)
            self.assertIn("prd", result)
            self.assertEqual(result["prd"].resolve(), prd.resolve())

    def test_resolve_overall_design_full_chain(self):
        """overall-design depends on prd and adr."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)

            (tmp_path / ".git").mkdir()
            adapter_dir = tmp_path / "adapter"
            arch = tmp_path / "architecture"
            arch.mkdir()
            design = arch / "DESIGN.md"
            prd = arch / "PRD.md"
            adr = arch / "ADR"
            design.write_text("# Design", encoding="utf-8")
            prd.write_text("# PRD", encoding="utf-8")
            adr.mkdir()

            _write_registry(
                project_root=tmp_path,
                adapter_dir=adapter_dir,
                entries=[
                    {"kind": "PRD", "system": "Test", "path": "architecture/PRD.md", "format": "FDD"},
                    {"kind": "ADR", "system": "Test", "path": "architecture/ADR", "format": "FDD"},
                    {"kind": "DESIGN", "system": "Test", "path": "architecture/DESIGN.md", "format": "FDD"},
                ],
            )

            result = resolve_dependencies("overall-design", design)
            self.assertIn("prd", result)
            self.assertIn("adr", result)

    def test_resolve_already_resolved_skipped(self):
        """Dependencies already resolved are skipped."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)

            (tmp_path / ".git").mkdir()
            adapter_dir = tmp_path / "adapter"
            arch = tmp_path / "architecture"
            arch.mkdir()
            design = arch / "DESIGN.md"
            prd = arch / "PRD.md"
            adr = arch / "ADR"
            design.write_text("# Design", encoding="utf-8")
            prd.write_text("# PRD", encoding="utf-8")
            adr.mkdir()

            _write_registry(
                project_root=tmp_path,
                adapter_dir=adapter_dir,
                entries=[
                    {"kind": "PRD", "system": "Test", "path": "architecture/PRD.md", "format": "FDD"},
                    {"kind": "ADR", "system": "Test", "path": "architecture/ADR", "format": "FDD"},
                    {"kind": "DESIGN", "system": "Test", "path": "architecture/DESIGN.md", "format": "FDD"},
                ],
            )

            existing = {"prd": prd}
            result = resolve_dependencies("overall-design", design, resolved=existing)
            self.assertIn("prd", result)


class TestValidateWithDependencies(unittest.TestCase):
    """Test cascading validation."""

    def test_validate_prd_no_deps(self):
        """Validate prd with no dependencies."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)

            (tmp_path / ".git").mkdir()
            adapter_dir = tmp_path / "adapter"
            arch = tmp_path / "architecture"
            arch.mkdir()
            prd = arch / "PRD.md"

            prd.write_text(
                "\n".join(
                    [
                        "# PRD",
                        "",
                        "## A. Vision",
                        "",
                        "**Purpose**: Test.",
                        "",
                        "Second paragraph.",
                        "",
                        "**Target Users**:",
                        "- User",
                        "",
                        "**Key Problems Solved**:",
                        "- Problem",
                        "",
                        "**Success Criteria**:",
                        "- Criterion",
                        "",
                        "**Capabilities**:",
                        "- Capability",
                        "",
                        "## B. Actors",
                        "",
                        "### Human Actors",
                        "",
                        "#### User",
                        "",
                        "**ID**: `fdd-test-actor-user`",
                        "**Role**: User",
                        "",
                        "### System Actors",
                        "",
                        "#### System",
                        "",
                        "**ID**: `fdd-test-actor-system`",
                        "**Role**: System",
                        "",
                        "## C. Functional Requirements",
                        "",
                        "#### Requirement A",
                        "",
                        "**ID**: `fdd-test-fr-a`",
                        "- Does something",
                        "- **Actors**: `fdd-test-actor-user`",
                        "",
                        "## D. Use Cases",
                        "",
                        "#### UC-001: Example",
                        "",
                        "**ID**: `fdd-test-usecase-a`",
                        "**Actor**: `fdd-test-actor-user`",
                        "**Preconditions**: Ready",
                        "**Flow**:",
                        "1. Step",
                        "**Postconditions**: Done",
                        "",
                        "## E. Non-functional requirements",
                        "",
                        "#### Security",
                        "",
                        "**ID**: `fdd-test-nfr-security`",
                        "- Authentication MUST be required.",
                        "",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            _write_registry(
                project_root=tmp_path,
                adapter_dir=adapter_dir,
                entries=[
                    {"kind": "PRD", "system": "Test", "path": "architecture/PRD.md", "format": "FDD"},
                ],
            )

            report = validate_with_dependencies(prd, skip_fs_checks=True)
            self.assertEqual(report["artifact_kind"], "prd")
            self.assertNotIn("dependency_validation", report)

    def test_validate_with_failing_dependency(self):
        """Validation fails if dependency fails."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)

            (tmp_path / ".git").mkdir()
            adapter_dir = tmp_path / "adapter"
            arch = tmp_path / "architecture"
            arch.mkdir()
            
            # Create invalid PRD.md (missing required content)
            prd = arch / "PRD.md"
            prd.write_text("# Empty PRD")
            
            # Create ADR directory (depends on prd)
            adr = arch / "ADR"
            adr.mkdir()
            (adr / "general").mkdir()
            (adr / "general" / "0001-fdd-test-adr-x.md").write_text("""# ADR-0001: X

**Date**: 2025-01-01

**Status**: Accepted

**ADR ID**: `fdd-test-adr-x`

## Context and Problem Statement

X

## Considered Options

- A

## Decision Outcome

Chosen option: \"A\", because test.

## Related Design Elements

- `fdd-test-actor-user`
""", encoding="utf-8")


            _write_registry(
                project_root=tmp_path,
                adapter_dir=adapter_dir,
                entries=[
                    {"kind": "PRD", "system": "Test", "path": "architecture/PRD.md", "format": "FDD"},
                    {"kind": "ADR", "system": "Test", "path": "architecture/ADR", "format": "FDD"},
                ],
            )

            report = validate_with_dependencies(adr, skip_fs_checks=True)
            # ADR validation should fail due to failing prd dependency
            self.assertIn("dependency_validation", report)
            self.assertIn("prd", report["dependency_validation"])


class TestCrossArtifactIdentifierStatuses(unittest.TestCase):
    def test_cross_artifact_status_rules_report_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".git").mkdir()
            adapter_dir = root / "adapter"
            arch = root / "architecture"
            features_dir = arch / "features"
            feature_a_dir = features_dir / "feature-a"
            feature_a_dir.mkdir(parents=True)

            # PRD.md: one functional requirement marked IMPLEMENTED and linked to feature-a.
            (arch / "PRD.md").write_text(
                "\n".join(
                    [
                        "# PRD",
                        "",
                        "## A. VISION",
                        "",
                        "**Purpose**: Test.",
                        "",
                        "Second paragraph.",
                        "",
                        "**Target Users**:",
                        "- User",
                        "",
                        "**Key Problems Solved**:",
                        "- Problem",
                        "",
                        "**Success Criteria**:",
                        "- Criterion",
                        "",
                        "**Capabilities**:",
                        "- Capability",
                        "",
                        "## B. Actors",
                        "",
                        "### Human Actors",
                        "",
                        "#### User",
                        "",
                        "**ID**: `fdd-test-actor-user`",
                        "**Role**: User",
                        "",
                        "### System Actors",
                        "",
                        "#### System",
                        "",
                        "**ID**: `fdd-test-actor-system`",
                        "**Role**: System",
                        "",
                        "## C. Functional Requirements",
                        "",
                        "#### Requirement A",
                        "",
                        "**ID**: `fdd-test-fr-a`",
                        "<!-- fdd-id-content -->",
                        "**Status**: IMPLEMENTED",
                        "- Does something",
                        "- **Actors**: `fdd-test-actor-user`",
                        "- **Features**:",
                        "  - [Feature A](feature-a/)",
                        "<!-- fdd-id-content -->",
                        "",
                        "## D. Use Cases",
                        "",
                        "#### UC-001: Example",
                        "",
                        "**ID**: `fdd-test-usecase-a`",
                        "<!-- fdd-id-content -->",
                        "**Actor**: `fdd-test-actor-user`",
                        "**Preconditions**: Ready",
                        "**Flow**:",
                        "1. Step",
                        "**Postconditions**: Done",
                        "<!-- fdd-id-content -->",
                        "",
                        "## E. Non-functional requirements",
                        "",
                        "#### Security",
                        "",
                        "**ID**: `fdd-test-nfr-security`",
                        "<!-- fdd-id-content -->",
                        "- Authentication MUST be required.",
                        "<!-- fdd-id-content -->",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            _write_registry(
                project_root=root,
                adapter_dir=adapter_dir,
                entries=[
                    {"kind": "PRD", "system": "Test", "path": "architecture/PRD.md", "format": "FDD"},
                    {"kind": "DESIGN", "system": "Test", "path": "architecture/DESIGN.md", "format": "FDD"},
                    {"kind": "ADR", "system": "Test", "path": "architecture/ADR", "format": "FDD"},
                    {"kind": "FEATURES", "system": "Test", "path": "architecture/features/FEATURES.md", "format": "FDD"},
                ],
            )

            # DESIGN.md: one requirement marked IMPLEMENTED.
            (arch / "DESIGN.md").write_text(
                "\n".join(
                    [
                        "# Technical Design",
                        "",
                        "## A. Overview",
                        "",
                        "Text.",
                        "",
                        "## B. Requirements",
                        "",
                        "#### FR-001: Example",
                        "",
                        "**ID**: `fdd-test-req-a`",
                        "<!-- fdd-id-content -->",
                        "**Status**: IMPLEMENTED",
                        "",
                        "**Capabilities**: `fdd-test-fr-a`",
                        "**Actors**: `fdd-test-actor-user`",
                        "",
                        "Some text.",
                        "<!-- fdd-id-content -->",
                        "",
                        "## C. Architecture",
                        "",
                        "Text.",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            # ADR/: minimal valid ADR entry for cross-artifact validation.
            adr_dir = arch / "ADR" / "general"
            adr_dir.mkdir(parents=True)
            (adr_dir / "0001-fdd-test-adr-a.md").write_text(
                "\n".join(
                    [
                        "# ADR-0001: A",
                        "",
                        "**Date**: 2026-01-01",
                        "",
                        "**Status**: Accepted",
                        "",
                        "**ADR ID**: `fdd-test-adr-a`",
                        "",
                        "## Context and Problem Statement",
                        "",
                        "X",
                        "",
                        "## Considered Options",
                        "",
                        "- A",
                        "",
                        "## Decision Outcome",
                        "",
                        "Chosen option: \"A\", because test.",
                        "",
                        "## Related Design Elements",
                        "",
                        "- `fdd-test-req-a`",
                        "",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            # FEATURES.md: feature-a exists but is NOT_STARTED, yet covers the implemented requirement.
            (features_dir / "FEATURES.md").write_text(
                "\n".join(
                    [
                        "# Features: Test",
                        "",
                        "**Status Overview**: 1 features total (0 completed, 0 in progress, 0 design ready, 0 in design, 1 not started)",
                        "",
                        "**Meaning**:",
                        "- ⏳ NOT_STARTED",
                        "- 📝 IN_DESIGN",
                        "- 📘 DESIGN_READY",
                        "- 🔄 IN_DEVELOPMENT",
                        "- ✅ IMPLEMENTED",
                        "",
                        "### 1. [fdd-test-feature-a](feature-a/) ⏳ LOW",
                        "",
                        "- **Purpose**: P",
                        "- **Status**: NOT_STARTED",
                        "- **Depends On**: None",
                        "- **Blocks**: None",
                        "- **Scope**:",
                        "  - s",
                        "- **Requirements Covered**:",
                        "  - fdd-test-req-a",
                        "- **Phases**:",
                        "  - `ph-1`: ⏳ NOT_STARTED — init",
                        "",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            rep = validate_all_artifacts(root, skip_fs_checks=False)
            self.assertEqual(rep.get("status"), "FAIL")
            av = rep.get("artifact_validation")
            self.assertIsInstance(av, dict)
            self.assertIn("Test:cross-artifact-status", av)
            cross = av["Test:cross-artifact-status"]
            errs = cross.get("errors", [])
            self.assertTrue(any("Functional requirement status is IMPLEMENTED" in e.get("message", "") for e in errs))
            self.assertTrue(any("DESIGN requirement status is IMPLEMENTED" in e.get("message", "") for e in errs))


if __name__ == "__main__":
    unittest.main()
