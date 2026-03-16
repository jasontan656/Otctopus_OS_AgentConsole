from __future__ import annotations

from dataclasses import dataclass
from typing import TypedDict


@dataclass(frozen=True)
class TargetProfile:
    doc_topology: str
    tooling_surface: str
    workflow_control: str
    source: str

    def as_dict(self) -> dict[str, str]:
        return {
            "doc_topology": self.doc_topology,
            "tooling_surface": self.tooling_surface,
            "workflow_control": self.workflow_control,
            "source": self.source,
        }


@dataclass(frozen=True)
class Issue:
    scope: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return {"scope": self.scope, "message": self.message}


class RuntimeSourcePolicy(TypedDict, total=False):
    runtime_rule_source: str
    documents_are_source_of_truth: bool
    command_names_are_repo_local_convention: bool


class ToolEntry(TypedDict):
    script: str
    commands: dict[str, str]


class ArtifactPolicyPayload(TypedDict, total=False):
    mode: str
    resolver: str


class RuntimeContractPayload(TypedDict, total=False):
    contract_name: str
    contract_version: str
    skill_name: str
    skill_role: str
    runtime_source_policy: RuntimeSourcePolicy
    profile_support: dict[str, list[str]]
    tool_entry: ToolEntry
    artifact_policy: ArtifactPolicyPayload
    hard_constraints: list[str]


class DirectiveIndexEntry(TypedDict):
    doc_kind: str
    json_path: str
    human_path: str


class DirectiveIndexPayload(TypedDict):
    topics: dict[str, DirectiveIndexEntry]


class DirectivePayload(TypedDict, total=False):
    directive_name: str
    directive_version: str
    doc_kind: str
    topic: str
    purpose: str
    instruction: list[str]
    workflow: list[str]
    rules: list[str]


class InspectPayload(TypedDict):
    status: str
    target_root: str
    profile: dict[str, str]
    root_entries: list[str]
    available_context_entries: list[str]


class LintIssuePayload(TypedDict):
    scope: str
    message: str


class LintPayload(TypedDict):
    status: str
    target_root: str
    profile: dict[str, str]
    issues: list[LintIssuePayload]


class CompiledSegment(TypedDict):
    source: str
    content: str


class CompilePayload(TypedDict, total=False):
    status: str
    target_root: str
    profile: dict[str, str]
    entry: str
    error: str
    available_entries: list[str]
    available_next: list[str]
    current_source: str
    resolved_chain: list[str]
    segments: list[CompiledSegment]
    compiled_markdown: str
