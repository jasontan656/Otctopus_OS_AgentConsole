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
    mother_doc_agents_target_contract,
)
from cli_parser_blocks import (
    register_development_log_parsers,
    register_skill_runtime_parsers,
    register_stage_contract_parsers,
    register_stage_summary_parsers,
)
from toolbox_ops import (
    DEFAULT_DOCUMENT_ROOT,
    DEFAULT_WORKSPACE_ROOT,
    materialize_layout,
    sync_mother_doc_navigation,
    sync_mother_doc_status,
    sync_mother_doc_status_from_git,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="2-Octupos-FullStack toolbox")
    subparsers = parser.add_subparsers(dest="command", required=True)

    register_skill_runtime_parsers(subparsers)

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
        help="refresh recursive README.md and same-name scope markdown files for Mother_Doc while removing legacy AGENTS.md in docs",
    )
    navigation.add_argument("--document-root", default=str(DEFAULT_DOCUMENT_ROOT), help="Mother_Doc root")
    navigation.add_argument("--dry-run", action="store_true")
    navigation.add_argument("--json", action="store_true")
    navigation.set_defaults(func=sync_mother_doc_navigation)

    agents_contract = subparsers.add_parser(
        "mother-doc-agents-contract",
        help="print the runtime contract for the root-only Mother_Doc AGENTS manager branch",
    )
    agents_contract.add_argument("--skill-root", default=None, help="override skill root")
    agents_contract.add_argument("--json", action="store_true")
    agents_contract.set_defaults(func=mother_doc_agents_contract)

    agents_directive = subparsers.add_parser(
        "mother-doc-agents-directive",
        help="print the stage directive for the root-only Mother_Doc AGENTS manager branch",
    )
    agents_directive.add_argument("--skill-root", default=None, help="override skill root")
    agents_directive.add_argument("--stage", choices=("scan", "collect", "push"), required=True)
    agents_directive.add_argument("--json", action="store_true")
    agents_directive.set_defaults(func=mother_doc_agents_directive)

    agents_registry = subparsers.add_parser(
        "mother-doc-agents-registry",
        help="print the collected registry for the managed Octopus_OS root AGENTS target",
    )
    agents_registry.add_argument("--skill-root", default=None, help="override skill root")
    agents_registry.add_argument("--json", action="store_true")
    agents_registry.set_defaults(func=mother_doc_agents_registry)

    agents_target_contract = subparsers.add_parser(
        "mother-doc-agents-target-contract",
        help="print the runtime contract for the managed Octopus_OS root AGENTS target",
    )
    agents_target_contract.add_argument("--skill-root", default=None, help="override skill root")
    agents_target_contract.add_argument("--relative-path", required=True)
    agents_target_contract.add_argument("--file-kind", choices=("agents",), required=True)
    agents_target_contract.add_argument("--json", action="store_true")
    agents_target_contract.set_defaults(func=mother_doc_agents_target_contract)

    agents_scan = subparsers.add_parser(
        "mother-doc-agents-scan",
        help="scan the single managed Octopus_OS root AGENTS target and detect forbidden extra AGENTS.md files",
    )
    agents_scan.add_argument("--skill-root", default=None, help="override skill root")
    agents_scan.add_argument("--document-root", default=str(DEFAULT_DOCUMENT_ROOT), help="Mother_Doc docs root")
    agents_scan.add_argument("--json", action="store_true")
    agents_scan.set_defaults(func=mother_doc_agents_scan)

    agents_collect = subparsers.add_parser(
        "mother-doc-agents-collect",
        help="collect the Octopus_OS root AGENTS target back into the skill-side managed human/machine pair",
    )
    agents_collect.add_argument("--skill-root", default=None, help="override skill root")
    agents_collect.add_argument("--json", action="store_true")
    agents_collect.set_defaults(func=mother_doc_agents_collect)

    agents_push = subparsers.add_parser(
        "mother-doc-agents-push",
        help="push the managed root AGENTS payload back to Octopus_OS and delete forbidden extra AGENTS.md files",
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

    register_development_log_parsers(subparsers, str(DEFAULT_DOCUMENT_ROOT))
    register_stage_contract_parsers(subparsers)
    register_stage_summary_parsers(subparsers)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
