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
    owner_surface: str
    canonical_fix_surface: str
    repair_boundary: str
    evidence_route: str


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


class AutoRepairRecord(TypedDict, total=False):
    optimization_id: str
    repair_type: str
    command: str
    workdir: str
    change_detection_root: str
    decision: str
    keyword_first_decision: str


class ExpectedFailureRule(TypedDict, total=False):
    rule_id: str
    stages: list[str]
    command_contains: list[str]
    output_contains: list[str]
    reason_codes: list[str]
    action: str
    reason: str


class ExpectedFailureMatch(TypedDict, total=False):
    matched: bool
    rule_id: str
    reason: str
    action: str


class CommandGovernanceContext(TypedDict, total=False):
    repo_root: str
    workdir: str
    change_detection_root: str
    backend_python: str


class CommandNormalizationResult(TypedDict, total=False):
    command: str
    normalized_command: str
    changed: bool
    repair_types: list[str]
    context: CommandGovernanceContext


class KeywordFirstReplacement(TypedDict, total=False):
    old: str
    new: str
    reason: str


class KeywordFirstEditDecision(TypedDict, total=False):
    decision: str
    rationale: str
    seamless_state: str
    requires_user_confirmation: bool
    confirmation_reason: str
    deletion_scope: list[str]
    replacement_pairs: list[KeywordFirstReplacement]
    forbidden_patterns_present: list[str]
    why_not_add: str


class PreExecCheckResult(TypedDict, total=False):
    status: str
    decision: str
    command: str
    normalized_command: str
    reason_code: str
    detail: str
    expected_failure: ExpectedFailureMatch
    repair_types: list[str]
    repair_context: CommandGovernanceContext
    keyword_first_edit: KeywordFirstEditDecision


class RuntimeFailureAnalysis(TypedDict, total=False):
    matched: bool
    issue_kind: str
    issue_subkind: str
    title: str
    summary: str
    why: str
    suggested_action: str
    adjudication: str
    expected_failure: ExpectedFailureMatch
    auto_repair: CommandNormalizationResult | dict[str, str]
    keyword_first_edit: KeywordFirstEditDecision


class OptimizationOpportunity(TypedDict, total=False):
    optimization_id: str
    classification: str
    kind: str
    optimization_level: str
    priority: str
    title: str
    summary: str
    evidence: list[str]
    current_approach: str
    better_pattern: str
    equivalence_conditions: list[str]
    exclusion_conditions: list[str]
    why_not_problem: str
    why_not_expected_failure: str
    knowledge_comparison_basis: str
    recommendation_class: str
    suggested_action: str
    recommendation_reason: str
    expected_benefit: str
    risk: str
    comparison_baseline: str
    should_recommend_execution: bool


class OptimizationAudit(TypedDict, total=False):
    status: str
    opportunity_count: int
    recommendation_buckets: dict[str, int]
    optimization_level_buckets: dict[str, int]
    opportunities: list[OptimizationOpportunity]
    summary: str


class TurnAuditCloseout(TypedDict, total=False):
    required: bool
    ran_at: str
    status: str


class TurnGroupSummary(TypedDict, total=False):
    group_count: int
    pending_group_count: int
    resolved_group_count: int


class RuntimePainBatchPayload(TypedDict, total=False):
    queue_summary: dict[str, object]
    group_summary: dict[str, object]
    source_mode: str


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


class WatcherState(TypedDict):
    schema_version: str
    codex_home: str
    updated_at: str
    file_cursors: dict[str, str]


class TurnHookAudit(TypedDict, total=False):
    schema_version: str
    session_id: str
    turn_id: str
    session_file: str
    started_at: str
    completed_at: str
    hook_mode: str
    hook_status: str
    source_mode: str
    cwd: str
    user_message: str
    issues_detected: int
    pending_issues: int
    resolved_optimization_ids: list[str]
    group_count: int
    groups: list[RuntimePainGroup]
    auto_repairs: list[AutoRepairRecord]
    repair_execution_v1: CommandExecutionResult
    issue_buckets: dict[str, int]
    keyword_first_buckets: dict[str, int]
    optimization_audit_v1: OptimizationAudit
    expected_failure_ids: list[str]
    strengthened_optimization_ids: list[str]
    pending_decision_ids: list[str]
    confirmation_required_ids: list[str]
    residual_risks: list[str]
    turn_audit_closeout: TurnAuditCloseout
    audit_recorded_at: str


class TurnHookResult(TypedDict, total=False):
    status: str
    hook_mode: str
    turn_hook_status: str
    session_id: str
    turn_id: str
    issues_detected: int
    pending_issues: int
    resolved_optimization_ids: list[str]
    turn_audit_path: str
    group_summary: TurnGroupSummary
    source_mode: str
    auto_repairs: list[AutoRepairRecord]
    repair_execution_v1: CommandExecutionResult
    issue_buckets: dict[str, int]
    keyword_first_buckets: dict[str, int]
    confirmation_required_ids: list[str]
    optimization_audit_v1: OptimizationAudit


class WatchSessionsResult(TypedDict, total=False):
    status: str
    codex_home: str
    processed_files: int
    processed_turns: list[TurnHookResult]
    watcher_state_json: str


class SessionExecEvent(TypedDict, total=False):
    session_id: str
    turn_id: str
    timestamp: str
    session_file: str
    citation: str
    cwd: str
    tool_name: str
    call_id: str
    raw_input: str
    command_preview: str
    command_signature: str
    trigger_script: str
    trigger_node: str
    output_preview: str
    output_raw: str
    status: str
    exit_code: int


class TurnEvidence(TypedDict, total=False):
    session_id: str
    turn_id: str
    session_file: str
    started_at: str
    completed_at: str
    cwd: str
    user_message: str
    assistant_messages: list[str]
    tool_events: list[SessionExecEvent]
    final_reply: str
    status: str


class SessionFallbackQueue(TypedDict, total=False):
    source_mode: str
    total_items: int
    pending_items: int
    resolved_items: int
    session_scope_mode: str
    thread_id: str
    items: list[dict[str, object]]


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
