#!/usr/bin/env python3
"""Profile and registry helpers for MSTG L0-L13 linear writeback."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import re
from typing import Any

import mstg_yaml as yaml


def extract_machine_map(markdown_text: str) -> dict[str, Any] | None:
    m = re.search(r"## Machine Map\s*```yaml\s*(.*?)\s*```", markdown_text, flags=re.S)
    if not m:
        return None
    try:
        obj = yaml.safe_load(m.group(1))
    except Exception:
        return None
    return obj if isinstance(obj, dict) else None


def normalize_anchor_token(token: str) -> str:
    return token.strip().replace("\\", "/")


def anchor_path_resolvable(token: str, instance_root: Path, target_skill_dir: Path | None) -> bool:
    candidate = Path(token)
    if candidate.is_absolute():
        return candidate.exists()

    rel = normalize_anchor_token(token)
    if not rel:
        return False

    if (instance_root / rel).exists():
        return True
    if target_skill_dir is not None and (target_skill_dir / rel).exists():
        return True
    return False


def _ensure_str_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    rows: list[str] = []
    for item in value:
        token = str(item).strip()
        if token:
            rows.append(token)
    return rows


def _safe_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def load_registry_tool_catalog(instance_root: Path) -> dict[str, str]:
    reg_path = instance_root / "runtime" / "TOOL_REGISTRY.yaml"
    if not reg_path.is_file():
        return {}
    try:
        payload = yaml.safe_load(reg_path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    if not isinstance(payload, dict):
        return {}

    rows = payload.get("tools")
    if not isinstance(rows, list):
        return {}

    catalog: dict[str, str] = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        tool_id = str(row.get("tool_id", "")).strip()
        entrypoint = normalize_anchor_token(str(row.get("entrypoint", "")))
        if not tool_id or not entrypoint:
            continue
        catalog[tool_id] = entrypoint
    return catalog


def load_registry_tool_rows(instance_root: Path) -> list[dict[str, str]]:
    reg_path = instance_root / "runtime" / "TOOL_REGISTRY.yaml"
    if not reg_path.is_file():
        return []
    try:
        payload = yaml.safe_load(reg_path.read_text(encoding="utf-8"))
    except Exception:
        return []
    if not isinstance(payload, dict):
        return []
    rows = payload.get("tools")
    if not isinstance(rows, list):
        return []

    out: list[dict[str, str]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        tool_id = str(row.get("tool_id", "")).strip()
        entrypoint = normalize_anchor_token(str(row.get("entrypoint", "")))
        if not tool_id or not entrypoint:
            continue
        out.append(
            {
                "tool_id": tool_id,
                "entrypoint": entrypoint,
                "owner": str(row.get("owner", "")).strip() or "unknown",
                "status": str(row.get("status", "")).strip() or "unknown",
                "domain": str(row.get("domain", "")).strip() or "unknown",
            }
        )
    return out


def load_tool_docs_structured_rows(instance_root: Path) -> dict[str, dict[str, Any]]:
    docs_path = instance_root / "runtime" / "TOOL_DOCS_STRUCTURED.yaml"
    if not docs_path.is_file():
        return {}
    try:
        payload = yaml.safe_load(docs_path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    if not isinstance(payload, dict):
        return {}

    rows = payload.get("tools")
    if not isinstance(rows, list):
        return {}

    out: dict[str, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        tool_id = str(row.get("tool_id", "")).strip()
        if not tool_id:
            continue
        out[tool_id] = row
    return out


def infer_toolbox_paths(tool_rows: list[dict[str, str]]) -> tuple[str, str]:
    script_dirs = {
        str(Path(row.get("entrypoint", "")).parent).strip()
        for row in tool_rows
        if row.get("entrypoint") and "/scripts/" in row.get("entrypoint", "")
    }
    if not script_dirs:
        return "tooling_governance/default/scripts", "tooling_governance/default"
    scripts_dir = sorted(script_dirs, key=len)[0]
    instance_dir = str(Path(scripts_dir).parent).strip() or "tooling_governance/default"
    return scripts_dir, instance_dir


def build_toolbox_profile(
    instance_root: Path,
    managed_skill: str,
    tool_rows: list[dict[str, str]],
) -> dict[str, Any]:
    docs_by_tool = load_tool_docs_structured_rows(instance_root)
    tools: dict[str, dict[str, Any]] = {}
    domains: dict[str, list[str]] = {}
    owners: dict[str, list[str]] = {}
    workflow_counter: Counter[str] = Counter()
    required_docs_counter: Counter[str] = Counter()
    command_samples: list[dict[str, str]] = []
    section_coverage = {"usage": 0, "modification": 0, "development": 0}

    for row in tool_rows:
        tool_id = row.get("tool_id", "").strip()
        if not tool_id:
            continue
        domain = row.get("domain", "unknown").strip() or "unknown"
        owner = row.get("owner", "unknown").strip() or "unknown"
        status = row.get("status", "unknown").strip() or "unknown"
        entrypoint = normalize_anchor_token(row.get("entrypoint", ""))

        tool_doc = _safe_dict(docs_by_tool.get(tool_id))
        usage = _safe_dict(tool_doc.get("usage"))
        modification = _safe_dict(tool_doc.get("modification"))
        development = _safe_dict(tool_doc.get("development"))

        command_examples = _ensure_str_list(usage.get("command_examples"))
        if command_examples:
            command_samples.append({"tool_id": tool_id, "command": command_examples[0]})
        for step in _ensure_str_list(modification.get("update_workflow")):
            workflow_counter[step] += 1
        for doc_path in _ensure_str_list(modification.get("required_docs")):
            required_docs_counter[doc_path] += 1

        if usage:
            section_coverage["usage"] += 1
        if modification:
            section_coverage["modification"] += 1
        if development:
            section_coverage["development"] += 1

        tools[tool_id] = {
            "tool_id": tool_id,
            "entrypoint": entrypoint,
            "domain": domain,
            "owner": owner,
            "status": status,
            "usage_summary": str(usage.get("summary", "")).strip(),
            "command_examples": command_examples,
            "inputs": _ensure_str_list(usage.get("inputs")),
            "outputs": _ensure_str_list(usage.get("outputs")),
            "script_anchor_refs": _ensure_str_list(usage.get("script_anchor_refs")),
            "doc_anchor_refs": _ensure_str_list(usage.get("doc_anchor_refs")),
            "workflow": _ensure_str_list(modification.get("update_workflow")),
            "required_docs": _ensure_str_list(modification.get("required_docs")),
            "sync_contract": _safe_dict(modification.get("sync_contract")),
            "notes": _ensure_str_list(modification.get("notes")),
            "development_owner": str(development.get("owner", "")).strip() or owner,
            "self_evolution_requirements": _ensure_str_list(development.get("self_evolution_requirements")),
            "records_count": len(_ensure_str_list(development.get("records"))),
        }

        domains.setdefault(domain, []).append(tool_id)
        owners.setdefault(owner, []).append(tool_id)

    for value in domains.values():
        value.sort()
    for value in owners.values():
        value.sort()

    scripts_dir, instance_dir = infer_toolbox_paths(tool_rows)
    return {
        "managed_skill": managed_skill,
        "tool_count": len(tools),
        "tool_ids": sorted(tools.keys()),
        "tools": tools,
        "domains": {k: domains[k] for k in sorted(domains.keys())},
        "owners": {k: owners[k] for k in sorted(owners.keys())},
        "workflow_steps_ranked": [name for name, _ in workflow_counter.most_common()],
        "required_docs_ranked": [name for name, _ in required_docs_counter.most_common()],
        "command_samples": command_samples[:20],
        "section_coverage": section_coverage,
        "toolbox_scripts_dir": scripts_dir,
        "toolbox_instance_dir": instance_dir,
    }


def resolve_tool_id(base_tool_id: str, registry_tool_ids: set[str]) -> str:
    if not registry_tool_ids:
        return base_tool_id
    if base_tool_id in registry_tool_ids:
        return base_tool_id

    if base_tool_id.startswith("tg_"):
        alt = base_tool_id[3:]
    else:
        alt = f"tg_{base_tool_id}"
    if alt in registry_tool_ids:
        return alt
    return ""
