from __future__ import annotations

from pathlib import Path
from typing import Protocol, TypedDict


class RuntimePainOptimizationRecord(TypedDict, total=False):
    optimization_id: str
    is_resolved: bool
    session_id: str
    thread_id: str


class RuntimePainEvent(TypedDict, total=False):
    command_preview: str
    command_signature: str
    command_preview_raw: str
    command_signature_raw: str
    outcome: str
    summary: str
    title: str
    tool_name: str
    why: str


class RuntimePainGroup(TypedDict, total=False):
    pain_group_key: str
    pain_topic: str
    priority_top: str
    pending_items: int
    problem_statement: str
    analysis: str
    remediation_plan: str
    latest_updated_at: str
    diagnosis_card_v2: dict[str, object]
    optimization_ids: list[RuntimePainOptimizationRecord]
    events: list[RuntimePainEvent]


class MemoryRuntimeResponse(TypedDict, total=False):
    status: str
    resolution_status: str
    memory_entry_id: str
    memory_path: str


class RepairWriteRecord(TypedDict, total=False):
    optimization_id: str
    group_key: str
    status: str
    error: str
    resolution_status: str
    resolution_summary: str
    memory_entry_id: str
    memory_path: str
    session_id: str
    thread_id: str


class RepairWriteResult(TypedDict, total=False):
    total_writes: int
    success_writes: int
    failed_writes: int
    writes: list[RepairWriteRecord]


class ChangeDetectionResult(TypedDict, total=False):
    change_detection_supported: bool
    repo_root: str
    all_changed_paths: list[str]
    all_changed_path_count: int


class CommandRunResult(TypedDict, total=False):
    index: int
    command: str
    status: str
    exit_code: int
    duration_sec: float
    stdout_preview: str
    stderr_preview: str
    changed_paths: list[str]
    changed_file_count: int
    preflight_reason_code: str


class CommandExecutionResult(TypedDict, total=False):
    total_commands: int
    success_commands: int
    failed_commands: int
    all_succeeded: bool
    change_detection_supported: bool
    runs: list[CommandRunResult]
    all_changed_paths: list[str]
    all_changed_path_count: int
    preflight_failed_commands: int
    preflight_reason_codes: list[str]


class RuntimePainBatchPayload(TypedDict, total=False):
    queue_summary: dict[str, object]
    group_summary: dict[str, object]


class RuntimePainBatchOutput(TypedDict, total=False):
    status: str
    runtime_pain_batch_selfcheck_v1: RuntimePainBatchPayload | dict[str, object]


class ObservabilityLogResult(TypedDict, total=False):
    status: str
    run_id: str
    machine_log_path: str
    human_log_path: str
    human_renderer: str
    error: str


class FocusGroupSummary(TypedDict, total=False):
    pain_group_key: str
    pain_topic: str
    priority_top: str
    pending_items: int
    selection_reason: str
    problem_statement: str
    first_evidence: dict[str, object]
    immediate_next_step: str
    what_we_were_doing: str
    expected_result: str
    actual_result: str
    why_this_created_hesitation: str
    strengthening_plan: str
    executive_summary: str
    decision_state: str
    how_to_fix_now: str
    adjudicated_directive_now: dict[str, object]
    route_now: dict[str, object]
    routing_table_preview: list[object]
    resolve_guard_summary: dict[str, object]
    before_state_v1: dict[str, object]
    after_state_target_v1: dict[str, object]
    change_manifest_v1: dict[str, object]
    reasoning_decision_recommendation: dict[str, object]
    meta_reasoningchain_v1: dict[str, object]
    target_state_after_fix: str
    expected_result_after_fix: str
    verification_next_check: str
    acceptance_preview: list[str]


class NarrativePackage(TypedDict, total=False):
    root_cause_hypotheses: list[str]
    action_plan_v1: list[dict[str, object]]
    acceptance_checks_v1: list[str]
    repair_strategy_v2: dict[str, object]
    manager_story_v1: dict[str, object]
    meta_reasoningchain_v1: dict[str, object]


class RunMemoryRuntime(Protocol):
    def __call__(self, memory_runtime: Path, args: list[str]) -> MemoryRuntimeResponse:
        ...
