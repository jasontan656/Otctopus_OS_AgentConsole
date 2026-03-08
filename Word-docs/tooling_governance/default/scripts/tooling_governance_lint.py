#!/usr/bin/env python3
"""Lint tooling governance instance structure and structured docs sync."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import mstg_yaml as yaml

REQUIRED_DOCS = [
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

REQUIRED_RUNTIME = [
    "TOOL_REGISTRY.yaml",
    "TOOL_DOCS_STRUCTURED.yaml",
    "TOOL_CHANGE_LEDGER.jsonl",
    "TOOLING_GOVERNANCE_STATE.yaml",
    "TOOLBOX_INJECTION_MANIFEST.yaml",
]


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def normalize_tool_ids_from_registry(payload: dict[str, Any]) -> list[str]:
    tools = payload.get("tools", [])
    if not isinstance(tools, list):
        return []
    ids: list[str] = []
    for row in tools:
        if isinstance(row, dict):
            tid = str(row.get("tool_id", "")).strip()
            if tid:
                ids.append(tid)
    return sorted(set(ids))


def normalize_tool_ids_from_docs(payload: dict[str, Any]) -> list[str]:
    tools = payload.get("tools", [])
    if not isinstance(tools, list):
        return []
    ids: list[str] = []
    for row in tools:
        if isinstance(row, dict):
            tid = str(row.get("tool_id", "")).strip()
            if tid:
                ids.append(tid)
    return sorted(set(ids))


def validate_docs_sections(payload: dict[str, Any], expected_ids: list[str]) -> list[dict[str, str]]:
    problems: list[dict[str, str]] = []
    tools = payload.get("tools", [])
    by_id: dict[str, dict[str, Any]] = {}
    for row in tools if isinstance(tools, list) else []:
        if isinstance(row, dict):
            tid = str(row.get("tool_id", "")).strip()
            if tid:
                by_id[tid] = row

    for tid in expected_ids:
        row = by_id.get(tid)
        if row is None:
            problems.append({"tool_id": tid, "issue": "missing_in_structured_docs"})
            continue
        usage = row.get("usage")
        mod = row.get("modification")
        dev = row.get("development")
        if not isinstance(usage, dict):
            problems.append({"tool_id": tid, "issue": "usage_section_missing"})
        if not isinstance(mod, dict):
            problems.append({"tool_id": tid, "issue": "modification_section_missing"})
        if not isinstance(dev, dict):
            problems.append({"tool_id": tid, "issue": "development_section_missing"})
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint tooling governance instance")
    parser.add_argument("--instance-root", required=True, help="Path to one governance instance")
    args = parser.parse_args()

    root = Path(args.instance_root).expanduser().resolve()
    docs_dir = root / "docs"
    runtime_dir = root / "runtime"
    assets_schema_dir = root / "assets" / "schemas"
    l1_chain_dir = docs_dir / "L1" / "chains"
    l2_chain_dir = docs_dir / "L2" / "chains"

    missing_docs = [name for name in REQUIRED_DOCS if not (docs_dir / name).exists()]
    missing_runtime = [name for name in REQUIRED_RUNTIME if not (runtime_dir / name).exists()]
    l1_chain_docs = sorted([str(p.relative_to(docs_dir)).replace("\\", "/") for p in l1_chain_dir.glob("*.md") if p.is_file()]) if l1_chain_dir.is_dir() else []
    l2_chain_docs = (
        sorted([str(p.relative_to(docs_dir)).replace("\\", "/") for p in l2_chain_dir.glob("*/README.md") if p.is_file()])
        if l2_chain_dir.is_dir()
        else []
    )
    chain_doc_missing = []
    if not l1_chain_docs:
        chain_doc_missing.append("L1/chains/*.md")
    if not l2_chain_docs:
        chain_doc_missing.append("L2/chains/*/README.md")

    checks = {
        "instance_root_exists": root.exists(),
        "docs_dir_exists": docs_dir.exists(),
        "runtime_dir_exists": runtime_dir.exists(),
        "assets_schema_dir_exists": assets_schema_dir.exists(),
        "l1_chain_dir_exists": l1_chain_dir.is_dir(),
        "l2_chain_dir_exists": l2_chain_dir.is_dir(),
    }

    structured_sync = {
        "registry_tool_count": 0,
        "structured_tool_count": 0,
        "registry_only": [],
        "structured_only": [],
        "section_problems": [],
    }

    if not missing_runtime:
        registry_payload = load_yaml(runtime_dir / "TOOL_REGISTRY.yaml")
        structured_payload = load_yaml(runtime_dir / "TOOL_DOCS_STRUCTURED.yaml")
        if not isinstance(registry_payload, dict):
            structured_sync["section_problems"].append({"tool_id": "*", "issue": "tool_registry_not_mapping"})
            registry_ids = []
        else:
            registry_ids = normalize_tool_ids_from_registry(registry_payload)

        if not isinstance(structured_payload, dict):
            structured_sync["section_problems"].append({"tool_id": "*", "issue": "tool_docs_structured_not_mapping"})
            structured_ids = []
        else:
            structured_ids = normalize_tool_ids_from_docs(structured_payload)

        structured_sync["registry_tool_count"] = len(registry_ids)
        structured_sync["structured_tool_count"] = len(structured_ids)
        structured_sync["registry_only"] = sorted(set(registry_ids) - set(structured_ids))
        structured_sync["structured_only"] = sorted(set(structured_ids) - set(registry_ids))
        structured_sync["section_problems"] = validate_docs_sections(structured_payload if isinstance(structured_payload, dict) else {}, registry_ids)

    has_sync_issues = bool(structured_sync["registry_only"] or structured_sync["structured_only"] or structured_sync["section_problems"])
    status = (
        "PASS"
        if all(checks.values()) and not missing_docs and not missing_runtime and not has_sync_issues and not chain_doc_missing
        else "FAIL"
    )

    result = {
        "status": status,
        "scope": "tooling_governance_instance",
        "instance_root": str(root),
        "checks": checks,
        "missing_docs": missing_docs,
        "missing_runtime": missing_runtime,
        "required_docs_count": len(REQUIRED_DOCS),
        "required_runtime_count": len(REQUIRED_RUNTIME),
        "chain_docs": {
            "l1_chain_docs": l1_chain_docs,
            "l2_chain_docs": l2_chain_docs,
            "missing_patterns": chain_doc_missing,
        },
        "structured_sync": structured_sync,
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
