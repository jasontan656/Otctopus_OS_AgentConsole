#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from os_graph_core import ENGINE_COMMANDS, emit_subprocess, engine_run, status_payload, sync_doc_bindings, sync_evidence


def _emit(payload: dict[str, object], *, as_json: bool) -> int:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for key, value in payload.items():
            print(f"{key}: {value}")
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="OS_graph evidence CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    status = subparsers.add_parser("status", help="show OS_graph runtime and bridge-engine readiness")
    status.add_argument("--json", action="store_true")
    status.set_defaults(func=lambda args: _emit(status_payload(), as_json=args.json))

    sync_docs = subparsers.add_parser("sync-doc-bindings", help="index Mother_Doc/docs into document nodes, edges, and frontend layer views")
    sync_docs.add_argument("--json", action="store_true")
    sync_docs.set_defaults(func=lambda args: _emit(sync_doc_bindings(), as_json=args.json))

    sync_evidence_parser = subparsers.add_parser("sync-evidence", help="index development logs and lifecycle states into evidence-side runtime assets")
    sync_evidence_parser.add_argument("--json", action="store_true")
    sync_evidence_parser.set_defaults(func=lambda args: _emit(sync_evidence(), as_json=args.json))

    for command in sorted(ENGINE_COMMANDS):
        engine = subparsers.add_parser(command, help=f"bridge {command} to the current OS_graph engine")
        engine.add_argument("command_args", nargs="*")
        engine.set_defaults(func=lambda args, command_name=command: emit_subprocess(engine_run([command_name, *args.command_args], cwd=Path.cwd(), capture_output=True)))

    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
