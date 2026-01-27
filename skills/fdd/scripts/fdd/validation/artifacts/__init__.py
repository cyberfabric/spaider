"""
FDD Validator - Artifacts Package

Validation for all FDD artifacts split into focused modules.
"""

from pathlib import Path
from typing import Dict, Optional

from .feature_design import validate_feature_design
from .overall_design import validate_overall_design
from .prd import validate_prd
from .adr import validate_adr
from .features import validate_features_manifest
from .common import validate_generic_sections, common_checks
from ...utils import find_placeholders


def validate_content_only(
    artifact_path: Path,
    *,
    skip_fs_checks: bool = False,
) -> Dict[str, object]:
    artifact_text = ""
    if artifact_path.is_file():
        artifact_text = artifact_path.read_text(encoding="utf-8")

    if not artifact_path.exists():
        return {
            "required_section_count": 0,
            "missing_sections": [],
            "placeholder_hits": [],
            "status": "FAIL",
            "errors": [{"type": "file", "message": "File not found"}],
        }

    if artifact_path.is_file() and not artifact_text.strip():
        return {
            "required_section_count": 0,
            "missing_sections": [],
            "placeholder_hits": [],
            "status": "FAIL",
            "errors": [{"type": "file", "message": "Empty file"}],
        }

    placeholders = find_placeholders(artifact_text)
    common_errors, common_placeholders = common_checks(
        artifact_text=artifact_text,
        artifact_path=artifact_path,
        requirements_path=artifact_path,
        artifact_kind="content-only",
        skip_fs_checks=skip_fs_checks,
    )

    out_placeholders = list(placeholders)
    out_placeholders.extend(common_placeholders)

    status = "PASS" if (not common_errors and not out_placeholders) else "FAIL"
    return {
        "required_section_count": 0,
        "missing_sections": [],
        "placeholder_hits": out_placeholders,
        "status": status,
        "errors": list(common_errors),
    }


def validate(
    artifact_path: Path,
    requirements_path: Path,
    artifact_kind: str,
    *,
    design_path: Optional[Path] = None,
    prd_path: Optional[Path] = None,
    adr_path: Optional[Path] = None,
    features_path: Optional[Path] = None,
    skip_fs_checks: bool = False,
) -> Dict[str, object]:
    """Main validation dispatcher - routes to appropriate validator."""
    artifact_text = ""
    if artifact_path.is_file():
        artifact_text = artifact_path.read_text(encoding="utf-8")

    if artifact_path.is_file() and not artifact_text.strip():
        return {
            "required_section_count": 0,
            "missing_sections": [],
            "placeholder_hits": [],
            "status": "FAIL",
            "errors": [{"type": "file", "message": "Empty file"}],
        }

    if artifact_kind == "features-manifest":
        report = validate_features_manifest(
            artifact_text,
            artifact_path=artifact_path,
            design_path=design_path,
            skip_fs_checks=skip_fs_checks,
        )
    elif artifact_kind == "prd":
        report = validate_prd(artifact_text)
    elif artifact_kind == "adr":
        report = validate_adr(
            artifact_text,
            artifact_path=artifact_path,
            prd_path=prd_path,
            design_path=design_path,
            skip_fs_checks=skip_fs_checks,
        )
    elif artifact_kind == "feature-design":
        report = validate_feature_design(
            artifact_text,
            artifact_path=artifact_path,
            prd_path=prd_path,
            features_path=features_path,
            skip_fs_checks=skip_fs_checks,
        )
    elif artifact_kind == "overall-design":
        report = validate_overall_design(
            artifact_text,
            artifact_path=artifact_path,
            prd_path=prd_path,
            adr_path=adr_path,
            skip_fs_checks=skip_fs_checks,
        )
    else:
        report = validate_generic_sections(artifact_text, requirements_path)

    # Apply common checks
    common_errors, common_placeholders = common_checks(
        artifact_text=artifact_text,
        artifact_path=artifact_path,
        requirements_path=requirements_path,
        artifact_kind=artifact_kind,
        skip_fs_checks=skip_fs_checks,
    )
    
    if "errors" not in report:
        report["errors"] = []
    report["errors"].extend(common_errors)
    
    if "placeholder_hits" not in report:
        report["placeholder_hits"] = []
    report["placeholder_hits"].extend(common_placeholders)
    
    if report.get("placeholder_hits"):
        report["status"] = "FAIL"
    if report.get("errors") and report.get("status") == "PASS":
        report["status"] = "FAIL"
    
    return report


__all__ = [
    "validate",
    "validate_content_only",
    "validate_feature_design",
    "validate_overall_design",
    "validate_prd",
    "validate_adr",
    "validate_features_manifest",
]
