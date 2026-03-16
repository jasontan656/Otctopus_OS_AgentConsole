#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from creation_contracts import directive_payload, runtime_contract_payload
from profile_registry import DEFAULT_PROFILE
from scaffold_models import (
    DOC_TOPOLOGY_VALUES,
    TOOLING_SURFACE_VALUES,
    WORKFLOW_CONTROL_VALUES,
    DirectivePayload,
    ProfileCatalogPayload,
    RuntimeContractPayload,
    ScaffoldRequest,
    ScaffoldResultPayload,
)
from scaffold_orchestrator import build_profile, profile_catalog_payload, scaffold_skill


Payload = RuntimeContractPayload | DirectivePayload | ProfileCatalogPayload | ScaffoldResultPayload


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


def cmd_profile(args: argparse.Namespace) -> int:
    return emit(profile_catalog_payload(), args.json)


def cmd_scaffold(args: argparse.Namespace) -> int:
    profile = build_profile(args.doc_topology, args.tooling_surface, args.workflow_control)
    request = ScaffoldRequest(
        skill_name=args.skill_name,
        description=args.description,
        target_root=Path(args.target_root),
        profile=profile,
        overwrite=args.overwrite,
    )
    return emit(scaffold_skill(request), args.json)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="SkillsManager-Creation-Template toolbox")
    subparsers = parser.add_subparsers(dest="command", required=True)

    contract = subparsers.add_parser("contract")
    contract.add_argument("--json", action="store_true")
    contract.set_defaults(func=cmd_contract)

    directive = subparsers.add_parser("directive")
    directive.add_argument("--topic", required=True)
    directive.add_argument("--json", action="store_true")
    directive.set_defaults(func=cmd_directive)

    profile = subparsers.add_parser("profile")
    profile.add_argument("--json", action="store_true")
    profile.set_defaults(func=cmd_profile)

    scaffold = subparsers.add_parser("scaffold")
    scaffold.add_argument("--skill-name", required=True)
    scaffold.add_argument("--target-root", required=True)
    scaffold.add_argument("--description", default="Governed skill scaffold.")
    scaffold.add_argument("--doc-topology", choices=DOC_TOPOLOGY_VALUES, default=DEFAULT_PROFILE.doc_topology)
    scaffold.add_argument(
        "--tooling-surface",
        choices=TOOLING_SURFACE_VALUES,
        default=DEFAULT_PROFILE.tooling_surface,
    )
    scaffold.add_argument(
        "--workflow-control",
        choices=WORKFLOW_CONTROL_VALUES,
        default=DEFAULT_PROFILE.workflow_control,
    )
    scaffold.add_argument("--overwrite", action="store_true")
    scaffold.add_argument("--json", action="store_true")
    scaffold.set_defaults(func=cmd_scaffold)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
