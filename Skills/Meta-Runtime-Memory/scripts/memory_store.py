#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from memory_models import SCHEMA_VERSION
from memory_models import AUDIT_SCHEMA_VERSION
from memory_models import iso_now
from memory_models import validate_active_runtime
from memory_models import validate_session_memory
from memory_models import validate_turn_audit
from memory_models import validate_active_task
from memory_models import validate_task_memory
from memory_models import validate_turn_delta_entries
from memory_models import validate_user_memory
from memory_models import validate_watcher_state
from memory_writeback import render_task_memory_md
from memory_writeback import render_turn_delta_md
from memory_writeback import render_user_memory_md


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
PRODUCT_ROOT = SKILL_ROOT.parents[1]
WORKSPACE_ROOT = PRODUCT_ROOT.parent
SKILL_NAME = SKILL_ROOT.name
TEMPLATE_ROOT = SKILL_ROOT / "assets" / "templates"


def _resolve_skill_root_from_env(var_name: str, default_container_name: str) -> Path:
    raw = __import__("os").environ.get(var_name)
    if raw:
        return Path(raw).expanduser().resolve() / SKILL_NAME
    return (WORKSPACE_ROOT / default_container_name / SKILL_NAME).resolve()


def runtime_root() -> Path:
    return _resolve_skill_root_from_env("CODEX_SKILL_RUNTIME_ROOT", "Codex_Skill_Runtime")


def result_root() -> Path:
    return _resolve_skill_root_from_env("CODEX_SKILL_RESULT_ROOT", "Codex_Skills_Result")


def active_task_path() -> Path:
    return result_root() / "ACTIVE_TASK.json"


def active_runtime_path() -> Path:
    return result_root() / "ACTIVE_RUNTIME.json"


def user_memory_json_path() -> Path:
    return result_root() / "user" / "USER_MEMORY.json"


def user_memory_md_path() -> Path:
    return result_root() / "user" / "USER_MEMORY.md"


def tasks_root() -> Path:
    return result_root() / "tasks"


def sessions_root() -> Path:
    return result_root() / "sessions"


def session_dir(session_id: str) -> Path:
    return sessions_root() / session_id


def session_memory_json_path(session_id: str) -> Path:
    return session_dir(session_id) / "SESSION_MEMORY.json"


def session_turns_root(session_id: str) -> Path:
    return session_dir(session_id) / "turns"


def turn_audit_json_path(session_id: str, turn_id: str) -> Path:
    return session_turns_root(session_id) / f"{turn_id}.json"


def task_dir(task_id: str) -> Path:
    return tasks_root() / task_id


def task_memory_json_path(task_id: str) -> Path:
    return task_dir(task_id) / "TASK_MEMORY.json"


def task_memory_md_path(task_id: str) -> Path:
    return task_dir(task_id) / "TASK_MEMORY.md"


def turn_delta_json_path(task_id: str) -> Path:
    return task_dir(task_id) / "TURN_DELTA.json"


def turn_delta_md_path(task_id: str) -> Path:
    return task_dir(task_id) / "TURN_DELTA.md"


def compiled_root() -> Path:
    return runtime_root() / "compiled"


def watcher_root() -> Path:
    return runtime_root() / "watcher"


def watcher_state_json_path() -> Path:
    return watcher_root() / "OBSERVER_STATE.json"


def logs_root() -> Path:
    return runtime_root() / "logs"


def machine_log_path() -> Path:
    return logs_root() / "machine.jsonl"


def human_log_path() -> Path:
    return logs_root() / "human.log"


def compiled_active_memory_json_path() -> Path:
    return compiled_root() / "ACTIVE_MEMORY.json"


def compiled_active_memory_md_path() -> Path:
    return compiled_root() / "ACTIVE_MEMORY.md"


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _read_template_json(name: str, replacements: dict[str, str] | None = None) -> Any:
    rendered = (TEMPLATE_ROOT / name).read_text(encoding="utf-8")
    for key, value in (replacements or {}).items():
        rendered = rendered.replace(key, value)
    return json.loads(rendered)


def deep_merge(base: Any, patch: Any) -> Any:
    if isinstance(base, dict) and isinstance(patch, dict):
        merged = dict(base)
        for key, value in patch.items():
            if key in merged:
                merged[key] = deep_merge(merged[key], value)
            else:
                merged[key] = value
        return merged
    return patch


def ensure_store_exists() -> dict[str, Any]:
    created: list[str] = []
    runtime_root().mkdir(parents=True, exist_ok=True)
    compiled_root().mkdir(parents=True, exist_ok=True)
    watcher_root().mkdir(parents=True, exist_ok=True)
    logs_root().mkdir(parents=True, exist_ok=True)
    tasks_root().mkdir(parents=True, exist_ok=True)
    sessions_root().mkdir(parents=True, exist_ok=True)
    (result_root() / "user").mkdir(parents=True, exist_ok=True)

    active_path = active_task_path()
    if not active_path.exists():
        payload = _read_template_json("ACTIVE_TASK_TEMPLATE.json")
        payload["schema_version"] = SCHEMA_VERSION
        payload["updated_at"] = iso_now()
        validate_active_task(payload)
        _write_json(active_path, payload)
        created.append(str(active_path))

    runtime_path = active_runtime_path()
    if not runtime_path.exists():
        payload = {
            "schema_version": AUDIT_SCHEMA_VERSION,
            "status": "idle",
            "session_id": None,
            "turn_id": None,
            "active_task_id": None,
            "last_writeback_decision": None,
            "last_turn_audit_path": None,
            "updated_at": iso_now(),
        }
        payload = validate_active_runtime(payload)
        _write_json(runtime_path, payload)
        created.append(str(runtime_path))

    user_json = user_memory_json_path()
    if not user_json.exists():
        payload = _read_template_json("USER_MEMORY_TEMPLATE.json")
        payload["schema_version"] = SCHEMA_VERSION
        payload["updated_at"] = iso_now()
        payload = validate_user_memory(payload)
        _write_json(user_json, payload)
        user_memory_md_path().write_text(render_user_memory_md(payload), encoding="utf-8")
        created.append(str(user_json))
        created.append(str(user_memory_md_path()))

    watcher_state_path = watcher_state_json_path()
    if not watcher_state_path.exists():
        payload = {
            "schema_version": AUDIT_SCHEMA_VERSION,
            "codex_home": "",
            "updated_at": iso_now(),
            "file_cursors": {},
        }
        watcher_state_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        created.append(str(watcher_state_path))

    return {
        "skill_name": SKILL_NAME,
        "runtime_root": str(runtime_root()),
        "result_root": str(result_root()),
        "created": created,
    }


def load_active_task() -> dict[str, Any]:
    return validate_active_task(_read_json(active_task_path()))


def load_active_runtime() -> dict[str, Any]:
    return validate_active_runtime(_read_json(active_runtime_path()))


def save_active_task(active_task_id: str | None) -> dict[str, Any]:
    payload = {
        "schema_version": SCHEMA_VERSION,
        "active_task_id": active_task_id,
        "updated_at": iso_now(),
    }
    payload = validate_active_task(payload)
    _write_json(active_task_path(), payload)
    return payload


def save_active_runtime(payload: dict[str, Any]) -> dict[str, Any]:
    payload["schema_version"] = AUDIT_SCHEMA_VERSION
    payload["updated_at"] = iso_now()
    validated = validate_active_runtime(payload)
    _write_json(active_runtime_path(), validated)
    return validated


def load_user_memory() -> dict[str, Any]:
    return validate_user_memory(_read_json(user_memory_json_path()))


def save_user_memory(payload: dict[str, Any]) -> dict[str, Any]:
    payload["schema_version"] = SCHEMA_VERSION
    payload["memory_kind"] = "user"
    payload["updated_at"] = iso_now()
    validated = validate_user_memory(payload)
    _write_json(user_memory_json_path(), validated)
    user_memory_md_path().write_text(render_user_memory_md(validated), encoding="utf-8")
    return validated


def create_task_memory(task_id: str, title: str) -> dict[str, Any]:
    task_json = task_memory_json_path(task_id)
    if task_json.exists():
        return load_task_memory(task_id)
    payload = _read_template_json(
        "TASK_MEMORY_TEMPLATE.json",
        replacements={"__TASK_ID__": task_id, "__TASK_TITLE__": title},
    )
    payload["schema_version"] = SCHEMA_VERSION
    payload["updated_at"] = iso_now()
    validated = validate_task_memory(payload)
    _write_json(task_json, validated)
    task_memory_md_path(task_id).write_text(render_task_memory_md(validated), encoding="utf-8")
    _write_json(turn_delta_json_path(task_id), [])
    turn_delta_md_path(task_id).write_text(render_turn_delta_md([]), encoding="utf-8")
    return validated


def load_task_memory(task_id: str) -> dict[str, Any]:
    return validate_task_memory(_read_json(task_memory_json_path(task_id)))


def save_task_memory(payload: dict[str, Any]) -> dict[str, Any]:
    payload["schema_version"] = SCHEMA_VERSION
    payload["memory_kind"] = "task"
    payload["updated_at"] = iso_now()
    validated = validate_task_memory(payload)
    _write_json(task_memory_json_path(validated["task_id"]), validated)
    task_memory_md_path(validated["task_id"]).write_text(render_task_memory_md(validated), encoding="utf-8")
    return validated


def load_turn_delta(task_id: str) -> list[dict[str, Any]]:
    return validate_turn_delta_entries(_read_json(turn_delta_json_path(task_id)))


def save_turn_delta(task_id: str, entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    validated = validate_turn_delta_entries(entries)
    _write_json(turn_delta_json_path(task_id), validated)
    turn_delta_md_path(task_id).write_text(render_turn_delta_md(validated), encoding="utf-8")
    return validated


def load_session_memory(session_id: str) -> dict[str, Any]:
    return validate_session_memory(_read_json(session_memory_json_path(session_id)))


def save_session_memory(payload: dict[str, Any]) -> dict[str, Any]:
    payload["schema_version"] = AUDIT_SCHEMA_VERSION
    payload["updated_at"] = iso_now()
    validated = validate_session_memory(payload)
    _write_json(session_memory_json_path(validated["session_id"]), validated)
    return validated


def load_turn_audit(session_id: str, turn_id: str) -> dict[str, Any]:
    return validate_turn_audit(_read_json(turn_audit_json_path(session_id, turn_id)))


def save_turn_audit(payload: dict[str, Any]) -> dict[str, Any]:
    payload["schema_version"] = AUDIT_SCHEMA_VERSION
    payload["audit_recorded_at"] = iso_now()
    validated = validate_turn_audit(payload)
    _write_json(turn_audit_json_path(validated["session_id"], validated["turn_id"]), validated)
    return validated


def load_watcher_state() -> dict[str, Any]:
    payload = _read_json(watcher_state_json_path())
    if not payload.get("codex_home"):
        payload["codex_home"] = ""
    return validate_watcher_state(payload)


def save_watcher_state(payload: dict[str, Any]) -> dict[str, Any]:
    payload["schema_version"] = AUDIT_SCHEMA_VERSION
    payload["updated_at"] = iso_now()
    validated = validate_watcher_state(payload)
    _write_json(watcher_state_json_path(), validated)
    return validated


def resolve_task_id(task_id: str | None) -> str:
    if task_id:
        return task_id
    active_payload = load_active_task()
    if not active_payload["active_task_id"]:
        raise ValueError("no active task is currently bound")
    return str(active_payload["active_task_id"])
