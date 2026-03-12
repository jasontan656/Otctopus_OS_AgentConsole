from __future__ import annotations

from typing import Literal, NotRequired, TypeAlias, TypedDict


class CommandSpec(TypedDict):
    name: str
    role: str


class RuntimeGovernancePayload(TypedDict):
    skill_runtime_root: str
    claims_dir: str
    result_root: str
    push_lock_dir: str
    runtime_log_policy: str
    result_policy: str
    legacy_runtime_fallbacks: list[str]
    migration_note: str


class RemotePolicyEntry(TypedDict):
    role: str
    automation_write_allowed: bool
    status: str
    manual_publish_allowed: NotRequired[bool]
    disabled_reason: NotRequired[str]
    notes: NotRequired[list[str]]


RemotePolicyMatrix: TypeAlias = dict[str, dict[str, RemotePolicyEntry]]


class ReleaseRemoteState(TypedDict):
    status: str
    disabled_reason: str


ReleasePublicationState: TypeAlias = dict[str, dict[str, ReleaseRemoteState]]


class PushContractPayload(TypedDict):
    contract_name: str
    contract_version: str
    validation_mode: str
    required_fields: list[str]
    optional_fields: list[str]
    entry: str
    purpose: str
    allowed_repos: list[str]
    commands: list[CommandSpec]
    remote_policy: RemotePolicyMatrix
    runtime_governance: RuntimeGovernancePayload
    rules: list[str]


class RollbackContractPayload(TypedDict):
    contract_name: str
    contract_version: str
    validation_mode: str
    required_fields: list[str]
    optional_fields: list[str]
    entry: str
    purpose: str
    allowed_repos: list[str]
    commands: list[CommandSpec]
    runtime_governance: RuntimeGovernancePayload
    rules: list[str]


class BaselineContractPayload(TypedDict):
    contract_name: str
    contract_version: str
    validation_mode: str
    required_fields: list[str]
    optional_fields: list[str]
    entry: str
    purpose: str
    allowed_repos: list[str]
    commands: list[CommandSpec]
    release_publication_state: ReleasePublicationState
    runtime_governance: RuntimeGovernancePayload
    rules: list[str]


class RemoteDescriptor(TypedDict):
    name: str
    role: str
    automation_write_allowed: bool
    manual_publish_allowed: bool
    status: str
    disabled_reason: str | None
    notes: list[str]


class RepoDescriptor(TypedDict):
    repo: str
    path: str
    remotes: list[RemoteDescriptor]


class RegistryAlias(TypedDict):
    alias: str
    repo: str


class RegistryPayload(TypedDict):
    repos: list[RepoDescriptor]
    aliases: list[RegistryAlias]


class RemotePolicyPayload(TypedDict):
    repo: str
    repo_root: str
    remotes: list[RemoteDescriptor]


class StatusEntry(TypedDict):
    status: str
    path: str


class AheadBehindPayload(TypedDict):
    behind: int
    ahead: int


class RepoStatusPayload(TypedDict):
    repo_root: str
    branch: str
    upstream: str | None
    ahead_behind: AheadBehindPayload | None
    dirty: bool
    staged_paths: list[str]
    entries: list[StatusEntry]


class GitRemoteUrl(TypedDict):
    remote: str
    url: str
    kind: str


class CommitResult(TypedDict):
    commit: str


class PushResult(TypedDict):
    remote: str
    branch: str
    force_with_lease: bool


class FetchResult(TypedDict):
    remote: str


class PullRebaseResult(TypedDict):
    remote: str
    branch: str


class TagResult(TypedDict):
    tag: str
    target_commit: str


class PushTagResult(TypedDict):
    remote: str
    tag: str


class CommitScopeAll(TypedDict):
    mode: Literal["all"]


class CommitScopeStaged(TypedDict):
    mode: Literal["staged"]


class CommitScopePaths(TypedDict):
    mode: Literal["paths"]
    paths: list[str]
    claims_file: NotRequired[str]


CommitScope: TypeAlias = CommitScopeAll | CommitScopeStaged | CommitScopePaths


class RollbackSyncAllPayload(TypedDict):
    to_ref: str
    mode: Literal["all"]
    paths: list[str]
    restored_paths: list[str]
    removed_paths: list[str]
    pruned_empty_dirs: list[str]


class RollbackSyncPathsPayload(TypedDict):
    to_ref: str
    mode: Literal["paths"]
    paths: list[str]
    restored_paths: list[str]
    removed_paths: list[str]
    pruned_empty_dirs: list[str]


RollbackSyncPayload: TypeAlias = RollbackSyncAllPayload | RollbackSyncPathsPayload


class RollbackPathsPayload(RollbackSyncPathsPayload):
    command: Literal["rollback-paths"]
