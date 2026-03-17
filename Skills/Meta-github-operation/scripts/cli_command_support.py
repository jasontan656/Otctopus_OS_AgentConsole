from __future__ import annotations

import json
from pathlib import Path

from git_cli_support import resolve_commit_scope, run_git, stage_paths
from registry_repo import resolve_repo
from runtime_contract_support import CommitScope


def emit_payload(payload: object, *, as_json: bool = False) -> None:
    if not isinstance(payload, dict):
        raise TypeError("runtime payload must be a dictionary-backed object")
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    for key, value in payload.items():
        print(f"{key}: {value}")


def resolve_repo_root(repo: str | None, repo_path: str | None) -> tuple[str, Path]:
    repo_name, repo_root = resolve_repo(repo, repo_path)
    if not repo_root.exists():
        raise ValueError(f"repo path does not exist: {repo_root}")
    return repo_name, repo_root


def apply_scope(repo_root: Path, scope: CommitScope) -> None:
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


def resolve_scope(
    repo_root: Path,
    *,
    repo_name: str,
    paths: list[str] | None,
    claims_file: str | None,
    use_latest_claims: bool,
    auto_scope: bool,
    use_all: bool,
) -> CommitScope:
    return resolve_commit_scope(
        repo_root,
        explicit_paths=list(paths or []),
        repo_name=repo_name,
        claims_file=claims_file,
        use_latest_claims=use_latest_claims,
        auto_scope=auto_scope,
        use_all=use_all,
    )
