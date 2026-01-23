"""
FDD Validator - Cascading Validation

Handles artifact dependency resolution and cascading validation.
Artifact dependency graph:
  - feature-changes -> feature-design -> features-manifest -> overall-design -> (business-context, adr)
  - feature-design -> features-manifest -> overall-design -> (business-context, adr)
  - features-manifest -> overall-design -> (business-context, adr)
  - overall-design -> (business-context, adr)
  - adr -> business-context
  - business-context -> (none)
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple

from ..utils import detect_requirements, load_text


def _parse_feature_coverage_and_status(features_text: str) -> Tuple[Dict[str, str], Dict[str, set]]:
    """Parse FEATURES.md for feature status and covered requirement IDs.

    Returns:
        - feature_status_by_path: e.g. {"feature-auth/": "IMPLEMENTED"}
        - covered_req_ids_by_path: e.g. {"feature-auth/": {"fdd-x-req-y", ...}}
    """
    import re

    from ..constants import FEATURE_HEADING_RE
    from ..utils import field_block
    from .artifacts.changes import _extract_id_list

    lines = features_text.splitlines()
    feature_indices: List[int] = []
    feature_headers: List[Dict[str, object]] = []
    for idx, line in enumerate(lines):
        m = FEATURE_HEADING_RE.match(line.strip())
        if not m:
            continue
        feature_indices.append(idx)
        feature_headers.append({"path": m.group(3), "id": m.group(2)})

    feature_status_by_path: Dict[str, str] = {}
    covered_req_ids_by_path: Dict[str, set] = {}
    valid_statuses = {"NOT_STARTED", "IN_DESIGN", "DESIGN_READY", "IN_DEVELOPMENT", "IMPLEMENTED"}

    for i, header in enumerate(feature_headers):
        start = feature_indices[i]
        end = feature_indices[i + 1] if i + 1 < len(feature_indices) else len(lines)
        block_lines = lines[start:end]

        fb_status = field_block(block_lines, "Status")
        status_value = None
        if fb_status is not None:
            status_value = str(fb_status["value"]).strip()
            if status_value == "IN_PROGRESS":
                status_value = "IN_DEVELOPMENT"
            if status_value not in valid_statuses:
                status_value = None

        fb_req = field_block(block_lines, "Requirements Covered")
        req_ids: set = set()
        if fb_req is not None:
            for rid in _extract_id_list(fb_req):
                req_ids.add(rid)

        p = str(header["path"])
        feature_status_by_path[p] = status_value or ""
        covered_req_ids_by_path[p] = req_ids

    return feature_status_by_path, covered_req_ids_by_path


def _cross_validate_identifier_statuses(
    *,
    business_path: Optional[Path],
    design_path: Optional[Path],
    features_path: Optional[Path],
    skip_fs_checks: bool,
) -> List[Dict[str, object]]:
    """Cross-artifact status checks.

    - BUSINESS capability status IMPLEMENTED => all linked features are IMPLEMENTED.
    - DESIGN requirement status IMPLEMENTED => covered by at least one IMPLEMENTED feature.
    """
    if skip_fs_checks:
        return []
    if business_path is None or design_path is None or features_path is None:
        return []
    if not (business_path.exists() and design_path.exists() and features_path.exists()):
        return []

    from ..utils import parse_business_capability_statuses, parse_design_requirement_statuses

    errors: List[Dict[str, object]] = []

    bt, berr = load_text(business_path)
    dt, derr = load_text(design_path)
    ft, ferr = load_text(features_path)
    if berr or derr or ferr:
        # Base validators will report file-level errors; do not duplicate.
        return []

    bt = bt or ""
    dt = dt or ""
    ft = ft or ""

    cap_info = parse_business_capability_statuses(bt)
    design_req_status = parse_design_requirement_statuses(dt)

    feature_status_by_path, covered_req_ids_by_path = _parse_feature_coverage_and_status(ft)

    # Rule 1: capability IMPLEMENTED => all listed features IMPLEMENTED
    for cap_id, info in cap_info.items():
        if not isinstance(info, dict):
            continue
        if info.get("status") != "IMPLEMENTED":
            continue
        feats = info.get("features")
        if not isinstance(feats, list) or not feats:
            continue
        not_impl = [p for p in feats if feature_status_by_path.get(str(p), "") != "IMPLEMENTED"]
        if not_impl:
            errors.append(
                {
                    "type": "cross",
                    "message": "Capability status is IMPLEMENTED but not all linked features are IMPLEMENTED",
                    "capability": cap_id,
                    "features_not_implemented": sorted(set(not_impl)),
                }
            )

    # Rule 2: DESIGN req IMPLEMENTED => covered by at least one IMPLEMENTED feature
    for rid, st in design_req_status.items():
        if st != "IMPLEMENTED":
            continue
        covered_by_impl = False
        for feat_path, fstatus in feature_status_by_path.items():
            if fstatus != "IMPLEMENTED":
                continue
            if rid in covered_req_ids_by_path.get(feat_path, set()):
                covered_by_impl = True
                break
        if not covered_by_impl:
            errors.append(
                {
                    "type": "cross",
                    "message": "DESIGN requirement status is IMPLEMENTED but it is not covered by any IMPLEMENTED feature",
                    "requirement": rid,
                }
            )

    return errors


# Artifact dependency graph: artifact_kind -> list of dependency kinds
ARTIFACT_DEPENDENCIES: Dict[str, List[str]] = {
    "feature-changes": ["feature-design"],
    "feature-design": ["features-manifest", "overall-design"],
    "features-manifest": ["overall-design"],
    "overall-design": ["business-context", "adr"],
    "adr": ["business-context"],
    "business-context": [],
}


def find_artifact_path(artifact_kind: str, from_path: Path) -> Optional[Path]:
    """
    Find artifact path by kind, searching from the given path upward.
    
    Returns None if not found.
    """
    if artifact_kind == "feature-design":
        # Look in same directory as CHANGES.md
        candidate = from_path.parent / "DESIGN.md"
        if candidate.exists() and candidate.is_file():
            return candidate
        return None
    
    if artifact_kind == "features-manifest":
        # Look for architecture/features/FEATURES.md
        for parent in from_path.parents:
            candidate = parent / "architecture" / "features" / "FEATURES.md"
            if candidate.exists() and candidate.is_file():
                return candidate
        return None
    
    if artifact_kind == "overall-design":
        # Look for architecture/DESIGN.md
        for parent in from_path.parents:
            candidate = parent / "architecture" / "DESIGN.md"
            if candidate.exists() and candidate.is_file():
                return candidate
        return None
    
    if artifact_kind == "business-context":
        # Look for architecture/BUSINESS.md
        for parent in from_path.parents:
            candidate = parent / "architecture" / "BUSINESS.md"
            if candidate.exists() and candidate.is_file():
                return candidate
        return None
    
    if artifact_kind == "adr":
        # Look for architecture/ADR/ directory.
        for parent in from_path.parents:
            candidate_dir = parent / "architecture" / "ADR"
            if candidate_dir.exists() and candidate_dir.is_dir():
                return candidate_dir
        return None
    
    return None


def resolve_dependencies(
    artifact_kind: str,
    artifact_path: Path,
    *,
    resolved: Optional[Dict[str, Path]] = None,
) -> Dict[str, Path]:
    """
    Resolve all dependencies for an artifact recursively.
    
    Returns dict mapping artifact_kind -> path for all dependencies.
    """
    if resolved is None:
        resolved = {}
    
    deps = ARTIFACT_DEPENDENCIES.get(artifact_kind, [])
    
    for dep_kind in deps:
        if dep_kind in resolved:
            continue
        
        dep_path = find_artifact_path(dep_kind, artifact_path)
        if dep_path:
            resolved[dep_kind] = dep_path
            # Recursively resolve dependencies of this dependency
            resolve_dependencies(dep_kind, dep_path, resolved=resolved)
    
    return resolved


def validate_with_dependencies(
    artifact_path: Path,
    *,
    skip_fs_checks: bool = False,
) -> Dict[str, object]:
    """
    Validate an artifact along with all its dependencies.
    
    Automatically discovers and validates all dependent artifacts.
    Returns a comprehensive report with main validation and dependency validations.
    """
    from . import validate
    
    # Detect artifact kind and requirements
    artifact_kind, requirements_path = detect_requirements(artifact_path)
    
    # Resolve all dependencies
    dependencies = resolve_dependencies(artifact_kind, artifact_path)
    
    # Validate dependencies first (bottom-up: business/adr -> overall -> features -> feature)
    dependency_reports: Dict[str, Dict[str, object]] = {}
    overall_status = "PASS"
    
    # Define validation order (dependencies first)
    validation_order = ["business-context", "adr", "overall-design", "features-manifest", "feature-design"]
    
    for dep_kind in validation_order:
        if dep_kind not in dependencies:
            continue
        
        dep_path = dependencies[dep_kind]
        dep_artifact_kind, dep_requirements = detect_requirements(dep_path)
        
        # Get paths for cross-reference validation
        design_path = dependencies.get("overall-design")
        business_path = dependencies.get("business-context")
        adr_path = dependencies.get("adr")
        
        dep_report = validate(
            dep_path,
            dep_requirements,
            dep_artifact_kind,
            design_path=design_path,
            business_path=business_path,
            adr_path=adr_path,
            skip_fs_checks=skip_fs_checks,
        )
        dep_report["artifact_kind"] = dep_artifact_kind
        dep_report["path"] = str(dep_path)
        dependency_reports[dep_kind] = dep_report
        
        if dep_report.get("status") != "PASS":
            overall_status = "FAIL"
    
    # Validate the main artifact
    design_path = dependencies.get("overall-design")
    business_path = dependencies.get("business-context")
    adr_path = dependencies.get("adr")
    features_path = dependencies.get("features-manifest")
    
    report = validate(
        artifact_path,
        requirements_path,
        artifact_kind,
        design_path=design_path,
        business_path=business_path,
        adr_path=adr_path,
        skip_fs_checks=skip_fs_checks,
    )
    report["artifact_kind"] = artifact_kind

    # Cross-artifact status checks (only when core paths are available)
    cross_errors = _cross_validate_identifier_statuses(
        business_path=business_path,
        design_path=design_path,
        features_path=features_path,
        skip_fs_checks=skip_fs_checks,
    )
    if cross_errors:
        report.setdefault("errors", [])
        report["errors"].extend(cross_errors)
        report["status"] = "FAIL"
    
    # Include dependency validation results
    if dependency_reports:
        report["dependency_validation"] = dependency_reports
        if overall_status == "FAIL" and report.get("status") == "PASS":
            report["status"] = "FAIL"
            if "errors" not in report:
                report["errors"] = []
            report["errors"].append({
                "type": "dependency",
                "message": "One or more dependencies failed validation",
            })
    
    return report


def validate_all_artifacts(
    code_root: Path,
    *,
    skip_fs_checks: bool = False,
) -> Dict[str, object]:
    """
    Validate all FDD artifacts in a codebase.
    
    Discovers and validates:
    - architecture/BUSINESS.md
    - architecture/ADR/ (directory)
    - architecture/DESIGN.md
    - architecture/features/FEATURES.md
    - All feature DESIGN.md and CHANGES.md
    
    Returns a comprehensive report with all artifact validations.
    """
    from . import validate
    
    artifact_reports: Dict[str, Dict[str, object]] = {}
    overall_status = "PASS"
    
    arch_dir = code_root / "architecture"
    adr_dir = arch_dir / "ADR"
    
    # Validate core artifacts in order (dependencies first)
    core_artifacts = [
        ("business-context", arch_dir / "BUSINESS.md"),
        ("adr", adr_dir),
        ("overall-design", arch_dir / "DESIGN.md"),
        ("features-manifest", arch_dir / "features" / "FEATURES.md"),
    ]
    
    for artifact_kind, artifact_path in core_artifacts:
        if not artifact_path.exists():
            continue
        
        # Get dependency paths for cross-reference validation
        business_path = arch_dir / "BUSINESS.md" if (arch_dir / "BUSINESS.md").exists() else None
        adr_path = adr_dir if adr_dir.exists() else None
        design_path = arch_dir / "DESIGN.md" if (arch_dir / "DESIGN.md").exists() else None
        
        ak, ar = detect_requirements(artifact_path)
        report = validate(
            artifact_path,
            ar,
            ak,
            design_path=design_path if artifact_kind != "overall-design" else None,
            business_path=business_path if artifact_kind not in ("business-context",) else None,
            adr_path=adr_path if artifact_kind not in ("adr", "business-context") else None,
            skip_fs_checks=skip_fs_checks,
        )
        report["artifact_kind"] = ak
        report["path"] = str(artifact_path)
        artifact_reports[artifact_kind] = report
        
        if report.get("status") != "PASS":
            overall_status = "FAIL"

    # Cross-artifact status checks across core artifacts
    cross_errors = _cross_validate_identifier_statuses(
        business_path=arch_dir / "BUSINESS.md" if (arch_dir / "BUSINESS.md").exists() else None,
        design_path=arch_dir / "DESIGN.md" if (arch_dir / "DESIGN.md").exists() else None,
        features_path=arch_dir / "features" / "FEATURES.md" if (arch_dir / "features" / "FEATURES.md").exists() else None,
        skip_fs_checks=skip_fs_checks,
    )
    if cross_errors:
        artifact_reports.setdefault("cross-artifact-status", {"status": "FAIL", "errors": [], "placeholder_hits": [], "missing_sections": [], "required_section_count": 0})
        artifact_reports["cross-artifact-status"].setdefault("errors", [])
        artifact_reports["cross-artifact-status"]["errors"].extend(cross_errors)
        overall_status = "FAIL"
    
    # Validate all feature artifacts
    features_dir = arch_dir / "features"
    if features_dir.exists():
        for feature_dir in sorted(features_dir.iterdir()):
            if not feature_dir.is_dir() or feature_dir.name.startswith("."):
                continue
            
            feature_slug = feature_dir.name
            
            # Validate feature DESIGN.md
            feature_design = feature_dir / "DESIGN.md"
            if feature_design.exists():
                fk, fr = detect_requirements(feature_design)
                report = validate(
                    feature_design,
                    fr,
                    fk,
                    design_path=arch_dir / "DESIGN.md" if (arch_dir / "DESIGN.md").exists() else None,
                    business_path=arch_dir / "BUSINESS.md" if (arch_dir / "BUSINESS.md").exists() else None,
                    adr_path=adr_dir if adr_dir.exists() else None,
                    skip_fs_checks=skip_fs_checks,
                )
                report["artifact_kind"] = fk
                report["path"] = str(feature_design)
                artifact_reports[f"feature-design:{feature_slug}"] = report
                
                if report.get("status") != "PASS":
                    overall_status = "FAIL"
            
            # Validate feature CHANGES.md
            feature_changes = feature_dir / "CHANGES.md"
            if feature_changes.exists():
                ck, cr = detect_requirements(feature_changes)
                report = validate(
                    feature_changes,
                    cr,
                    ck,
                    design_path=feature_design if feature_design.exists() else None,
                    skip_fs_checks=skip_fs_checks,
                )
                report["artifact_kind"] = ck
                report["path"] = str(feature_changes)
                artifact_reports[f"feature-changes:{feature_slug}"] = report
                
                if report.get("status") != "PASS":
                    overall_status = "FAIL"
    
    return {
        "status": overall_status,
        "artifact_validation": artifact_reports,
    }


__all__ = [
    "ARTIFACT_DEPENDENCIES",
    "find_artifact_path",
    "resolve_dependencies",
    "validate_with_dependencies",
    "validate_all_artifacts",
]
