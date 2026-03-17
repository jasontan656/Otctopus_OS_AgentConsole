from __future__ import annotations

from typing import NotRequired, TypedDict


class StageMetadata(TypedDict):
    purpose: str
    entry_requirements: list[str]
    required_objects: list[str]
    required_artifacts: list[str]
    writeback_targets: list[str]
    lint_focus: list[str]


class RuntimeContractPayload(TypedDict):
    status: str
    skill_name: str
    skill_mode: str
    root_shape: list[str]
    entry_doc: str
    commands: list[str]
    stage_order: list[str]
    workspace_layout: dict[str, str]
    stage_artifacts: dict[str, str]
    layout_rule: str
    compiler_rule: str
    artifact_managed_root: str
    task_runtime_root: str
    artifact_write_policy: str
    task_runtime_policy: str
    artifact_handoff_commands: dict[str, str]


class ReadingChainSegment(TypedDict):
    source: str
    title: str
    content: str


class ReadingChainPayload(TypedDict):
    status: str
    entry: str
    resolved_chain: NotRequired[list[str]]
    segments: NotRequired[list[ReadingChainSegment]]
    compiled_markdown: NotRequired[str]
    error: NotRequired[str]
    available_entries: NotRequired[list[str]]
    available_next: NotRequired[list[str]]
    current_source: NotRequired[str]


class StageChecklistPayload(StageMetadata):
    stage: str
    workspace_layout: dict[str, str]
    stage_artifacts: dict[str, str]


class LintMessage(TypedDict):
    code: str
    source: str
    message: str


class BoundaryErrorPayload(TypedDict):
    status: str
    reason: str
    workspace_root: str
    managed_root: str
    message: str
    artifact_handoff_commands: dict[str, str]


class WorkspaceScaffoldPayload(TypedDict):
    status: str
    workspace_root: str
    requested_workspace_root: str
    created_files: list[str]
    skipped_files: list[str]
    workspace_layout: dict[str, str]
    stage_artifacts: dict[str, str]
    reason: NotRequired[str]
    task_runtime_root: NotRequired[str]
    open_tasks: NotRequired[list[dict[str, str]]]
    message: NotRequired[str]


class CheckedFilesPayload(TypedDict):
    manifest: str
    evidence_registry: str
    architect_assessment: str
    preview_projection: str
    design_decisions: str
    impact_map: str
    milestone_packages: str
    implementation_ledger: str
    artifact_research: str
    artifact_architect: str
    artifact_preview: str
    artifact_design: str
    artifact_impact: str
    artifact_plan: str
    artifact_implementation: str
    artifact_validation: str
    artifact_final_delivery: str


class StageLintPayload(TypedDict):
    status: str
    stage: str
    workspace_root: str
    errors: list[LintMessage]
    warnings: list[LintMessage]
    checked_files: CheckedFilesPayload
    reason: NotRequired[str]
    managed_root: NotRequired[str]
    message: NotRequired[str]
    artifact_handoff_commands: NotRequired[dict[str, str]]


class TaskGateWarning(TypedDict):
    code: str
    message: str


class OpenTaskPayload(TypedDict):
    task_root: str
    reason: NotRequired[str]
    resume_hint: str
    task_id: NotRequired[str]
    task_status: NotRequired[str]
    current_stage: NotRequired[str]
    current_step: NotRequired[str]
    ended_stage: NotRequired[str]
    ended_step: NotRequired[str]
    detail: NotRequired[str]


class TaskGateCheckPayload(TypedDict):
    status: str
    reason: str
    task_runtime_root: str
    open_tasks: list[OpenTaskPayload]
    warnings: list[TaskGateWarning]


class TaskRuntimeScaffoldPayload(TypedDict):
    status: str
    task_root: str
    task_runtime_file: str
    task_id: str
    task_runtime_root: str
    workspace_root: str
    reused_existing: bool
