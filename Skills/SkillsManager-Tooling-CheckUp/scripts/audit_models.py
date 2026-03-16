from __future__ import annotations

from dataclasses import dataclass
from typing import TypedDict


@dataclass(frozen=True)
class AuditIssue:
    scope: str
    severity: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return {
            "scope": self.scope,
            "severity": self.severity,
            "message": self.message,
        }


class RuntimeSourcePolicy(TypedDict, total=False):
    runtime_rule_source: str
    documents_are_source_of_truth: bool
    command_names_are_repo_local_convention: bool


class ToolEntry(TypedDict):
    commands: dict[str, str]


class ArtifactPolicyPayload(TypedDict, total=False):
    mode: str
    resolver: str
    notes: list[str]
    root: str


class RuntimeContractPayload(TypedDict, total=False):
    contract_name: str
    contract_version: str
    skill_name: str
    skill_role: str
    runtime_source_policy: RuntimeSourcePolicy
    tool_entry: ToolEntry
    artifact_policy: ArtifactPolicyPayload


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


class SurfaceProbe(TypedDict):
    scripts_present: bool
    cli_path: str | None
    runtime_contract_json: str | None
    tooling_docs_present: bool
    tests_present: bool


class AuditIssuePayload(TypedDict):
    scope: str
    severity: str
    message: str


class AuditPayload(TypedDict):
    status: str
    target_skill_root: str
    tooling_surface: str
    contract_source: str | None
    surface: SurfaceProbe
    issues: list[AuditIssuePayload]
    remediation_gate: list[str]
