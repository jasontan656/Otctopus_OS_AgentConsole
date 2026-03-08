from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RepoSpec:
    name: str
    path: Path


REPO_REGISTRY = {
    "Codex_Skills_Mirror": RepoSpec("Codex_Skills_Mirror", Path("/home/jasontan656/AI_Projects/Codex_Skills_Mirror")),
    "OctuposOS_RunTime_Frontend": RepoSpec("OctuposOS_RunTime_Frontend", Path("/home/jasontan656/AI_Projects/OctuposOS_RunTime_Frontend")),
    "Octopus_CodeBase_Backend": RepoSpec("Octopus_CodeBase_Backend", Path("/home/jasontan656/AI_Projects/Octopus_CodeBase_Backend")),
    "OctuposOS_Runtime_Backend": RepoSpec("OctuposOS_Runtime_Backend", Path("/home/jasontan656/AI_Projects/OctuposOS_Runtime_Backend")),
    "Octopus_CodeBase_Frontend": RepoSpec("Octopus_CodeBase_Frontend", Path("/home/jasontan656/AI_Projects/Octopus_CodeBase_Frontend")),
}

REPO_ALIASES = {
    "Octopus_CodeBase": "Octopus_CodeBase_Backend",
    "OctuposOS_Runtime": "OctuposOS_Runtime_Backend",
    "OctuposOS_Runtime_Frontend": "OctuposOS_RunTime_Frontend",
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
    if repo_name and repo_path:
        raise ValueError("pass either --repo or --repo-path, not both")
    if repo_path:
        return ("custom", Path(repo_path).expanduser().resolve())
    if repo_name is None:
        raise ValueError("one of --repo or --repo-path is required")
    canonical_name = REPO_ALIASES.get(repo_name, repo_name)
    spec = REPO_REGISTRY.get(canonical_name)
    if spec is None:
        raise ValueError(f"unknown repo identifier: {repo_name}")
    return (spec.name, spec.path)
