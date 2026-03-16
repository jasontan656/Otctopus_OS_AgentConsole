from __future__ import annotations

import json
import shlex
from pathlib import Path

from workflow_policy_contract import IMPLEMENTATION_SOURCE_POLICY

GRAPH_CORE_ENTRY = (
    Path(__file__).resolve().parents[2]
    / "Meta-code-graph-base"
    / "assets"
    / "gitnexus_core"
    / "dist"
    / "cli"
    / "index.js"
)

SOURCE_EXTENSIONS = {
    ".py",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".go",
    ".rs",
    ".java",
    ".kt",
    ".cs",
    ".rb",
}


def registry_entries(graph_runtime_root: Path) -> list[dict]:
    registry_path = graph_runtime_root / "registry" / "registry.json"
    if not registry_path.exists():
        return []
    return json.loads(registry_path.read_text(encoding="utf-8"))


def repo_has_substantial_code(repo: Path) -> bool:
    if not repo.exists():
        return False
    count = 0
    for path in repo.rglob("*"):
        if not path.is_file():
            continue
        if any(part.startswith(".") and part not in {".github", ".gitlab"} for part in path.parts):
            continue
        if any(part in {"node_modules", ".venv", ".venv-wsl", "dist", "build", "__pycache__"} for part in path.parts):
            continue
        if path.suffix.lower() in SOURCE_EXTENSIONS:
            count += 1
            if count >= 5:
                return True
    return False


def is_indexed(repo: Path, graph_runtime_root: Path) -> bool:
    resolved = repo.resolve()
    for entry in registry_entries(graph_runtime_root):
        if Path(entry["path"]).resolve() == resolved:
            return True
    return False


def indexed_repo_name(repo: Path, graph_runtime_root: Path) -> str | None:
    resolved = repo.resolve()
    for entry in registry_entries(graph_runtime_root):
        if Path(entry["path"]).resolve() == resolved:
            return str(entry["name"])
    return None


def graph_core_command(
    graph_runtime_root: Path,
    *args: str,
    repo_cwd: Path | None = None,
) -> str:
    base_parts = [
        f"META_CODE_GRAPH_RUNTIME_ROOT={shlex.quote(str(graph_runtime_root))}",
        "node",
        shlex.quote(str(GRAPH_CORE_ENTRY)),
    ]
    base_parts.extend(shlex.quote(str(arg)) for arg in args)
    command = " ".join(base_parts)
    if repo_cwd is None:
        return command
    return f"cd {shlex.quote(str(repo_cwd))} && {command}"


def graph_resource_context_command(repo_name: str | None, graph_runtime_root: Path) -> str:
    target_name = repo_name or "<indexed_repo_name>"
    return graph_core_command(
        graph_runtime_root,
        "resource",
        f"codegraph://repo/{target_name}/context",
    )


def graph_query_command(repo_name: str | None, graph_runtime_root: Path) -> str:
    target_name = repo_name or "<indexed_repo_name>"
    return graph_core_command(
        graph_runtime_root,
        "query",
        "<search_query>",
        "--repo",
        target_name,
    )


def graph_impact_command(repo_name: str | None, graph_runtime_root: Path) -> str:
    target_name = repo_name or "<indexed_repo_name>"
    return graph_core_command(
        graph_runtime_root,
        "impact",
        "<symbol_name_or_uid>",
        "--direction",
        "upstream",
        "--repo",
        target_name,
    )


def graph_preflight_summary(repo: Path, allow_missing_index: bool, graph_runtime_root: Path) -> dict:
    indexed = is_indexed(repo, graph_runtime_root)
    repo_name = indexed_repo_name(repo, graph_runtime_root)
    substantial = repo_has_substantial_code(repo)
    if indexed:
        action = "use_graph_context"
    elif substantial:
        action = "run_analyze"
    elif allow_missing_index:
        action = "skip_non_blocking"
    else:
        action = "missing_index_blocked"
    return {
        "repo": str(repo),
        "repo_exists": repo.exists(),
        "indexed": indexed,
        "substantial_codebase": substantial,
        "recommended_action": action,
        "default_baseline_mode": "real_codebase" if substantial else "empty_baseline",
        "implementation_source_scope": "current_worktree_only",
        "forbidden_non_worktree_actions": IMPLEMENTATION_SOURCE_POLICY["forbidden_actions"],
        "guardrail_note": "When current worktree is near-empty, use only current worktree and runtime artifacts as implementation sources.",
        "graph_consumer_contract_version": "1.0",
        "direct_cli_io_contract": {
            "primary_channel": "stdout",
            "fallback_channel": "stderr",
            "rule": "parse stdout first, then fallback to stderr when stdout is empty because some native graph commands emit structured payloads there",
        },
        "preferred_read_sequence": [
            "run status inside the target repo cwd when you need freshness or indexed/stale evidence",
            "if recommended_action=run_analyze, build the index before semantic lookup",
            "use resource repo context first for repo-level orientation",
            "use context when symbol name or uid is already known",
            "use query when only a fuzzy concept or workflow phrase is known",
            "use impact only after a concrete symbol target exists",
        ],
        "status_command": graph_core_command(graph_runtime_root, "status", repo_cwd=repo),
        "analyze_command": graph_core_command(graph_runtime_root, "analyze", str(repo)),
        "resource_context_command": graph_resource_context_command(repo_name, graph_runtime_root),
        "context_command": graph_core_command(
            graph_runtime_root,
            "context",
            "<symbol_name_or_uid>",
            repo_cwd=repo,
        ),
        "query_command": graph_query_command(repo_name, graph_runtime_root),
        "impact_command": graph_impact_command(repo_name, graph_runtime_root),
    }


def graph_postflight_summary(repo: Path, graph_runtime_root: Path) -> dict:
    indexed = is_indexed(repo, graph_runtime_root)
    repo_name = indexed_repo_name(repo, graph_runtime_root)
    return {
        "repo": str(repo),
        "indexed": indexed,
        "graph_consumer_contract_version": "1.0",
        "postflight_sequence": []
        if not indexed
        else [
            "run detect-changes first to anchor the modified surface in current worktree reality",
            "if detect-changes returns concrete symbols or flows, use context or impact on those exact targets instead of running a broad query first",
            "only reread resource repo context when you need to summarize the repo-level picture after implementation",
        ],
        "recommended_commands": []
        if not indexed
        else [
            graph_core_command(graph_runtime_root, "detect-changes", repo_cwd=repo),
        ],
        "optional_followup_commands": []
        if not indexed
        else [
            graph_resource_context_command(repo_name, graph_runtime_root),
            graph_impact_command(repo_name, graph_runtime_root),
        ],
    }
