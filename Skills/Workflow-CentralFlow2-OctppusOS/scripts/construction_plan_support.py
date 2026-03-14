from __future__ import annotations

import shutil
from pathlib import Path

from construction_plan_contract import GUIDANCE_MARKERS, PACK_DIR_PATTERN, PLAN_KIND_VALUES
from construction_plan_contract import PACK_MACHINE_FILES, PACK_MARKDOWN_FILES, ROOT_REQUIRED_FILES
from construction_plan_rendering import (
    OFFICIAL_PLAN_KIND,
    PREVIEW_PLAN_KIND,
    default_steps,
    design_steps_from_plan,
    render_pack_registry,
    render_root_index,
    slugify,
    write_pack,
)
from construction_plan_schema import _parse_yaml, machine_schema_violations, validate_pack_registry
from mother_doc_lint_support import mother_doc_lint_summary


def _official_plan_prerequisites(design_plan_path: Path) -> tuple[dict, int] | None:
    mother_doc_root = design_plan_path.parent
    if not design_plan_path.exists():
        return {
            "status": "fail",
            "reason": "design_plan_missing",
            "design_plan_path": str(design_plan_path),
            "hint": "official construction plan requires an existing mother doc design plan",
        }, 1
    mother_doc_summary = mother_doc_lint_summary(mother_doc_root)
    if mother_doc_summary["status"] != "pass":
        return {
            "status": "fail",
            "reason": "mother_doc_not_ready_for_construction_plan",
            "design_plan_path": str(design_plan_path),
            "mother_doc_root": str(mother_doc_root),
            "mother_doc_lint": mother_doc_summary,
            "hint": "official construction plan can be created only after mother-doc-lint passes",
        }, 1
    steps = design_steps_from_plan(design_plan_path)
    if not steps:
        return {
            "status": "fail",
            "reason": "design_plan_has_no_design_steps",
            "design_plan_path": str(design_plan_path),
            "hint": "official construction plan requires concrete design_step rows in 08_dev_execution_plan.md",
        }, 1
    return None


def construction_plan_init_result(
    target: Path,
    design_plan_path: Path,
    force: bool,
    plan_kind: str,
) -> tuple[dict, int]:
    if plan_kind not in PLAN_KIND_VALUES:
        return {
            "status": "fail",
            "reason": "invalid_plan_kind",
            "plan_kind": plan_kind,
            "allowed_plan_kinds": PLAN_KIND_VALUES,
        }, 1
    if target.exists() and any(target.iterdir()) and not force:
        return {
            "status": "fail",
            "target": str(target),
            "reason": "target_not_empty",
            "hint": "rerun with --force to replace the existing construction plan root",
        }, 1
    if plan_kind == OFFICIAL_PLAN_KIND:
        prerequisite_failure = _official_plan_prerequisites(design_plan_path)
        if prerequisite_failure is not None:
            return prerequisite_failure
    if target.exists() and force:
        shutil.rmtree(target)
    steps = design_steps_from_plan(design_plan_path)
    if not steps:
        steps = default_steps()
    target.mkdir(parents=True, exist_ok=True)
    target.joinpath("00_index.md").write_text(render_root_index(steps, plan_kind), encoding="utf-8")
    target.joinpath("pack_registry.yaml").write_text(
        render_pack_registry(steps, design_plan_path, plan_kind),
        encoding="utf-8",
    )
    pack_dirs: list[str] = []
    for index, step in enumerate(steps, start=1):
        pack_dir = target / f"{index:02d}_{slugify(step['design_step_id'])}"
        write_pack(pack_dir, step, index, plan_kind)
        pack_dirs.append(str(pack_dir))
    return {
        "status": "pass",
        "target": str(target),
        "plan_kind": plan_kind,
        "created_packs": pack_dirs,
        "construction_plan_lint_command": (
            "./.venv_backend_skills/bin/python Skills/Workflow-CentralFlow2-OctppusOS/scripts/Cli_Toolbox.py "
            f"construction-plan-lint --path {target} --json"
        ),
    }, 0


def _validate_pack_registry_structure(root: Path) -> tuple[dict[str, object] | None, list[str]]:
    violations = validate_pack_registry(root)
    if violations:
        return None, violations
    payload, parse_errors = _parse_yaml(root / "pack_registry.yaml")
    if parse_errors:
        return None, [f"pack_registry.yaml: {error}" for error in parse_errors]
    if not isinstance(payload, dict):
        return None, ["pack_registry.yaml: top-level payload must be an object"]
    return payload, []


def construction_plan_lint_summary(path: Path, require_execution_eligible: bool = False) -> dict:
    root = path if path.is_dir() else path.parent if path.name == "00_index.md" else path
    exists = root.exists()
    pack_dirs = sorted([pack_dir for pack_dir in root.iterdir() if pack_dir.is_dir() and PACK_DIR_PATTERN.match(pack_dir.name)]) if exists else []
    mother_doc_root = root.parent
    design_plan_path = mother_doc_root / "08_dev_execution_plan.md"
    missing_root_files = [name for name in ROOT_REQUIRED_FILES if not (root / name).exists()] if exists else list(ROOT_REQUIRED_FILES)
    missing_pack_files = {
        pack_dir.name: [name for name in PACK_MARKDOWN_FILES + PACK_MACHINE_FILES if not (pack_dir / name).exists()]
        for pack_dir in pack_dirs
    }
    missing_pack_files = {key: value for key, value in missing_pack_files.items() if value}
    files_to_check = [root / name for name in ROOT_REQUIRED_FILES if (root / name).exists()] + [
        pack_dir / name
        for pack_dir in pack_dirs
        for name in PACK_MARKDOWN_FILES + PACK_MACHINE_FILES
        if (pack_dir / name).exists()
    ]
    replace_me_hits = [
        str(file_path.relative_to(root))
        for file_path in files_to_check
        if "replace_me" in file_path.read_text(encoding="utf-8")
    ]
    guidance_hits = [
        str(file_path.relative_to(root))
        for file_path in files_to_check
        if file_path.suffix == ".md"
        and any(marker in file_path.read_text(encoding="utf-8") for marker in GUIDANCE_MARKERS)
    ]
    schema_violations = [
        violation
        for pack_dir in pack_dirs
        if not missing_pack_files.get(pack_dir.name)
        for violation in machine_schema_violations(pack_dir)
    ]
    source_ref_violations: list[str] = []
    registry_payload: dict[str, object] | None = None
    registry_violations: list[str] = []
    if exists and not missing_root_files:
        registry_payload, registry_violations = _validate_pack_registry_structure(root)
    design_coverage_violations: list[str] = []
    execution_eligibility_violations: list[str] = []
    if registry_payload is not None:
        design_steps = design_steps_from_plan(design_plan_path)
        plan_kind = registry_payload["plan_kind"]
        packs = registry_payload["packs"]
        assert isinstance(packs, list)
        registry_step_ids = [str(item["design_step_id"]) for item in packs if isinstance(item, dict) and "design_step_id" in item]
        if plan_kind == OFFICIAL_PLAN_KIND:
            design_step_ids = [step["design_step_id"] for step in design_steps]
            missing_steps = sorted(set(design_step_ids) - set(registry_step_ids))
            unexpected_steps = sorted(set(registry_step_ids) - set(design_step_ids))
            if missing_steps:
                design_coverage_violations.append(
                    f"pack_registry.yaml: official plan missing design steps {missing_steps}"
                )
            if unexpected_steps:
                design_coverage_violations.append(
                    f"pack_registry.yaml: official plan has unexpected design steps {unexpected_steps}"
                )
        if require_execution_eligible:
            if registry_payload["execution_eligible"] is not True:
                execution_eligibility_violations.append(
                    "pack_registry.yaml: execution-eligible lint requires execution_eligible=true"
                )
            if registry_payload["plan_kind"] != OFFICIAL_PLAN_KIND:
                execution_eligibility_violations.append(
                    "pack_registry.yaml: execution-eligible lint requires plan_kind=official_plan"
                )
            if registry_payload["plan_state"] not in {"planned_unused", "in_execution"}:
                execution_eligibility_violations.append(
                    "pack_registry.yaml: execution-eligible lint requires plan_state in {planned_unused,in_execution}"
                )
        pack_dirs_from_registry = {
            str(item["pack_dir"]): item for item in packs if isinstance(item, dict) and "pack_dir" in item
        }
        missing_registry_pack_dirs = sorted({pack_dir.name for pack_dir in pack_dirs} - set(pack_dirs_from_registry))
        missing_disk_pack_dirs = sorted(set(pack_dirs_from_registry) - {pack_dir.name for pack_dir in pack_dirs})
        if missing_registry_pack_dirs:
            design_coverage_violations.append(
                f"pack_registry.yaml: registry missing pack entries for directories {missing_registry_pack_dirs}"
            )
        if missing_disk_pack_dirs:
            design_coverage_violations.append(
                f"pack_registry.yaml: pack entries missing on disk {missing_disk_pack_dirs}"
            )
        for pack_dir in pack_dirs:
            if missing_pack_files.get(pack_dir.name):
                continue
            manifest_payload, parse_errors = _parse_yaml(pack_dir / "pack_manifest.yaml")
            if parse_errors or not isinstance(manifest_payload, dict):
                continue
            source_refs = manifest_payload.get("source_mother_doc_refs")
            if isinstance(source_refs, list):
                for source_ref in source_refs:
                    ref_path = mother_doc_root / str(source_ref)
                    if not ref_path.exists():
                        source_ref_violations.append(
                            f"{pack_dir.name}/pack_manifest.yaml: source_mother_doc_ref_missing={source_ref}"
                        )
            registry_pack = pack_dirs_from_registry.get(pack_dir.name)
            if isinstance(registry_pack, dict):
                for shared_key in (
                    "pack_id",
                    "design_step_id",
                    "plan_kind",
                    "pack_state",
                    "execution_eligible",
                    "state_sync_eligible",
                    "reusable_as_official_plan",
                ):
                    if manifest_payload.get(shared_key) != registry_pack.get(shared_key):
                        design_coverage_violations.append(
                            f"{pack_dir.name}/pack_manifest.yaml: {shared_key} must match pack_registry.yaml"
                        )
                if require_execution_eligible:
                    if manifest_payload.get("execution_eligible") is not True:
                        execution_eligibility_violations.append(
                            f"{pack_dir.name}/pack_manifest.yaml: execution_eligible must be true"
                        )
                    if manifest_payload.get("pack_state") not in {"planned_unused", "in_execution"}:
                        execution_eligibility_violations.append(
                            f"{pack_dir.name}/pack_manifest.yaml: pack_state must be planned_unused or in_execution"
                        )
    status = (
        "pass"
        if exists
        and pack_dirs
        and not missing_root_files
        and not missing_pack_files
        and not replace_me_hits
        and not guidance_hits
        and not schema_violations
        and not registry_violations
        and not design_coverage_violations
        and not source_ref_violations
        and not execution_eligibility_violations
        else "fail"
    )
    return {
        "path": str(path),
        "resolved_root": str(root),
        "exists": exists,
        "status": status,
        "missing_root_files": missing_root_files,
        "missing_pack_dirs": [] if pack_dirs else ["expected at least one NN_* pack directory"],
        "missing_pack_files": missing_pack_files,
        "files_with_replace_me": replace_me_hits,
        "files_with_template_guidance": guidance_hits,
        "pack_registry_violations": registry_violations,
        "machine_schema_violations": schema_violations,
        "design_coverage_violations": design_coverage_violations,
        "source_mother_doc_ref_violations": source_ref_violations,
        "execution_eligibility_violations": execution_eligibility_violations,
        "pack_markdown_files": PACK_MARKDOWN_FILES,
        "pack_machine_files": PACK_MACHINE_FILES,
        "construction_plan_gate_allowed": status == "pass",
    }
