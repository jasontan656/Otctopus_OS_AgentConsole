from __future__ import annotations

import datetime as dt
import json
import os
from pathlib import Path

from runtime_pain_types import TurnHookAudit
from runtime_pain_types import WatcherState


SCHEMA_VERSION = "1.0.0"
SKILL_NAME = "Meta-Runtime-Selfcheck"


def iso_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def _is_blocked_runtime_parent(path: Path) -> bool:
    text = str(path.resolve()).replace("\\", "/")
    return (
        "/.codex/skills" in text
        or "/Otctopus_OS_AgentConsole" in text
        or "/Codex_Skills_Mirror" in text
    )


def _discover_runtime_root() -> Path:
    override = str(os.environ.get("CODEX_SKILL_RUNTIME_ROOT", "") or "").strip()
    if override:
        return Path(override).expanduser().resolve()

    script_path = Path(__file__).resolve()
    repo_root = next((parent for parent in script_path.parents if parent.name == "Otctopus_OS_AgentConsole"), None)
    if repo_root is not None:
        candidate = (repo_root.parent / "Codex_Skill_Runtime").resolve()
        if not _is_blocked_runtime_parent(candidate.parent):
            return candidate

    return (Path.home() / ".codex" / "Codex_Skill_Runtime").resolve()


def runtime_root() -> Path:
    return (_discover_runtime_root() / SKILL_NAME).resolve()


def sessions_root() -> Path:
    return runtime_root() / "sessions"


def watcher_root() -> Path:
    return runtime_root() / "watcher"


def watcher_state_json_path() -> Path:
    return watcher_root() / "OBSERVER_STATE.json"


def session_dir(session_id: str) -> Path:
    return sessions_root() / session_id


def turn_dir(session_id: str) -> Path:
    return session_dir(session_id) / "turns"


def turn_audit_json_path(session_id: str, turn_id: str) -> Path:
    return turn_dir(session_id) / f"{turn_id}.json"


def ensure_store_exists() -> list[str]:
    created: list[str] = []
    for path in (runtime_root(), sessions_root(), watcher_root()):
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            created.append(str(path))
    if not watcher_state_json_path().exists():
        payload = {
            "schema_version": SCHEMA_VERSION,
            "codex_home": "",
            "updated_at": "",
            "file_cursors": {},
        }
        watcher_state_json_path().write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        created.append(str(watcher_state_json_path()))
    return created


def _read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def load_watcher_state() -> WatcherState:
    ensure_store_exists()
    payload = _read_json(watcher_state_json_path())
    if not isinstance(payload, dict):
        raise ValueError("watcher_state must be a JSON object")
    raw_file_cursors = payload.get("file_cursors", {})
    if not isinstance(raw_file_cursors, dict):
        raise ValueError("watcher_state.file_cursors must be a JSON object")
    return {
        "schema_version": str(payload.get("schema_version", SCHEMA_VERSION) or SCHEMA_VERSION),
        "codex_home": str(payload.get("codex_home", "") or ""),
        "updated_at": str(payload.get("updated_at", "") or ""),
        "file_cursors": {
            str(path): str(value)
            for path, value in raw_file_cursors.items()
            if str(path).strip()
        },
    }


def save_watcher_state(payload: WatcherState) -> WatcherState:
    ensure_store_exists()
    normalized: WatcherState = {
        "schema_version": SCHEMA_VERSION,
        "codex_home": str(payload.get("codex_home", "") or ""),
        "updated_at": str(payload.get("updated_at", "") or iso_now()),
        "file_cursors": {
            str(path): str(value)
            for path, value in dict(payload.get("file_cursors", {})).items()
            if str(path).strip()
        },
    }
    watcher_state_json_path().write_text(
        json.dumps(normalized, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return normalized


def load_turn_audit(session_id: str, turn_id: str) -> TurnHookAudit:
    payload = _read_json(turn_audit_json_path(session_id, turn_id))
    if not isinstance(payload, dict):
        raise ValueError("turn audit must be a JSON object")
    normalized: TurnHookAudit = dict(payload)
    return normalized


def save_turn_audit(payload: TurnHookAudit) -> TurnHookAudit:
    ensure_store_exists()
    session_id = str(payload.get("session_id", "") or "").strip()
    turn_id = str(payload.get("turn_id", "") or "").strip()
    if not session_id or not turn_id:
        raise ValueError("turn audit requires session_id and turn_id")
    normalized: TurnHookAudit = dict(payload)
    normalized["schema_version"] = SCHEMA_VERSION
    normalized["audit_recorded_at"] = iso_now()
    path = turn_audit_json_path(session_id, turn_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(normalized, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return normalized
