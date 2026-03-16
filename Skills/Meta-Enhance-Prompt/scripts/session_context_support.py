#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


SESSION_KEY_ALIASES = {
    "codex_id": "id",
    "session_id": "id",
    "resume_id": "id",
    "id": "id",
    "cwd": "cwd",
    "originator": "originator",
    "cli_version": "cli_version",
    "source": "source",
    "model_provider": "model_provider",
}
ROLLOUT_KEY_ALIASES = {"rollout_path", "rollout_filename", "rollout_stem"}
MESSAGE_KEY_ALIASES = {
    "text": "text",
    "role": "role",
    "timestamp": "timestamp",
    "source_file": "source_file",
    "line_number": "line_number",
}
DEFAULT_CONTEXT_ROLES = ("user", "assistant")
SESSION_NOT_FOUND = 2
MESSAGE_NOT_FOUND = 3


class SessionContextError(RuntimeError):
    def __init__(self, code: int, payload: dict[str, object]) -> None:
        super().__init__(str(payload.get("message", "")))
        self.code = code
        self.payload = payload


def print_json(payload: dict[str, object]) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def resolve_codex_home(override: str | None) -> Path:
    candidates: list[Path] = []
    if override:
        candidates.append(Path(os.path.expanduser(override)).resolve())
    script_path = Path(__file__).resolve()
    repo_root = next((parent for parent in script_path.parents if parent.name == "Otctopus_OS_AgentConsole"), None)
    if repo_root is not None:
        candidates.append((repo_root.parent / ".codex").resolve())
    env_home = os.getenv("CODEX_HOME")
    if env_home:
        candidates.append(Path(os.path.expanduser(env_home)).resolve())
    candidates.append((Path.home() / ".codex").resolve())

    for candidate in candidates:
        if candidate.exists() and candidate.is_dir():
            return candidate
    raise SessionContextError(
        SESSION_NOT_FOUND,
        {
            "status": "error",
            "message": "Cannot resolve Codex home.",
            "hint": "Pass --codex-home or ensure ~/.codex exists.",
        },
    )


def _sessions_root(codex_home: Path) -> Path:
    sessions_root = codex_home / "sessions"
    if not sessions_root.exists():
        raise SessionContextError(
            SESSION_NOT_FOUND,
            {
                "status": "error",
                "message": "Sessions root not found.",
                "codex_home": str(codex_home),
                "sessions_root": str(sessions_root),
            },
        )
    return sessions_root


def content_to_text(content: object) -> str:
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


def _trim_text(text: str, limit: int) -> tuple[str, bool]:
    clean = str(text or "").strip()
    if limit <= 0 or len(clean) <= limit:
        return clean, False
    return clean[: max(0, limit - 3)].rstrip() + "...", True


def _normalize_key(value: str) -> str:
    return str(value or "").strip().lower().replace("-", "_")


def _match_value(candidate: object, query: str, *, match_mode: str, case_sensitive: bool) -> bool:
    left = str(candidate or "")
    right = str(query or "")
    if not case_sensitive:
        left = left.casefold()
        right = right.casefold()
    if match_mode == "contains":
        return right in left
    return left == right


def _read_session_meta(path: Path) -> dict[str, object]:
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line_no, line in enumerate(handle, start=1):
            raw = line.strip()
            if not raw:
                continue
            try:
                entry = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if entry.get("type") != "session_meta":
                continue
            payload = entry.get("payload") or {}
            if not isinstance(payload, dict):
                payload = {}
            return {
                "path": str(path),
                "rollout_filename": path.name,
                "rollout_stem": path.stem,
                "rollout_path": str(path),
                "session_id": str(payload.get("id", "") or "").strip(),
                "session_timestamp": str(payload.get("timestamp", "") or entry.get("timestamp", "") or "").strip(),
                "session_meta": payload,
                "session_meta_line_number": line_no,
            }
    return {
        "path": str(path),
        "rollout_filename": path.name,
        "rollout_stem": path.stem,
        "rollout_path": str(path),
        "session_id": "",
        "session_timestamp": "",
        "session_meta": {},
        "session_meta_line_number": 0,
    }


def _candidate_paths(codex_home: Path, lookup_key: str, lookup_value: str) -> list[Path]:
    sessions_root = _sessions_root(codex_home)
    normalized_key = _normalize_key(lookup_key)
    if normalized_key in {"codex_id", "session_id", "resume_id", "id", "rollout_filename", "rollout_stem", "rollout_path"}:
        pattern = f"*{lookup_value}*.jsonl"
        matched = sorted(path for path in sessions_root.rglob(pattern) if path.is_file())
        if matched:
            return matched
    return sorted(path for path in sessions_root.rglob("*.jsonl") if path.is_file())


def _session_values(record: dict[str, object], lookup_key: str) -> list[str]:
    normalized_key = _normalize_key(lookup_key)
    session_meta = record.get("session_meta")
    if not isinstance(session_meta, dict):
        session_meta = {}
    if normalized_key in SESSION_KEY_ALIASES:
        value = session_meta.get(SESSION_KEY_ALIASES[normalized_key], "")
        return [str(value or "")]
    if normalized_key in ROLLOUT_KEY_ALIASES:
        return [str(record.get(normalized_key, "") or "")]
    dotted_key = normalized_key.removeprefix("session_meta.").removeprefix("payload.")
    current: object = session_meta
    for segment in dotted_key.split("."):
        if not segment:
            continue
        if not isinstance(current, dict):
            current = ""
            break
        current = current.get(segment, "")
    if isinstance(current, list):
        return [str(item) for item in current]
    if isinstance(current, dict):
        return [json.dumps(current, ensure_ascii=False, sort_keys=True)]
    return [str(current or "")]


def locate_session_record(
    *,
    codex_home: Path,
    lookup_key: str,
    lookup_value: str,
    match_mode: str,
    case_sensitive: bool,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    matches: list[dict[str, object]] = []
    for path in _candidate_paths(codex_home, lookup_key, lookup_value):
        record = _read_session_meta(path)
        for candidate in _session_values(record, lookup_key):
            if candidate and _match_value(candidate, lookup_value, match_mode=match_mode, case_sensitive=case_sensitive):
                matches.append(record)
                break
    if not matches:
        raise SessionContextError(
            SESSION_NOT_FOUND,
            {
                "status": "error",
                "message": "Session rollout not found for lookup.",
                "lookup_key": lookup_key,
                "lookup_value": lookup_value,
                "match_mode": match_mode,
                "codex_home": str(codex_home),
            },
        )
    matches.sort(key=lambda item: (str(item.get("session_timestamp", "")), str(item.get("rollout_path", ""))))
    return matches[-1], matches


def _tool_call_text(payload: dict[str, object]) -> str:
    name = str(payload.get("name", "") or "").strip()
    arguments = str(payload.get("arguments", "") or "").strip()
    if name and arguments:
        return f"{name}\n{arguments}".strip()
    return name or arguments


def iter_message_records(session_file: Path) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    with session_file.open("r", encoding="utf-8", errors="replace") as handle:
        for line_no, line in enumerate(handle, start=1):
            raw = line.strip()
            if not raw:
                continue
            try:
                entry = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if entry.get("type") != "response_item":
                continue
            payload = entry.get("payload") or {}
            if not isinstance(payload, dict):
                continue
            payload_type = str(payload.get("type", "") or "")
            role = ""
            text = ""
            if payload_type == "message":
                role = str(payload.get("role", "") or "").strip()
                text = content_to_text(payload.get("content"))
            elif payload_type in {"function_call", "custom_tool_call"}:
                role = "tool_call"
                text = _tool_call_text(payload)
            elif payload_type in {"function_call_output", "custom_tool_call_output"}:
                role = "tool_output"
                text = str(payload.get("output", "") or "").strip()
            if not role or not text:
                continue
            records.append(
                {
                    "timestamp": str(entry.get("timestamp", "") or "").strip(),
                    "role": role,
                    "text": text,
                    "source_file": str(session_file),
                    "line_number": line_no,
                }
            )
    records.sort(key=lambda item: (str(item.get("timestamp", "")), str(item.get("source_file", "")), int(item.get("line_number", 0))))
    for index, item in enumerate(records):
        item["index"] = index
    return records


def _message_matches(
    message: dict[str, object],
    *,
    message_role: str,
    message_key: str | None,
    message_query: str | None,
    message_match_mode: str,
    case_sensitive: bool,
) -> bool:
    normalized_role = _normalize_key(message_role)
    if normalized_role and normalized_role != "any" and _normalize_key(str(message.get("role", ""))) != normalized_role:
        return False
    if not message_key or message_query is None:
        return True
    field_name = MESSAGE_KEY_ALIASES.get(_normalize_key(message_key), _normalize_key(message_key))
    return _match_value(
        message.get(field_name, ""),
        message_query,
        match_mode=message_match_mode,
        case_sensitive=case_sensitive,
    )


def select_anchor_message(
    messages: list[dict[str, object]],
    *,
    message_role: str,
    message_key: str | None,
    message_query: str | None,
    message_match_mode: str,
    case_sensitive: bool,
    select_mode: str,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    matched = [
        item
        for item in messages
        if _message_matches(
            item,
            message_role=message_role,
            message_key=message_key,
            message_query=message_query,
            message_match_mode=message_match_mode,
            case_sensitive=case_sensitive,
        )
    ]
    if not matched:
        raise SessionContextError(
            MESSAGE_NOT_FOUND,
            {
                "status": "error",
                "message": "No session messages matched the requested selector.",
                "message_role": message_role,
                "message_key": message_key or "",
                "message_query": message_query or "",
            },
        )
    selected = matched[0] if str(select_mode or "").strip().lower() == "first" else matched[-1]
    return selected, matched


def _nearest_message(messages: list[dict[str, object]], *, start_index: int, role: str, reverse: bool) -> dict[str, object] | None:
    indices = range(start_index - 1, -1, -1) if reverse else range(start_index + 1, len(messages))
    for idx in indices:
        candidate = messages[idx]
        if str(candidate.get("role", "")) == role:
            return candidate
    return None


def build_focus_pair(messages: list[dict[str, object]], anchor: dict[str, object]) -> tuple[dict[str, object] | None, dict[str, object] | None]:
    anchor_index = int(anchor.get("index", 0))
    anchor_role = str(anchor.get("role", "") or "")
    if anchor_role == "assistant":
        return _nearest_message(messages, start_index=anchor_index, role="user", reverse=True), anchor
    if anchor_role == "user":
        return anchor, _nearest_message(messages, start_index=anchor_index, role="assistant", reverse=False)
    return _nearest_message(messages, start_index=anchor_index, role="user", reverse=True), _nearest_message(
        messages,
        start_index=anchor_index,
        role="assistant",
        reverse=False,
    )


def _serialize_message(message: dict[str, object] | None, *, trim_chars: int) -> dict[str, object] | None:
    if message is None:
        return None
    text = str(message.get("text", "") or "")
    rendered_text, truncated = _trim_text(text, trim_chars)
    return {
        "index": int(message.get("index", 0)),
        "timestamp": str(message.get("timestamp", "") or ""),
        "role": str(message.get("role", "") or ""),
        "source_file": str(message.get("source_file", "") or ""),
        "line_number": int(message.get("line_number", 0) or 0),
        "text": rendered_text,
        "text_length": len(text),
        "text_truncated": truncated,
    }


def _parse_context_roles(include_roles: list[str] | None) -> tuple[str, ...]:
    if not include_roles:
        return DEFAULT_CONTEXT_ROLES
    parsed: list[str] = []
    for item in include_roles:
        for token in str(item or "").split(","):
            role = str(token or "").strip()
            if role and role not in parsed:
                parsed.append(role)
    return tuple(parsed or DEFAULT_CONTEXT_ROLES)


def _context_items(
    messages: list[dict[str, object]],
    *,
    anchor: dict[str, object],
    context_mode: str,
    window_before: int,
    window_after: int,
    include_roles: tuple[str, ...],
    trim_chars: int,
) -> list[dict[str, object]]:
    normalized_mode = str(context_mode or "").strip().lower()
    anchor_index = int(anchor.get("index", 0))
    if normalized_mode == "all":
        rows = [item for item in messages if str(item.get("role", "")) in include_roles]
        return [_serialize_message(item, trim_chars=trim_chars) for item in rows if item]  # type: ignore[list-item]
    if normalized_mode == "window":
        start = max(0, anchor_index - max(0, window_before))
        end = min(len(messages), anchor_index + max(0, window_after) + 1)
        rows = [item for item in messages[start:end] if str(item.get("role", "")) in include_roles]
        return [_serialize_message(item, trim_chars=trim_chars) for item in rows if item]  # type: ignore[list-item]

    user_prompt, assistant_reply = build_focus_pair(messages, anchor)
    focus_rows = [row for row in (user_prompt, assistant_reply) if row is not None]
    if not focus_rows and str(anchor.get("role", "")) in include_roles:
        focus_rows = [anchor]
    return [_serialize_message(item, trim_chars=trim_chars) for item in focus_rows if item]  # type: ignore[list-item]


def _message_counts(messages: list[dict[str, object]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in messages:
        role = str(item.get("role", "") or "")
        counts[role] = counts.get(role, 0) + 1
    return counts


def _session_match_payload(record: dict[str, object]) -> dict[str, object]:
    session_meta = record.get("session_meta")
    if not isinstance(session_meta, dict):
        session_meta = {}
    return {
        "session_id": str(record.get("session_id", "") or ""),
        "session_timestamp": str(record.get("session_timestamp", "") or ""),
        "rollout_filename": str(record.get("rollout_filename", "") or ""),
        "rollout_stem": str(record.get("rollout_stem", "") or ""),
        "rollout_path": str(record.get("rollout_path", "") or ""),
        "cwd": str(session_meta.get("cwd", "") or ""),
        "originator": str(session_meta.get("originator", "") or ""),
        "cli_version": str(session_meta.get("cli_version", "") or ""),
        "model_provider": str(session_meta.get("model_provider", "") or ""),
        "source": str(session_meta.get("source", "") or ""),
    }


def read_session_context(
    *,
    lookup_key: str,
    lookup_value: str,
    codex_home_override: str | None,
    match_mode: str,
    case_sensitive: bool,
    message_role: str,
    message_key: str | None,
    message_query: str | None,
    message_match_mode: str,
    select_mode: str,
    context_mode: str,
    window_before: int,
    window_after: int,
    include_roles: list[str] | None,
    trim_chars: int,
) -> dict[str, object]:
    if not str(lookup_key or "").strip() or not str(lookup_value or "").strip():
        raise SessionContextError(
            SESSION_NOT_FOUND,
            {
                "status": "error",
                "message": "Missing lookup key/value. Provide --lookup-key and --lookup-id.",
            },
        )

    codex_home = resolve_codex_home(codex_home_override)
    matched_record, matched_candidates = locate_session_record(
        codex_home=codex_home,
        lookup_key=lookup_key,
        lookup_value=lookup_value,
        match_mode=match_mode,
        case_sensitive=case_sensitive,
    )
    session_file = Path(str(matched_record["rollout_path"]))
    messages = iter_message_records(session_file)
    if not messages:
        raise SessionContextError(
            MESSAGE_NOT_FOUND,
            {
                "status": "error",
                "message": "Matched session has no readable chat messages.",
                "rollout_path": str(session_file),
            },
        )

    anchor, matched_messages = select_anchor_message(
        messages,
        message_role=message_role,
        message_key=message_key,
        message_query=message_query,
        message_match_mode=message_match_mode,
        case_sensitive=case_sensitive,
        select_mode=select_mode,
    )
    user_prompt, assistant_reply = build_focus_pair(messages, anchor)
    context_roles = _parse_context_roles(include_roles)

    return {
        "status": "ok",
        "lookup": {
            "lookup_key": lookup_key,
            "lookup_value": lookup_value,
            "match_mode": match_mode,
            "case_sensitive": case_sensitive,
            "matched_rollout_count": len(matched_candidates),
        },
        "matched_session": _session_match_payload(matched_record),
        "selection": {
            "message_role": message_role,
            "message_key": message_key or "",
            "message_query": message_query or "",
            "message_match_mode": message_match_mode,
            "select_mode": select_mode,
            "context_mode": context_mode,
            "window_before": max(0, window_before),
            "window_after": max(0, window_after),
            "include_roles": list(context_roles),
            "matched_message_count": len(matched_messages),
        },
        "focused_chat": {
            "user_prompt": _serialize_message(user_prompt, trim_chars=trim_chars),
            "assistant_reply": _serialize_message(assistant_reply, trim_chars=trim_chars),
            "anchor_message": _serialize_message(anchor, trim_chars=trim_chars),
        },
        "context_items": _context_items(
            messages,
            anchor=anchor,
            context_mode=context_mode,
            window_before=window_before,
            window_after=window_after,
            include_roles=context_roles,
            trim_chars=trim_chars,
        ),
        "message_counts": _message_counts(messages),
        "codex_home": str(codex_home),
        "chat_focus_policy": "Default output is narrowed to the paired user prompt and assistant reply. Expand context only when the downstream task needs more evidence.",
    }


def render_session_context_text(payload: dict[str, object]) -> str:
    matched_session = payload.get("matched_session") or {}
    focused_chat = payload.get("focused_chat") or {}
    user_prompt = focused_chat.get("user_prompt") if isinstance(focused_chat, dict) else None
    assistant_reply = focused_chat.get("assistant_reply") if isinstance(focused_chat, dict) else None
    lines = [
        "session-context",
        f"lookup: {payload.get('lookup', {})}",
        f"matched_session: {matched_session}",
        "",
        "user_prompt:",
        str((user_prompt or {}).get("text", "") if isinstance(user_prompt, dict) else ""),
        "",
        "assistant_reply:",
        str((assistant_reply or {}).get("text", "") if isinstance(assistant_reply, dict) else ""),
    ]
    return "\n".join(lines).rstrip() + "\n"
