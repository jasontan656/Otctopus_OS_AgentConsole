from __future__ import annotations

import json
from pathlib import Path

from workflow_policy_contract import IMPLEMENTATION_SOURCE_POLICY

GRAPH_SKILL_SCRIPT = Path(
    "/home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-code-graph-base/scripts/meta_code_graph_base.py"
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


def graph_preflight_payload(repo: Path, allow_missing_index: bool, graph_runtime_root: Path) -> dict:
    indexed = is_indexed(repo, graph_runtime_root)
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
        "status_command": f"python3 {GRAPH_SKILL_SCRIPT} status",
        "analyze_command": f"python3 {GRAPH_SKILL_SCRIPT} analyze {repo}",
        "context_command": f"python3 {GRAPH_SKILL_SCRIPT} context --repo {repo}",
    }


def graph_postflight_payload(repo: Path, graph_runtime_root: Path) -> dict:
    indexed = is_indexed(repo, graph_runtime_root)
    return {
        "repo": str(repo),
        "indexed": indexed,
        "recommended_commands": []
        if not indexed
        else [
            f"python3 {GRAPH_SKILL_SCRIPT} detect-changes --repo {repo}",
            f"python3 {GRAPH_SKILL_SCRIPT} map {repo}",
            f"python3 {GRAPH_SKILL_SCRIPT} wiki {repo}",
        ],
    }
