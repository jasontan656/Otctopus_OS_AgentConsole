#!/usr/bin/env python3
from __future__ import annotations

from datetime import datetime, timezone
from typing import TypeAlias, TypedDict, cast


SCHEMA_VERSION = "1.0.0"
AUDIT_SCHEMA_VERSION = "1.0.0"
WRITEBACK_DECISIONS = {"applied", "skipped", "deferred"}
TASK_STATUSES = {"active", "paused", "done", "archived"}
RUNTIME_STATUSES = {"idle", "active"}
SESSION_STATUSES = {"active", "completed"}
USER_TOP_LAYER_KEYS = {
    "long_term_objectives",
    "communication_style",
    "work_style",
    "collaboration_style",
    "global_preferences",
    "habit_patterns",
    "stable_constraints",
}
TASK_LAYER_KEYS = {
    "task_goal",
    "current_state",
    "working_style",
    "constraints",
    "mindset",
    "next_steps",
    "open_questions",
    "artifacts",
    "handoff_notes",
}
USER_MEMORY_KEYS = {"schema_version", "memory_kind", "updated_at", "top_layer"}
TASK_MEMORY_KEYS = {"schema_version", "memory_kind", "task_id", "title", "status", "updated_at", "task_layer"}
ACTIVE_TASK_KEYS = {"schema_version", "active_task_id", "updated_at"}
ACTIVE_RUNTIME_KEYS = {
    "schema_version",
    "status",
    "session_id",
    "turn_id",
    "active_task_id",
    "last_writeback_decision",
    "last_turn_audit_path",
    "updated_at",
}
SESSION_MEMORY_KEYS = {
    "schema_version",
    "session_id",
    "session_file",
    "started_at",
    "updated_at",
    "status",
    "current_task_id",
    "latest_turn_id",
    "turn_ids",
}
TURN_DELTA_KEYS = {
    "timestamp",
    "summary",
    "user_memory_updates",
    "task_memory_updates",
    "next_actions",
    "writeback_decision",
}
TURN_AUDIT_KEYS = {
    "schema_version",
    "session_id",
    "turn_id",
    "session_file",
    "started_at",
    "user_message",
    "task_id",
    "task_title",
    "turn_start_status",
    "turn_start_bound_at",
    "turn_start_compiled_at",
    "completed_at",
    "assistant_final_reply",
    "changed_paths",
    "validation_runs",
    "writeback_decision",
    "user_memory_updates",
    "task_memory_updates",
    "next_actions",
    "audit_recorded_at",
}
VALIDATION_RUN_KEYS = {"command", "result"}
WATCHER_STATE_KEYS = {"schema_version", "codex_home", "updated_at", "file_cursors"}


JsonScalar: TypeAlias = str | int | float | bool | None
JsonValue: TypeAlias = JsonScalar | list["JsonValue"] | dict[str, "JsonValue"]
JsonObject: TypeAlias = dict[str, JsonValue]
StringMap: TypeAlias = dict[str, str]


class UserTopLayerPayload(TypedDict):
    long_term_objectives: list[str]
    communication_style: list[str]
    work_style: list[str]
    collaboration_style: list[str]
    global_preferences: list[str]
    habit_patterns: list[str]
    stable_constraints: list[str]


class TaskLayerPayload(TypedDict):
    task_goal: str
    current_state: list[str]
    working_style: list[str]
    constraints: list[str]
    mindset: list[str]
    next_steps: list[str]
    open_questions: list[str]
    artifacts: list[str]
    handoff_notes: list[str]


class ActiveTaskPayload(TypedDict):
    schema_version: str
    active_task_id: str | None
    updated_at: str


class ActiveRuntimePayload(TypedDict):
    schema_version: str
    status: str
    session_id: str | None
    turn_id: str | None
    active_task_id: str | None
    last_writeback_decision: str | None
    last_turn_audit_path: str | None
    updated_at: str


class UserMemoryPayload(TypedDict):
    schema_version: str
    memory_kind: str
    updated_at: str
    top_layer: UserTopLayerPayload


class TaskMemoryPayload(TypedDict):
    schema_version: str
    memory_kind: str
    task_id: str
    title: str
    status: str
    updated_at: str
    task_layer: TaskLayerPayload


class TurnDeltaEntryPayload(TypedDict):
    timestamp: str
    summary: str
    user_memory_updates: list[str]
    task_memory_updates: list[str]
    next_actions: list[str]
    writeback_decision: str


class SessionMemoryPayload(TypedDict):
    schema_version: str
    session_id: str
    session_file: str
    started_at: str
    updated_at: str
    status: str
    current_task_id: str | None
    latest_turn_id: str | None
    turn_ids: list[str]


class ValidationRunPayload(TypedDict):
    command: str
    result: str


class TurnAuditPayload(TypedDict):
    schema_version: str
    session_id: str
    turn_id: str
    session_file: str
    started_at: str
    user_message: str
    task_id: str | None
    task_title: str | None
    turn_start_status: str
    turn_start_bound_at: str | None
    turn_start_compiled_at: str | None
    completed_at: str | None
    assistant_final_reply: str
    changed_paths: list[str]
    validation_runs: list[ValidationRunPayload]
    writeback_decision: str
    user_memory_updates: list[str]
    task_memory_updates: list[str]
    next_actions: list[str]
    audit_recorded_at: str


class WatcherStatePayload(TypedDict):
    schema_version: str
    codex_home: str
    updated_at: str
    file_cursors: StringMap


class WritebackPolicyPayload(TypedDict, total=False):
    turn_start: str
    turn_end: str


class CompiledMemoryPayload(TypedDict):
    skill_name: str
    compiled_at: str
    memory_definition: str
    active_task_id: str | None
    user_memory: UserMemoryPayload
    task_memory: TaskMemoryPayload | None
    writeback_policy: WritebackPolicyPayload
    ignore_by_default: list[str]


class MemoryValidationError(ValueError):
    """Raised when a runtime memory payload violates the governed schema."""


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def ensure_object(payload: object, label: str) -> JsonObject:
    if not isinstance(payload, dict):
        raise MemoryValidationError(f"{label} must be an object")
    return cast(JsonObject, payload)


def ensure_string(value: object, label: str, *, allow_empty: bool = False) -> str:
    if not isinstance(value, str):
        raise MemoryValidationError(f"{label} must be a string")
    normalized = value.strip()
    if not normalized and not allow_empty:
        raise MemoryValidationError(f"{label} must be non-empty")
    return normalized


def ensure_string_list(value: object, label: str) -> list[str]:
    if not isinstance(value, list):
        raise MemoryValidationError(f"{label} must be a list")
    normalized: list[str] = []
    seen: set[str] = set()
    for index, item in enumerate(value):
        if not isinstance(item, str):
            raise MemoryValidationError(f"{label}[{index}] must be a string")
        text = item.strip()
        if not text:
            raise MemoryValidationError(f"{label}[{index}] must be non-empty")
        if text in seen:
            continue
        seen.add(text)
        normalized.append(text)
    return normalized


def ensure_optional_string(value: object, label: str) -> str | None:
    if value is None:
        return None
    return ensure_string(value, label)


def ensure_string_mapping(value: object, label: str) -> StringMap:
    obj = ensure_object(value, label)
    normalized: StringMap = {}
    for key, item in obj.items():
        if not isinstance(key, str) or not key.strip():
            raise MemoryValidationError(f"{label} keys must be non-empty strings")
        normalized[key] = ensure_string(item, f"{label}.{key}", allow_empty=True)
    return normalized


def _ensure_exact_keys(payload: JsonObject, expected: set[str], label: str) -> None:
    keys = set(payload.keys())
    if keys != expected:
        missing = sorted(expected - keys)
        extra = sorted(keys - expected)
        problems: list[str] = []
        if missing:
            problems.append(f"missing={missing}")
        if extra:
            problems.append(f"extra={extra}")
        raise MemoryValidationError(f"{label} keys mismatch: {', '.join(problems)}")


def validate_active_task(payload: object) -> ActiveTaskPayload:
    obj = cast(ActiveTaskPayload, ensure_object(payload, "active_task"))
    _ensure_exact_keys(obj, ACTIVE_TASK_KEYS, "active_task")
    if obj["schema_version"] != SCHEMA_VERSION:
        raise MemoryValidationError("active_task.schema_version mismatch")
    if obj["active_task_id"] is not None:
        obj["active_task_id"] = ensure_string(obj["active_task_id"], "active_task.active_task_id")
    obj["updated_at"] = ensure_string(obj["updated_at"], "active_task.updated_at", allow_empty=True)
    return obj


def validate_user_memory(payload: object) -> UserMemoryPayload:
    obj = cast(UserMemoryPayload, ensure_object(payload, "user_memory"))
    _ensure_exact_keys(obj, USER_MEMORY_KEYS, "user_memory")
    if obj["schema_version"] != SCHEMA_VERSION:
        raise MemoryValidationError("user_memory.schema_version mismatch")
    if obj["memory_kind"] != "user":
        raise MemoryValidationError("user_memory.memory_kind must be 'user'")
    obj["updated_at"] = ensure_string(obj["updated_at"], "user_memory.updated_at", allow_empty=True)
    top_layer = cast(UserTopLayerPayload, ensure_object(obj["top_layer"], "user_memory.top_layer"))
    _ensure_exact_keys(top_layer, USER_TOP_LAYER_KEYS, "user_memory.top_layer")
    for key in sorted(USER_TOP_LAYER_KEYS):
        top_layer[key] = ensure_string_list(top_layer[key], f"user_memory.top_layer.{key}")
    obj["top_layer"] = top_layer
    return obj


def validate_task_memory(payload: object) -> TaskMemoryPayload:
    obj = cast(TaskMemoryPayload, ensure_object(payload, "task_memory"))
    _ensure_exact_keys(obj, TASK_MEMORY_KEYS, "task_memory")
    if obj["schema_version"] != SCHEMA_VERSION:
        raise MemoryValidationError("task_memory.schema_version mismatch")
    if obj["memory_kind"] != "task":
        raise MemoryValidationError("task_memory.memory_kind must be 'task'")
    obj["task_id"] = ensure_string(obj["task_id"], "task_memory.task_id")
    obj["title"] = ensure_string(obj["title"], "task_memory.title")
    obj["updated_at"] = ensure_string(obj["updated_at"], "task_memory.updated_at", allow_empty=True)
    status = ensure_string(obj["status"], "task_memory.status")
    if status not in TASK_STATUSES:
        raise MemoryValidationError(f"task_memory.status must be one of {sorted(TASK_STATUSES)}")
    obj["status"] = status
    task_layer = cast(TaskLayerPayload, ensure_object(obj["task_layer"], "task_memory.task_layer"))
    _ensure_exact_keys(task_layer, TASK_LAYER_KEYS, "task_memory.task_layer")
    task_layer["task_goal"] = ensure_string(task_layer["task_goal"], "task_memory.task_layer.task_goal", allow_empty=True)
    for key in sorted(TASK_LAYER_KEYS - {"task_goal"}):
        task_layer[key] = ensure_string_list(task_layer[key], f"task_memory.task_layer.{key}")
    obj["task_layer"] = task_layer
    return obj


def validate_turn_delta_entries(payload: object) -> list[TurnDeltaEntryPayload]:
    if not isinstance(payload, list):
        raise MemoryValidationError("turn_delta must be a list")
    entries: list[TurnDeltaEntryPayload] = []
    for index, item in enumerate(payload):
        entry = cast(TurnDeltaEntryPayload, ensure_object(item, f"turn_delta[{index}]"))
        _ensure_exact_keys(entry, TURN_DELTA_KEYS, f"turn_delta[{index}]")
        entry["timestamp"] = ensure_string(entry["timestamp"], f"turn_delta[{index}].timestamp")
        entry["summary"] = ensure_string(entry["summary"], f"turn_delta[{index}].summary")
        entry["user_memory_updates"] = ensure_string_list(
            entry["user_memory_updates"], f"turn_delta[{index}].user_memory_updates"
        )
        entry["task_memory_updates"] = ensure_string_list(
            entry["task_memory_updates"], f"turn_delta[{index}].task_memory_updates"
        )
        entry["next_actions"] = ensure_string_list(entry["next_actions"], f"turn_delta[{index}].next_actions")
        decision = ensure_string(entry["writeback_decision"], f"turn_delta[{index}].writeback_decision")
        if decision not in WRITEBACK_DECISIONS:
            raise MemoryValidationError(
                f"turn_delta[{index}].writeback_decision must be one of {sorted(WRITEBACK_DECISIONS)}"
            )
        entry["writeback_decision"] = decision
        entries.append(entry)
    return entries


def validate_active_runtime(payload: object) -> ActiveRuntimePayload:
    obj = cast(ActiveRuntimePayload, ensure_object(payload, "active_runtime"))
    _ensure_exact_keys(obj, ACTIVE_RUNTIME_KEYS, "active_runtime")
    if obj["schema_version"] != AUDIT_SCHEMA_VERSION:
        raise MemoryValidationError("active_runtime.schema_version mismatch")
    status = ensure_string(obj["status"], "active_runtime.status")
    if status not in RUNTIME_STATUSES:
        raise MemoryValidationError(f"active_runtime.status must be one of {sorted(RUNTIME_STATUSES)}")
    obj["status"] = status
    obj["session_id"] = ensure_optional_string(obj["session_id"], "active_runtime.session_id")
    obj["turn_id"] = ensure_optional_string(obj["turn_id"], "active_runtime.turn_id")
    obj["active_task_id"] = ensure_optional_string(obj["active_task_id"], "active_runtime.active_task_id")
    decision = ensure_optional_string(obj["last_writeback_decision"], "active_runtime.last_writeback_decision")
    if decision is not None and decision not in WRITEBACK_DECISIONS:
        raise MemoryValidationError(
            f"active_runtime.last_writeback_decision must be one of {sorted(WRITEBACK_DECISIONS)}"
        )
    obj["last_writeback_decision"] = decision
    obj["last_turn_audit_path"] = ensure_optional_string(obj["last_turn_audit_path"], "active_runtime.last_turn_audit_path")
    obj["updated_at"] = ensure_string(obj["updated_at"], "active_runtime.updated_at", allow_empty=True)
    return obj


def validate_session_memory(payload: object) -> SessionMemoryPayload:
    obj = cast(SessionMemoryPayload, ensure_object(payload, "session_memory"))
    _ensure_exact_keys(obj, SESSION_MEMORY_KEYS, "session_memory")
    if obj["schema_version"] != AUDIT_SCHEMA_VERSION:
        raise MemoryValidationError("session_memory.schema_version mismatch")
    obj["session_id"] = ensure_string(obj["session_id"], "session_memory.session_id")
    obj["session_file"] = ensure_string(obj["session_file"], "session_memory.session_file")
    obj["started_at"] = ensure_string(obj["started_at"], "session_memory.started_at", allow_empty=True)
    obj["updated_at"] = ensure_string(obj["updated_at"], "session_memory.updated_at", allow_empty=True)
    status = ensure_string(obj["status"], "session_memory.status")
    if status not in SESSION_STATUSES:
        raise MemoryValidationError(f"session_memory.status must be one of {sorted(SESSION_STATUSES)}")
    obj["status"] = status
    obj["current_task_id"] = ensure_optional_string(obj["current_task_id"], "session_memory.current_task_id")
    obj["latest_turn_id"] = ensure_optional_string(obj["latest_turn_id"], "session_memory.latest_turn_id")
    obj["turn_ids"] = ensure_string_list(obj["turn_ids"], "session_memory.turn_ids")
    return obj


def validate_validation_runs(payload: object) -> list[ValidationRunPayload]:
    if not isinstance(payload, list):
        raise MemoryValidationError("validation_runs must be a list")
    runs: list[ValidationRunPayload] = []
    for index, item in enumerate(payload):
        run = cast(ValidationRunPayload, ensure_object(item, f"validation_runs[{index}]"))
        _ensure_exact_keys(run, VALIDATION_RUN_KEYS, f"validation_runs[{index}]")
        runs.append(
            ValidationRunPayload(
                command=ensure_string(run["command"], f"validation_runs[{index}].command"),
                result=ensure_string(run["result"], f"validation_runs[{index}].result"),
            )
        )
    return runs


def validate_turn_audit(payload: object) -> TurnAuditPayload:
    obj = cast(TurnAuditPayload, ensure_object(payload, "turn_audit"))
    _ensure_exact_keys(obj, TURN_AUDIT_KEYS, "turn_audit")
    if obj["schema_version"] != AUDIT_SCHEMA_VERSION:
        raise MemoryValidationError("turn_audit.schema_version mismatch")
    obj["session_id"] = ensure_string(obj["session_id"], "turn_audit.session_id")
    obj["turn_id"] = ensure_string(obj["turn_id"], "turn_audit.turn_id")
    obj["session_file"] = ensure_string(obj["session_file"], "turn_audit.session_file")
    obj["started_at"] = ensure_string(obj["started_at"], "turn_audit.started_at", allow_empty=True)
    obj["user_message"] = ensure_string(obj["user_message"], "turn_audit.user_message", allow_empty=True)
    obj["task_id"] = ensure_optional_string(obj["task_id"], "turn_audit.task_id")
    obj["task_title"] = ensure_optional_string(obj["task_title"], "turn_audit.task_title")
    obj["turn_start_status"] = ensure_string(obj["turn_start_status"], "turn_audit.turn_start_status")
    obj["turn_start_bound_at"] = ensure_optional_string(obj["turn_start_bound_at"], "turn_audit.turn_start_bound_at")
    obj["turn_start_compiled_at"] = ensure_optional_string(
        obj["turn_start_compiled_at"], "turn_audit.turn_start_compiled_at"
    )
    obj["completed_at"] = ensure_optional_string(obj["completed_at"], "turn_audit.completed_at")
    obj["assistant_final_reply"] = ensure_string(
        obj["assistant_final_reply"], "turn_audit.assistant_final_reply", allow_empty=True
    )
    obj["changed_paths"] = ensure_string_list(obj["changed_paths"], "turn_audit.changed_paths")
    obj["validation_runs"] = validate_validation_runs(obj["validation_runs"])
    decision = ensure_string(obj["writeback_decision"], "turn_audit.writeback_decision")
    if decision not in WRITEBACK_DECISIONS:
        raise MemoryValidationError(f"turn_audit.writeback_decision must be one of {sorted(WRITEBACK_DECISIONS)}")
    obj["writeback_decision"] = decision
    obj["user_memory_updates"] = ensure_string_list(obj["user_memory_updates"], "turn_audit.user_memory_updates")
    obj["task_memory_updates"] = ensure_string_list(obj["task_memory_updates"], "turn_audit.task_memory_updates")
    obj["next_actions"] = ensure_string_list(obj["next_actions"], "turn_audit.next_actions")
    obj["audit_recorded_at"] = ensure_string(obj["audit_recorded_at"], "turn_audit.audit_recorded_at", allow_empty=True)
    return obj


def validate_watcher_state(payload: object) -> WatcherStatePayload:
    obj = cast(WatcherStatePayload, ensure_object(payload, "watcher_state"))
    _ensure_exact_keys(obj, WATCHER_STATE_KEYS, "watcher_state")
    if obj["schema_version"] != AUDIT_SCHEMA_VERSION:
        raise MemoryValidationError("watcher_state.schema_version mismatch")
    obj["codex_home"] = ensure_string(obj["codex_home"], "watcher_state.codex_home", allow_empty=True)
    obj["updated_at"] = ensure_string(obj["updated_at"], "watcher_state.updated_at", allow_empty=True)
    obj["file_cursors"] = ensure_string_mapping(obj["file_cursors"], "watcher_state.file_cursors")
    return obj


def validate_compiled_memory(payload: object) -> CompiledMemoryPayload:
    obj = cast(CompiledMemoryPayload, ensure_object(payload, "compiled_memory"))
    required_keys = {
        "skill_name",
        "compiled_at",
        "memory_definition",
        "active_task_id",
        "user_memory",
        "task_memory",
        "writeback_policy",
        "ignore_by_default",
    }
    _ensure_exact_keys(obj, required_keys, "compiled_memory")
    obj["skill_name"] = ensure_string(obj["skill_name"], "compiled_memory.skill_name")
    obj["compiled_at"] = ensure_string(obj["compiled_at"], "compiled_memory.compiled_at")
    obj["memory_definition"] = ensure_string(obj["memory_definition"], "compiled_memory.memory_definition")
    if obj["active_task_id"] is not None:
        obj["active_task_id"] = ensure_string(obj["active_task_id"], "compiled_memory.active_task_id")
    obj["user_memory"] = validate_user_memory(obj["user_memory"])
    if obj["task_memory"] is not None:
        obj["task_memory"] = validate_task_memory(obj["task_memory"])
    obj["writeback_policy"] = cast(
        WritebackPolicyPayload, ensure_object(obj["writeback_policy"], "compiled_memory.writeback_policy")
    )
    obj["ignore_by_default"] = ensure_string_list(obj["ignore_by_default"], "compiled_memory.ignore_by_default")
    return obj
