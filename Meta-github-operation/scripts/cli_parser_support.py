from __future__ import annotations

import argparse


def build_parser(
    cmd_registry,
    cmd_status,
    cmd_remote_info,
    cmd_fetch,
    cmd_pull_rebase,
    cmd_commit,
    cmd_commit_and_push,
    cmd_push,
    cmd_push_contract,
    cmd_rollback_contract,
    cmd_rollback_paths,
    cmd_rollback_sync,
) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    registry = subparsers.add_parser("registry")
    registry.add_argument("--json", action="store_true")
    registry.set_defaults(func=cmd_registry)

    push_contract = subparsers.add_parser("push-contract")
    push_contract.add_argument("--json", action="store_true")
    push_contract.set_defaults(func=cmd_push_contract)

    rollback_contract = subparsers.add_parser("rollback-contract")
    rollback_contract.add_argument("--json", action="store_true")
    rollback_contract.set_defaults(func=cmd_rollback_contract)

    status = subparsers.add_parser("status")
    status.add_argument("--repo")
    status.add_argument("--repo-path")
    status.add_argument("--fetch", action="store_true")
    status.add_argument("--json", action="store_true")
    status.set_defaults(func=cmd_status)

    remote_info = subparsers.add_parser("remote-info")
    remote_info.add_argument("--repo")
    remote_info.add_argument("--repo-path")
    remote_info.add_argument("--json", action="store_true")
    remote_info.set_defaults(func=cmd_remote_info)

    fetch_parser = subparsers.add_parser("fetch")
    fetch_parser.add_argument("--repo")
    fetch_parser.add_argument("--repo-path")
    fetch_parser.add_argument("--remote", default="origin")
    fetch_parser.add_argument("--json", action="store_true")
    fetch_parser.set_defaults(func=cmd_fetch)

    pull_parser = subparsers.add_parser("pull-rebase")
    pull_parser.add_argument("--repo")
    pull_parser.add_argument("--repo-path")
    pull_parser.add_argument("--remote", default="origin")
    pull_parser.add_argument("--branch")
    pull_parser.add_argument("--json", action="store_true")
    pull_parser.set_defaults(func=cmd_pull_rebase)

    for name, func in {"commit": cmd_commit, "commit-and-push": cmd_commit_and_push}.items():
        sub = subparsers.add_parser(name)
        sub.add_argument("--repo")
        sub.add_argument("--repo-path")
        sub.add_argument("--message", required=True)
        sub.add_argument("--path", action="append", default=[])
        sub.add_argument("--claims-file")
        sub.add_argument("--use-latest-claims", action="store_true")
        sub.add_argument("--auto-scope", action="store_true")
        sub.add_argument("--all", action="store_true")
        sub.add_argument("--allow-empty", action="store_true")
        sub.add_argument("--remote", default="origin")
        sub.add_argument("--branch")
        sub.add_argument("--force-with-lease", action="store_true")
        sub.add_argument("--json", action="store_true")
        sub.set_defaults(func=func)

    push_parser = subparsers.add_parser("push")
    push_parser.add_argument("--repo")
    push_parser.add_argument("--repo-path")
    push_parser.add_argument("--remote", default="origin")
    push_parser.add_argument("--branch")
    push_parser.add_argument("--force-with-lease", action="store_true")
    push_parser.add_argument("--json", action="store_true")
    push_parser.set_defaults(func=cmd_push)

    rollback = subparsers.add_parser("rollback-paths")
    rollback.add_argument("--repo")
    rollback.add_argument("--repo-path")
    rollback.add_argument("--to-ref", required=True)
    rollback.add_argument("--path", action="append", required=True)
    rollback.add_argument("--json", action="store_true")
    rollback.set_defaults(func=cmd_rollback_paths)

    rollback_sync = subparsers.add_parser("rollback-sync")
    rollback_sync.add_argument("--repo")
    rollback_sync.add_argument("--repo-path")
    rollback_sync.add_argument("--to-ref", required=True)
    rollback_sync.add_argument("--path", action="append", default=[])
    rollback_sync.add_argument("--all", action="store_true")
    rollback_sync.add_argument("--json", action="store_true")
    rollback_sync.set_defaults(func=cmd_rollback_sync)
    return parser
