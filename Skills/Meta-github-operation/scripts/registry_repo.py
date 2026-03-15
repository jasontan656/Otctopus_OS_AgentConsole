from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from runtime_contract_support import RegistryAlias, RegistryPayload, RemoteDescriptor, RemotePolicyPayload


@dataclass(frozen=True)
class RemoteSpec:
    name: str
    role: str
    automation_write_allowed: bool
    status: str
    manual_publish_allowed: bool = True
    disabled_reason: str | None = None
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class RepoSpec:
    name: str
    path: Path
    remotes: tuple[RemoteSpec, ...] = ()


def _resolve_product_root() -> Path:
    script_path = Path(__file__).resolve()
    repo_root = next((parent for parent in script_path.parents if parent.name == "Otctopus_OS_AgentConsole"), None)
    if repo_root is None:
        raise RuntimeError("cannot resolve product root from Meta-github-operation script path")
    return repo_root.parent


PRODUCT_ROOT = _resolve_product_root()
OCTOPUS_OS_REPO_ROOT = (PRODUCT_ROOT / "Octopus_OS").resolve()
PRODUCT_REPO_ROOT = (PRODUCT_ROOT / "Otctopus_OS_AgentConsole").resolve()


REPO_REGISTRY: dict[str, RepoSpec] = {}
REPO_REGISTRY: dict[str, RepoSpec] = {
    "Octopus_OS": RepoSpec(
        name="Octopus_OS",
        path=OCTOPUS_OS_REPO_ROOT,
        remotes=(
            RemoteSpec(
                name="origin",
                role="private_ai_daily_remote",
                automation_write_allowed=True,
                status="enabled",
                notes=(
                    "Repository is expected to remain closed-source/private.",
                    "Origin is reserved for AI daily iteration pushes and should point to the Octopus_OS_AI repository.",
                ),
            ),
            RemoteSpec(
                name="human-sync",
                role="private_human_explicit_remote",
                automation_write_allowed=False,
                manual_publish_allowed=True,
                status="enabled",
                notes=(
                    "Repository is expected to remain closed-source/private.",
                    "This remote should point to the Octopus_OS_humen repository.",
                    "Only use it when the human explicitly asks for a push.",
                ),
            ),
        ),
    ),
    "Otctopus_OS_AgentConsole": RepoSpec(
        name="Otctopus_OS_AgentConsole",
        path=PRODUCT_REPO_ROOT,
        remotes=(
            RemoteSpec(
                name="origin",
                role="private_ai_daily_remote",
                automation_write_allowed=True,
                status="enabled",
                notes=(
                    "Use for AI daily iteration pushes and same-turn Git traceability.",
                    "This remote should point to the Otctopus_OS_AgentConsole_AI_dev repository.",
                ),
            ),
            RemoteSpec(
                name="public-release",
                role="human_explicit_public_release_remote",
                automation_write_allowed=False,
                manual_publish_allowed=True,
                status="enabled",
                notes=(
                    "This remote is the open-source publication repository for Otctopus_OS_AgentConsole.",
                    "Only use it when the human explicitly asks for a push.",
                ),
            ),
        ),
    ),
}

REPO_ALIASES: dict[str, str] = {
    "octopus_os": "Octopus_OS",
    "skills_mirror": "Otctopus_OS_AgentConsole",
    "codex_skills_mirror": "Otctopus_OS_AgentConsole",
    "Codex_Skills_Mirror": "Otctopus_OS_AgentConsole",
    "otctopus_os_agent_console": "Otctopus_OS_AgentConsole",
}


def _remote_descriptor(remote: RemoteSpec) -> RemoteDescriptor:
    return {
        "name": remote.name,
        "role": remote.role,
        "automation_write_allowed": remote.automation_write_allowed,
        "manual_publish_allowed": remote.manual_publish_allowed,
        "status": remote.status,
        "disabled_reason": remote.disabled_reason,
        "notes": list(remote.notes),
    }


def registry_payload() -> RegistryPayload:
    aliases: list[RegistryAlias] = [
        {"alias": alias, "repo": canonical}
        for alias, canonical in sorted(REPO_ALIASES.items())
    ]
    return {
        "repos": [
            {
                "repo": spec.name,
                "path": str(spec.path),
                "remotes": [_remote_descriptor(remote) for remote in spec.remotes],
            }
            for spec in REPO_REGISTRY.values()
        ],
        "aliases": aliases,
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


def repo_spec_for_name(repo_name: str) -> RepoSpec:
    spec = REPO_REGISTRY.get(repo_name)
    if spec is None:
        raise ValueError(f"unknown repo: {repo_name}")
    return spec


def remote_policy_payload(repo_name: str) -> RemotePolicyPayload:
    spec = repo_spec_for_name(repo_name)
    return {
        "repo": spec.name,
        "repo_root": str(spec.path),
        "remotes": [_remote_descriptor(remote) for remote in spec.remotes],
    }


def ensure_remote_write_allowed(
    repo_name: str,
    remote_name: str,
    *,
    operation: str,
    human_explicit_request: bool = False,
) -> None:
    spec = REPO_REGISTRY.get(repo_name)
    if spec is None:
        return
    for remote in spec.remotes:
        if remote.name != remote_name:
            continue
        if remote.automation_write_allowed:
            return
        if remote.manual_publish_allowed and human_explicit_request:
            return
        if remote.manual_publish_allowed:
            raise ValueError(
                "remote_write_blocked: "
                f"repo={repo_name} remote={remote_name} operation={operation} "
                "reason=remote requires explicit human request"
            )
        reason = remote.disabled_reason or "remote write is disabled by current policy"
        raise ValueError(
            f"remote_write_blocked: repo={repo_name} remote={remote_name} operation={operation} reason={reason}"
        )
    if spec.remotes:
        raise ValueError(
            f"remote_write_blocked: repo={repo_name} remote={remote_name} operation={operation} "
            "reason=remote is not registered for write operations in the current policy"
        )
