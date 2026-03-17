#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import time
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Any

from memory_bind_task import bind_task
from memory_bind_task import normalize_task_id
from memory_compile import compile_active_memory
from memory_models import AUDIT_SCHEMA_VERSION
from memory_models import SessionMemoryPayload
from memory_models import TurnAuditPayload
from memory_models import iso_now
from memory_store import active_runtime_path
from memory_store import active_task_path
from memory_store import compiled_active_memory_json_path
from memory_store import ensure_store_exists
from memory_store import human_log_path
from memory_store import load_session_memory
from memory_store import load_task_memory
from memory_store import load_turn_audit
from memory_store import load_turn_delta
from memory_store import load_watcher_state
from memory_store import machine_log_path
from memory_store import result_root
from memory_store import save_active_runtime
from memory_store import save_session_memory
from memory_store import save_task_memory
from memory_store import save_turn_audit
from memory_store import save_turn_delta
from memory_store import save_watcher_state
from memory_store import session_memory_json_path
from memory_store import sessions_root
from memory_store import task_memory_json_path
from memory_store import tasks_root
from memory_store import turn_audit_json_path
from memory_store import turn_delta_json_path
from memory_store import watcher_state_json_path


VALIDATION_HINT_RE = re.compile(r"\b(pytest|vitest|ruff|eslint|npm test|pnpm test|cargo test|stage-lint)\b", re.I)
SESSION_ID_RE = re.compile(r"([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$")
ABSOLUTE_PATH_RE = re.compile(r"(/[^ \n\t\"']+)")
RESULT_LINE_RE = re.compile(r"Process exited with code (?P<code>\d+)")
PATCH_STATUS_LINE_RE = re.compile(r"^(?P<status>[ACDMRTU])\s+(?P<path>.+?)\s*$", re.M)


@dataclass
class PendingTool:
    call_id: str
    tool_type: str
    name: str
    raw_input: str


@dataclass
class LiveTurn:
    session_id: str
    turn_id: str
    session_file: str
    started_at: str
    cwd: str | None = None
    user_message: str = ""
    task_id: str | None = None
    task_title: str | None = None
    turn_start_bound_at: str | None = None
    turn_start_compiled_at: str | None = None
    assistant_messages: list[str] = field(default_factory=list)
    changed_paths: list[str] = field(default_factory=list)
    validation_runs: list[dict[str, str]] = field(default_factory=list)
    pending_tools: dict[str, PendingTool] = field(default_factory=dict)


def resolve_codex_home(override: str | None) -> Path:
    if override:
        candidate = Path(os.path.expanduser(override))
        candidate.mkdir(parents=True, exist_ok=True)
        return candidate.resolve()
    candidates: list[Path] = []
    script_path = Path(__file__).resolve()
    repo_root = next((parent for parent in script_path.parents if parent.name == "Otctopus_OS_AgentConsole"), None)
    if repo_root is not None:
        candidates.append((repo_root.parent / ".codex").resolve())
    env_home = os.getenv("CODEX_HOME")
    if env_home:
        candidates.append(Path(os.path.expanduser(env_home)))
    candidates.append(Path.home() / ".codex")
    for candidate in candidates:
        if candidate.exists() and candidate.is_dir():
            return candidate.resolve()
    raise FileNotFoundError("Cannot resolve Codex home from override, workspace, $CODEX_HOME, or ~/.codex")


def find_session_files(codex_home: Path, session_id_filter: str | None = None) -> list[Path]:
    sessions_path = codex_home / "sessions"
    if not sessions_path.exists():
        return []
    if session_id_filter:
        pattern = f"*{session_id_filter}*.jsonl"
        return sorted(path for path in sessions_path.rglob(pattern) if path.is_file())
    return sorted(path for path in sessions_path.rglob("*.jsonl") if path.is_file())


def _session_id_from_path(path: Path) -> str | None:
    match = SESSION_ID_RE.search(path.stem)
    if match:
        return match.group(1)
    return None


def _trim_text(text: str, max_len: int = 240) -> str:
    clean = re.sub(r"\s+", " ", text.strip())
    if len(clean) <= max_len:
        return clean
    return clean[: max_len - 3] + "..."


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        text = item.strip()
        if not text or text in seen:
            continue
        seen.add(text)
        result.append(text)
    return result


def _append_machine_event(event_type: str, payload: dict[str, Any]) -> None:
    machine_log_path().parent.mkdir(parents=True, exist_ok=True)
    record = {"timestamp": iso_now(), "event": event_type, "payload": payload}
    with machine_log_path().open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def _append_human_log(message: str) -> None:
    human_log_path().parent.mkdir(parents=True, exist_ok=True)
    with human_log_path().open("a", encoding="utf-8") as handle:
        handle.write(f"[{iso_now()}] {message}\n")


def _derive_task_title(user_message: str) -> str:
    for raw_line in user_message.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        line = re.sub(r"^[#>*\-\d\.\s]+", "", line).strip()
        if line:
            return _trim_text(line, max_len=96)
    return "session-task"


def _derive_task_id(session_id: str, title: str) -> str:
    try:
        slug = normalize_task_id(title or "session-task")
    except ValueError:
        slug = "session-task"
    session_prefix = session_id.split("-")[0]
    return f"{slug[:48]}-{session_prefix}"


def _load_or_create_session_memory(session_id: str, session_file: str, started_at: str) -> SessionMemoryPayload:
    path = session_memory_json_path(session_id)
    if path.exists():
        payload = load_session_memory(session_id)
        if payload["session_file"] != session_file:
            payload["session_file"] = session_file
            payload = save_session_memory(payload)
        return payload
    payload = {
        "schema_version": AUDIT_SCHEMA_VERSION,
        "session_id": session_id,
        "session_file": session_file,
        "started_at": started_at,
        "updated_at": started_at,
        "status": "active",
        "current_task_id": None,
        "latest_turn_id": None,
        "turn_ids": [],
    }
    return save_session_memory(payload)


def _build_turn_audit(live_turn: LiveTurn) -> TurnAuditPayload:
    return {
        "schema_version": AUDIT_SCHEMA_VERSION,
        "session_id": live_turn.session_id,
        "turn_id": live_turn.turn_id,
        "session_file": live_turn.session_file,
        "started_at": live_turn.started_at,
        "user_message": live_turn.user_message,
        "task_id": live_turn.task_id,
        "task_title": live_turn.task_title,
        "turn_start_status": "applied",
        "turn_start_bound_at": live_turn.turn_start_bound_at,
        "turn_start_compiled_at": live_turn.turn_start_compiled_at,
        "completed_at": None,
        "assistant_final_reply": "",
        "changed_paths": _dedupe(live_turn.changed_paths),
        "validation_runs": list(live_turn.validation_runs),
        "writeback_decision": "deferred",
        "user_memory_updates": [],
        "task_memory_updates": [],
        "next_actions": [],
        "audit_recorded_at": iso_now(),
    }


def _record_turn_start(live_turn: LiveTurn) -> None:
    audit = _build_turn_audit(live_turn)
    saved_audit = save_turn_audit(audit)
    save_active_runtime(
        {
            "schema_version": AUDIT_SCHEMA_VERSION,
            "status": "active",
            "session_id": live_turn.session_id,
            "turn_id": live_turn.turn_id,
            "active_task_id": live_turn.task_id,
            "last_writeback_decision": None,
            "last_turn_audit_path": str(turn_audit_json_path(live_turn.session_id, live_turn.turn_id)),
            "updated_at": live_turn.turn_start_compiled_at or iso_now(),
        }
    )
    _append_machine_event(
        "turn_start_loaded",
        {
            "session_id": live_turn.session_id,
            "turn_id": live_turn.turn_id,
            "task_id": live_turn.task_id,
            "audit_path": str(turn_audit_json_path(live_turn.session_id, live_turn.turn_id)),
            "compiled_at": saved_audit["turn_start_compiled_at"],
        },
    )
    _append_human_log(
        f"turn-start loaded session={live_turn.session_id} turn={live_turn.turn_id} task={live_turn.task_id}"
    )


def _bind_task_for_turn(live_turn: LiveTurn) -> None:
    session_memory = _load_or_create_session_memory(
        live_turn.session_id,
        session_file=live_turn.session_file,
        started_at=live_turn.started_at,
    )
    task_id = session_memory["current_task_id"]
    task_title = live_turn.task_title or _derive_task_title(live_turn.user_message)
    if task_id is None:
        task_id = _derive_task_id(live_turn.session_id, task_title)
        bind_task(task_id=task_id, title=task_title, goal=task_title)
    live_turn.task_id = task_id
    live_turn.task_title = task_title
    live_turn.turn_start_bound_at = iso_now()
    session_memory["current_task_id"] = task_id
    session_memory["latest_turn_id"] = live_turn.turn_id
    session_memory["status"] = "active"
    session_memory["turn_ids"] = _dedupe([*session_memory["turn_ids"], live_turn.turn_id])
    save_session_memory(session_memory)
    compile_payload = compile_active_memory()
    live_turn.turn_start_compiled_at = compile_payload["compiled_at"]
    _record_turn_start(live_turn)


def _extract_text_from_message_payload(payload: dict[str, Any]) -> str:
    content = payload.get("content")
    if not isinstance(content, list):
        return ""
    chunks: list[str] = []
    for item in content:
        if not isinstance(item, dict):
            continue
        text = item.get("text")
        if isinstance(text, str) and text.strip():
            chunks.append(text.strip())
    return "\n".join(chunks).strip()


def _register_tool_call(live_turn: LiveTurn, payload: dict[str, Any]) -> None:
    call_id = payload.get("call_id")
    if not isinstance(call_id, str) or not call_id:
        return
    tool_type = str(payload.get("type") or "")
    tool_name = str(payload.get("name") or "")
    raw_input = str(payload.get("arguments") or payload.get("input") or "")
    live_turn.pending_tools[call_id] = PendingTool(
        call_id=call_id,
        tool_type=tool_type,
        name=tool_name,
        raw_input=raw_input,
    )


def _normalize_changed_path(candidate: str, cwd: str | None) -> str | None:
    text = candidate.strip().strip("\"'")
    if not text:
        return None
    if " -> " in text:
        text = text.split(" -> ", 1)[1].strip()
    try:
        path = Path(text)
        if path.is_absolute():
            return str(path.resolve())
        if cwd is None:
            return None
        return str((Path(cwd) / path).resolve())
    except OSError:
        return None


def _extract_changed_paths(text: str, cwd: str | None = None) -> list[str]:
    candidates = [match.group(1) for match in ABSOLUTE_PATH_RE.finditer(text)]
    candidates.extend(match.group("path") for match in PATCH_STATUS_LINE_RE.finditer(text))
    normalized = [
        resolved
        for item in candidates
        if (resolved := _normalize_changed_path(item, cwd)) is not None
    ]
    return _dedupe(normalized)


def _parse_exec_output(
    tool: PendingTool,
    output_text: str,
    *,
    cwd: str | None = None,
) -> tuple[list[str], list[dict[str, str]]]:
    changed_paths: list[str] = []
    validation_runs: list[dict[str, str]] = []
    try:
        payload = json.loads(tool.raw_input)
    except json.JSONDecodeError:
        payload = {}
    command = str(payload.get("cmd") or "").strip()
    if command and VALIDATION_HINT_RE.search(command):
        match = RESULT_LINE_RE.search(output_text)
        result = "passed" if match and match.group("code") == "0" else "failed"
        validation_runs.append({"command": command, "result": result})
    return _dedupe(changed_paths), validation_runs


def _parse_apply_patch_output(output_text: str, *, cwd: str | None = None) -> list[str]:
    try:
        payload = json.loads(output_text)
        text = str(payload.get("output") or "")
    except json.JSONDecodeError:
        text = output_text
    return _extract_changed_paths(text, cwd)


def _register_tool_output(live_turn: LiveTurn, payload: dict[str, Any]) -> None:
    call_id = payload.get("call_id")
    if not isinstance(call_id, str):
        return
    tool = live_turn.pending_tools.pop(call_id, None)
    if tool is None:
        return
    output_text = str(payload.get("output") or "")
    if tool.name == "exec_command":
        changed_paths, validation_runs = _parse_exec_output(tool, output_text, cwd=live_turn.cwd)
        live_turn.changed_paths.extend(changed_paths)
        live_turn.validation_runs.extend(validation_runs)
        return
    if tool.name == "apply_patch":
        live_turn.changed_paths.extend(_parse_apply_patch_output(output_text, cwd=live_turn.cwd))


def _apply_task_snapshot_updates(
    task_id: str,
    turn_id: str,
    session_id: str,
    final_reply: str,
    changed_paths: list[str],
    validation_runs: list[dict[str, str]],
    audit_path: str,
) -> list[str]:
    task_memory = load_task_memory(task_id)
    updates: list[str] = []
    current_state = list(task_memory["task_layer"]["current_state"])
    artifacts = list(task_memory["task_layer"]["artifacts"])
    handoff_notes = list(task_memory["task_layer"]["handoff_notes"])

    current_state.append(f"session {session_id} turn {turn_id} completed")
    updates.append(f"snapshot: session {session_id} turn {turn_id} completed")
    if changed_paths:
        current_state.append(f"changed_paths: {', '.join(changed_paths[:5])}")
        artifacts.extend(changed_paths)
        updates.append(f"changed_paths: {', '.join(changed_paths[:5])}")
    for run in validation_runs:
        current_state.append(f"validation: {run['command']} => {run['result']}")
        updates.append(f"validation: {run['command']} => {run['result']}")
    if final_reply:
        handoff_notes.append(f"turn {turn_id}: {_trim_text(final_reply, max_len=180)}")
        updates.append(f"final_reply_excerpt: {_trim_text(final_reply, max_len=120)}")
    artifacts.append(audit_path)
    updates.append(f"audit: {audit_path}")

    task_memory["task_layer"]["current_state"] = _dedupe(current_state)
    task_memory["task_layer"]["artifacts"] = _dedupe(artifacts)
    task_memory["task_layer"]["handoff_notes"] = _dedupe(handoff_notes)
    save_task_memory(task_memory)
    return _dedupe(updates)


def _append_turn_delta_auto(
    task_id: str,
    summary: str,
    task_memory_updates: list[str],
    next_actions: list[str],
    writeback_decision: str,
) -> None:
    entries = load_turn_delta(task_id)
    entries.append(
        {
            "timestamp": iso_now(),
            "summary": summary,
            "user_memory_updates": [],
            "task_memory_updates": _dedupe(task_memory_updates),
            "next_actions": _dedupe(next_actions),
            "writeback_decision": writeback_decision,
        }
    )
    save_turn_delta(task_id, entries)


def _finalize_turn(live_turn: LiveTurn, final_reply: str) -> dict[str, Any]:
    audit = load_turn_audit(live_turn.session_id, live_turn.turn_id)
    changed_paths = _dedupe(live_turn.changed_paths)
    validation_runs = list(live_turn.validation_runs)
    writeback_decision = "applied" if changed_paths or validation_runs else "skipped"
    task_memory_updates: list[str] = []
    next_actions: list[str] = []
    audit_path = str(turn_audit_json_path(live_turn.session_id, live_turn.turn_id))

    if live_turn.task_id and writeback_decision == "applied":
        task_memory_updates = _apply_task_snapshot_updates(
            task_id=live_turn.task_id,
            turn_id=live_turn.turn_id,
            session_id=live_turn.session_id,
            final_reply=final_reply,
            changed_paths=changed_paths,
            validation_runs=validation_runs,
            audit_path=audit_path,
        )
    elif final_reply:
        next_actions.append(f"no durable writeback: {_trim_text(final_reply, max_len=120)}")
    else:
        next_actions.append("no durable writeback signal observed")

    if live_turn.task_id:
        summary = _trim_text(final_reply, max_len=140) if final_reply else f"turn {live_turn.turn_id} completed"
        _append_turn_delta_auto(
            task_id=live_turn.task_id,
            summary=summary,
            task_memory_updates=task_memory_updates,
            next_actions=next_actions,
            writeback_decision=writeback_decision,
        )

    audit["completed_at"] = iso_now()
    audit["assistant_final_reply"] = final_reply
    audit["changed_paths"] = changed_paths
    audit["validation_runs"] = validation_runs
    audit["writeback_decision"] = writeback_decision
    audit["task_memory_updates"] = _dedupe(task_memory_updates)
    audit["next_actions"] = _dedupe(next_actions)
    saved_audit = save_turn_audit(audit)

    session_memory = _load_or_create_session_memory(
        live_turn.session_id,
        session_file=live_turn.session_file,
        started_at=live_turn.started_at,
    )
    session_memory["latest_turn_id"] = live_turn.turn_id
    session_memory["status"] = "completed"
    save_session_memory(session_memory)
    compile_active_memory()
    save_active_runtime(
        {
            "schema_version": AUDIT_SCHEMA_VERSION,
            "status": "idle",
            "session_id": live_turn.session_id,
            "turn_id": live_turn.turn_id,
            "active_task_id": live_turn.task_id,
            "last_writeback_decision": writeback_decision,
            "last_turn_audit_path": audit_path,
            "updated_at": saved_audit["audit_recorded_at"],
        }
    )
    _append_machine_event(
        "turn_end_checked",
        {
            "session_id": live_turn.session_id,
            "turn_id": live_turn.turn_id,
            "task_id": live_turn.task_id,
            "writeback_decision": writeback_decision,
            "audit_path": audit_path,
            "changed_paths": changed_paths,
            "validation_runs": validation_runs,
        },
    )
    _append_human_log(
        f"turn-end checked session={live_turn.session_id} turn={live_turn.turn_id} "
        f"task={live_turn.task_id} decision={writeback_decision}"
    )
    return {
        "session_id": live_turn.session_id,
        "turn_id": live_turn.turn_id,
        "task_id": live_turn.task_id,
        "writeback_decision": writeback_decision,
        "audit_path": audit_path,
    }


def _consume_entry(
    entry: dict[str, Any],
    session_file: Path,
    live_turns: dict[str, LiveTurn],
    session_cwds: dict[str, str],
    processed_turns: list[dict[str, Any]],
) -> None:
    session_id = _session_id_from_path(session_file)
    if session_id is None:
        return
    entry_type = entry.get("type")
    payload = entry.get("payload")
    if not isinstance(payload, dict):
        return

    if entry_type == "session_meta":
        cwd = payload.get("cwd")
        if isinstance(cwd, str) and cwd.strip():
            session_cwds[session_id] = cwd.strip()
        return

    if entry_type == "turn_context":
        cwd = payload.get("cwd")
        if isinstance(cwd, str) and cwd.strip():
            session_cwds[session_id] = cwd.strip()
            live_turn = live_turns.get(session_id)
            if live_turn is not None:
                live_turn.cwd = cwd.strip()
        return

    if entry_type == "event_msg":
        event_type = payload.get("type")
        if event_type == "task_started":
            turn_id = str(payload.get("turn_id") or "").strip()
            if not turn_id:
                return
            live_turns[session_id] = LiveTurn(
                session_id=session_id,
                turn_id=turn_id,
                session_file=str(session_file),
                started_at=str(entry.get("timestamp") or iso_now()),
                cwd=session_cwds.get(session_id),
            )
            return
        live_turn = live_turns.get(session_id)
        if live_turn is None:
            return
        if event_type == "user_message":
            live_turn.user_message = str(payload.get("message") or "")
            live_turn.task_title = _derive_task_title(live_turn.user_message)
            if live_turn.task_id is None:
                _bind_task_for_turn(live_turn)
            return
        if event_type == "agent_message":
            message = str(payload.get("message") or "").strip()
            if message:
                live_turn.assistant_messages.append(message)
            return
        if event_type == "task_complete":
            final_reply = str(payload.get("last_agent_message") or "").strip()
            if not final_reply:
                final_reply = live_turn.assistant_messages[-1] if live_turn.assistant_messages else ""
            processed_turns.append(_finalize_turn(live_turn, final_reply=final_reply))
            live_turns.pop(session_id, None)
            return

    if entry_type == "response_item":
        payload_type = payload.get("type")
        live_turn = live_turns.get(session_id)
        if live_turn is None:
            return
        if payload_type in {"function_call", "custom_tool_call"}:
            _register_tool_call(live_turn, payload)
            return
        if payload_type in {"function_call_output", "custom_tool_call_output"}:
            _register_tool_output(live_turn, payload)
            return
        if payload_type == "message" and payload.get("role") == "assistant":
            text = _extract_text_from_message_payload(payload)
            if text:
                live_turn.assistant_messages.append(text)


def _scan_session_file(
    path: Path,
    start_line: int,
    live_turns: dict[str, LiveTurn],
    session_cwds: dict[str, str],
    processed_turns: list[dict[str, Any]],
) -> int:
    if not path.exists():
        return start_line
    last_line = start_line
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line_no, raw_line in enumerate(handle, start=1):
            if line_no <= start_line:
                continue
            line = raw_line.strip()
            last_line = line_no
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            _consume_entry(
                entry,
                session_file=path,
                live_turns=live_turns,
                session_cwds=session_cwds,
                processed_turns=processed_turns,
            )
    return last_line


def watch_codex_sessions(
    codex_home_override: str | None = None,
    *,
    poll_interval_ms: int = 500,
    idle_exit_seconds: float | None = None,
    once: bool = False,
    session_id_filter: str | None = None,
) -> dict[str, object]:
    ensure_store_exists()
    codex_home = resolve_codex_home(codex_home_override)
    watcher_state = load_watcher_state()
    file_cursors = {path: int(value or "0") for path, value in watcher_state["file_cursors"].items()}
    live_turns: dict[str, LiveTurn] = {}
    session_cwds: dict[str, str] = {}
    processed_turns: list[dict[str, Any]] = []
    processed_files = 0
    last_activity = time.monotonic()

    while True:
        activity_seen = False
        session_files = find_session_files(codex_home, session_id_filter=session_id_filter)
        for session_file in session_files:
            cursor = file_cursors.get(str(session_file), 0)
            next_cursor = _scan_session_file(
                session_file,
                start_line=cursor,
                live_turns=live_turns,
                session_cwds=session_cwds,
                processed_turns=processed_turns,
            )
            if next_cursor > cursor:
                file_cursors[str(session_file)] = next_cursor
                processed_files += 1
                activity_seen = True
        watcher_state = save_watcher_state(
            {
                "schema_version": AUDIT_SCHEMA_VERSION,
                "codex_home": str(codex_home),
                "updated_at": iso_now(),
                "file_cursors": {path: str(line_no) for path, line_no in sorted(file_cursors.items())},
            }
        )
        if once:
            break
        if activity_seen:
            last_activity = time.monotonic()
        elif idle_exit_seconds is not None and (time.monotonic() - last_activity) >= idle_exit_seconds:
            break
        time.sleep(max(poll_interval_ms, 100) / 1000.0)

    return {
        "status": "ok",
        "codex_home": str(codex_home),
        "processed_files": processed_files,
        "processed_turns": processed_turns,
        "watcher_state_json": str(watcher_state_json_path()),
        "active_runtime_json": str(active_runtime_path()),
        "active_task_json": str(active_task_path()),
        "compiled_active_memory_json": str(compiled_active_memory_json_path()),
        "machine_log": str(machine_log_path()),
        "human_log": str(human_log_path()),
    }


def recall_memory(task_id: str | None = None, session_id: str | None = None, *, limit: int = 5) -> dict[str, object]:
    ensure_store_exists()
    if task_id is None and session_id is None:
        raise ValueError("Provide --task-id or --session-id.")
    payload: dict[str, object] = {"status": "ok"}
    if task_id:
        task_memory = load_task_memory(task_id)
        turns = load_turn_delta(task_id)
        payload["task_id"] = task_id
        payload["task_memory"] = task_memory
        payload["recent_turn_delta"] = turns[-limit:]
        return payload
    assert session_id is not None
    session_memory = load_session_memory(session_id)
    payload["session_id"] = session_id
    payload["session_memory"] = session_memory
    audits: list[dict[str, Any]] = []
    for turn_id in session_memory["turn_ids"][-limit:]:
        audit_path = turn_audit_json_path(session_id, turn_id)
        if audit_path.exists():
            audits.append(load_turn_audit(session_id, turn_id))
    payload["turn_audits"] = audits
    return payload


def search_memory(query: str, *, limit: int = 10) -> dict[str, object]:
    ensure_store_exists()
    needle = query.strip().lower()
    if not needle:
        raise ValueError("query must be non-empty")
    task_hits: list[dict[str, Any]] = []
    for task_path in sorted(tasks_root().glob("*/TASK_MEMORY.json")):
        payload = load_task_memory(task_path.parent.name)
        haystack = "\n".join(
            [
                payload["title"],
                payload["task_layer"]["task_goal"],
                *payload["task_layer"]["current_state"],
                *payload["task_layer"]["handoff_notes"],
                *payload["task_layer"]["artifacts"],
            ]
        ).lower()
        if needle in haystack:
            task_hits.append({"task_id": payload["task_id"], "title": payload["title"]})
    turn_hits: list[dict[str, Any]] = []
    for audit_path in sorted(sessions_root().glob("*/turns/*.json")):
        session_id = audit_path.parent.parent.name
        turn_id = audit_path.stem
        payload = load_turn_audit(session_id, turn_id)
        haystack = "\n".join(
            [
                payload["user_message"],
                payload["assistant_final_reply"],
                *(payload["changed_paths"] or []),
                *(payload["task_memory_updates"] or []),
                *(payload["next_actions"] or []),
            ]
        ).lower()
        if needle in haystack:
            turn_hits.append(
                {
                    "session_id": session_id,
                    "turn_id": turn_id,
                    "task_id": payload["task_id"],
                    "writeback_decision": payload["writeback_decision"],
                }
            )
    return {
        "status": "ok",
        "query": query,
        "task_hits": task_hits[:limit],
        "turn_hits": turn_hits[:limit],
    }
