#!/usr/bin/env python3
from __future__ import annotations

from typing import Annotated, Literal

import typer

from cli_command_support import apply_scope, emit_payload, resolve_repo_root, resolve_scope
from entry_support import baseline_contract_payload, push_contract_payload, rollback_contract_payload
from git_cli_support import commit as git_commit
from git_cli_support import create_annotated_tag
from git_cli_support import fetch as git_fetch
from git_cli_support import normalize_baseline_tag
from git_cli_support import pull_rebase as git_pull_rebase
from git_cli_support import push as git_push
from git_cli_support import push_tag
from git_cli_support import remote_urls, repo_status_payload, rollback_paths, rollback_sync
from github_bootstrap_support import bootstrap_private_origin
from push_execution_support import normalize_traceability_message, serial_push_lock
from registry_repo import ensure_remote_write_allowed, registry_payload, remote_policy_payload


app = typer.Typer(add_completion=False, pretty_exceptions_enable=False)

RepoNameOption = Annotated[str | None, typer.Option("--repo")]
RepoPathOption = Annotated[str | None, typer.Option("--repo-path")]
JsonOption = Annotated[bool, typer.Option("--json")]
PathListOption = Annotated[list[str] | None, typer.Option("--path")]


@app.command("registry")
def registry_command(json_output: JsonOption = False) -> None:
    emit_payload(registry_payload(), as_json=json_output)


@app.command("push-contract")
def push_contract_command(json_output: JsonOption = False) -> None:
    emit_payload(push_contract_payload(), as_json=json_output)


@app.command("baseline-contract")
def baseline_contract_command(json_output: JsonOption = False) -> None:
    emit_payload(baseline_contract_payload(), as_json=json_output)


@app.command("rollback-contract")
def rollback_contract_command(json_output: JsonOption = False) -> None:
    emit_payload(rollback_contract_payload(), as_json=json_output)


@app.command("status")
def status_command(
    repo: RepoNameOption = None,
    repo_path: RepoPathOption = None,
    fetch: Annotated[bool, typer.Option("--fetch")] = False,
    json_output: JsonOption = False,
) -> None:
    repo_name, repo_root = resolve_repo_root(repo, repo_path)
    payload = dict(repo_status_payload(repo_root, fetch_first=fetch))
    payload["repo"] = repo_name
    emit_payload(payload, as_json=json_output)


@app.command("remote-info")
def remote_info_command(
    repo: RepoNameOption = None,
    repo_path: RepoPathOption = None,
    json_output: JsonOption = False,
) -> None:
    repo_name, repo_root = resolve_repo_root(repo, repo_path)
    payload = {
        "repo": repo_name,
        "repo_root": str(repo_root),
        "remotes": remote_urls(repo_root),
        "managed_remote_policy": remote_policy_payload(repo_name),
    }
    emit_payload(payload, as_json=json_output)


@app.command("fetch")
def fetch_command(
    repo: RepoNameOption = None,
    repo_path: RepoPathOption = None,
    remote: Annotated[str, typer.Option("--remote")] = "origin",
    json_output: JsonOption = False,
) -> None:
    repo_name, repo_root = resolve_repo_root(repo, repo_path)
    payload = dict(git_fetch(repo_root, remote=remote))
    payload["repo"] = repo_name
    payload["repo_root"] = str(repo_root)
    emit_payload(payload, as_json=json_output)


@app.command("pull-rebase")
def pull_rebase_command(
    repo: RepoNameOption = None,
    repo_path: RepoPathOption = None,
    remote: Annotated[str, typer.Option("--remote")] = "origin",
    branch: Annotated[str | None, typer.Option("--branch")] = None,
    json_output: JsonOption = False,
) -> None:
    repo_name, repo_root = resolve_repo_root(repo, repo_path)
    payload = dict(git_pull_rebase(repo_root, remote=remote, branch=branch))
    payload["repo"] = repo_name
    payload["repo_root"] = str(repo_root)
    emit_payload(payload, as_json=json_output)


@app.command("commit")
def commit_command(
    repo: RepoNameOption = None,
    repo_path: RepoPathOption = None,
    message: Annotated[str, typer.Option("--message")] = ...,
    paths: PathListOption = None,
    claims_file: Annotated[str | None, typer.Option("--claims-file")] = None,
    use_latest_claims: Annotated[bool, typer.Option("--use-latest-claims")] = False,
    auto_scope: Annotated[bool, typer.Option("--auto-scope")] = False,
    use_all: Annotated[bool, typer.Option("--all")] = False,
    allow_empty: Annotated[bool, typer.Option("--allow-empty")] = False,
    json_output: JsonOption = False,
) -> None:
    repo_name, repo_root = resolve_repo_root(repo, repo_path)
    normalized_message = normalize_traceability_message(message)
    scope = resolve_scope(
        repo_root,
        repo_name=repo_name,
        paths=paths,
        claims_file=claims_file,
        use_latest_claims=use_latest_claims,
        auto_scope=auto_scope,
        use_all=use_all,
    )
    apply_scope(repo_root, scope)
    payload = {"repo": repo_name, "repo_root": str(repo_root), "scope": scope, "message": normalized_message}
    payload.update(git_commit(repo_root, normalized_message, allow_empty=allow_empty))
    emit_payload(payload, as_json=json_output)


@app.command("commit-and-push")
def commit_and_push_command(
    repo: RepoNameOption = None,
    repo_path: RepoPathOption = None,
    message: Annotated[str, typer.Option("--message")] = ...,
    paths: PathListOption = None,
    claims_file: Annotated[str | None, typer.Option("--claims-file")] = None,
    use_latest_claims: Annotated[bool, typer.Option("--use-latest-claims")] = False,
    auto_scope: Annotated[bool, typer.Option("--auto-scope")] = False,
    use_all: Annotated[bool, typer.Option("--all")] = False,
    allow_empty: Annotated[bool, typer.Option("--allow-empty")] = False,
    remote: Annotated[str, typer.Option("--remote")] = "origin",
    human_explicit_request: Annotated[bool, typer.Option("--human-explicit-request")] = False,
    branch: Annotated[str | None, typer.Option("--branch")] = None,
    force_with_lease: Annotated[bool, typer.Option("--force-with-lease")] = False,
    json_output: JsonOption = False,
) -> None:
    repo_name, repo_root = resolve_repo_root(repo, repo_path)
    normalized_message = normalize_traceability_message(message)
    ensure_remote_write_allowed(
        repo_name,
        remote,
        operation="commit-and-push",
        human_explicit_request=human_explicit_request,
    )
    scope = resolve_scope(
        repo_root,
        repo_name=repo_name,
        paths=paths,
        claims_file=claims_file,
        use_latest_claims=use_latest_claims,
        auto_scope=auto_scope,
        use_all=use_all,
    )
    apply_scope(repo_root, scope)
    payload = {"repo": repo_name, "repo_root": str(repo_root), "scope": scope, "message": normalized_message}
    with serial_push_lock(repo_name, "commit-and-push") as push_lock:
        payload["push_lock"] = push_lock
        payload.update(git_commit(repo_root, normalized_message, allow_empty=allow_empty))
        payload["push"] = git_push(
            repo_root,
            remote=remote,
            branch=branch,
            force_with_lease=force_with_lease,
        )
    emit_payload(payload, as_json=json_output)


@app.command("push")
def push_command(
    repo: RepoNameOption = None,
    repo_path: RepoPathOption = None,
    remote: Annotated[str, typer.Option("--remote")] = "origin",
    human_explicit_request: Annotated[bool, typer.Option("--human-explicit-request")] = False,
    branch: Annotated[str | None, typer.Option("--branch")] = None,
    force_with_lease: Annotated[bool, typer.Option("--force-with-lease")] = False,
    json_output: JsonOption = False,
) -> None:
    repo_name, repo_root = resolve_repo_root(repo, repo_path)
    ensure_remote_write_allowed(
        repo_name,
        remote,
        operation="push",
        human_explicit_request=human_explicit_request,
    )
    payload = {"repo": repo_name, "repo_root": str(repo_root)}
    with serial_push_lock(repo_name, "push") as push_lock:
        payload["push_lock"] = push_lock
        payload.update(
            git_push(
                repo_root,
                remote=remote,
                branch=branch,
                force_with_lease=force_with_lease,
            )
        )
    emit_payload(payload, as_json=json_output)


@app.command("repo-bootstrap")
def repo_bootstrap_command(
    repo: RepoNameOption = None,
    repo_path: RepoPathOption = None,
    owner: Annotated[str | None, typer.Option("--owner")] = None,
    repo_name: Annotated[str | None, typer.Option("--repo-name")] = None,
    remote: Annotated[str, typer.Option("--remote")] = "origin",
    human_explicit_request: Annotated[bool, typer.Option("--human-explicit-request")] = False,
    visibility: Annotated[Literal["private", "public", "internal"], typer.Option("--visibility")] = "private",
    message: Annotated[str | None, typer.Option("--message")] = None,
    use_all: Annotated[bool, typer.Option("--all")] = False,
    allow_empty: Annotated[bool, typer.Option("--allow-empty")] = False,
    json_output: JsonOption = False,
) -> None:
    repo_name_resolved, repo_root = resolve_repo_root(repo, repo_path)
    ensure_remote_write_allowed(
        repo_name_resolved,
        remote,
        operation="repo-bootstrap",
        human_explicit_request=human_explicit_request,
    )
    normalized_message = normalize_traceability_message(message) if message else None
    payload = {
        "repo": repo_name_resolved,
        "repo_root": str(repo_root),
        "operation": "repo-bootstrap",
    }
    with serial_push_lock(repo_name_resolved, "repo-bootstrap") as push_lock:
        payload["push_lock"] = push_lock
        payload.update(
            bootstrap_private_origin(
                repo_root,
                owner=owner,
                repo_name=repo_name,
                remote_name=remote,
                visibility=visibility,
                commit_message=normalized_message,
                use_all=use_all,
                allow_empty=allow_empty,
            )
        )
    emit_payload(payload, as_json=json_output)


@app.command("baseline-create")
def baseline_create_command(
    repo: RepoNameOption = None,
    repo_path: RepoPathOption = None,
    name: Annotated[str, typer.Option("--name")] = ...,
    message: Annotated[str | None, typer.Option("--message")] = None,
    publish: Annotated[Literal["local", "remote"], typer.Option("--publish")] = "local",
    paths: PathListOption = None,
    claims_file: Annotated[str | None, typer.Option("--claims-file")] = None,
    use_latest_claims: Annotated[bool, typer.Option("--use-latest-claims")] = False,
    auto_scope: Annotated[bool, typer.Option("--auto-scope")] = False,
    use_all: Annotated[bool, typer.Option("--all")] = False,
    remote: Annotated[str, typer.Option("--remote")] = "origin",
    human_explicit_request: Annotated[bool, typer.Option("--human-explicit-request")] = False,
    branch: Annotated[str | None, typer.Option("--branch")] = None,
    json_output: JsonOption = False,
) -> None:
    repo_name, repo_root = resolve_repo_root(repo, repo_path)
    status_payload = repo_status_payload(repo_root)
    dirty = bool(status_payload["dirty"])
    tag_name = normalize_baseline_tag(name)
    resolved_message = message or f"baseline: {name}"

    payload = {
        "repo": repo_name,
        "repo_root": str(repo_root),
        "baseline_name": name,
        "tag": tag_name,
        "publish": publish,
        "dirty_before": dirty,
    }

    if dirty:
        scope = resolve_scope(
            repo_root,
            repo_name=repo_name,
            paths=paths,
            claims_file=claims_file,
            use_latest_claims=use_latest_claims,
            auto_scope=auto_scope,
            use_all=use_all,
        )
        apply_scope(repo_root, scope)
        payload["scope"] = scope
        payload.update(git_commit(repo_root, resolved_message, allow_empty=False))
        payload["baseline_mode"] = "commit_plus_tag"
    else:
        payload["baseline_mode"] = "tag_only"

    payload["tag_result"] = create_annotated_tag(repo_root, tag_name=tag_name, message=resolved_message)
    if publish == "remote":
        ensure_remote_write_allowed(
            repo_name,
            remote,
            operation="baseline-create:publish",
            human_explicit_request=human_explicit_request,
        )
        with serial_push_lock(repo_name, "baseline-create:publish") as push_lock:
            published = {
                "push_lock": push_lock,
                "tag": push_tag(repo_root, remote=remote, tag_name=tag_name),
            }
            if dirty:
                published["branch"] = git_push(
                    repo_root,
                    remote=remote,
                    branch=branch,
                    force_with_lease=False,
                )
        payload["publish_result"] = published
    emit_payload(payload, as_json=json_output)


@app.command("rollback-paths")
def rollback_paths_command(
    repo: RepoNameOption = None,
    repo_path: RepoPathOption = None,
    to_ref: Annotated[str, typer.Option("--to-ref")] = ...,
    paths: Annotated[list[str], typer.Option("--path")] = ...,
    json_output: JsonOption = False,
) -> None:
    repo_name, repo_root = resolve_repo_root(repo, repo_path)
    payload = dict(rollback_paths(repo_root, to_ref=to_ref, paths=list(paths)))
    payload["repo"] = repo_name
    payload["repo_root"] = str(repo_root)
    emit_payload(payload, as_json=json_output)


@app.command("rollback-sync")
def rollback_sync_command(
    repo: RepoNameOption = None,
    repo_path: RepoPathOption = None,
    to_ref: Annotated[str, typer.Option("--to-ref")] = ...,
    paths: PathListOption = None,
    use_all: Annotated[bool, typer.Option("--all")] = False,
    json_output: JsonOption = False,
) -> None:
    if use_all == bool(paths):
        raise ValueError("pass exactly one of --all or at least one --path")
    repo_name, repo_root = resolve_repo_root(repo, repo_path)
    payload = dict(
        rollback_sync(
            repo_root,
            to_ref=to_ref,
            paths=list(paths or []),
            use_all=use_all,
        )
    )
    payload["repo"] = repo_name
    payload["repo_root"] = str(repo_root)
    emit_payload(payload, as_json=json_output)


def main() -> int:
    app()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
