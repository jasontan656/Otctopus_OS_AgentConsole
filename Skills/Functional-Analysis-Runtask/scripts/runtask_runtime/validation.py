from __future__ import annotations

from pathlib import Path

from .task_runtime import workspace_root_boundary_error
from .types import BoundaryErrorPayload, StageLintPayload
from .validation_common import _checked_files_payload, _load_workspace
from .validation_rules import (
    _validate_architect_assessment,
    _validate_completed_packages_have_witness,
    _validate_design_decisions,
    _validate_evidence_registry,
    _validate_implementation_ledger,
    _validate_impact_map,
    _validate_manifest,
    _validate_milestone_packages,
    _validate_preview_projection,
    _validate_stage_artifacts,
    _validate_stage_consistency,
)


def stage_lint_payload(workspace_root: Path, stage: str) -> StageLintPayload | BoundaryErrorPayload:
    resolved_workspace_root = workspace_root.resolve()
    boundary_error = workspace_root_boundary_error(resolved_workspace_root)
    if boundary_error is not None:
        return {
            **boundary_error,
            "stage": stage,
            "workspace_root": str(resolved_workspace_root),
            "errors": [],
            "warnings": [],
            "checked_files": _checked_files_payload(resolved_workspace_root),
        }
    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []
    loaded = _load_workspace(resolved_workspace_root, errors)
    if not loaded:
        return {
            "status": "fail",
            "stage": stage,
            "workspace_root": str(resolved_workspace_root),
            "errors": errors,
            "warnings": warnings,
            "checked_files": _checked_files_payload(resolved_workspace_root),
        }

    manifest = loaded["manifest"]
    evidence_ids = _validate_evidence_registry(resolved_workspace_root, loaded["evidence_registry"], errors, warnings)
    _validate_manifest(resolved_workspace_root, manifest, errors, warnings)

    if stage in {"architect", "preview", "design", "impact", "plan", "implementation", "validation", "final_delivery", "all"}:
        _validate_architect_assessment(resolved_workspace_root, loaded["architect_assessment"], evidence_ids, errors)
        _validate_preview_projection(resolved_workspace_root, loaded["preview_projection"], evidence_ids, errors)
        _validate_design_decisions(resolved_workspace_root, loaded["design_decisions"], evidence_ids, errors)
        _validate_impact_map(resolved_workspace_root, loaded["impact_map"], evidence_ids, errors)

    package_ids, active_package_ids, completed_package_ids = set(), [], []
    if stage in {"plan", "implementation", "validation", "final_delivery", "all"}:
        package_ids, active_package_ids, completed_package_ids = _validate_milestone_packages(resolved_workspace_root, loaded["milestone_packages"], errors)

    if stage in {"implementation", "validation", "final_delivery", "all"}:
        _validate_implementation_ledger(resolved_workspace_root, loaded["implementation_ledger"], package_ids, evidence_ids, errors)
        _validate_completed_packages_have_witness(loaded["implementation_ledger"], completed_package_ids, errors)

    _validate_stage_artifacts(resolved_workspace_root, manifest, stage, errors)
    _validate_stage_consistency(resolved_workspace_root, manifest, stage, active_package_ids, loaded["implementation_ledger"], errors, warnings)
    return {
        "status": "pass" if not errors else "fail",
        "stage": stage,
        "workspace_root": str(resolved_workspace_root),
        "errors": errors,
        "warnings": warnings,
        "checked_files": _checked_files_payload(resolved_workspace_root),
    }
