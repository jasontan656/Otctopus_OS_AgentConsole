#!/usr/bin/env python3
"""Shared helpers for mstg_target_governance_outcome_lint."""
from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import Any

import mstg_yaml as yaml

DEFAULT_CONTRACT = Path(__file__).resolve().parents[1] / "references" / "mstg_target_outcome_lint_contract.yaml"
DEFAULT_REQUIRED_DOCS = [
    "L0/README.md",
    "L1/README.md",
    "L2/README.md",
    "L3/README.md",
    "L4/README.md",
    "L5/README.md",
    "L6/README.md",
    "L7/README.md",
    "L8/README.md",
    "L9/README.md",
    "L10/README.md",
    "L11/README.md",
    "L12/README.md",
    "L13/README.md",
]
DEFAULT_REQUIRED_RUNTIME_FILES = ["TOOL_REGISTRY.yaml", "TOOL_DOCS_STRUCTURED.yaml", "TOOL_CHANGE_LEDGER.jsonl", "TOOLING_GOVERNANCE_STATE.yaml", "TOOLBOX_INJECTION_MANIFEST.yaml"]
DEFAULT_REQUIRED_SCRIPTS = [
    "mstg_three_mode_workflow.py",
    "tooling_governance_apply_change.py",
    "tooling_governance_auto_writeback.py",
    "tooling_governance_context_backfill.py",
    "tooling_docs_query.py",
    "tooling_docs_record.py",
    "tooling_change_ledger.py",
    "tooling_change_impact_mapper.py",
    "tooling_governance_lint.py",
    "mstg_l0_l13_linear_writeback.py",
    "mstg_l0_l13_linear_layers.py",
    "mstg_l0_l13_linear_profile.py",
    "mstg_l0_l13_linear_flow.py",
    "mstg_l0_l13_linear_composite.py",
    "mstg_l0_l13_writeback_contracts.py",
    "mstg_l0_l13_linear_lint.py",
    "mstg_l0_l13_layer_schema_lint.py",
    "mstg_l0_l13_full_gate_lint.py",
    "mstg_target_governance_outcome_lint.py",
    "mstg_target_outcome_lint_helpers.py",
    "mstg_target_skill_audit_helpers.py",
    "governance_audit_log.py",
]
DEFAULT_SELF_MAINTENANCE_ENTRY_HEADING = "## Governance Self-Maintenance Entry"
DEFAULT_SELF_MAINTENANCE_ENTRY_TOKENS = [
    "tooling_governance/{instance_name}/docs/L0/README.md",
    "tooling_governance/{instance_name}/docs/L11/README.md",
    "tooling_governance/{instance_name}/docs/tooling/TOOL_DOC_SYNC_CONTRACT.md",
    "tooling_governance/{instance_name}/docs/evolution/SELF_EVOLUTION_TRACEABILITY.md",
    "tooling_governance/{instance_name}/scripts/tooling_governance_auto_writeback.py",
    "tooling_governance/{instance_name}/scripts/mstg_l0_l13_full_gate_lint.py",
    "tooling_governance/{instance_name}/scripts/mstg_target_governance_outcome_lint.py",
]
DEFAULT_TARGET_SURFACE_MARKERS = {
    "begin": "<!-- MSTG_GOVERNANCE_CONTRACT_BEGIN -->",
    "end": "<!-- MSTG_GOVERNANCE_CONTRACT_END -->",
}
DEFAULT_MACHINE_MAP_REQUIRED_FIELDS = [
    "layer_id",
    "anchor",
    "dependency",
    "input",
    "output",
    "acceptance",
    "upstream",
    "downstream",
    "decision_control_ref",
    "execution_spec_ref",
    "acceptance_evidence_ref",
    "tool_anchor_refs",
    "script_anchor_refs",
    "asset_anchor_refs",
    "evidence_anchor_refs",
    "code_mapping_refs",
    "path",
]
DEFAULT_MACHINE_MAP_REQUIRED_ANCHOR_FIELDS = [
    "tool_anchor_refs",
    "script_anchor_refs",
    "asset_anchor_refs",
    "evidence_anchor_refs",
]
DEFAULT_MACHINE_MAP_ANCHOR_PATH_FIELDS = [
    "script_anchor_refs",
    "asset_anchor_refs",
    "evidence_anchor_refs",
]


def detect_runtime_root() -> Path:
    env_root = os.environ.get("MSTG_RUNTIME_ROOT", "").strip()
    if env_root:
        p = Path(env_root).expanduser().resolve()
        if p.is_dir():
            return p

    cwd = Path.cwd().resolve()
    for p in [cwd, *cwd.parents]:
        candidate = p / "Codex_Skill_Runtime"
        if candidate.is_dir():
            return candidate.resolve()

    home = Path.home().resolve()
    try:
        children = sorted(home.iterdir())
    except Exception:
        children = []
    for child in children:
        candidate = child / "Codex_Skill_Runtime"
        if candidate.is_dir():
            return candidate.resolve()

    return (home / "Codex_Skill_Runtime").resolve()


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def ensure_list(raw: Any) -> list[str]:
    if not isinstance(raw, list):
        return []
    out: list[str] = []
    for item in raw:
        token = str(item).strip()
        if token:
            out.append(token)
    return out


def render_token(value: str, *, instance_name: str, target_skill: str) -> str:
    return (
        value.replace("{instance_name}", instance_name)
        .replace("{target_skill}", target_skill)
        .strip()
    )


def add_violation(
    rows: list[dict[str, Any]],
    *,
    vid: str,
    severity: str,
    message: str,
    evidence: list[str] | None = None,
) -> None:
    rows.append(
        {
            "id": vid,
            "severity": severity,
            "message": message,
            "evidence": evidence or [],
        }
    )


def add_violation_if(
    rows: list[dict[str, Any]],
    *,
    condition: bool,
    vid: str,
    severity: str,
    message: str,
    evidence: list[str] | None = None,
) -> None:
    if condition:
        add_violation(rows, vid=vid, severity=severity, message=message, evidence=evidence)


def parse_tool_ids(payload: Any) -> list[str]:
    if not isinstance(payload, dict):
        return []
    tools = payload.get("tools")
    if not isinstance(tools, list):
        return []
    out: list[str] = []
    for row in tools:
        if not isinstance(row, dict):
            continue
        tid = str(row.get("tool_id", "")).strip()
        if tid:
            out.append(tid)
    return sorted(set(out))


def tool_docs_by_id(payload: Any) -> dict[str, dict[str, Any]]:
    if not isinstance(payload, dict):
        return {}
    tools = payload.get("tools")
    if not isinstance(tools, list):
        return {}
    out: dict[str, dict[str, Any]] = {}
    for row in tools:
        if not isinstance(row, dict):
            continue
        tid = str(row.get("tool_id", "")).strip()
        if tid:
            out[tid] = row
    return out


def parse_jsonl(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    records: list[dict[str, Any]] = []
    errors: list[str] = []
    if not path.is_file():
        return records, errors
    for idx, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        raw = line.strip()
        if not raw:
            continue
        try:
            obj = json.loads(raw)
        except Exception:
            errors.append(f"line={idx}:json_parse_error")
            continue
        if not isinstance(obj, dict):
            errors.append(f"line={idx}:json_not_object")
            continue
        records.append(obj)
    return records, errors


def extract_machine_map(markdown_text: str) -> dict[str, Any] | None:
    m = re.search(r"## Machine Map\s*```yaml\s*(.*?)\s*```", markdown_text, flags=re.S)
    if not m:
        return None
    try:
        payload = yaml.safe_load(m.group(1))
    except Exception:
        return None
    return payload if isinstance(payload, dict) else None


def normalize_anchor_path(value: str) -> str:
    token = str(value or "").strip().replace("\\", "/")
    token = token.split("#", 1)[0].strip()
    while token.startswith("./"):
        token = token[2:]
    return token


def anchor_path_resolvable(value: str, *, instance_root: Path, target_skill_dir: Path) -> bool:
    rel = normalize_anchor_path(value)
    if not rel:
        return False
    p = Path(rel)
    if p.is_absolute():
        return p.exists()
    return (instance_root / rel).exists() or (target_skill_dir / rel).exists()


def infer_target_skill_dir(instance_root: Path) -> Path:
    if len(instance_root.parents) < 2:
        return instance_root
    parent_name = instance_root.parent.name
    if parent_name in {"tooling_governance", "governance_instance"}:
        return instance_root.parents[1]
    return instance_root.parents[1]


def resolve_instance_root(target_skill_dir: Path, instance_name: str) -> Path | None:
    candidates = [
        target_skill_dir / "tooling_governance" / instance_name,
        target_skill_dir / "governance_instance" / instance_name,
        target_skill_dir / "governance_instance" / "self",
    ]
    for p in candidates:
        if p.is_dir() and (p / "docs").is_dir() and (p / "runtime").is_dir():
            return p.resolve()
    return None


def severity_counts(violations: list[dict[str, Any]]) -> dict[str, int]:
    out = {"high": 0, "medium": 0, "low": 0}
    for row in violations:
        sev = str(row.get("severity", "")).lower()
        out[sev] = out.get(sev, 0) + (1 if sev in out else 0)
    return out


def load_contract(path: Path, *, instance_name: str, target_skill: str) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    if path.is_file():
        parsed = load_yaml(path)
        if isinstance(parsed, dict):
            payload = parsed

    required = payload.get("required", {}) if isinstance(payload.get("required"), dict) else {}
    non_empty = payload.get("non_empty_rules", {}) if isinstance(payload.get("non_empty_rules"), dict) else {}
    traceability = payload.get("traceability_rules", {}) if isinstance(payload.get("traceability_rules"), dict) else {}
    machine_map = required.get("machine_map", {}) if isinstance(required.get("machine_map"), dict) else {}

    target_surface = required.get("target_skill_surface", {}) if isinstance(required.get("target_skill_surface"), dict) else {}
    markers = target_surface.get("contract_markers", {}) if isinstance(target_surface.get("contract_markers"), dict) else {}
    marker_begin = str(markers.get("begin", DEFAULT_TARGET_SURFACE_MARKERS["begin"])).strip()
    marker_end = str(markers.get("end", DEFAULT_TARGET_SURFACE_MARKERS["end"])).strip()
    keyword_templates = ensure_list(target_surface.get("contract_keywords"))
    rendered_keywords = [render_token(k, instance_name=instance_name, target_skill=target_skill) for k in keyword_templates]
    entry_tokens = ensure_list(target_surface.get("self_maintenance_entry_required_tokens")) or list(
        DEFAULT_SELF_MAINTENANCE_ENTRY_TOKENS
    )
    rendered_entry_tokens = [render_token(k, instance_name=instance_name, target_skill=target_skill) for k in entry_tokens]

    return {
        "schema_version": str(payload.get("schema_version", "mstg_target_outcome_lint_contract_v3")),
        "required": {
            "target_skill_surface": {
                "require_skill_md_exists": bool(target_surface.get("require_skill_md_exists", True)),
                "require_injected_contract_markers": bool(target_surface.get("require_injected_contract_markers", False)),
                "require_meta_mode_keywords_in_target_skill": bool(target_surface.get("require_meta_mode_keywords_in_target_skill", False)),
                "require_self_maintenance_entry": bool(target_surface.get("require_self_maintenance_entry", True)),
                "self_maintenance_entry_heading": str(
                    target_surface.get("self_maintenance_entry_heading", DEFAULT_SELF_MAINTENANCE_ENTRY_HEADING)
                ).strip(),
                "self_maintenance_entry_required_tokens": rendered_entry_tokens,
                "contract_markers": {
                    "begin": marker_begin,
                    "end": marker_end,
                },
                "contract_keywords": rendered_keywords,
            },
            "instance_required_docs": ensure_list(required.get("instance_required_docs")) or list(DEFAULT_REQUIRED_DOCS),
            "instance_required_runtime_files": ensure_list(required.get("instance_required_runtime_files")) or list(DEFAULT_REQUIRED_RUNTIME_FILES),
            "toolbox_required_scripts": ensure_list(required.get("toolbox_required_scripts")) or list(DEFAULT_REQUIRED_SCRIPTS),
            "machine_map": {
                "required_fields": ensure_list(machine_map.get("required_fields")) or list(DEFAULT_MACHINE_MAP_REQUIRED_FIELDS),
                "required_anchor_fields": ensure_list(machine_map.get("required_anchor_fields"))
                or list(DEFAULT_MACHINE_MAP_REQUIRED_ANCHOR_FIELDS),
                "anchor_path_fields": ensure_list(machine_map.get("anchor_path_fields"))
                or list(DEFAULT_MACHINE_MAP_ANCHOR_PATH_FIELDS),
            },
            "structured_docs": {
                "required_sections": (
                    ensure_list((required.get("structured_docs") or {}).get("required_sections")) or ["usage", "modification", "development"]
                )
                if isinstance(required.get("structured_docs"), dict)
                else ["usage", "modification", "development"],
                "usage_required_keys": (
                    ensure_list((required.get("structured_docs") or {}).get("usage_required_keys")) or ["summary", "command_examples", "inputs", "outputs"]
                )
                if isinstance(required.get("structured_docs"), dict)
                else ["summary", "command_examples", "inputs", "outputs"],
            },
        },
        "non_empty_rules": {
            "min_non_ws_chars_per_doc": int(non_empty.get("min_non_ws_chars_per_doc", 120)),
            "forbidden_tokens": ensure_list(non_empty.get("forbidden_tokens")) or ["replace_me"],
        },
        "traceability_rules": {
            "require_nonempty_tool_change_ledger": bool(traceability.get("require_nonempty_tool_change_ledger", True)),
            "require_valid_jsonl_tool_change_ledger": bool(traceability.get("require_valid_jsonl_tool_change_ledger", True)),
            "required_tool_change_ledger_keys": ensure_list(traceability.get("required_tool_change_ledger_keys"))
            or ["event_id", "timestamp_utc", "tool_id", "change_type", "summary"],
            "require_governance_audit_timeline": bool(traceability.get("require_governance_audit_timeline", True)),
            "require_valid_governance_audit_jsonl": bool(traceability.get("require_valid_governance_audit_jsonl", True)),
            "governance_audit_event_schema_version": str(traceability.get("governance_audit_event_schema_version", "mstg_governance_audit_event_v1")).strip(),
            "require_target_trace_in_governance_audit": bool(traceability.get("require_target_trace_in_governance_audit", True)),
        },
    }
