#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from docstructure_runtime import build_anchor_graph
from docstructure_runtime import inspect_target
from docstructure_runtime import lint_anchor_graph
from docstructure_runtime import lint_docstructure
from docstructure_runtime import lint_reading_chain
from docstructure_runtime import lint_root_shape
from docstructure_runtime import runtime_contract_payload


def _print_payload(payload: dict[str, object], as_json: bool) -> int:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    print(payload.get("status", "ok"))
    return 0


def _add_target_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--target", required=True, help="Absolute or relative target skill root")


def main() -> int:
    parser = argparse.ArgumentParser(description="SkillsManager-Doc-Structure Python toolbox")
    subparsers = parser.add_subparsers(dest="command", required=True)

    contract_parser = subparsers.add_parser("contract", help="Read the runtime contract")
    contract_parser.add_argument("--json", action="store_true")

    runtime_contract_parser = subparsers.add_parser("runtime-contract", help="Read the runtime contract")
    runtime_contract_parser.add_argument("--json", action="store_true")

    inspect_parser = subparsers.add_parser("inspect-target", help="Inspect target skill shape")
    _add_target_argument(inspect_parser)
    inspect_parser.add_argument("--json", action="store_true")

    root_shape_parser = subparsers.add_parser("lint-root-shape", help="Lint target root shape")
    _add_target_argument(root_shape_parser)
    root_shape_parser.add_argument("--json", action="store_true")

    chain_parser = subparsers.add_parser("lint-reading-chain", help="Lint target reading chain")
    _add_target_argument(chain_parser)
    chain_parser.add_argument("--json", action="store_true")

    graph_parser = subparsers.add_parser("build-anchor-graph", help="Build target anchor graph")
    _add_target_argument(graph_parser)
    graph_parser.add_argument("--json", action="store_true")

    anchor_lint_parser = subparsers.add_parser("lint-anchor-graph", help="Lint target anchor graph")
    _add_target_argument(anchor_lint_parser)
    anchor_lint_parser.add_argument("--json", action="store_true")

    doc_lint_parser = subparsers.add_parser("lint-docstructure", help="Lint target skill docstructure")
    _add_target_argument(doc_lint_parser)
    doc_lint_parser.add_argument("--json", action="store_true")

    args = parser.parse_args()

    if args.command in {"contract", "runtime-contract"}:
        return _print_payload(runtime_contract_payload(), args.json)

    target_root = Path(args.target).expanduser().resolve()

    if args.command == "inspect-target":
        return _print_payload(inspect_target(target_root), args.json)
    if args.command == "lint-root-shape":
        return _print_payload(lint_root_shape(target_root), args.json)
    if args.command == "lint-reading-chain":
        return _print_payload(lint_reading_chain(target_root), args.json)
    if args.command == "build-anchor-graph":
        return _print_payload(build_anchor_graph(target_root), args.json)
    if args.command == "lint-anchor-graph":
        return _print_payload(lint_anchor_graph(target_root), args.json)
    if args.command == "lint-docstructure":
        return _print_payload(lint_docstructure(target_root), args.json)

    raise ValueError(f"unsupported command: {args.command}")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2))
        raise SystemExit(1)
