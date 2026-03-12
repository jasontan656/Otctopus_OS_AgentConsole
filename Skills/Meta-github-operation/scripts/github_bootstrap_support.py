from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Literal

from git_cli_support import commit as git_commit
from git_cli_support import current_branch, remote_urls, run_git, stage_paths


Visibility = Literal["private", "public", "internal"]

IGNORE_SECTION_HEADER = "# Common local-only assets"
DEFAULT_IGNORE_PATTERNS: tuple[str, ...] = (
    "*.log",
    "logs/",
    "log/",
    "tmp/",
    "temp/",
    ".tmp/",
    ".temp/",
    ".cache/",
    "__pycache__/",
    ".pytest_cache/",
    ".mypy_cache/",
    ".ruff_cache/",
    ".venv/",
    ".venv*/",
    "venv/",
    "venv*/",
    "env/",
    "env*/",
    ".env",
    ".env.*",
    ".env.example",
)


def run_gh(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        ["gh", *args],
        text=True,
        capture_output=True,
        check=False,
    )
    if check and completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or completed.stdout.strip() or "gh command failed")
    return completed


def gh_current_user() -> str:
    completed = run_gh("api", "user", "--jq", ".login", check=True)
    login = completed.stdout.strip()
    if not login:
        raise RuntimeError("unable to resolve active GitHub login")
    return login


def gh_repo_view(repo_slug: str) -> dict[str, object] | None:
    completed = run_gh(
        "repo",
        "view",
        repo_slug,
        "--json",
        "name,visibility,isPrivate,defaultBranchRef,url",
        check=False,
    )
    if completed.returncode != 0:
        return None
    return json.loads(completed.stdout)


def gh_repo_create(repo_slug: str, visibility: Visibility) -> None:
    visibility_flag = {
        "private": "--private",
        "public": "--public",
        "internal": "--internal",
    }[visibility]
    run_gh("repo", "create", repo_slug, visibility_flag, "--confirm", check=True)


def gh_repo_edit_visibility(repo_slug: str, visibility: Visibility) -> None:
    visibility_flag = {
        "private": "private",
        "public": "public",
        "internal": "internal",
    }[visibility]
    args = ["repo", "edit", repo_slug, "--visibility", visibility_flag]
    if visibility == "private":
        args.append("--accept-visibility-change-consequences")
    run_gh(*args, check=True)


def ssh_remote_url(owner: str, repo_name: str) -> str:
    return f"git@github.com:{owner}/{repo_name}.git"


def ensure_gitignore_patterns(
    repo_root: Path,
    patterns: tuple[str, ...] = DEFAULT_IGNORE_PATTERNS,
) -> dict[str, object]:
    gitignore_path = repo_root / ".gitignore"
    existed = gitignore_path.exists()
    lines = gitignore_path.read_text(encoding="utf-8").splitlines() if existed else []
    normalized = {line.strip() for line in lines if line.strip()}

    appended: list[str] = []
    next_lines = list(lines)

    if IGNORE_SECTION_HEADER not in normalized:
        if next_lines and next_lines[-1] != "":
            next_lines.append("")
        next_lines.append(IGNORE_SECTION_HEADER)
        normalized.add(IGNORE_SECTION_HEADER)

    for pattern in patterns:
        if pattern in normalized:
            continue
        next_lines.append(pattern)
        normalized.add(pattern)
        appended.append(pattern)

    if not existed or appended:
        gitignore_path.write_text("\n".join(next_lines).rstrip() + "\n", encoding="utf-8")

    return {
        "gitignore_path": str(gitignore_path),
        "created": not existed,
        "appended_patterns": appended,
    }


def ensure_remote(repo_root: Path, *, remote_name: str, remote_url: str) -> dict[str, object]:
    remotes = remote_urls(repo_root)
    fetch_url = next((item["url"] for item in remotes if item["remote"] == remote_name and item["kind"] == "fetch"), None)
    push_url = next((item["url"] for item in remotes if item["remote"] == remote_name and item["kind"] == "push"), None)

    if fetch_url is None:
        run_git(repo_root, "remote", "add", remote_name, remote_url, check=True)
        return {
            "remote": remote_name,
            "action": "added",
            "url": remote_url,
        }

    if fetch_url == remote_url and (push_url is None or push_url == remote_url):
        return {
            "remote": remote_name,
            "action": "unchanged",
            "url": remote_url,
        }

    run_git(repo_root, "remote", "set-url", remote_name, remote_url, check=True)
    run_git(repo_root, "remote", "set-url", "--push", remote_name, remote_url, check=True)
    return {
        "remote": remote_name,
        "action": "updated",
        "previous_fetch_url": fetch_url,
        "previous_push_url": push_url,
        "url": remote_url,
    }


def bootstrap_private_origin(
    repo_root: Path,
    *,
    owner: str | None,
    repo_name: str | None,
    remote_name: str,
    visibility: Visibility,
    commit_message: str | None,
    use_all: bool,
    allow_empty: bool,
) -> dict[str, object]:
    resolved_owner = owner or gh_current_user()
    resolved_repo_name = repo_name or repo_root.name
    repo_slug = f"{resolved_owner}/{resolved_repo_name}"

    ignore_payload = ensure_gitignore_patterns(repo_root)

    repo_view_before = gh_repo_view(repo_slug)
    repo_created = False
    visibility_changed = False
    if repo_view_before is None:
        gh_repo_create(repo_slug, visibility)
        repo_created = True
    elif str(repo_view_before.get("visibility", "")).lower() != visibility:
        gh_repo_edit_visibility(repo_slug, visibility)
        visibility_changed = True

    repo_view_after = gh_repo_view(repo_slug)
    if repo_view_after is None:
        raise RuntimeError(f"unable to verify GitHub repository after bootstrap: {repo_slug}")

    remote_payload = ensure_remote(
        repo_root,
        remote_name=remote_name,
        remote_url=ssh_remote_url(resolved_owner, resolved_repo_name),
    )

    commit_payload: dict[str, object] | None = None
    if commit_message:
        if use_all:
            run_git(repo_root, "add", "-A", check=True)
        else:
            paths = []
            if ignore_payload["created"] or ignore_payload["appended_patterns"]:
                paths.append(".gitignore")
            if paths:
                stage_paths(repo_root, paths)
        commit_payload = git_commit(repo_root, commit_message, allow_empty=allow_empty)

    branch = current_branch(repo_root)
    run_git(repo_root, "push", "-u", remote_name, branch, check=True)

    return {
        "repo_root": str(repo_root),
        "repo_slug": repo_slug,
        "owner": resolved_owner,
        "repo_name": resolved_repo_name,
        "visibility": visibility,
        "repo_created": repo_created,
        "visibility_changed": visibility_changed,
        "remote": remote_payload,
        "gitignore": ignore_payload,
        "commit": commit_payload,
        "branch": branch,
        "github_repo": repo_view_after,
    }
