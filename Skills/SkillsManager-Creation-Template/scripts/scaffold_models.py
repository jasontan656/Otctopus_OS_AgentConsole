from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TypedDict


DOC_TOPOLOGY_VALUES = ("inline", "referenced", "workflow_path")
TOOLING_SURFACE_VALUES = ("none", "contract_cli", "automation_cli")
WORKFLOW_CONTROL_VALUES = ("advisory", "guardrailed", "compiled")


@dataclass(frozen=True)
class SkillProfile:
    doc_topology: str
    tooling_surface: str
    workflow_control: str

    def as_dict(self) -> dict[str, str]:
        return {
            "doc_topology": self.doc_topology,
            "tooling_surface": self.tooling_surface,
            "workflow_control": self.workflow_control,
        }

    def key(self) -> str:
        return f"{self.doc_topology}:{self.tooling_surface}:{self.workflow_control}"


@dataclass(frozen=True)
class ScaffoldRequest:
    skill_name: str
    description: str
    target_root: Path
    profile: SkillProfile
    overwrite: bool = False

    @property
    def skill_root(self) -> Path:
        return self.target_root / self.skill_name

    @property
    def slug(self) -> str:
        value = self.skill_name.lower().replace(" ", "_").replace("-", "_")
        return "_".join(part for part in value.split("_") if part)


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
    notes: list[str]


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


class ProfileCatalogEntry(TypedDict):
    name: str
    profile: dict[str, str]
    recommended_for: str


class ProfileCatalogPayload(TypedDict):
    status: str
    default_profile: dict[str, str]
    profiles: list[ProfileCatalogEntry]


class ScaffoldResultPayload(TypedDict):
    status: str
    skill_root: str
    profile: dict[str, str]
    written_files: list[str]
