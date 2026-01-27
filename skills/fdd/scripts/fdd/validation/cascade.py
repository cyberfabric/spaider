"""
FDD Validator - Cascading Validation

Handles artifact dependency resolution and cascading validation.
Artifact dependency graph:
  - feature-design -> features-manifest -> overall-design -> (prd, adr)
  - features-manifest -> overall-design -> (prd, adr)
  - overall-design -> (prd, adr)
  - adr -> prd
  - prd -> (none)
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple

from ..utils import (
    find_adapter_directory,
    find_project_root,
    fdd_root_from_this_file,
    iter_registry_entries,
    load_artifacts_registry,
    load_text,
)


def _suggest_workflow_for_registry_kind(kind: Optional[str]) -> Optional[str]:
    if not isinstance(kind, str):
        return None
    m = {
        "PRD": "workflows/prd.md",
        "DESIGN": "workflows/design.md",
        "ADR": "workflows/adr.md",
        "FEATURES": "workflows/features.md",
        "FEATURE": "workflows/feature.md",
    }
    return m.get(kind)


def _parse_feature_coverage_and_status(features_text: str) -> Tuple[Dict[str, str], Dict[str, set]]:
    """Parse FEATURES.md for feature status and covered requirement IDs.

    Returns:
        - feature_status_by_path: e.g. {"feature-auth/": "IMPLEMENTED"}
        - covered_req_ids_by_path: e.g. {"feature-auth/": {"fdd-x-req-y", ...}}
    """
    import re

    from ..constants import FEATURE_HEADING_RE
    from ..utils import field_block
    from .artifacts.common import _extract_id_list

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
    prd_path: Optional[Path],
    design_path: Optional[Path],
    features_path: Optional[Path],
    skip_fs_checks: bool,
) -> List[Dict[str, object]]:
    """Cross-artifact status checks.

    - PRD functional requirement status IMPLEMENTED => all linked features are IMPLEMENTED.
    - DESIGN requirement status IMPLEMENTED => covered by at least one IMPLEMENTED feature.
    """
    if skip_fs_checks:
        return []
    if prd_path is None or design_path is None or features_path is None:
        return []
    if not (prd_path.exists() and design_path.exists() and features_path.exists()):
        return []

    from ..utils import parse_prd_capability_statuses, parse_design_requirement_statuses

    errors: List[Dict[str, object]] = []

    bt, berr = load_text(prd_path)
    dt, derr = load_text(design_path)
    ft, ferr = load_text(features_path)
    if berr or derr or ferr:
        # Base validators will report file-level errors; do not duplicate.
        return []

    bt = bt or ""
    dt = dt or ""
    ft = ft or ""

    cap_info = parse_prd_capability_statuses(bt)
    design_req_status = parse_design_requirement_statuses(dt)

    feature_status_by_path, covered_req_ids_by_path = _parse_feature_coverage_and_status(ft)

    # Rule 1: functional requirement IMPLEMENTED => all listed features IMPLEMENTED
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
                    "message": "Functional requirement status is IMPLEMENTED but not all linked features are IMPLEMENTED",
                    "functional_requirement": cap_id,
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


ARTIFACT_DEPENDENCIES: Dict[str, List[str]] = {
    "feature-design": ["features-manifest", "overall-design"],
    "features-manifest": ["overall-design"],
    "overall-design": ["prd", "adr"],
    "adr": ["prd"],
    "prd": [],
}


def _norm_registry_path(p: str) -> str:
    s = str(p or "").strip()
    if s.startswith("./"):
        s = s[2:]
    return s


def _kind_from_registry_entry(entry: dict) -> Optional[str]:
    k = entry.get("kind")
    if not isinstance(k, str):
        return None
    m = {
        "PRD": "prd",
        "ADR": "adr",
        "DESIGN": "overall-design",
        "FEATURES": "features-manifest",
        "FEATURE": "feature-design",
    }
    return m.get(k)


def _requirements_path_for_artifact_kind(artifact_kind: str) -> Optional[Path]:
    fdd_root = fdd_root_from_this_file()
    m = {
        "prd": "requirements/prd-structure.md",
        "adr": "requirements/adr-structure.md",
        "overall-design": "requirements/overall-design-structure.md",
        "features-manifest": "requirements/features-manifest-structure.md",
        "feature-design": "requirements/feature-design-structure.md",
    }
    rel = m.get(artifact_kind)
    if rel is None:
        return None
    return (fdd_root / rel).resolve()


def _registry_abs_path(project_root: Path, entry: dict) -> Optional[Path]:
    p = entry.get("path")
    if not isinstance(p, str) or not p.strip():
        return None
    s = _norm_registry_path(p)
    if s.startswith("/"):
        return Path(s).resolve()
    return (project_root / s).resolve()


def _traceability_enabled(entry: Optional[dict]) -> bool:
    if not isinstance(entry, dict):
        return False
    v = entry.get("traceability_enabled")
    if v is False:
        return False
    # Default: enabled
    return True


def _system_parent_map(entries: List[dict]) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for e in entries:
        sysv = e.get("system")
        parent = e.get("parent")
        if not isinstance(sysv, str) or not sysv.strip():
            continue
        if not isinstance(parent, str) or not parent.strip():
            continue
        if sysv not in out:
            out[sysv] = parent
    return out


def _system_chain(system: str, parents: Dict[str, str]) -> List[str]:
    seen: set = set()
    out: List[str] = []
    cur = system
    while cur and cur not in seen:
        seen.add(cur)
        out.append(cur)
        cur = parents.get(cur, "")
    return out


def _find_entry_for_path(project_root: Path, entries: List[dict], artifact_path: Path) -> Optional[dict]:
    try:
        rel = artifact_path.resolve().relative_to(project_root.resolve()).as_posix()
    except Exception:
        return None
    rel = _norm_registry_path(rel)
    for e in entries:
        p = e.get("path")
        if not isinstance(p, str):
            continue
        if _norm_registry_path(p) == rel:
            return e
    return None


def _pick_path_for_kind(
    *,
    project_root: Path,
    entries: List[dict],
    system: str,
    kind: str,
    parents: Dict[str, str],
) -> Optional[Path]:
    for sysv in _system_chain(system, parents):
        candidates: List[Path] = []
        for e in entries:
            if e.get("system") != sysv:
                continue
            if _kind_from_registry_entry(e) != kind:
                continue
            ap = _registry_abs_path(project_root, e)
            if ap is None:
                continue
            candidates.append(ap)
        if not candidates:
            continue
        dirs = [p for p in candidates if p.exists() and p.is_dir()]
        if dirs:
            return dirs[0]
        return candidates[0]
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
    
    project_root = find_project_root(artifact_path if artifact_path.is_dir() else artifact_path.parent)
    if project_root is None:
        return resolved

    adapter_dir = find_adapter_directory(project_root)
    if adapter_dir is None:
        return resolved

    registry, err = load_artifacts_registry(adapter_dir)
    if err or registry is None:
        return resolved

    entries = iter_registry_entries(registry)
    parents = _system_parent_map(entries)

    entry = _find_entry_for_path(project_root, entries, artifact_path)
    if entry is None:
        return resolved
    sysv = entry.get("system")
    if not isinstance(sysv, str) or not sysv.strip():
        return resolved

    deps = ARTIFACT_DEPENDENCIES.get(artifact_kind, [])
    for dep_kind in deps:
        if dep_kind in resolved:
            continue
        dep_path = _pick_path_for_kind(
            project_root=project_root,
            entries=entries,
            system=sysv,
            kind=dep_kind,
            parents=parents,
        )
        if dep_path is None:
            continue
        resolved[dep_kind] = dep_path
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
    from .artifacts import validate_content_only

    project_root = find_project_root(artifact_path if artifact_path.is_dir() else artifact_path.parent)
    if project_root is None:
        return {"status": "FAIL", "errors": [{"type": "file", "message": "Project root not found"}], "placeholder_hits": [], "missing_sections": [], "required_section_count": 0}
    adapter_dir = find_adapter_directory(project_root)
    if adapter_dir is None:
        return {"status": "FAIL", "errors": [{"type": "file", "message": "Adapter directory not found"}], "placeholder_hits": [], "missing_sections": [], "required_section_count": 0}
    registry, err = load_artifacts_registry(adapter_dir)
    if err or registry is None:
        return {"status": "FAIL", "errors": [{"type": "file", "message": err or "Missing artifacts registry"}], "placeholder_hits": [], "missing_sections": [], "required_section_count": 0}
    entries = iter_registry_entries(registry)
    entry = _find_entry_for_path(project_root, entries, artifact_path)
    if entry is None:
        # If the file is not registered, we cannot infer its artifact kind or dependencies.
        # Treat this as a skipped validation (PASS) unless the caller explicitly
        # provides requirements/kind via other entry points.
        return {
            "status": "PASS",
            "artifact_kind": "unregistered",
            "skipped": True,
            "skipped_reason": "Artifact is not registered in artifacts.json",
            "path": str(artifact_path),
            "placeholder_hits": [],
            "missing_sections": [],
            "required_section_count": 0,
        }

    if entry.get("format") != "FDD":
        report = validate_content_only(artifact_path, skip_fs_checks=skip_fs_checks)
        report["artifact_kind"] = "content-only"
        report["registry_format"] = entry.get("format")
        report["suggested_workflow"] = _suggest_workflow_for_registry_kind(entry.get("kind"))
        report.setdefault("errors", [])
        report["errors"].append(
            {
                "type": "registry",
                "message": "Artifact registry entry is not format=FDD; performed content-only validation",
                "path": str(artifact_path),
                "format": entry.get("format"),
            }
        )
        return report
    artifact_kind = _kind_from_registry_entry(entry)
    if artifact_kind is None:
        return {"status": "FAIL", "errors": [{"type": "registry", "message": "Unsupported artifact kind in artifacts.json", "path": str(artifact_path)}], "placeholder_hits": [], "missing_sections": [], "required_section_count": 0}
    requirements_path = _requirements_path_for_artifact_kind(artifact_kind)
    if requirements_path is None:
        return {"status": "FAIL", "errors": [{"type": "registry", "message": "No requirements mapping for artifact kind", "kind": artifact_kind}], "placeholder_hits": [], "missing_sections": [], "required_section_count": 0}

    entries_by_kind: Dict[str, dict] = {artifact_kind: entry}
    traceability_by_kind: Dict[str, bool] = {artifact_kind: _traceability_enabled(entry)}

    dependencies = resolve_dependencies(artifact_kind, artifact_path)
    missing_dependencies: List[str] = [k for k in ARTIFACT_DEPENDENCIES.get(artifact_kind, []) if k not in dependencies]

    # Index dependency entries and traceability flags.
    for dep_kind, dep_path in dependencies.items():
        dep_entry = _find_entry_for_path(project_root, entries, dep_path)
        if isinstance(dep_entry, dict):
            entries_by_kind[dep_kind] = dep_entry
            traceability_by_kind[dep_kind] = _traceability_enabled(dep_entry)
        else:
            traceability_by_kind[dep_kind] = False
    
    # Validate dependencies first (bottom-up: prd/adr -> overall -> features -> feature)
    dependency_reports: Dict[str, Dict[str, object]] = {}
    overall_status = "PASS"
    
    # Define validation order (dependencies first)
    validation_order = ["prd", "adr", "overall-design", "features-manifest", "feature-design"]
    
    for dep_kind in validation_order:
        if dep_kind not in dependencies:
            continue
        
        dep_path = dependencies[dep_kind]
        dep_artifact_kind = dep_kind
        dep_requirements = _requirements_path_for_artifact_kind(dep_kind)
        if dep_requirements is None:
            continue
        
        src_trace = traceability_by_kind.get(dep_kind, False)

        # Get paths for cross-reference validation, gated by traceability_enabled.
        design_path = dependencies.get("overall-design") if (src_trace and traceability_by_kind.get("overall-design", False)) else None
        prd_path = dependencies.get("prd") if (src_trace and traceability_by_kind.get("prd", False)) else None
        adr_path = dependencies.get("adr") if (src_trace and traceability_by_kind.get("adr", False)) else None
        features_path = dependencies.get("features-manifest") if (src_trace and traceability_by_kind.get("features-manifest", False)) else None
        
        dep_report = validate(
            dep_path,
            dep_requirements,
            dep_artifact_kind,
            design_path=design_path,
            prd_path=prd_path,
            adr_path=adr_path,
            features_path=features_path,
            skip_fs_checks=skip_fs_checks,
        )
        dep_report["artifact_kind"] = dep_artifact_kind
        dep_report["path"] = str(dep_path)
        dependency_reports[dep_kind] = dep_report
        
        if dep_report.get("status") != "PASS":
            overall_status = "FAIL"
    
    # Validate the main artifact
    src_trace = traceability_by_kind.get(artifact_kind, False)
    design_path = dependencies.get("overall-design") if (src_trace and traceability_by_kind.get("overall-design", False)) else None
    prd_path = dependencies.get("prd") if (src_trace and traceability_by_kind.get("prd", False)) else None
    adr_path = dependencies.get("adr") if (src_trace and traceability_by_kind.get("adr", False)) else None
    features_path = dependencies.get("features-manifest") if (src_trace and traceability_by_kind.get("features-manifest", False)) else None
    
    report = validate(
        artifact_path,
        requirements_path,
        artifact_kind,
        design_path=design_path,
        prd_path=prd_path,
        adr_path=adr_path,
        features_path=features_path,
        skip_fs_checks=skip_fs_checks,
    )
    report["artifact_kind"] = artifact_kind

    # Cross-artifact status checks (only when core paths are available)
    cross_errors: List[Dict[str, object]] = []
    if src_trace and traceability_by_kind.get("prd", False) and traceability_by_kind.get("overall-design", False) and traceability_by_kind.get("features-manifest", False):
        cross_errors = _cross_validate_identifier_statuses(
            prd_path=prd_path,
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
    
    if missing_dependencies:
        report.setdefault("errors", [])
        report["errors"].append({
            "type": "dependency",
            "message": "One or more dependencies were not found in artifacts registry",
            "missing": missing_dependencies,
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
    - architecture/PRD.md
    - architecture/ADR/ (directory)
    - architecture/DESIGN.md
    - architecture/features/FEATURES.md
    - All feature DESIGN.md
    
    Returns a comprehensive report with all artifact validations.
    """
    from . import validate
    from .artifacts import validate_content_only
    
    artifact_reports: Dict[str, Dict[str, object]] = {}
    overall_status = "PASS"
    
    project_root = find_project_root(code_root)
    if project_root is None:
        return {"status": "FAIL", "artifact_validation": {"errors": [{"type": "file", "message": "Project root not found"}]}}

    adapter_dir = find_adapter_directory(project_root)
    if adapter_dir is None:
        return {"status": "FAIL", "artifact_validation": {"errors": [{"type": "file", "message": "Adapter directory not found"}]}}

    registry, err = load_artifacts_registry(adapter_dir)
    if err or registry is None:
        return {"status": "FAIL", "artifact_validation": {"errors": [{"type": "file", "message": err or "Missing artifacts registry"}]}}

    entries = iter_registry_entries(registry)
    parents = _system_parent_map(entries)
    systems = sorted({str(e.get("system")) for e in entries if isinstance(e.get("system"), str) and str(e.get("system")).strip()})

    for system in systems:
        prd_path = _pick_path_for_kind(project_root=project_root, entries=entries, system=system, kind="prd", parents=parents)
        adr_path = _pick_path_for_kind(project_root=project_root, entries=entries, system=system, kind="adr", parents=parents)
        design_path = _pick_path_for_kind(project_root=project_root, entries=entries, system=system, kind="overall-design", parents=parents)
        features_path = _pick_path_for_kind(project_root=project_root, entries=entries, system=system, kind="features-manifest", parents=parents)

        prd_entry = _find_entry_for_path(project_root, entries, prd_path) if prd_path is not None else None
        adr_entry = _find_entry_for_path(project_root, entries, adr_path) if adr_path is not None else None
        design_entry = _find_entry_for_path(project_root, entries, design_path) if design_path is not None else None
        features_entry = _find_entry_for_path(project_root, entries, features_path) if features_path is not None else None

        prd_trace = _traceability_enabled(prd_entry)
        adr_trace = _traceability_enabled(adr_entry)
        design_trace = _traceability_enabled(design_entry)
        features_trace = _traceability_enabled(features_entry)

        core = [
            ("prd", prd_path),
            ("adr", adr_path),
            ("overall-design", design_path),
            ("features-manifest", features_path),
        ]

        for kind, p in core:
            if p is None:
                continue
            ent = _find_entry_for_path(project_root, entries, p)
            if ent is not None and ent.get("format") != "FDD":
                rep = validate_content_only(p, skip_fs_checks=skip_fs_checks)
                rep["artifact_kind"] = "content-only"
                rep["registry_format"] = ent.get("format")
                rep["suggested_workflow"] = _suggest_workflow_for_registry_kind(ent.get("kind"))
                rep.setdefault("errors", [])
                rep["errors"].append(
                    {
                        "type": "registry",
                        "message": "Artifact registry entry is not format=FDD; performed content-only validation",
                        "path": str(p),
                        "format": ent.get("format"),
                    }
                )
            else:
                ak = kind
                ar = _requirements_path_for_artifact_kind(kind)
                if ar is None:
                    continue

                src_trace = _traceability_enabled(ent)
                gated_design_path = design_path if (src_trace and design_trace) else None
                gated_prd_path = prd_path if (src_trace and prd_trace) else None
                gated_adr_path = adr_path if (src_trace and adr_trace) else None
                gated_features_path = features_path if (src_trace and features_trace) else None
                rep = validate(
                    p,
                    ar,
                    ak,
                    design_path=gated_design_path,
                    prd_path=gated_prd_path,
                    adr_path=gated_adr_path,
                    features_path=gated_features_path,
                    skip_fs_checks=skip_fs_checks,
                )
                rep["artifact_kind"] = ak
            rep["path"] = str(p)
            artifact_reports[f"{system}:{kind}"] = rep
            if rep.get("status") != "PASS":
                overall_status = "FAIL"

        if prd_path is not None and design_path is not None and features_path is not None and prd_trace and design_trace and features_trace:
            cross_errors = _cross_validate_identifier_statuses(
                prd_path=prd_path,
                design_path=design_path,
                features_path=features_path,
                skip_fs_checks=skip_fs_checks,
            )
            if cross_errors:
                artifact_reports.setdefault(f"{system}:cross-artifact-status", {"status": "FAIL", "errors": [], "placeholder_hits": [], "missing_sections": [], "required_section_count": 0})
                artifact_reports[f"{system}:cross-artifact-status"].setdefault("errors", [])
                artifact_reports[f"{system}:cross-artifact-status"]["errors"].extend(cross_errors)
                overall_status = "FAIL"

        for e in entries:
            if e.get("system") != system:
                continue
            if _kind_from_registry_entry(e) != "feature-design":
                continue
            fp = _registry_abs_path(project_root, e)
            if fp is None:
                continue
            if not fp.exists():
                continue
            if e.get("format") != "FDD":
                rep = validate_content_only(fp, skip_fs_checks=skip_fs_checks)
                rep["artifact_kind"] = "content-only"
                rep["registry_format"] = e.get("format")
                rep["suggested_workflow"] = _suggest_workflow_for_registry_kind(e.get("kind"))
                rep.setdefault("errors", [])
                rep["errors"].append(
                    {
                        "type": "registry",
                        "message": "Artifact registry entry is not format=FDD; performed content-only validation",
                        "path": str(fp),
                        "format": e.get("format"),
                    }
                )
            else:
                fk = "feature-design"
                fr = _requirements_path_for_artifact_kind("feature-design")
                if fr is None:
                    continue

                src_trace = _traceability_enabled(e)
                gated_design_path = design_path if (src_trace and design_trace) else None
                gated_prd_path = prd_path if (src_trace and prd_trace) else None
                gated_adr_path = adr_path if (src_trace and adr_trace) else None
                gated_features_path = features_path if (src_trace and features_trace) else None
                rep = validate(
                    fp,
                    fr,
                    fk,
                    design_path=gated_design_path,
                    prd_path=gated_prd_path,
                    adr_path=gated_adr_path,
                    features_path=gated_features_path,
                    skip_fs_checks=skip_fs_checks,
                )
                rep["artifact_kind"] = fk
            rep["path"] = str(fp)
            artifact_reports[f"{system}:feature-design:{_norm_registry_path(str(e.get('path', '')))}"] = rep
            if rep.get("status") != "PASS":
                overall_status = "FAIL"
    
    return {
        "status": overall_status,
        "artifact_validation": artifact_reports,
    }


__all__ = [
    "ARTIFACT_DEPENDENCIES",
    "resolve_dependencies",
    "validate_with_dependencies",
    "validate_all_artifacts",
]
