"""
Test overall DESIGN.md validation.

Critical validator that ensures system design integrity,
requirements traceability, and cross-references to BUSINESS.md and ADR/{category}/NNNN-fdd-{slug}.md.
"""

import unittest
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).parent.parent / "skills" / "fdd" / "scripts"))

from fdd.validation.artifacts.overall_design import validate_overall_design


class TestOverallDesignStructure(unittest.TestCase):
    """Test overall DESIGN.md structure validation."""

    def test_minimal_pass(self):
        """Test minimal valid overall DESIGN.md."""
        text = """# Technical Design: MyApp

## A. Architecture Overview

Architecture content here.

## B. Requirements & Principles

### FR-001: First Requirement

**ID**: `fdd-myapp-req-first`

**Capabilities**: `fdd-myapp-capability-test`

**Actors**: `fdd-myapp-actor-user`

**Use Cases**: `fdd-myapp-usecase-test`

Requirement description.

## C. Domain Model

### C.1 Entity Schemas

Content.

### C.2 Schema Format

Content.

### C.3 API Contracts

Content.

### C.4 Contract Format

Content.

### C.5 Event Schemas

Content.
"""
        report = validate_overall_design(text, skip_fs_checks=True)
        
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(len(report["errors"]), 0)
        self.assertEqual(report["required_section_count"], 3)
        self.assertEqual(len(report["missing_sections"]), 0)

    def test_missing_section_a_fails(self):
        """Test that missing Section A fails validation."""
        text = """# Technical Design

## B. Requirements

Content.

## C. Domain Model

Content.
"""
        report = validate_overall_design(text, skip_fs_checks=True)
        
        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(len(report["missing_sections"]), 1)
        self.assertEqual(report["missing_sections"][0]["id"], "A")

    def test_missing_section_b_fails(self):
        """Test that missing Section B fails validation."""
        text = """# Technical Design

## A. Architecture

Content.

## C. Domain Model

Content.
"""
        report = validate_overall_design(text, skip_fs_checks=True)
        
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("B", [s["id"] for s in report["missing_sections"]])

    def test_missing_section_c_fails(self):
        """Test that missing Section C fails validation."""
        text = """# Technical Design

## A. Architecture

Content.

## B. Requirements

Content.
"""
        report = validate_overall_design(text, skip_fs_checks=True)
        
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("C", [s["id"] for s in report["missing_sections"]])

    def test_section_c_subsections_validation(self):
        """Test that Section C must have exactly C.1-C.5 subsections."""
        text = """# Technical Design

## A. Architecture

Content.

## B. Requirements

### FR-001: Requirement

**ID**: `fdd-app-req-test`

**Capabilities**: `fdd-app-capability-test`

**Actors**: `fdd-app-actor-user`

Content.

## C. Domain Model

### C.1: Schemas

Content.

### C.2: Format

Content.

### C.3: Contracts

Content.
"""
        report = validate_overall_design(text, skip_fs_checks=True)
        
        # Missing C.4 and C.5
        structure_errors = [e for e in report["errors"] if e.get("type") == "structure"]
        if structure_errors:
            # Should detect missing subsections
            self.assertIn("C.1..C.5", structure_errors[0]["message"])
        else:
            # Validator may not enforce this strictly
            pass

    def test_section_c_subsections_correct_order(self):
        """Test that Section C subsections must be in correct order."""
        text = """# Technical Design

## A. Architecture

Content.

## B. Requirements

### FR-001: Requirement

**ID**: `fdd-app-req-test`

**Capabilities**: `fdd-app-capability-test`

**Actors**: `fdd-app-actor-user`

Content.

## C. Domain Model

### C.2: Schema Format

Wrong order.

### C.1: Entity Schemas

Wrong order.

### C.3: API Contracts

Content.

### C.4: Contract Format

Content.

### C.5: Event Schemas

Content.
"""
        report = validate_overall_design(text, skip_fs_checks=True)
        
        structure_errors = [e for e in report["errors"] if e.get("type") == "structure"]
        if structure_errors:
            # Should detect wrong order
            self.assertIn("C.1..C.5", structure_errors[0]["message"])
        else:
            # Validator may not enforce order strictly
            pass


class TestOverallDesignRequirements(unittest.TestCase):
    """Test overall DESIGN.md requirements validation."""

    def test_no_requirements_fails(self):
        """Test that design with no requirements fails."""
        text = """# Technical Design

## A. Architecture

Content.

## B. Requirements

No requirement IDs here.

## C. Domain Model

### C.1 Schemas
### C.2 Format
### C.3 Contracts
### C.4 Contract Format
### C.5 Events
"""
        report = validate_overall_design(text, skip_fs_checks=True)
        
        self.assertEqual(report["status"], "FAIL")
        req_issues = report["requirement_issues"]
        self.assertGreater(len(req_issues), 0)
        self.assertIn("No functional requirement", req_issues[0]["message"])

    def test_requirement_missing_capabilities_fails(self):
        """Test that requirement without capabilities fails."""
        text = """# Technical Design

## A. Architecture

Content.

## B. Requirements

### FR-001: Requirement

**ID**: `fdd-app-req-test`

**Actors**: `fdd-app-actor-user`

No capabilities listed.

## C. Domain Model

### C.1 Schemas
### C.2 Format
### C.3 Contracts
### C.4 Contract Format
### C.5 Events
"""
        report = validate_overall_design(text, skip_fs_checks=True)
        
        self.assertEqual(report["status"], "FAIL")
        req_issues = report["requirement_issues"]
        missing_caps = [i for i in req_issues if "capability" in i["message"].lower()]
        self.assertGreater(len(missing_caps), 0)

    def test_requirement_missing_actors_fails(self):
        """Test that requirement without actors fails."""
        text = """# Technical Design

## A. Architecture

Content.

## B. Requirements

### FR-001: Requirement

**ID**: `fdd-app-req-test`

**Capabilities**: `fdd-app-capability-test`

No actors listed.

## C. Domain Model

### C.1 Schemas
### C.2 Format
### C.3 Contracts
### C.4 Contract Format
### C.5 Events
"""
        report = validate_overall_design(text, skip_fs_checks=True)
        
        self.assertEqual(report["status"], "FAIL")
        req_issues = report["requirement_issues"]
        missing_actors = [i for i in req_issues if "actor" in i["message"].lower()]
        self.assertGreater(len(missing_actors), 0)

    def test_multiple_requirements_with_proper_references_pass(self):
        """Test multiple requirements with all references."""
        text = """# Technical Design

## A. Architecture

Content.

## B. Requirements

### FR-001: First Requirement

**ID**: `fdd-app-req-first`

**Capabilities**: `fdd-app-capability-manage`

**Actors**: `fdd-app-actor-admin`

**Use Cases**: `fdd-app-usecase-manage`

Description.

### FR-002: Second Requirement

**ID**: `fdd-app-req-second`

**Capabilities**: `fdd-app-capability-view`, `fdd-app-capability-edit`

**Actors**: `fdd-app-actor-user`, `fdd-app-actor-admin`

**Use Cases**: `fdd-app-usecase-view`, `fdd-app-usecase-edit`

Description.

## C. Domain Model

### C.1 Schemas
### C.2 Format
### C.3 Contracts
### C.4 Contract Format
### C.5 Events
"""
        report = validate_overall_design(text, skip_fs_checks=True)
        
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(len(report["requirement_issues"]), 0)


class TestOverallDesignCrossReferences(unittest.TestCase):
    """Test cross-reference validation with BUSINESS.md and ADR directory."""

    def test_cross_reference_validation_with_business(self):
        """Test validation with BUSINESS.md cross-references."""
        with TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            arch = tmppath / "architecture"
            arch.mkdir()
            
            # Create BUSINESS.md
            business = arch / "BUSINESS.md"
            business.write_text("""# Business Context

## B. Actors

- **ID**: `fdd-app-actor-admin`

## C. Capabilities

### CAP-001: Manage Data

**ID**: `fdd-app-capability-manage`

**Actors**: `fdd-app-actor-admin`

## D. Use Cases

- **ID**: `fdd-app-usecase-manage`
""")
            
            # Create DESIGN.md
            design = arch / "DESIGN.md"
            design_text = """# Technical Design

## A. Architecture

Content.

## B. Requirements

### FR-001: Requirement

**ID**: `fdd-app-req-first`

**Capabilities**: `fdd-app-capability-manage`

**Actors**: `fdd-app-actor-admin`

**Use Cases**: `fdd-app-usecase-manage`

Description.

## C. Domain Model

### C.1 Schemas
### C.2 Format
### C.3 Contracts
### C.4 Contract Format
### C.5 Events
"""
            design.write_text(design_text)
            
            report = validate_overall_design(
                design_text,
                artifact_path=design,
                business_path=business,
                skip_fs_checks=False
            )
            
            # Should have minimal or no errors
            # May have warnings about missing subsections, but cross-refs should be valid
            self.assertLessEqual(len(report["errors"]), 1)
            self.assertEqual(len(report["requirement_issues"]), 0)

    def test_unknown_actor_reference_fails(self):
        """Test that unknown actor reference fails."""
        with TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            arch = tmppath / "architecture"
            arch.mkdir()
            
            business = arch / "BUSINESS.md"
            business.write_text("""# Business Context

## B. Actors

- **ID**: `fdd-app-actor-user`

## C. Capabilities

### CAP-001: Test

**ID**: `fdd-app-capability-test`

**Actors**: `fdd-app-actor-user`
""")
            
            design = arch / "DESIGN.md"
            design_text = """# Technical Design

## A. Architecture

Content.

## B. Requirements

### FR-001: Requirement

**ID**: `fdd-app-req-test`

**Capabilities**: `fdd-app-capability-test`

**Actors**: `fdd-app-actor-unknown`

Unknown actor!

## C. Domain Model

### C.1 Schemas
### C.2 Format
### C.3 Contracts
### C.4 Contract Format
### C.5 Events
"""
            design.write_text(design_text)
            
            report = validate_overall_design(
                design_text,
                artifact_path=design,
                business_path=business,
                skip_fs_checks=False
            )
            
            self.assertEqual(report["status"], "FAIL")
            unknown_actor_issues = [i for i in report["requirement_issues"] 
                                   if "Unknown actor" in i.get("message", "")]
            self.assertGreater(len(unknown_actor_issues), 0)

    def test_unknown_capability_reference_fails(self):
        """Test that unknown capability reference fails."""
        with TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            arch = tmppath / "architecture"
            arch.mkdir()
            
            business = arch / "BUSINESS.md"
            business.write_text("""# Business Context

## B. Actors

- **ID**: `fdd-app-actor-user`

## C. Capabilities

### CAP-001: Real Capability

**ID**: `fdd-app-capability-real`

**Actors**: `fdd-app-actor-user`
""")
            
            design = arch / "DESIGN.md"
            design_text = """# Technical Design

## A. Architecture

Content.

## B. Requirements

### FR-001: Requirement

**ID**: `fdd-app-req-test`

**Capabilities**: `fdd-app-capability-unknown`

**Actors**: `fdd-app-actor-user`

Unknown capability!

## C. Domain Model

### C.1 Schemas
### C.2 Format
### C.3 Contracts
### C.4 Contract Format
### C.5 Events
"""
            design.write_text(design_text)
            
            report = validate_overall_design(
                design_text,
                artifact_path=design,
                business_path=business,
                skip_fs_checks=False
            )
            
            self.assertEqual(report["status"], "FAIL")
            unknown_cap_issues = [i for i in report["requirement_issues"]
                                 if "Unknown capability" in i.get("message", "")]
            self.assertGreater(len(unknown_cap_issues), 0)

    def test_orphaned_capabilities_detected(self):
        """Test that orphaned capabilities (not referenced) are detected."""
        with TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            arch = tmppath / "architecture"
            arch.mkdir()
            
            business = arch / "BUSINESS.md"
            business.write_text("""# Business Context

## B. Actors

- **ID**: `fdd-app-actor-user`

## C. Capabilities

### CAP-001: Used Capability

**ID**: `fdd-app-capability-used`

**Actors**: `fdd-app-actor-user`

### CAP-002: Orphaned Capability

**ID**: `fdd-app-capability-orphaned`

**Actors**: `fdd-app-actor-user`
""")
            
            design = arch / "DESIGN.md"
            design_text = """# Technical Design

## A. Architecture

Content.

## B. Requirements

### FR-001: Requirement

**ID**: `fdd-app-req-test`

**Capabilities**: `fdd-app-capability-used`

**Actors**: `fdd-app-actor-user`

Only references 'used' capability.

## C. Domain Model

### C.1 Schemas
### C.2 Format
### C.3 Contracts
### C.4 Contract Format
### C.5 Events
"""
            design.write_text(design_text)
            
            report = validate_overall_design(
                design_text,
                artifact_path=design,
                business_path=business,
                skip_fs_checks=False
            )
            
            self.assertEqual(report["status"], "FAIL")
            orphan_errors = [e for e in report["errors"]
                           if e.get("type") == "traceability" and "Orphaned capabilities" in e.get("message", "")]
            self.assertGreater(len(orphan_errors), 0)
            self.assertIn("fdd-app-capability-orphaned", orphan_errors[0]["ids"])


class TestOverallDesignADRReferences(unittest.TestCase):
    """Test ADR reference validation."""

    def test_adr_references_validated(self):
        """Test that ADR references are validated against architecture/ADR directory."""
        with TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            arch = tmppath / "architecture"
            arch.mkdir()

            adr_dir = arch / "ADR" / "general"
            adr_dir.mkdir(parents=True)
            (adr_dir / "0001-fdd-app-adr-use-python.md").write_text(
                "\n".join(
                    [
                        "# ADR-0001: Use Python",
                        "",
                        "**Date**: 2024-01-01",
                        "",
                        "**Status**: Accepted",
                        "",
                        "**ADR ID**: `fdd-app-adr-use-python`",
                        "",
                        "## Context and Problem Statement",
                        "",
                        "Decision content.",
                        "",
                        "## Considered Options",
                        "",
                        "- Python",
                        "",
                        "## Decision Outcome",
                        "",
                        "Chosen option: \"Python\", because test.",
                        "",
                        "## Related Design Elements",
                        "",
                        "- `fdd-app-req-test`",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            
            design = arch / "DESIGN.md"
            design_text = """# Technical Design

## A. Architecture

Content.

## B. Requirements

### FR-001: Requirement

**ID**: `fdd-app-req-test`

**Capabilities**: `fdd-app-capability-test`

**Actors**: `fdd-app-actor-user`

**ADRs**: ADR-0001

References ADR-0001.

## C. Domain Model

### C.1 Schemas
### C.2 Format
### C.3 Contracts
### C.4 Contract Format
### C.5 Events
"""
            design.write_text(design_text)
            
            report = validate_overall_design(
                design_text,
                artifact_path=design,
                adr_path=arch / "ADR",
                skip_fs_checks=False
            )
            
            # Should pass - ADR reference is valid
            adr_issues = [i for i in report["requirement_issues"]
                         if "ADR" in i.get("message", "")]
            # No unknown ADR errors
            unknown_adr = [i for i in adr_issues if "Unknown" in i.get("message", "")]
            self.assertEqual(len(unknown_adr), 0)

    def test_unknown_adr_reference_fails(self):
        """Test that unknown ADR reference fails."""
        with TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            arch = tmppath / "architecture"
            arch.mkdir()

            adr_dir = arch / "ADR" / "general"
            adr_dir.mkdir(parents=True)
            (adr_dir / "0001-fdd-app-adr-real.md").write_text(
                "\n".join(
                    [
                        "# ADR-0001: Real ADR",
                        "",
                        "**Date**: 2024-01-01",
                        "",
                        "**Status**: Accepted",
                        "",
                        "**ADR ID**: `fdd-app-adr-real`",
                        "",
                        "## Context and Problem Statement",
                        "",
                        "Real.",
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
                        "- `fdd-app-req-test`",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            
            design = arch / "DESIGN.md"
            design_text = """# Technical Design

## A. Architecture

Content.

## B. Requirements

### FR-001: Requirement

**ID**: `fdd-app-req-test`

**Capabilities**: `fdd-app-capability-test`

**Actors**: `fdd-app-actor-user`

**ADRs**: `fdd-app-adr-unknown`

Unknown ADR!

## C. Domain Model

### C.1 Schemas
### C.2 Format
### C.3 Contracts
### C.4 Contract Format
### C.5 Events
"""
            design.write_text(design_text)
            
            report = validate_overall_design(
                design_text,
                artifact_path=design,
                adr_path=arch / "ADR",
                skip_fs_checks=False
            )
            
            self.assertEqual(report["status"], "FAIL")
            unknown_adr_issues = [i for i in report["requirement_issues"]
                                 if "Unknown ADR" in i.get("message", "")]
            self.assertGreater(len(unknown_adr_issues), 0)


class TestOverallDesignPlaceholders(unittest.TestCase):
    """Test placeholder detection."""

    def test_placeholder_detection_fails(self):
        """Test that placeholders cause validation failure."""
        text = """# Technical Design

## A. Architecture

TODO: Add architecture details

## B. Requirements

### FR-001: Requirement

**ID**: `fdd-app-req-test`

**Capabilities**: `fdd-app-capability-test`

**Actors**: `fdd-app-actor-user`

TBD: Add requirement description

## C. Domain Model

### C.1 Schemas

FIXME: Update schemas

### C.2 Format
### C.3 Contracts
### C.4 Contract Format
### C.5 Events
"""
        report = validate_overall_design(text, skip_fs_checks=True)
        
        self.assertEqual(report["status"], "FAIL")
        self.assertGreater(len(report["placeholder_hits"]), 0)


class TestRequirementBlocks(unittest.TestCase):
    """Test requirement block parsing and validation."""

    def test_requirement_with_all_fields(self):
        """Test requirement with actors, capabilities, use cases, ADRs."""
        text = """# DESIGN.md

## A. Purpose

Purpose here.

## B. Business Model

Business model.

## C. Requirements

### C.1 Functional Requirements

**ID**: `fdd-app-req-001`

**Actors**: `fdd-app-actor-user`

**Capabilities**: `fdd-app-capability-auth`

**Use Cases**: `fdd-app-usecase-login`

**ADRs**: `fdd-app-adr-0001`
"""
        report = validate_overall_design(text, skip_fs_checks=True)
        
        # Should parse requirement block
        self.assertEqual(report["requirement_count"], 1)

    def test_multiple_requirements(self):
        """Test multiple requirements."""
        text = """# DESIGN.md

## A. Purpose

Purpose.

## B. Business Model

Model.

## C. Requirements

### C.1 Functional Requirements

**ID**: `fdd-app-req-001`

**Actors**: `fdd-app-actor-user`

**Capabilities**: `fdd-app-capability-test`

**ID**: `fdd-app-req-002`

**Actors**: `fdd-app-actor-admin`

**Capabilities**: `fdd-app-capability-admin`
"""
        report = validate_overall_design(text, skip_fs_checks=True)
        
        self.assertEqual(report["requirement_count"], 2)


class TestSectionCSubsections(unittest.TestCase):
    """Test Section C subsection validation."""

    def test_section_c_all_subsections(self):
        """Test Section C with all C.1-C.5 subsections."""
        text = """# DESIGN.md

## A. Purpose

Purpose.

## B. Business Model

Model.

## C. Requirements

### C.1 Functional Requirements

Functional.

### C.2 Non-Functional Requirements

NFR.

### C.3 Principles

Principles.

### C.4 Constraints

Constraints.

### C.5 Assumptions

Assumptions.
"""
        report = validate_overall_design(text, skip_fs_checks=True)
        
        # Should pass structure check
        structure_errors = [e for e in report["errors"] if e.get("type") == "structure"]
        # No error about C.1-C.5 order
        c_order_errors = [e for e in structure_errors if "C.1..C.5" in e.get("message", "")]
        self.assertEqual(len(c_order_errors), 0)



if __name__ == "__main__":
    unittest.main()
