#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from audit_orchestrator import audit_target
from audit_models import AuditPayload, DirectivePayload, RuntimeContractPayload
from tooling_contracts import directive_payload, runtime_contract_payload


Payload = RuntimeContractPayload | DirectivePayload | AuditPayload


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


def cmd_audit(args: argparse.Namespace) -> int:
    return emit(audit_target(Path(args.target_skill_root)), args.json)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="SkillsManager-Tooling-CheckUp toolbox")
    subparsers = parser.add_subparsers(dest="command", required=True)

    contract = subparsers.add_parser("contract")
    contract.add_argument("--json", action="store_true")
    contract.set_defaults(func=cmd_contract)

    directive = subparsers.add_parser("directive")
    directive.add_argument("--topic", required=True)
    directive.add_argument("--json", action="store_true")
    directive.set_defaults(func=cmd_directive)

    audit = subparsers.add_parser("audit")
    audit.add_argument("--target-skill-root", required=True)
    audit.add_argument("--json", action="store_true")
    audit.set_defaults(func=cmd_audit)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
