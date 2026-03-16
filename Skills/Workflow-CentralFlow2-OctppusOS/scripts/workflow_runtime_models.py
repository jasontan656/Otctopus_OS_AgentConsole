from __future__ import annotations

from typing import Literal, TypedDict


class SkillProfile(TypedDict):
    doc_topology: Literal["workflow_path"]
    tooling_surface: Literal["automation_cli"]
    workflow_control: Literal["compiled"]


class RuntimeSourcePolicy(TypedDict):
    primary_runtime_source: Literal["CLI_JSON"]
    human_markdown_role: str
    markdown_is_not_primary_instruction_source: bool


class ToolEntry(TypedDict):
    script: str
    commands: dict[str, str]


class ArtifactPolicy(TypedDict):
    mode: str
    resolver: str
    notes: list[str]


class RuntimeContractPayload(TypedDict):
    contract_name: str
    contract_version: str
    skill_name: str
    skill_profile: SkillProfile
    runtime_source_policy: RuntimeSourcePolicy
    tool_entry: ToolEntry
    artifact_policy: ArtifactPolicy
    entry_doc: str
    root_shape: list[str]
    commands: list[str]
    must_use_sequence: list[str]
    hard_constraints: list[str]


class ReadingSegment(TypedDict):
    source: str
    title: str
    content: str


class EntryNotFoundPayload(TypedDict):
    status: Literal["error"]
    error: Literal["entry_not_found"]
    entry: str
    available_entries: list[str]


class BranchSelectionPayload(TypedDict):
    status: Literal["branch_selection_required"]
    entry: str
    resolved_chain: list[str]
    segments: list[ReadingSegment]
    available_next: list[str]
    current_source: str


class CompiledReadingPayload(TypedDict):
    status: Literal["ok"]
    entry: str
    resolved_chain: list[str]
    segments: list[ReadingSegment]
    compiled_markdown: str


ReadingChainPayload = EntryNotFoundPayload | BranchSelectionPayload | CompiledReadingPayload
