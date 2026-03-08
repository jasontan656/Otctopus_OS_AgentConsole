from __future__ import annotations

import subprocess
from pathlib import Path

from rollback_support import path_exists_in_ref, prune_empty_path_ancestors, remove_explicit_path
from thread_claims_support import latest_claims_file, load_claim_paths


def run_git(repo_root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        ["git", "-C", str(repo_root), *args],
        text=True,
        capture_output=True,
        check=False,
    )
    if check and completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or completed.stdout.strip() or "git command failed")
    return completed


def list_status_entries(repo_root: Path) -> list[dict[str, str]]:
    completed = run_git(repo_root, "status", "--porcelain", check=True)
    entries: list[dict[str, str]] = []
    for raw_line in completed.stdout.splitlines():
        if not raw_line:
            continue
        status = raw_line[:2]
        path = raw_line[3:]
        entries.append({"status": status, "path": path})
    return entries


def staged_paths(repo_root: Path) -> list[str]:
    completed = run_git(repo_root, "diff", "--cached", "--name-only", check=True)
    return [line.strip() for line in completed.stdout.splitlines() if line.strip()]


def changed_paths(repo_root: Path) -> list[str]:
    return [entry["path"] for entry in list_status_entries(repo_root)]


def current_branch(repo_root: Path) -> str:
    return run_git(repo_root, "branch", "--show-current", check=True).stdout.strip()


def upstream_branch(repo_root: Path) -> str | None:
    completed = run_git(repo_root, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}", check=False)
    if completed.returncode != 0:
        return None
    value = completed.stdout.strip()
    return value or None


def remote_urls(repo_root: Path) -> list[dict[str, str]]:
    completed = run_git(repo_root, "remote", "-v", check=True)
    rows: list[dict[str, str]] = []
    for line in completed.stdout.splitlines():
        parts = line.split()
        if len(parts) >= 3:
            rows.append({"remote": parts[0], "url": parts[1], "kind": parts[2].strip("()")})
    return rows


def ahead_behind(repo_root: Path, upstream: str | None) -> dict[str, int] | None:
    if not upstream:
        return None
    completed = run_git(repo_root, "rev-list", "--left-right", "--count", f"{upstream}...HEAD", check=True)
    left, right = completed.stdout.strip().split()
    return {"behind": int(left), "ahead": int(right)}


def repo_status_payload(repo_root: Path, *, fetch_first: bool = False) -> dict[str, object]:
    if fetch_first:
        run_git(repo_root, "fetch", "--all", "--prune", check=False)
    entries = list_status_entries(repo_root)
    staged = staged_paths(repo_root)
    branch = current_branch(repo_root)
    upstream = upstream_branch(repo_root)
    return {
        "repo_root": str(repo_root),
        "branch": branch,
        "upstream": upstream,
        "ahead_behind": ahead_behind(repo_root, upstream),
        "dirty": bool(entries),
        "staged_paths": staged,
        "entries": entries,
    }


def stage_paths(repo_root: Path, paths: list[str]) -> None:
    if not paths:
        raise ValueError("no paths provided for staging")
    run_git(repo_root, "add", "--", *paths, check=True)


def commit(repo_root: Path, message: str, *, allow_empty: bool = False) -> dict[str, object]:
    args = ["commit", "-m", message]
    if allow_empty:
        args.insert(1, "--allow-empty")
    completed = run_git(repo_root, *args, check=False)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or completed.stdout.strip() or "git commit failed")
    sha = run_git(repo_root, "rev-parse", "--short", "HEAD", check=True).stdout.strip()
    return {"commit": sha}


def push(repo_root: Path, *, remote: str = "origin", branch: str | None = None, force_with_lease: bool = False) -> dict[str, object]:
    branch_name = branch or current_branch(repo_root)
    args = ["push"]
    if force_with_lease:
        args.append("--force-with-lease")
    upstream = upstream_branch(repo_root)
    if upstream is None:
        args.extend(["-u", remote, branch_name])
    else:
        args.extend([remote, branch_name])
    run_git(repo_root, *args, check=True)
    return {"remote": remote, "branch": branch_name, "force_with_lease": force_with_lease}


def fetch(repo_root: Path, *, remote: str = "origin") -> dict[str, object]:
    run_git(repo_root, "fetch", remote, "--prune", check=True)
    return {"remote": remote}


def pull_rebase(repo_root: Path, *, remote: str = "origin", branch: str | None = None) -> dict[str, object]:
    args = ["pull", "--rebase", remote]
    if branch:
        args.append(branch)
    run_git(repo_root, *args, check=True)
    return {"remote": remote, "branch": branch or current_branch(repo_root)}


def rollback_paths(repo_root: Path, *, to_ref: str, paths: list[str]) -> dict[str, object]:
    if not paths:
        raise ValueError("at least one --path is required")
    restore_paths: list[str] = []
    removed_paths: list[str] = []
    for raw_path in paths:
        if path_exists_in_ref(run_git, repo_root, to_ref, raw_path):
            restore_paths.append(raw_path)
            continue
        remove_explicit_path(repo_root / raw_path)
        removed_paths.append(raw_path)
    if restore_paths:
        run_git(repo_root, "restore", "--source", to_ref, "--", *restore_paths, check=True)
    pruned_dirs: list[str] = []
    for raw_path in paths:
        pruned_dirs.extend(prune_empty_path_ancestors(repo_root, raw_path))
    return {
        "to_ref": to_ref,
        "paths": paths,
        "restored_paths": restore_paths,
        "removed_paths": removed_paths,
        "pruned_empty_dirs": sorted(set(pruned_dirs)),
    }


def resolve_commit_scope(
    repo_root: Path,
    *,
    explicit_paths: list[str],
    repo_name: str,
    claims_file: str | None,
    use_latest_claims: bool,
    auto_scope: bool,
    use_all: bool,
) -> dict[str, object]:
    if use_all:
        return {"mode": "all"}
    if explicit_paths:
        return {"mode": "paths", "paths": explicit_paths}

    claim_path_obj = Path(claims_file).expanduser().resolve() if claims_file else None
    if claim_path_obj is None and use_latest_claims:
        claim_path_obj = latest_claims_file()
    if claim_path_obj is not None and claim_path_obj.exists():
        claim_paths = load_claim_paths(claim_path_obj, repo_name)
        if claim_paths:
            return {"mode": "paths", "paths": claim_paths, "claims_file": str(claim_path_obj)}

    if auto_scope:
        staged = staged_paths(repo_root)
        if staged:
            return {"mode": "staged"}
        changed = changed_paths(repo_root)
        if len(changed) == 1:
            return {"mode": "paths", "paths": changed}
        raise RuntimeError("scope_ambiguous: no claims, no staged paths, and changed path count is not exactly 1")

    raise RuntimeError("no commit scope resolved; pass --path, --all, or claims information")
