from __future__ import annotations

import json
from pathlib import Path

import yaml

from construction_plan_contract import INNER_PHASE_PATTERN, INNER_PHASE_REQUIRED_KEYS
from construction_plan_contract import INNER_PHASE_TOP_LEVEL_REQUIRED_KEYS, MANIFEST_MACHINE_FILE_MAP
from construction_plan_contract import MANIFEST_REQUIRED_KEYS, PACK_ALLOWED_WRITEBACK_FILES
from construction_plan_contract import PACK_ID_PATTERN, PACK_PLAN_STATE_VALUES, PLAN_KIND_VALUES
from construction_plan_contract import ROOT_PACK_ENTRY_REQUIRED_KEYS, ROOT_PLAN_STATE_VALUES
from construction_plan_contract import ROOT_REGISTRY_REQUIRED_KEYS

# contract_name: octopus_devflow_construction_plan_schema
# contract_version: 2.0.0
# validation_mode: strict
# required_fields: validate_pack_registry, validate_pack_manifest, validate_inner_phase_plan, machine_schema_violations
# optional_fields: []


def _is_non_empty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _is_non_empty_string_list(value: object) -> bool:
    return isinstance(value, list) and bool(value) and all(_is_non_empty_string(item) for item in value)


def _parse_yaml(path: Path) -> tuple[object | None, list[str]]:
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        return None, [f"invalid yaml ({exc})"]
    return payload, []


def _is_bool(value: object) -> bool:
    return isinstance(value, bool)


def validate_pack_registry(root: Path) -> list[str]:
    registry_path = root / "pack_registry.yaml"
    payload, parse_errors = _parse_yaml(registry_path)
    if parse_errors:
        return [f"pack_registry.yaml: {error}" for error in parse_errors]
    if not isinstance(payload, dict):
        return ["pack_registry.yaml: top-level payload must be an object"]

    violations: list[str] = []
    missing_keys = sorted(ROOT_REGISTRY_REQUIRED_KEYS - set(payload))
    extra_keys = sorted(set(payload) - ROOT_REGISTRY_REQUIRED_KEYS)
    if missing_keys:
        violations.append(f"pack_registry.yaml: missing keys {missing_keys}")
    if extra_keys:
        violations.append(f"pack_registry.yaml: unexpected keys {extra_keys}")

    plan_kind = payload.get("plan_kind")
    if plan_kind not in PLAN_KIND_VALUES:
        violations.append(f"pack_registry.yaml: plan_kind must be one of {PLAN_KIND_VALUES}")

    plan_state = payload.get("plan_state")
    if plan_state not in ROOT_PLAN_STATE_VALUES:
        violations.append(f"pack_registry.yaml: plan_state must be one of {ROOT_PLAN_STATE_VALUES}")

    for key in ("execution_eligible", "state_sync_eligible", "reusable_as_official_plan"):
        if not _is_bool(payload.get(key)):
            violations.append(f"pack_registry.yaml: {key} must be a boolean")

    if not _is_non_empty_string(payload.get("design_plan_path")):
        violations.append("pack_registry.yaml: design_plan_path must be a non-empty string")

    design_step_ids = payload.get("design_step_ids")
    if not _is_non_empty_string_list(design_step_ids):
        violations.append("pack_registry.yaml: design_step_ids must be a non-empty string list")

    packs = payload.get("packs")
    if not isinstance(packs, list) or not packs:
        return violations + ["pack_registry.yaml: packs must be a non-empty list"]

    seen_pack_ids: set[str] = set()
    seen_pack_dirs: set[str] = set()
    for index, pack in enumerate(packs, start=1):
        prefix = f"pack_registry.yaml: packs[{index}]"
        if not isinstance(pack, dict):
            violations.append(f"{prefix} must be an object")
            continue
        missing_pack_keys = sorted(ROOT_PACK_ENTRY_REQUIRED_KEYS - set(pack))
        extra_pack_keys = sorted(set(pack) - ROOT_PACK_ENTRY_REQUIRED_KEYS)
        if missing_pack_keys:
            violations.append(f"{prefix} missing keys {missing_pack_keys}")
        if extra_pack_keys:
            violations.append(f"{prefix} unexpected keys {extra_pack_keys}")

        pack_id = pack.get("pack_id")
        if not _is_non_empty_string(pack_id):
            violations.append(f"{prefix}.pack_id must be a non-empty string")
        else:
            pack_id_value = str(pack_id)
            if not PACK_ID_PATTERN.match(pack_id_value):
                violations.append(f"{prefix}.pack_id must match PACK-NN")
            if pack_id_value in seen_pack_ids:
                violations.append(f"{prefix}.pack_id must be unique")
            seen_pack_ids.add(pack_id_value)

        if not _is_non_empty_string(pack.get("design_step_id")):
            violations.append(f"{prefix}.design_step_id must be a non-empty string")
        if pack.get("plan_kind") not in PLAN_KIND_VALUES:
            violations.append(f"{prefix}.plan_kind must be one of {PLAN_KIND_VALUES}")
        if pack.get("pack_state") not in PACK_PLAN_STATE_VALUES:
            violations.append(f"{prefix}.pack_state must be one of {PACK_PLAN_STATE_VALUES}")
        for bool_key in ("execution_eligible", "state_sync_eligible", "reusable_as_official_plan"):
            if not _is_bool(pack.get(bool_key)):
                violations.append(f"{prefix}.{bool_key} must be a boolean")
        for path_key in ("pack_dir", "machine_manifest", "progress_ledger", "evidence_registry"):
            if not _is_non_empty_string(pack.get(path_key)):
                violations.append(f"{prefix}.{path_key} must be a non-empty string")
        pack_dir = pack.get("pack_dir")
        if _is_non_empty_string(pack_dir):
            pack_dir_value = str(pack_dir)
            if pack_dir_value in seen_pack_dirs:
                violations.append(f"{prefix}.pack_dir must be unique")
            seen_pack_dirs.add(pack_dir_value)

    plan_kind_value = payload.get("plan_kind")
    execution_eligible = payload.get("execution_eligible")
    state_sync_eligible = payload.get("state_sync_eligible")
    reusable_as_official_plan = payload.get("reusable_as_official_plan")
    plan_state_value = payload.get("plan_state")
    if plan_kind_value == "preview_skeleton":
        if execution_eligible is not False:
            violations.append("pack_registry.yaml: preview_skeleton must set execution_eligible=false")
        if state_sync_eligible is not False:
            violations.append("pack_registry.yaml: preview_skeleton must set state_sync_eligible=false")
        if reusable_as_official_plan is not False:
            violations.append("pack_registry.yaml: preview_skeleton must set reusable_as_official_plan=false")
        if plan_state_value != "preview_only":
            violations.append("pack_registry.yaml: preview_skeleton must use plan_state=preview_only")
    if plan_kind_value == "official_plan":
        if execution_eligible is not True:
            violations.append("pack_registry.yaml: official_plan must set execution_eligible=true")
        if state_sync_eligible is not True:
            violations.append("pack_registry.yaml: official_plan must set state_sync_eligible=true")
        if plan_state_value == "preview_only":
            violations.append("pack_registry.yaml: official_plan cannot use plan_state=preview_only")
    return violations


def validate_pack_manifest(pack_dir: Path) -> list[str]:
    manifest_path = pack_dir / "pack_manifest.yaml"
    manifest, parse_errors = _parse_yaml(manifest_path)
    if parse_errors:
        return [f"{pack_dir.name}/pack_manifest.yaml: {error}" for error in parse_errors]
    if not isinstance(manifest, dict):
        return [f"{pack_dir.name}/pack_manifest.yaml: top-level payload must be an object"]

    violations: list[str] = []
    missing_keys = sorted(MANIFEST_REQUIRED_KEYS - set(manifest))
    extra_keys = sorted(set(manifest) - MANIFEST_REQUIRED_KEYS)
    if missing_keys:
        violations.append(f"{pack_dir.name}/pack_manifest.yaml: missing keys {missing_keys}")
    if extra_keys:
        violations.append(f"{pack_dir.name}/pack_manifest.yaml: unexpected keys {extra_keys}")
    if not _is_non_empty_string(manifest.get("pack_id")):
        violations.append(f"{pack_dir.name}/pack_manifest.yaml: pack_id must be a non-empty string")
    elif not PACK_ID_PATTERN.match(str(manifest["pack_id"])):
        violations.append(f"{pack_dir.name}/pack_manifest.yaml: pack_id must match PACK-NN")
    if not _is_non_empty_string(manifest.get("design_step_id")):
        violations.append(f"{pack_dir.name}/pack_manifest.yaml: design_step_id must be a non-empty string")
    if manifest.get("plan_kind") not in PLAN_KIND_VALUES:
        violations.append(f"{pack_dir.name}/pack_manifest.yaml: plan_kind must be one of {PLAN_KIND_VALUES}")
    if manifest.get("pack_state") not in PACK_PLAN_STATE_VALUES:
        violations.append(
            f"{pack_dir.name}/pack_manifest.yaml: pack_state must be one of {PACK_PLAN_STATE_VALUES}"
        )
    for key in ("execution_eligible", "state_sync_eligible", "reusable_as_official_plan"):
        if not _is_bool(manifest.get(key)):
            violations.append(f"{pack_dir.name}/pack_manifest.yaml: {key} must be a boolean")
    if not _is_non_empty_string(manifest.get("pack_goal")):
        violations.append(f"{pack_dir.name}/pack_manifest.yaml: pack_goal must be a non-empty string")
    for key in (
        "design_plan_refs",
        "source_mother_doc_refs",
        "target_requirement_atoms",
        "implementation_actions",
        "changed_files_boundary",
        "stage_acceptance_target",
    ):
        if not _is_non_empty_string_list(manifest.get(key)):
            violations.append(f"{pack_dir.name}/pack_manifest.yaml: {key} must be a non-empty string list")
    machine_files = manifest.get("machine_files")
    if not isinstance(machine_files, dict):
        violations.append(f"{pack_dir.name}/pack_manifest.yaml: machine_files must be a mapping")
        return violations
    missing_machine_keys = sorted(set(MANIFEST_MACHINE_FILE_MAP) - set(machine_files))
    extra_machine_keys = sorted(set(machine_files) - set(MANIFEST_MACHINE_FILE_MAP))
    if missing_machine_keys:
        violations.append(f"{pack_dir.name}/pack_manifest.yaml: machine_files missing keys {missing_machine_keys}")
    if extra_machine_keys:
        violations.append(
            f"{pack_dir.name}/pack_manifest.yaml: machine_files unexpected keys {extra_machine_keys}"
        )
    for key, expected_file in MANIFEST_MACHINE_FILE_MAP.items():
        if machine_files.get(key) != expected_file:
            violations.append(f"{pack_dir.name}/pack_manifest.yaml: machine_files.{key} must equal {expected_file}")

    if manifest.get("plan_kind") == "preview_skeleton":
        if manifest.get("execution_eligible") is not False:
            violations.append(f"{pack_dir.name}/pack_manifest.yaml: preview_skeleton must set execution_eligible=false")
        if manifest.get("state_sync_eligible") is not False:
            violations.append(f"{pack_dir.name}/pack_manifest.yaml: preview_skeleton must set state_sync_eligible=false")
        if manifest.get("pack_state") != "preview_only":
            violations.append(f"{pack_dir.name}/pack_manifest.yaml: preview_skeleton must use pack_state=preview_only")
    if manifest.get("plan_kind") == "official_plan":
        if manifest.get("execution_eligible") is not True:
            violations.append(f"{pack_dir.name}/pack_manifest.yaml: official_plan must set execution_eligible=true")
        if manifest.get("state_sync_eligible") is not True:
            violations.append(f"{pack_dir.name}/pack_manifest.yaml: official_plan must set state_sync_eligible=true")
        if manifest.get("pack_state") == "preview_only":
            violations.append(f"{pack_dir.name}/pack_manifest.yaml: official_plan cannot use pack_state=preview_only")
    return violations


def validate_inner_phase_plan(pack_dir: Path) -> list[str]:
    path = pack_dir / "inner_phase_plan.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{pack_dir.name}/inner_phase_plan.json: invalid json ({exc.msg})"]
    if not isinstance(payload, dict):
        return [f"{pack_dir.name}/inner_phase_plan.json: top-level payload must be an object"]
    violations: list[str] = []
    missing_keys = sorted(INNER_PHASE_TOP_LEVEL_REQUIRED_KEYS - set(payload))
    extra_keys = sorted(set(payload) - INNER_PHASE_TOP_LEVEL_REQUIRED_KEYS)
    if missing_keys:
        violations.append(f"{pack_dir.name}/inner_phase_plan.json: missing keys {missing_keys}")
    if extra_keys:
        violations.append(f"{pack_dir.name}/inner_phase_plan.json: unexpected keys {extra_keys}")
    if not _is_non_empty_string(payload.get("pack_id")):
        violations.append(f"{pack_dir.name}/inner_phase_plan.json: pack_id must be a non-empty string")
    elif not PACK_ID_PATTERN.match(str(payload["pack_id"])):
        violations.append(f"{pack_dir.name}/inner_phase_plan.json: pack_id must match PACK-NN")
    if not _is_non_empty_string(payload.get("design_step_id")):
        violations.append(f"{pack_dir.name}/inner_phase_plan.json: design_step_id must be a non-empty string")
    if payload.get("plan_kind") not in PLAN_KIND_VALUES:
        violations.append(f"{pack_dir.name}/inner_phase_plan.json: plan_kind must be one of {PLAN_KIND_VALUES}")
    if payload.get("pack_state") not in PACK_PLAN_STATE_VALUES:
        violations.append(
            f"{pack_dir.name}/inner_phase_plan.json: pack_state must be one of {PACK_PLAN_STATE_VALUES}"
        )
    if not _is_bool(payload.get("execution_eligible")):
        violations.append(f"{pack_dir.name}/inner_phase_plan.json: execution_eligible must be a boolean")
    inner_phases = payload.get("inner_phases")
    if not isinstance(inner_phases, list) or not inner_phases:
        return violations + [f"{pack_dir.name}/inner_phase_plan.json: inner_phases must be a non-empty array"]
    seen_phase_ids: set[str] = set()
    for index, phase in enumerate(inner_phases, start=1):
        prefix = f"{pack_dir.name}/inner_phase_plan.json: inner_phases[{index}]"
        if not isinstance(phase, dict):
            violations.append(f"{prefix} must be an object")
            continue
        missing_phase_keys = sorted(INNER_PHASE_REQUIRED_KEYS - set(phase))
        extra_phase_keys = sorted(set(phase) - INNER_PHASE_REQUIRED_KEYS)
        if missing_phase_keys:
            violations.append(f"{prefix} missing keys {missing_phase_keys}")
        if extra_phase_keys:
            violations.append(f"{prefix} unexpected keys {extra_phase_keys}")
        phase_id = phase.get("inner_phase_id")
        if not _is_non_empty_string(phase_id):
            violations.append(f"{prefix}.inner_phase_id must be a non-empty string")
        else:
            phase_id_value = str(phase_id)
            if not INNER_PHASE_PATTERN.match(phase_id_value):
                violations.append(f"{prefix}.inner_phase_id must match PHASE-NN")
            if phase_id_value in seen_phase_ids:
                violations.append(f"{prefix}.inner_phase_id must be unique")
            seen_phase_ids.add(phase_id_value)
        if not _is_non_empty_string(phase.get("phase_goal")):
            violations.append(f"{prefix}.phase_goal must be a non-empty string")
        if not _is_non_empty_string(phase.get("phase_exit_signal")):
            violations.append(f"{prefix}.phase_exit_signal must be a non-empty string")
        for key in ("implementation_slice", "validation_slice", "evidence_writeback_slice"):
            if not _is_non_empty_string_list(phase.get(key)):
                violations.append(f"{prefix}.{key} must be a non-empty string list")
        evidence_refs = phase.get("evidence_writeback_slice")
        if isinstance(evidence_refs, list):
            invalid_refs = sorted({item for item in evidence_refs if item not in PACK_ALLOWED_WRITEBACK_FILES})
            if invalid_refs:
                violations.append(f"{prefix}.evidence_writeback_slice has unsupported refs {invalid_refs}")
    return violations


def machine_schema_violations(pack_dir: Path) -> list[str]:
    manifest_violations = validate_pack_manifest(pack_dir)
    phase_violations = validate_inner_phase_plan(pack_dir)
    if manifest_violations or phase_violations:
        return manifest_violations + phase_violations
    manifest, _ = _parse_yaml(pack_dir / "pack_manifest.yaml")
    payload = json.loads((pack_dir / "inner_phase_plan.json").read_text(encoding="utf-8"))
    assert isinstance(manifest, dict)
    shared_keys = ("pack_id", "design_step_id", "plan_kind", "pack_state", "execution_eligible")
    mismatched = [key for key in shared_keys if manifest.get(key) != payload.get(key)]
    if mismatched:
        return [
            f"{pack_dir.name}: pack_manifest.yaml and inner_phase_plan.json must share {', '.join(mismatched)}"
        ]
    return []
