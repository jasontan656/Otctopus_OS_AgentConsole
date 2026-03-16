from __future__ import annotations

import os
from pathlib import Path

# permission_boundary_markers:
#   - action
#   - actor_id
#   - role
#   - scope
#   - authz_result
#   - deny_code
#   - policy_version


def _candidate_workspace_roots(script_path: Path) -> list[Path]:
    candidates: list[Path] = []

    def add(path: Path | None) -> None:
        if path is None:
            return
        resolved = path.resolve()
        if resolved not in candidates:
            candidates.append(resolved)

    for env_key in ("OCTOPUS_WORKSPACE_ROOT", "AI_PROJECTS_ROOT", "WORKSPACE_ROOT"):
        raw = os.environ.get(env_key, "").strip()
        if raw:
            add(Path(raw))

    mdm_workspace_root = os.environ.get("MDM_WORKSPACE_ROOT", "").strip()
    if mdm_workspace_root:
        mdm_root = Path(mdm_workspace_root).expanduser().resolve()
        add(mdm_root / "AI_Projects")
        add(mdm_root)

    for parent in script_path.parents:
        if parent.name == "AI_Projects":
            add(parent)
        if parent.name == ".codex":
            add(parent.parent / "AI_Projects")
            add(parent.parent)

    add(Path.home() / "AI_Projects")
    add(Path.cwd())
    return candidates


def resolve_product_root() -> Path:
    script_path = Path(__file__).resolve()
    repo_root = next((parent for parent in script_path.parents if parent.name == "Otctopus_OS_AgentConsole"), None)
    if repo_root is not None:
        return repo_root.parent

    for workspace_root in _candidate_workspace_roots(script_path):
        candidate_repo = workspace_root / "Otctopus_OS_AgentConsole"
        if candidate_repo.exists():
            return workspace_root

    raise RuntimeError(
        "cannot resolve product root from Workflow-CentralFlow2-OctppusOS script path or workspace hints"
    )
