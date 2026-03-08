#!/usr/bin/env python3
"""Append structured tool change event to governance ledger with impact mapping."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any

import mstg_yaml as yaml


def now_utc() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def update_state_file(state_file: Path, last_event_id: str, changed_tool_id: str, updated_at: str) -> None:
    state: dict[str, Any] = {}
    if state_file.is_file():
        parsed = yaml.safe_load(state_file.read_text(encoding="utf-8"))
        if isinstance(parsed, dict):
            state = parsed
    state["governance_status"] = "active"
    state["last_event_id"] = last_event_id
    state["last_changed_tool_id"] = changed_tool_id
    state["last_updated_at_utc"] = updated_at
    state_file.write_text(yaml.safe_dump(state, allow_unicode=True, sort_keys=False), encoding="utf-8")


def layer_docs_for_paths(paths: list[str]) -> list[str]:
    docs: set[str] = set()
    for p in paths:
        s = p.replace("\\", "/")
        if s.startswith("scripts/") and "lint" in s:
            docs.update(["docs/L9/README.md", "docs/L12/README.md", "docs/L13/README.md"])
        elif s.startswith("scripts/") and "writeback" in s:
            docs.update(["docs/L6/README.md", "docs/L8/README.md", "docs/L10/README.md"])
        elif s.startswith("runtime/TOOL_REGISTRY"):
            docs.update(["docs/L1/README.md", "docs/L1/chains", "docs/L2/README.md", "docs/L2/chains"])
        elif s.startswith("runtime/TOOL_DOCS_STRUCTURED"):
            docs.update(["docs/L0/README.md", "docs/L5/README.md", "docs/L10/README.md"])
        else:
            docs.update(["docs/L0/README.md", "docs/L13/README.md"])
    return sorted(docs)


def main() -> int:
    parser = argparse.ArgumentParser(description="Append tool change record")
    parser.add_argument("--instance-root", required=True)
    parser.add_argument("--tool-id", required=True)
    parser.add_argument("--change-type", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--changed-path", action="append", default=[])
    parser.add_argument("--docs-updated", action="append", default=[])
    parser.add_argument("--artifacts-updated", action="append", default=[])
    args = parser.parse_args()

    root = Path(args.instance_root).expanduser().resolve()
    runtime_dir = root / "runtime"
    runtime_dir.mkdir(parents=True, exist_ok=True)

    ledger_file = runtime_dir / "TOOL_CHANGE_LEDGER.jsonl"
    state_file = runtime_dir / "TOOLING_GOVERNANCE_STATE.yaml"

    timestamp = now_utc()
    event_id = f"evt-{dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"

    impact_docs = args.docs_updated if args.docs_updated else layer_docs_for_paths(args.changed_path)

    payload = {
        "event_id": event_id,
        "timestamp_utc": timestamp,
        "tool_id": args.tool_id,
        "change_type": args.change_type,
        "summary": args.summary,
        "changed_paths": args.changed_path,
        "docs_updated": impact_docs,
        "artifacts_updated": args.artifacts_updated,
    }

    with ledger_file.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, ensure_ascii=False) + "\n")

    update_state_file(state_file, event_id, args.tool_id, timestamp)

    print(json.dumps({"status": "PASS", "event": payload}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
