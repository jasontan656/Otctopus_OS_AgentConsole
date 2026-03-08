#!/usr/bin/env python3
from __future__ import annotations

import json

from cli_parser_support import build_parser
from git_cli_support import (
    commit,
    fetch,
    pull_rebase,
    push,
    remote_urls,
    repo_status_payload,
    resolve_commit_scope,
    rollback_paths,
    stage_paths,
)
from registry_repo import registry_payload, resolve_repo


def print_payload(payload: dict[str, object], as_json: bool) -> int:
    if as_json:
        print(json.dumps(payload, indent=2))
    else:
        for key, value in payload.items():
            print(f"{key}: {value}")
    return 0


def cmd_registry(args: argparse.Namespace) -> int:
    return print_payload(registry_payload(), args.json)


def cmd_status(args: argparse.Namespace) -> int:
    repo_name, repo_root = resolve_repo(args.repo, args.repo_path)
    payload = {"repo": repo_name, **repo_status_payload(repo_root, fetch_first=args.fetch)}
    return print_payload(payload, args.json)


def cmd_remote_info(args: argparse.Namespace) -> int:
    repo_name, repo_root = resolve_repo(args.repo, args.repo_path)
    payload = {"repo": repo_name, **repo_status_payload(repo_root, fetch_first=False)}
    payload["remotes"] = remote_urls(repo_root)
    return print_payload(payload, args.json)


def cmd_fetch(args: argparse.Namespace) -> int:
    repo_name, repo_root = resolve_repo(args.repo, args.repo_path)
    payload = {"repo": repo_name, "repo_root": str(repo_root), **fetch(repo_root, remote=args.remote)}
    return print_payload(payload, args.json)


def cmd_pull_rebase(args: argparse.Namespace) -> int:
    repo_name, repo_root = resolve_repo(args.repo, args.repo_path)
    payload = {"repo": repo_name, "repo_root": str(repo_root), **pull_rebase(repo_root, remote=args.remote, branch=args.branch)}
    return print_payload(payload, args.json)


def _stage_from_scope(repo_name: str, repo_root, args: argparse.Namespace) -> dict[str, object]:
    try:
        scope = resolve_commit_scope(
            repo_root,
            explicit_paths=args.path or [],
            repo_name=repo_name,
            claims_file=args.claims_file,
            use_latest_claims=args.use_latest_claims,
            auto_scope=args.auto_scope,
            use_all=args.all,
        )
    except RuntimeError:
        if args.allow_empty:
            status_payload = repo_status_payload(repo_root, fetch_first=False)
            if not status_payload["dirty"]:
                return {"mode": "allow_empty_marker"}
        raise
    if scope["mode"] == "all":
        raise RuntimeError("unsafe_default_denied: whole-repo staging is disabled; pass explicit paths or claims")
    if scope["mode"] == "paths":
        stage_paths(repo_root, scope["paths"])
    return scope


def cmd_commit(args: argparse.Namespace) -> int:
    repo_name, repo_root = resolve_repo(args.repo, args.repo_path)
    scope = _stage_from_scope(repo_name, repo_root, args)
    result = commit(repo_root, args.message, allow_empty=args.allow_empty)
    payload = {"repo": repo_name, "repo_root": str(repo_root), "scope": scope, **result}
    return print_payload(payload, args.json)


def cmd_push(args: argparse.Namespace) -> int:
    repo_name, repo_root = resolve_repo(args.repo, args.repo_path)
    payload = {"repo": repo_name, "repo_root": str(repo_root), **push(repo_root, remote=args.remote, branch=args.branch, force_with_lease=args.force_with_lease)}
    return print_payload(payload, args.json)


def cmd_commit_and_push(args: argparse.Namespace) -> int:
    repo_name, repo_root = resolve_repo(args.repo, args.repo_path)
    scope = _stage_from_scope(repo_name, repo_root, args)
    commit_payload = commit(repo_root, args.message, allow_empty=args.allow_empty)
    push_payload = push(repo_root, remote=args.remote, branch=args.branch, force_with_lease=args.force_with_lease)
    payload = {
        "repo": repo_name,
        "repo_root": str(repo_root),
        "scope": scope,
        "commit": commit_payload["commit"],
        "push": push_payload,
    }
    return print_payload(payload, args.json)


def cmd_rollback_paths(args: argparse.Namespace) -> int:
    repo_name, repo_root = resolve_repo(args.repo, args.repo_path)
    payload = {"repo": repo_name, "repo_root": str(repo_root), **rollback_paths(repo_root, to_ref=args.to_ref, paths=args.path)}
    return print_payload(payload, args.json)


def main() -> int:
    parser = build_parser(
        cmd_registry,
        cmd_status,
        cmd_remote_info,
        cmd_fetch,
        cmd_pull_rebase,
        cmd_commit,
        cmd_commit_and_push,
        cmd_push,
        cmd_rollback_paths,
    )
    args = parser.parse_args()
    try:
        return int(args.func(args))
    except Exception as exc:  # noqa: BLE001
        raise SystemExit(str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
