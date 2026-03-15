#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from docstructure_runtime import compile_reading_chain
from docstructure_runtime import inspect_target
from docstructure_runtime import lint_docstructure
from docstructure_runtime import lint_reading_chain
from docstructure_runtime import lint_root_shape
from docstructure_runtime import runtime_contract_payload

SKILL_ROOT = Path(__file__).resolve().parents[1]


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

    for name in ("contract", "runtime-contract"):
        sub = subparsers.add_parser(name, help="Read the runtime contract")
        sub.add_argument("--json", action="store_true")

    inspect_parser = subparsers.add_parser("inspect-target", help="Inspect target skill shape")
    _add_target_argument(inspect_parser)
    inspect_parser.add_argument("--json", action="store_true")

    root_shape_parser = subparsers.add_parser("lint-root-shape", help="Lint target root shape")
    _add_target_argument(root_shape_parser)
    root_shape_parser.add_argument("--json", action="store_true")

    chain_parser = subparsers.add_parser("lint-reading-chain", help="Lint target reading chain")
    _add_target_argument(chain_parser)
    chain_parser.add_argument("--json", action="store_true")

    compile_parser = subparsers.add_parser("compile-reading-chain", help="Compile a full reading-chain context")
    _add_target_argument(compile_parser)
    compile_parser.add_argument("--entry", required=True, help="Top-level entry key declared under SKILL.md section 2")
    compile_parser.add_argument(
        "--selection",
        default="",
        help="Comma-separated branch keys used when the chain hits a branch node",
    )
    compile_parser.add_argument("--json", action="store_true")

    for name in ("read-path-context", "read-contract-context"):
        self_compile_parser = subparsers.add_parser(name, help="Compile this skill's own reading chain into one contract context")
        self_compile_parser.add_argument("--entry", required=True, help="Top-level entry key declared under SKILL.md section 2")
        self_compile_parser.add_argument("--selection", default="", help="Comma-separated branch keys used when the chain hits a branch node")
        self_compile_parser.add_argument("--json", action="store_true")

    doc_lint_parser = subparsers.add_parser("lint-docstructure", help="Lint target skill docstructure")
    _add_target_argument(doc_lint_parser)
    doc_lint_parser.add_argument("--json", action="store_true")

    args = parser.parse_args()

    if args.command in {"contract", "runtime-contract"}:
        return _print_payload(runtime_contract_payload(), args.json)

    if args.command == "inspect-target":
        target_root = Path(args.target).expanduser().resolve()
        return _print_payload(inspect_target(target_root), args.json)
    if args.command == "lint-root-shape":
        target_root = Path(args.target).expanduser().resolve()
        return _print_payload(lint_root_shape(target_root), args.json)
    if args.command == "lint-reading-chain":
        target_root = Path(args.target).expanduser().resolve()
        return _print_payload(lint_reading_chain(target_root), args.json)
    if args.command == "compile-reading-chain":
        target_root = Path(args.target).expanduser().resolve()
        selection = [item.strip() for item in args.selection.split(",") if item.strip()]
        return _print_payload(compile_reading_chain(target_root, args.entry, selection), args.json)
    if args.command in {"read-path-context", "read-contract-context"}:
        selection = [item.strip() for item in args.selection.split(",") if item.strip()]
        return _print_payload(compile_reading_chain(SKILL_ROOT, args.entry, selection), args.json)
    if args.command == "lint-docstructure":
        target_root = Path(args.target).expanduser().resolve()
        return _print_payload(lint_docstructure(target_root), args.json)

    raise ValueError(f"unsupported command: {args.command}")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2))
        raise SystemExit(1)
