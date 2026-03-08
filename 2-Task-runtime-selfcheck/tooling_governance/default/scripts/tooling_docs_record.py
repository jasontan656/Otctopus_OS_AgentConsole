#!/usr/bin/env python3
"""Append structured records into TOOL_DOCS_STRUCTURED.yaml."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any

import mstg_yaml as yaml


def now_utc() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_yaml(path: Path) -> Any:
    if not path.is_file():
        return None
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def save_yaml(path: Path, payload: Any) -> None:
    path.write_text(yaml.safe_dump(payload, allow_unicode=True, sort_keys=False), encoding="utf-8")


def ensure_payload(payload: Any, managed_skill: str) -> dict[str, Any]:
    if not isinstance(payload, dict):
        payload = {}
    payload.setdefault("schema_version", "mstg_tool_docs_structured_v1")
    payload.setdefault("managed_skill", managed_skill)
    payload.setdefault("tools", [])
    if not isinstance(payload.get("tools"), list):
        payload["tools"] = []
    return payload


def ensure_tool_entry(payload: dict[str, Any], tool_id: str) -> dict[str, Any]:
    for item in payload["tools"]:
        if isinstance(item, dict) and str(item.get("tool_id", "")).strip() == tool_id:
            return item
    created = {
        "tool_id": tool_id,
        "usage": {
            "summary": "replace_me",
            "command_examples": [],
            "inputs": [],
            "outputs": [],
        },
        "modification": {
            "update_workflow": [],
            "required_docs": [],
            "notes": [],
        },
        "development": {
            "owner": "ai_maintained",
            "records": [],
        },
    }
    payload["tools"].append(created)
    return created


def append_record(entry: dict[str, Any], record_type: str, record: dict[str, Any]) -> None:
    if record_type == "development":
        section = entry.setdefault("development", {})
        rows = section.setdefault("records", [])
        if not isinstance(rows, list):
            rows = []
            section["records"] = rows
        rows.append(record)
        return

    section = entry.setdefault("modification", {})
    rows = section.setdefault("notes", [])
    if not isinstance(rows, list):
        rows = []
        section["notes"] = rows
    rows.append(record)


def main() -> int:
    parser = argparse.ArgumentParser(description="Append records into TOOL_DOCS_STRUCTURED.yaml")
    parser.add_argument("--instance-root", required=True)
    parser.add_argument("--tool-id", required=True)
    parser.add_argument("--record-type", choices=["development", "modification"], required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--author", default="ai_maintained")
    parser.add_argument("--evidence", action="append", default=[])
    args = parser.parse_args()

    instance_root = Path(args.instance_root).expanduser().resolve()
    runtime_dir = instance_root / "runtime"
    runtime_dir.mkdir(parents=True, exist_ok=True)

    registry_path = runtime_dir / "TOOL_REGISTRY.yaml"
    docs_path = runtime_dir / "TOOL_DOCS_STRUCTURED.yaml"
    state_path = runtime_dir / "TOOLING_GOVERNANCE_STATE.yaml"

    managed_skill = "unknown_skill"
    reg_payload = load_yaml(registry_path)
    if isinstance(reg_payload, dict):
        managed_skill = str(reg_payload.get("managed_skill", managed_skill))

    docs_payload = ensure_payload(load_yaml(docs_path), managed_skill)
    entry = ensure_tool_entry(docs_payload, args.tool_id)

    record = {
        "timestamp_utc": now_utc(),
        "author": args.author,
        "summary": args.summary,
        "evidence": args.evidence,
    }
    append_record(entry, args.record_type, record)
    save_yaml(docs_path, docs_payload)

    state_payload = load_yaml(state_path)
    if not isinstance(state_payload, dict):
        state_payload = {}
    state_payload["governance_status"] = "active"
    state_payload["last_updated_at_utc"] = record["timestamp_utc"]
    state_payload["last_changed_tool_id"] = args.tool_id
    save_yaml(state_path, state_payload)

    result = {
        "status": "PASS",
        "tool_id": args.tool_id,
        "record_type": args.record_type,
        "record": record,
        "docs_path": str(docs_path),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
