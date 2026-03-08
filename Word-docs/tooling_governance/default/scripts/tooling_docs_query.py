#!/usr/bin/env python3
"""Query structured tooling docs by tool id and view."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import mstg_yaml as yaml


def load_yaml(path: Path) -> Any:
    if not path.is_file():
        raise FileNotFoundError(f"missing file: {path}")
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def find_tool_entry(payload: dict[str, Any], tool_id: str) -> dict[str, Any] | None:
    tools = payload.get("tools", [])
    if not isinstance(tools, list):
        return None
    for item in tools:
        if isinstance(item, dict) and str(item.get("tool_id", "")).strip() == tool_id:
            return item
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Query TOOL_DOCS_STRUCTURED.yaml")
    parser.add_argument("--instance-root", required=True)
    parser.add_argument("--tool-id", required=True)
    parser.add_argument("--view", choices=["full", "usage", "modification", "development"], default="full")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    instance_root = Path(args.instance_root).expanduser().resolve()
    docs_path = instance_root / "runtime" / "TOOL_DOCS_STRUCTURED.yaml"

    payload = load_yaml(docs_path)
    if not isinstance(payload, dict):
        raise RuntimeError("TOOL_DOCS_STRUCTURED.yaml must be YAML mapping")

    entry = find_tool_entry(payload, args.tool_id)
    if entry is None:
        result = {
            "status": "FAIL",
            "error": "TOOL_NOT_FOUND",
            "tool_id": args.tool_id,
            "docs_path": str(docs_path),
        }
        print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None))
        return 1

    if args.view == "full":
        data = entry
    else:
        data = entry.get(args.view, {})

    result = {
        "status": "PASS",
        "tool_id": args.tool_id,
        "view": args.view,
        "data": data,
        "source": str(docs_path),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
