#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from audit_orchestrator import compile_target_context, inspect_target, lint_target
from doc_models import CompilePayload, DirectivePayload, InspectPayload, LintPayload, RuntimeContractPayload
from doc_contracts import directive_payload, runtime_contract_payload


Payload = RuntimeContractPayload | DirectivePayload | InspectPayload | LintPayload | CompilePayload


def emit(payload: Payload, as_json: bool) -> int:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    print(payload.get("status", "ok"))
    return 0


def cmd_contract(args: argparse.Namespace) -> int:
    return emit(runtime_contract_payload(), args.json)


def cmd_directive(args: argparse.Namespace) -> int:
    return emit(directive_payload(args.topic), args.json)


def cmd_inspect(args: argparse.Namespace) -> int:
    return emit(inspect_target(Path(args.target)), args.json)


def cmd_lint(args: argparse.Namespace) -> int:
    return emit(lint_target(Path(args.target)), args.json)


def cmd_compile_context(args: argparse.Namespace) -> int:
    selection = [item.strip() for item in args.selection.split(",") if item.strip()]
    return emit(compile_target_context(Path(args.target), args.entry, selection), args.json)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="SkillsManager-Doc-Structure toolbox")
    subparsers = parser.add_subparsers(dest="command", required=True)

    contract = subparsers.add_parser("contract")
    contract.add_argument("--json", action="store_true")
    contract.set_defaults(func=cmd_contract)

    directive = subparsers.add_parser("directive")
    directive.add_argument("--topic", required=True)
    directive.add_argument("--json", action="store_true")
    directive.set_defaults(func=cmd_directive)

    inspect = subparsers.add_parser("inspect")
    inspect.add_argument("--target", required=True)
    inspect.add_argument("--json", action="store_true")
    inspect.set_defaults(func=cmd_inspect)

    lint = subparsers.add_parser("lint")
    lint.add_argument("--target", required=True)
    lint.add_argument("--json", action="store_true")
    lint.set_defaults(func=cmd_lint)

    compile_context = subparsers.add_parser("compile-context")
    compile_context.add_argument("--target", required=True)
    compile_context.add_argument("--entry")
    compile_context.add_argument("--selection", default="")
    compile_context.add_argument("--json", action="store_true")
    compile_context.set_defaults(func=cmd_compile_context)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
