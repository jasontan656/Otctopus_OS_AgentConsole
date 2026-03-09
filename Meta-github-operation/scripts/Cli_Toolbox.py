#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from cli_parser_support import build_parser
from entry_support import push_contract_payload, rollback_contract_payload
from git_cli_support import commit as git_commit
from git_cli_support import fetch as git_fetch
from git_cli_support import pull_rebase as git_pull_rebase
from git_cli_support import push as git_push
from git_cli_support import remote_urls, repo_status_payload, resolve_commit_scope, rollback_paths, rollback_sync, run_git, stage_paths
from registry_repo import registry_payload, resolve_repo


def emit(payload: dict[str, object], *, as_json: bool = False) -> int:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    for key, value in payload.items():
        print(f"{key}: {value}")
    return 0


def resolve_repo_root(args) -> tuple[str, Path]:
    repo_name, repo_root = resolve_repo(args.repo, args.repo_path)
    if not repo_root.exists():
        raise ValueError(f"repo path does not exist: {repo_root}")
    return repo_name, repo_root


def cmd_registry(args) -> int:
    return emit(registry_payload(), as_json=args.json)


def cmd_push_contract(args) -> int:
    return emit(push_contract_payload(), as_json=args.json)


def cmd_rollback_contract(args) -> int:
    return emit(rollback_contract_payload(), as_json=args.json)


def cmd_status(args) -> int:
    repo_name, repo_root = resolve_repo_root(args)
    payload = repo_status_payload(repo_root, fetch_first=bool(args.fetch))
    payload["repo"] = repo_name
    return emit(payload, as_json=args.json)


def cmd_remote_info(args) -> int:
    repo_name, repo_root = resolve_repo_root(args)
    payload = {
        "repo": repo_name,
        "repo_root": str(repo_root),
        "remotes": remote_urls(repo_root),
    }
    return emit(payload, as_json=args.json)


def cmd_fetch(args) -> int:
    repo_name, repo_root = resolve_repo_root(args)
    payload = git_fetch(repo_root, remote=args.remote)
    payload["repo"] = repo_name
    payload["repo_root"] = str(repo_root)
    return emit(payload, as_json=args.json)


def cmd_pull_rebase(args) -> int:
    repo_name, repo_root = resolve_repo_root(args)
    payload = git_pull_rebase(repo_root, remote=args.remote, branch=args.branch)
    payload["repo"] = repo_name
    payload["repo_root"] = str(repo_root)
    return emit(payload, as_json=args.json)


def apply_scope(repo_root: Path, scope: dict[str, object]) -> None:
    mode = scope["mode"]
    if mode == "all":
        run_git(repo_root, "add", "-A", check=True)
        return
    if mode == "paths":
        stage_paths(repo_root, list(scope["paths"]))
        return
    if mode == "staged":
        return
    raise ValueError(f"unsupported scope mode: {mode}")


def cmd_commit(args) -> int:
    repo_name, repo_root = resolve_repo_root(args)
    scope = resolve_commit_scope(
        repo_root,
        explicit_paths=list(args.path or []),
        repo_name=repo_name,
        claims_file=args.claims_file,
        use_latest_claims=bool(args.use_latest_claims),
        auto_scope=bool(args.auto_scope),
        use_all=bool(args.all),
    )
    apply_scope(repo_root, scope)
    payload = {"repo": repo_name, "repo_root": str(repo_root), "scope": scope}
    payload.update(git_commit(repo_root, args.message, allow_empty=bool(args.allow_empty)))
    return emit(payload, as_json=args.json)


def cmd_commit_and_push(args) -> int:
    repo_name, repo_root = resolve_repo_root(args)
    scope = resolve_commit_scope(
        repo_root,
        explicit_paths=list(args.path or []),
        repo_name=repo_name,
        claims_file=args.claims_file,
        use_latest_claims=bool(args.use_latest_claims),
        auto_scope=bool(args.auto_scope),
        use_all=bool(args.all),
    )
    apply_scope(repo_root, scope)
    payload = {"repo": repo_name, "repo_root": str(repo_root), "scope": scope}
    payload.update(git_commit(repo_root, args.message, allow_empty=bool(args.allow_empty)))
    payload["push"] = git_push(
        repo_root,
        remote=args.remote,
        branch=args.branch,
        force_with_lease=bool(args.force_with_lease),
    )
    return emit(payload, as_json=args.json)


def cmd_push(args) -> int:
    repo_name, repo_root = resolve_repo_root(args)
    payload = {"repo": repo_name, "repo_root": str(repo_root)}
    payload.update(
        git_push(
            repo_root,
            remote=args.remote,
            branch=args.branch,
            force_with_lease=bool(args.force_with_lease),
        )
    )
    return emit(payload, as_json=args.json)


def cmd_rollback_paths(args) -> int:
    repo_name, repo_root = resolve_repo_root(args)
    payload = rollback_paths(repo_root, to_ref=args.to_ref, paths=list(args.path))
    payload["repo"] = repo_name
    payload["repo_root"] = str(repo_root)
    return emit(payload, as_json=args.json)


def cmd_rollback_sync(args) -> int:
    if bool(args.all) == bool(args.path):
        raise ValueError("pass exactly one of --all or at least one --path")
    repo_name, repo_root = resolve_repo_root(args)
    payload = rollback_sync(
        repo_root,
        to_ref=args.to_ref,
        paths=list(args.path or []),
        use_all=bool(args.all),
    )
    payload["repo"] = repo_name
    payload["repo_root"] = str(repo_root)
    return emit(payload, as_json=args.json)


def main() -> int:
    parser = build_parser(
        cmd_registry=cmd_registry,
        cmd_status=cmd_status,
        cmd_remote_info=cmd_remote_info,
        cmd_fetch=cmd_fetch,
        cmd_pull_rebase=cmd_pull_rebase,
        cmd_commit=cmd_commit,
        cmd_commit_and_push=cmd_commit_and_push,
        cmd_push=cmd_push,
        cmd_push_contract=cmd_push_contract,
        cmd_rollback_contract=cmd_rollback_contract,
        cmd_rollback_paths=cmd_rollback_paths,
        cmd_rollback_sync=cmd_rollback_sync,
    )
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
