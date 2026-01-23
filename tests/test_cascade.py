"""Tests for cascading validation module."""

import tempfile
import unittest
from pathlib import Path

from skills.fdd.scripts.fdd.validation.cascade import (
    ARTIFACT_DEPENDENCIES,
    find_artifact_path,
    resolve_dependencies,
    validate_all_artifacts,
    validate_with_dependencies,
)


class TestArtifactDependencies(unittest.TestCase):
    """Test artifact dependency graph."""

    def test_dependency_graph_structure(self):
        """Verify dependency graph has expected structure."""
        self.assertEqual(ARTIFACT_DEPENDENCIES["feature-changes"], ["feature-design"])
        self.assertEqual(ARTIFACT_DEPENDENCIES["feature-design"], ["features-manifest", "overall-design"])
        self.assertEqual(ARTIFACT_DEPENDENCIES["features-manifest"], ["overall-design"])
        self.assertEqual(ARTIFACT_DEPENDENCIES["overall-design"], ["business-context", "adr"])
        self.assertEqual(ARTIFACT_DEPENDENCIES["adr"], ["business-context"])
        self.assertEqual(ARTIFACT_DEPENDENCIES["business-context"], [])

    def test_unknown_artifact_has_no_dependencies(self):
        """Unknown artifact kind returns empty list."""
        self.assertEqual(ARTIFACT_DEPENDENCIES.get("unknown", []), [])


class TestFindArtifactPath(unittest.TestCase):
    """Test artifact path discovery."""

    def test_find_feature_design_exists(self):
        """Find DESIGN.md in same directory as CHANGES.md."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            changes = tmp_path / "CHANGES.md"
            design = tmp_path / "DESIGN.md"
            changes.write_text("# Changes")
            design.write_text("# Design")
            
            result = find_artifact_path("feature-design", changes)
            self.assertEqual(result, design)

    def test_find_feature_design_not_exists(self):
        """Return None if DESIGN.md not found."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            changes = tmp_path / "CHANGES.md"
            changes.write_text("# Changes")
            
            result = find_artifact_path("feature-design", changes)
            self.assertIsNone(result)

    def test_find_features_manifest_exists(self):
        """Find FEATURES.md in architecture/features/."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            arch_features = tmp_path / "architecture" / "features"
            arch_features.mkdir(parents=True)
            features = arch_features / "FEATURES.md"
            features.write_text("# Features")
            artifact = tmp_path / "some" / "path" / "artifact.md"
            artifact.parent.mkdir(parents=True)
            artifact.write_text("# Artifact")
            
            result = find_artifact_path("features-manifest", artifact)
            self.assertEqual(result, features)

    def test_find_features_manifest_not_exists(self):
        """Return None if FEATURES.md not found."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            artifact = tmp_path / "artifact.md"
            artifact.write_text("# Artifact")
            
            result = find_artifact_path("features-manifest", artifact)
            self.assertIsNone(result)

    def test_find_overall_design_exists(self):
        """Find DESIGN.md in architecture/."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            arch = tmp_path / "architecture"
            arch.mkdir()
            design = arch / "DESIGN.md"
            design.write_text("# Design")
            artifact = tmp_path / "some" / "path" / "artifact.md"
            artifact.parent.mkdir(parents=True)
            artifact.write_text("# Artifact")
            
            result = find_artifact_path("overall-design", artifact)
            self.assertEqual(result, design)

    def test_find_overall_design_not_exists(self):
        """Return None if overall DESIGN.md not found."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            artifact = tmp_path / "artifact.md"
            artifact.write_text("# Artifact")
            
            result = find_artifact_path("overall-design", artifact)
            self.assertIsNone(result)

    def test_find_business_context_exists(self):
        """Find BUSINESS.md in architecture/."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            arch = tmp_path / "architecture"
            arch.mkdir()
            business = arch / "BUSINESS.md"
            business.write_text("# Business")
            artifact = tmp_path / "some" / "path" / "artifact.md"
            artifact.parent.mkdir(parents=True)
            artifact.write_text("# Artifact")
            
            result = find_artifact_path("business-context", artifact)
            self.assertEqual(result, business)

    def test_find_business_context_not_exists(self):
        """Return None if BUSINESS.md not found."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            artifact = tmp_path / "artifact.md"
            artifact.write_text("# Artifact")
            
            result = find_artifact_path("business-context", artifact)
            self.assertIsNone(result)

    def test_find_adr_exists(self):
        """Find ADR directory in architecture/."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            arch = tmp_path / "architecture"
            arch.mkdir()
            adr = arch / "ADR"
            adr.mkdir()
            artifact = tmp_path / "some" / "path" / "artifact.md"
            artifact.parent.mkdir(parents=True)
            artifact.write_text("# Artifact")
            
            result = find_artifact_path("adr", artifact)
            self.assertEqual(result, adr)

    def test_find_adr_not_exists(self):
        """Return None if ADR directory not found."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            artifact = tmp_path / "artifact.md"
            artifact.write_text("# Artifact")
            
            result = find_artifact_path("adr", artifact)
            self.assertIsNone(result)

    def test_find_unknown_artifact_kind(self):
        """Return None for unknown artifact kind."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            artifact = tmp_path / "artifact.md"
            artifact.write_text("# Artifact")
            
            result = find_artifact_path("unknown-kind", artifact)
            self.assertIsNone(result)


class TestResolveDependencies(unittest.TestCase):
    """Test dependency resolution."""

    def test_resolve_no_dependencies(self):
        """business-context has no dependencies."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            business = tmp_path / "BUSINESS.md"
            business.write_text("# Business")
            
            result = resolve_dependencies("business-context", business)
            self.assertEqual(result, {})

    def test_resolve_adr_depends_on_business(self):
        """ADR depends on business-context."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            arch = tmp_path / "architecture"
            arch.mkdir()
            adr = arch / "ADR"
            business = arch / "BUSINESS.md"
            adr.mkdir()
            business.write_text("# Business")
            
            result = resolve_dependencies("adr", adr)
            self.assertIn("business-context", result)
            self.assertEqual(result["business-context"], business)

    def test_resolve_overall_design_full_chain(self):
        """overall-design depends on business-context and adr."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            arch = tmp_path / "architecture"
            arch.mkdir()
            design = arch / "DESIGN.md"
            business = arch / "BUSINESS.md"
            adr = arch / "ADR"
            design.write_text("# Design")
            business.write_text("# Business")
            adr.mkdir()
            
            result = resolve_dependencies("overall-design", design)
            self.assertIn("business-context", result)
            self.assertIn("adr", result)

    def test_resolve_already_resolved_skipped(self):
        """Dependencies already resolved are skipped."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            arch = tmp_path / "architecture"
            arch.mkdir()
            design = arch / "DESIGN.md"
            business = arch / "BUSINESS.md"
            design.write_text("# Design")
            business.write_text("# Business")
            
            # Pre-populate resolved
            existing = {"business-context": business}
            result = resolve_dependencies("overall-design", design, resolved=existing)
            # Should still have business-context from pre-populated
            self.assertIn("business-context", result)


class TestValidateWithDependencies(unittest.TestCase):
    """Test cascading validation."""

    def test_validate_business_context_no_deps(self):
        """Validate business-context with no dependencies."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            business = tmp_path / "BUSINESS.md"
            business.write_text("""---
fdd: true
type: business-context
name: Test Business
version: "1.0"
purpose: Test
---

# FDD: Test Business Context

## Overview

Test overview.

## Actors

### Actor: Test Actor

**ID**: `fdd-test-actor-user`

**Description**: Test user actor.

## Capabilities

### Capability: Test Capability

**ID**: `fdd-test-capability-main`

Provided by `fdd-test-actor-user`.

## Use Cases

None yet.
""")
            
            report = validate_with_dependencies(business, skip_fs_checks=True)
            self.assertEqual(report["artifact_kind"], "business-context")
            self.assertNotIn("dependency_validation", report)

    def test_validate_with_failing_dependency(self):
        """Validation fails if dependency fails."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            arch = tmp_path / "architecture"
            arch.mkdir()
            
            # Create invalid BUSINESS.md (missing required content)
            business = arch / "BUSINESS.md"
            business.write_text("# Empty Business")
            
            # Create ADR directory (depends on business-context)
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

            adr_text = """---
fdd: true
type: adr
name: Test ADR
version: "1.0"
purpose: Test
---

# FDD: Test ADR

## Overview

Test overview.

## Context and Problem Statement

None.

## Superseded ADRs

None.
"""
            
            report = validate_with_dependencies(adr, skip_fs_checks=True)
            # ADR validation should fail due to failing business dependency
            self.assertIn("dependency_validation", report)
            self.assertIn("business-context", report["dependency_validation"])


class TestCrossArtifactIdentifierStatuses(unittest.TestCase):
    def test_cross_artifact_status_rules_report_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            arch = root / "architecture"
            features_dir = arch / "features"
            feature_a_dir = features_dir / "feature-a"
            feature_a_dir.mkdir(parents=True)

            # BUSINESS.md: one capability marked IMPLEMENTED and linked to feature-a.
            (arch / "BUSINESS.md").write_text(
                "\n".join(
                    [
                        "# Business Context",
                        "",
                        "## A. Feature Context",
                        "",
                        "**Purpose**: Test",
                        "",
                        "**Target Users**:",
                        "- User",
                        "",
                        "**Key Problems Solved**:",
                        "- Problem",
                        "",
                        "**Success Criteria**:",
                        "- Success",
                        "",
                        "## B. Actors",
                        "",
                        "### Human Actors",
                        "",
                        "#### User",
                        "",
                        "**ID**: `fdd-test-actor-user`",
                        "<!-- fdd-id-content -->",
                        "**Role**: User",
                        "<!-- fdd-id-content -->",
                        "",
                        "### System Actors",
                        "",
                        "#### System",
                        "",
                        "**ID**: `fdd-test-actor-system`",
                        "<!-- fdd-id-content -->",
                        "**Role**: System",
                        "<!-- fdd-id-content -->",
                        "",
                        "## C. Capabilities",
                        "",
                        "#### Capability A",
                        "",
                        "**ID**: `fdd-test-capability-a`",
                        "<!-- fdd-id-content -->",
                        "**Status**: IMPLEMENTED",
                        "- Does something",
                        "- **Actors**: `fdd-test-actor-user`",
                        "- **Features**:",
                        "  - [Feature A](feature-a/)",
                        "<!-- fdd-id-content -->",
                        "",
                    ]
                )
                + "\n",
                encoding="utf-8",
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
                        "**Capabilities**: `fdd-test-capability-a`",
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
            self.assertIn("cross-artifact-status", av)
            cross = av["cross-artifact-status"]
            errs = cross.get("errors", [])
            self.assertTrue(any("Capability status is IMPLEMENTED" in e.get("message", "") for e in errs))
            self.assertTrue(any("DESIGN requirement status is IMPLEMENTED" in e.get("message", "") for e in errs))


if __name__ == "__main__":
    unittest.main()
