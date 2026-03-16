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


class CreationChainPosition(TypedDict):
    recommended_order: list[str]
    insert_before: str
    insert_after: str


class RunstateContractSchema(TypedDict):
    governed_type_values: list[str]
    checklist_fields: list[str]
    behavior_flags: list[str]


class RuntimeContractPayload(TypedDict, total=False):
    contract_name: str
    contract_version: str
    skill_name: str
    skill_role: str
    runtime_source_policy: RuntimeSourcePolicy
    profile_support: dict[str, list[str]]
    creation_chain_position: CreationChainPosition
    tool_entry: ToolEntry
    runstate_contract_schema: RunstateContractSchema
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


class GovernedTypeDefinition(TypedDict):
    governed_type: str
    applicability: str
    required_checklists: list[str]
    template_files: list[str]
    success_criteria: list[str]


class ProfilePayload(TypedDict):
    doc_topology: str
    tooling_surface: str
    workflow_control: str


class InspectPayload(TypedDict, total=False):
    status: str
    target_skill_root: str
    skill_name: str
    profile: ProfilePayload
    governed_type: str
    applicability: str
    detection_source: str
    reasons: list[str]
    required_checklists: list[str]
    template_files: list[str]
    success_criteria: list[str]


class ScaffoldPayload(TypedDict, total=False):
    status: str
    target_skill_root: str
    skill_name: str
    governed_type: str
    applicability: str
    written_files: list[str]
    skipped: bool
    message: str


class AuditPayload(TypedDict, total=False):
    status: str
    target_skill_root: str
    skill_name: str
    governed_type: str
    applicability: str
    issues: list[dict[str, str]]
    remediation_gate: list[str]
    evidence: dict[str, object]
