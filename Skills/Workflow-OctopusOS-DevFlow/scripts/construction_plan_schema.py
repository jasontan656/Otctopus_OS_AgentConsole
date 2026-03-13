from __future__ import annotations
import json
from pathlib import Path
from construction_plan_contract import INNER_PHASE_PATTERN, INNER_PHASE_REQUIRED_KEYS
from construction_plan_contract import MANIFEST_MACHINE_FILE_MAP, MANIFEST_REQUIRED_KEYS
from construction_plan_contract import PACK_ALLOWED_WRITEBACK_FILES, PACK_ID_PATTERN
# contract_name: octopus_devflow_construction_plan_schema
# contract_version: 1.0.0
# validation_mode: strict
# required_fields: validate_pack_manifest, validate_inner_phase_plan, machine_schema_violations
# optional_fields: []
def _is_non_empty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())

def _is_non_empty_string_list(value: object) -> bool:
    return isinstance(value, list) and bool(value) and all(_is_non_empty_string(item) for item in value)

def _parse_simple_yaml(path: Path) -> tuple[dict[str, object] | None, list[str]]:
    data: dict[str, object] = {}
    current_key: str | None = None
    errors: list[str] = []
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.rstrip()
        if not line.strip():
            continue
        if not line.startswith(" "):
            if ":" not in line:
                errors.append(f"line {line_number}: expected key: value")
                current_key = None
                continue
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            if not key:
                errors.append(f"line {line_number}: empty key")
                current_key = None
            elif value:
                data[key] = value
                current_key = None
            else:
                data[key] = None
                current_key = key
            continue
        if current_key is None:
            errors.append(f"line {line_number}: indented entry without parent key")
            continue
        if line.startswith("  - "):
            item = line[4:].strip()
            if not item:
                errors.append(f"line {line_number}: empty list item")
            elif data.get(current_key) is None:
                data[current_key] = [item]
            elif isinstance(data[current_key], list):
                data[current_key].append(item)
            else:
                errors.append(f"line {line_number}: mixed list/map content under {current_key}")
            continue
        stripped = line.strip()
        if ":" not in stripped:
            errors.append(f"line {line_number}: expected nested key: value under {current_key}")
            continue
        nested_key, nested_value = stripped.split(":", 1)
        nested_key = nested_key.strip()
        nested_value = nested_value.strip()
        if not nested_key or not nested_value:
            errors.append(f"line {line_number}: nested key/value must be non-empty under {current_key}")
        elif data.get(current_key) is None:
            data[current_key] = {nested_key: nested_value}
        elif isinstance(data[current_key], dict):
            data[current_key][nested_key] = nested_value
        else:
            errors.append(f"line {line_number}: mixed list/map content under {current_key}")
    return (data if not errors else None), errors
def validate_pack_manifest(pack_dir: Path) -> list[str]:
    manifest_path = pack_dir / "pack_manifest.yaml"
    manifest, parse_errors = _parse_simple_yaml(manifest_path)
    if parse_errors:
        return [f"{pack_dir.name}/pack_manifest.yaml: {error}" for error in parse_errors]
    assert manifest is not None
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
        violations.append(f"{pack_dir.name}/pack_manifest.yaml: machine_files unexpected keys {extra_machine_keys}")
    for key, expected_file in MANIFEST_MACHINE_FILE_MAP.items():
        if machine_files.get(key) != expected_file:
            violations.append(f"{pack_dir.name}/pack_manifest.yaml: machine_files.{key} must equal {expected_file}")
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
    missing_keys = sorted({"pack_id", "design_step_id", "inner_phases"} - set(payload))
    extra_keys = sorted(set(payload) - {"pack_id", "design_step_id", "inner_phases"})
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
    manifest, _ = _parse_simple_yaml(pack_dir / "pack_manifest.yaml")
    payload = json.loads((pack_dir / "inner_phase_plan.json").read_text(encoding="utf-8"))
    if manifest and (manifest["pack_id"] != payload["pack_id"] or manifest["design_step_id"] != payload["design_step_id"]):
        return [f"{pack_dir.name}: pack_manifest.yaml and inner_phase_plan.json must share pack_id/design_step_id"]
    return []
