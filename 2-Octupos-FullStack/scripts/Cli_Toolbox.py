#!/usr/bin/env python3
from __future__ import annotations
import argparse
from agents_branch_ops import (
    mother_doc_agents_collect,
    mother_doc_agents_contract,
    mother_doc_agents_directive,
    mother_doc_agents_push,
    mother_doc_agents_registry,
    mother_doc_agents_scan,
)
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
    sync_mother_doc_status_from_git,
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
        help="refresh recursive README.md and AGENTS.md navigation files for Mother_Doc",
    )
    navigation.add_argument("--document-root", default=str(DEFAULT_DOCUMENT_ROOT), help="Mother_Doc root")
    navigation.add_argument("--dry-run", action="store_true")
    navigation.add_argument("--json", action="store_true")
    navigation.set_defaults(func=sync_mother_doc_navigation)

    agents_contract = subparsers.add_parser(
        "mother-doc-agents-contract",
        help="print the runtime contract for the Mother_Doc AGENTS/README manager branch",
    )
    agents_contract.add_argument("--skill-root", default=None, help="override skill root")
    agents_contract.add_argument("--json", action="store_true")
    agents_contract.set_defaults(func=mother_doc_agents_contract)

    agents_directive = subparsers.add_parser(
        "mother-doc-agents-directive",
        help="print the stage directive for the Mother_Doc AGENTS/README manager branch",
    )
    agents_directive.add_argument("--skill-root", default=None, help="override skill root")
    agents_directive.add_argument("--stage", choices=("scan", "collect", "push"), required=True)
    agents_directive.add_argument("--json", action="store_true")
    agents_directive.set_defaults(func=mother_doc_agents_directive)

    agents_registry = subparsers.add_parser(
        "mother-doc-agents-registry",
        help="print the collected registry for managed Mother_Doc AGENTS/README files",
    )
    agents_registry.add_argument("--skill-root", default=None, help="override skill root")
    agents_registry.add_argument("--json", action="store_true")
    agents_registry.set_defaults(func=mother_doc_agents_registry)

    agents_scan = subparsers.add_parser(
        "mother-doc-agents-scan",
        help="scan managed AGENTS/README scopes across Octopus_OS root, container roots, and Mother_Doc/docs",
    )
    agents_scan.add_argument("--skill-root", default=None, help="override skill root")
    agents_scan.add_argument("--document-root", default=str(DEFAULT_DOCUMENT_ROOT), help="Mother_Doc docs root")
    agents_scan.add_argument("--json", action="store_true")
    agents_scan.set_defaults(func=mother_doc_agents_scan)

    agents_collect = subparsers.add_parser(
        "mother-doc-agents-collect",
        help="collect current managed AGENTS/README files back into the skill-side registry",
    )
    agents_collect.add_argument("--skill-root", default=None, help="override skill root")
    agents_collect.add_argument("--json", action="store_true")
    agents_collect.set_defaults(func=mother_doc_agents_collect)

    agents_push = subparsers.add_parser(
        "mother-doc-agents-push",
        help="push the current AGENTS/README template tree back through Octopus_OS root, container roots, and Mother_Doc/docs",
    )
    agents_push.add_argument("--skill-root", default=None, help="override skill root")
    agents_push.add_argument("--document-root", default=str(DEFAULT_DOCUMENT_ROOT), help="Mother_Doc docs root")
    agents_push.add_argument("--dry-run", action="store_true")
    agents_push.add_argument("--json", action="store_true")
    agents_push.set_defaults(func=mother_doc_agents_push)

    status = subparsers.add_parser(
        "sync-mother-doc-status",
        help="update mechanical development-status blocks for Mother_Doc markdown files",
    )
    status.add_argument("--document-root", default=str(DEFAULT_DOCUMENT_ROOT), help="Mother_Doc root")
    status.add_argument("--stage", choices=("mother_doc", "implementation", "evidence"), required=True)
    status.add_argument("--path", action="append", default=[], help="relative Mother_Doc path; repeat for multiple files or directories")
    status.add_argument("--block-id", action="append", default=[], help="block id to write into the registry; repeat for multiple blocks")
    status.add_argument("--lifecycle-state", choices=("modified", "developed", "null"), required=True, help="mechanical lifecycle state")
    status.add_argument("--dry-run", action="store_true")
    status.add_argument("--json", action="store_true")
    status.set_defaults(func=sync_mother_doc_status)

    status_from_git = subparsers.add_parser(
        "sync-mother-doc-status-from-git",
        help="derive Mother_Doc lifecycle states from local git-backed diff plus existing state carry-forward",
    )
    status_from_git.add_argument("--repo-root", default=str(DEFAULT_WORKSPACE_ROOT), help="Octopus_OS repo root")
    status_from_git.add_argument("--document-root", default=str(DEFAULT_DOCUMENT_ROOT), help="Mother_Doc root")
    status_from_git.add_argument("--stage", choices=("mother_doc",), default="mother_doc")
    status_from_git.add_argument("--path", action="append", default=[], help="relative Mother_Doc path; repeat for multiple files or directories")
    status_from_git.add_argument("--block-id", action="append", default=[], help="block id to write into the registry; repeat for multiple blocks")
    status_from_git.add_argument("--dry-run", action="store_true")
    status_from_git.add_argument("--json", action="store_true")
    status_from_git.set_defaults(func=sync_mother_doc_status_from_git)

    implementation_log = subparsers.add_parser(
        "append-implementation-log",
        help="append an evidence-stage implementation batch log entry under Mother_Doc/common/development_logs",
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
        help="append an evidence-stage deployment checkpoint log entry under Mother_Doc/common/development_logs",
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
