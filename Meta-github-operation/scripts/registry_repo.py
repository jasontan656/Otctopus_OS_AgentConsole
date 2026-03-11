from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RepoSpec:
    name: str
    path: Path


REPO_REGISTRY: dict[str, RepoSpec] = {}
REPO_REGISTRY: dict[str, RepoSpec] = {
    "Octopus_OS": RepoSpec(
        name="Octopus_OS",
        path=Path("/home/jasontan656/AI_Projects/Octopus_OS"),
    ),
    "octopus-os-agent-console": RepoSpec(
        name="octopus-os-agent-console",
        path=Path("/home/jasontan656/AI_Projects/octopus-os-agent-console"),
    ),
}

REPO_ALIASES: dict[str, str] = {
    "octopus_os": "Octopus_OS",
    "skills_mirror": "octopus-os-agent-console",
    "codex_skills_mirror": "octopus-os-agent-console",
    "Codex_Skills_Mirror": "octopus-os-agent-console",
    "octopus_os_agent_console": "octopus-os-agent-console",
}


def registry_payload() -> dict[str, object]:
    return {
        "repos": [
            {"repo": spec.name, "path": str(spec.path)}
            for spec in REPO_REGISTRY.values()
        ],
        "aliases": [
            {"alias": alias, "repo": canonical}
            for alias, canonical in sorted(REPO_ALIASES.items())
        ],
    }


def resolve_repo(repo_name: str | None, repo_path: str | None) -> tuple[str, Path]:
    if repo_name:
        canonical = REPO_ALIASES.get(repo_name, repo_name)
        spec = REPO_REGISTRY.get(canonical)
        if spec is None:
            raise ValueError(f"unknown repo: {repo_name}")
        return spec.name, spec.path
    if repo_path:
        path = Path(repo_path).expanduser().resolve()
        for spec in REPO_REGISTRY.values():
            if spec.path.resolve() == path:
                return spec.name, spec.path
        return path.name, path
    raise ValueError("either --repo or --repo-path is required")
