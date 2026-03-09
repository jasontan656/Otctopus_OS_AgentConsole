#!/usr/bin/env python3
from __future__ import annotations

import argparse

from stage_contract_support import (
    get_stage_checklist,
    get_stage_command_contract,
    get_stage_doc_contract,
    get_stage_graph_contract,
)
from stage_runtime import emit_stage_payload
from toolbox_ops import (
    DEFAULT_DOCUMENT_ROOT,
    DEFAULT_WORKSPACE_ROOT,
    append_development_log,
    emit_contract,
    materialize_layout,
    sync_mother_doc_navigation,
    sync_mother_doc_status,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="2-Octupos-FullStack toolbox")
    subparsers = parser.add_subparsers(dest="command", required=True)

    materialize = subparsers.add_parser(
        "materialize-container-layout",
        help="create workspace and Mother_Doc directories for already-decided containers",
    )
    materialize.add_argument("--workspace-root", default=str(DEFAULT_WORKSPACE_ROOT), help="Octopus_OS workspace root")
    materialize.add_argument("--document-root", default=str(DEFAULT_DOCUMENT_ROOT), help="Mother_Doc root")
    materialize.add_argument("--container", action="append", default=[], help="container name; repeat for multiple containers")
    materialize.add_argument("--dry-run", action="store_true")
    materialize.add_argument("--json", action="store_true")
    materialize.set_defaults(func=materialize_layout)

    navigation = subparsers.add_parser(
        "sync-mother-doc-navigation",
        help="refresh recursive README.md and agents.md navigation files for Mother_Doc",
    )
    navigation.add_argument("--document-root", default=str(DEFAULT_DOCUMENT_ROOT), help="Mother_Doc root")
    navigation.add_argument("--dry-run", action="store_true")
    navigation.add_argument("--json", action="store_true")
    navigation.set_defaults(func=sync_mother_doc_navigation)

    status = subparsers.add_parser(
        "sync-mother-doc-status",
        help="update mechanical development-status blocks for Mother_Doc markdown files",
    )
    status.add_argument("--document-root", default=str(DEFAULT_DOCUMENT_ROOT), help="Mother_Doc root")
    status.add_argument("--stage", choices=("mother_doc", "implementation", "evidence"), required=True)
    status.add_argument("--path", action="append", default=[], help="relative Mother_Doc path; repeat for multiple files or directories")
    status.add_argument("--block-id", action="append", default=[], help="block id to write into the registry; repeat for multiple blocks")
    status.add_argument("--sync-status", default="pending_implementation", help="mechanical sync status string")
    status.add_argument("--requires-development", action=argparse.BooleanOptionalAction, default=True)
    status.add_argument("--dry-run", action="store_true")
    status.add_argument("--json", action="store_true")
    status.set_defaults(func=sync_mother_doc_status)

    implementation_log = subparsers.add_parser(
        "append-implementation-log",
        help="append an implementation batch log entry under Mother_Doc/common/development_logs",
    )
    implementation_log.add_argument("--document-root", default=str(DEFAULT_DOCUMENT_ROOT), help="Mother_Doc root")
    implementation_log.add_argument("--summary", required=True)
    implementation_log.add_argument("--doc-path", action="append", default=[])
    implementation_log.add_argument("--code-path", action="append", default=[])
    implementation_log.add_argument("--dry-run", action="store_true")
    implementation_log.add_argument("--json", action="store_true")
    implementation_log.set_defaults(func=lambda args: append_development_log(argparse.Namespace(**vars(args), kind="implementation")))

    deployment_log = subparsers.add_parser(
        "append-deployment-log",
        help="append a deployment checkpoint log entry under Mother_Doc/common/development_logs",
    )
    deployment_log.add_argument("--document-root", default=str(DEFAULT_DOCUMENT_ROOT), help="Mother_Doc root")
    deployment_log.add_argument("--summary", required=True)
    deployment_log.add_argument("--doc-path", action="append", default=[])
    deployment_log.add_argument("--code-path", action="append", default=[])
    deployment_log.add_argument("--dry-run", action="store_true")
    deployment_log.add_argument("--json", action="store_true")
    deployment_log.set_defaults(func=lambda args: append_development_log(argparse.Namespace(**vars(args), kind="deployment")))

    checklist = subparsers.add_parser(
        "stage-checklist",
        help="print the checklist for a specific stage",
    )
    checklist.add_argument("--stage", choices=("mother_doc", "implementation", "evidence"), required=True)
    checklist.add_argument("--json", action="store_true")
    checklist.set_defaults(func=lambda args: emit_contract(get_stage_checklist(args.stage), as_json=args.json))

    doc_contract = subparsers.add_parser(
        "stage-doc-contract",
        help="print the document-loading contract for a specific stage",
    )
    doc_contract.add_argument("--stage", choices=("mother_doc", "implementation", "evidence"), required=True)
    doc_contract.add_argument("--json", action="store_true")
    doc_contract.set_defaults(func=lambda args: emit_contract(get_stage_doc_contract(args.stage), as_json=args.json))

    command_contract = subparsers.add_parser(
        "stage-command-contract",
        help="print the command contract for a specific stage",
    )
    command_contract.add_argument("--stage", choices=("mother_doc", "implementation", "evidence"), required=True)
    command_contract.add_argument("--json", action="store_true")
    command_contract.set_defaults(func=lambda args: emit_contract(get_stage_command_contract(args.stage), as_json=args.json))

    graph_contract = subparsers.add_parser(
        "stage-graph-contract",
        help="print the graph contract for a specific stage",
    )
    graph_contract.add_argument("--stage", choices=("mother_doc", "implementation", "evidence"), required=True)
    graph_contract.add_argument("--json", action="store_true")
    graph_contract.set_defaults(func=lambda args: emit_contract(get_stage_graph_contract(args.stage), as_json=args.json))

    mother_doc = subparsers.add_parser(
        "mother-doc-stage",
        help="print scope and carry-forward requirements for the mother_doc stage",
    )
    mother_doc.add_argument("--json", action="store_true")
    mother_doc.set_defaults(func=lambda args: emit_stage_payload("mother_doc", as_json=args.json))

    implementation = subparsers.add_parser(
        "implementation-stage",
        help="print scope and carry-forward requirements for the implementation stage",
    )
    implementation.add_argument("--json", action="store_true")
    implementation.set_defaults(func=lambda args: emit_stage_payload("implementation", as_json=args.json))

    evidence = subparsers.add_parser(
        "evidence-stage",
        help="print scope and carry-forward requirements for the evidence stage",
    )
    evidence.add_argument("--json", action="store_true")
    evidence.set_defaults(func=lambda args: emit_stage_payload("evidence", as_json=args.json))
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
