#!/usr/bin/env python3
from __future__ import annotations

from memory_models import validate_active_task
from memory_models import validate_active_runtime
from memory_models import validate_compiled_memory
from memory_models import validate_session_memory
from memory_models import validate_task_memory
from memory_models import validate_turn_audit
from memory_models import validate_turn_delta_entries
from memory_models import validate_user_memory
from memory_models import validate_watcher_state
from memory_store import active_runtime_path
from memory_store import compiled_active_memory_json_path
from memory_store import load_active_task
from memory_store import load_active_runtime
from memory_store import load_session_memory
from memory_store import load_task_memory
from memory_store import load_turn_audit
from memory_store import load_turn_delta
from memory_store import load_user_memory
from memory_store import sessions_root
from memory_store import tasks_root
from memory_store import watcher_state_json_path


def validate_store() -> dict[str, object]:
    checked_files: list[str] = []
    task_ids: list[str] = []

    active = validate_active_task(load_active_task())
    checked_files.append("ACTIVE_TASK.json")

    if active_runtime_path().exists():
        validate_active_runtime(load_active_runtime())
        checked_files.append("ACTIVE_RUNTIME.json")

    user_memory = validate_user_memory(load_user_memory())
    checked_files.append("user/USER_MEMORY.json")

    if tasks_root().exists():
        for task_dir in sorted(path for path in tasks_root().iterdir() if path.is_dir()):
            task_ids.append(task_dir.name)
            validate_task_memory(load_task_memory(task_dir.name))
            validate_turn_delta_entries(load_turn_delta(task_dir.name))
            checked_files.append(f"tasks/{task_dir.name}/TASK_MEMORY.json")
            checked_files.append(f"tasks/{task_dir.name}/TURN_DELTA.json")

    session_ids: list[str] = []
    turn_audit_count = 0
    if sessions_root().exists():
        for session_dir in sorted(path for path in sessions_root().iterdir() if path.is_dir()):
            session_ids.append(session_dir.name)
            validate_session_memory(load_session_memory(session_dir.name))
            checked_files.append(f"sessions/{session_dir.name}/SESSION_MEMORY.json")
            turns_dir = session_dir / "turns"
            if turns_dir.exists():
                for audit_path in sorted(path for path in turns_dir.iterdir() if path.is_file()):
                    validate_turn_audit(load_turn_audit(session_dir.name, audit_path.stem))
                    checked_files.append(f"sessions/{session_dir.name}/turns/{audit_path.name}")
                    turn_audit_count += 1

    compiled_file = compiled_active_memory_json_path()
    compiled_available = compiled_file.exists()
    if compiled_available:
        import json

        validate_compiled_memory(json.loads(compiled_file.read_text(encoding="utf-8")))
        checked_files.append("compiled/ACTIVE_MEMORY.json")

    watcher_state = watcher_state_json_path()
    if watcher_state.exists():
        import json

        validate_watcher_state(json.loads(watcher_state.read_text(encoding="utf-8")))
        checked_files.append("watcher/OBSERVER_STATE.json")

    return {
        "status": "ok",
        "active_task_id": active["active_task_id"],
        "task_ids": task_ids,
        "session_ids": session_ids,
        "turn_audit_count": turn_audit_count,
        "checked_files": checked_files,
        "compiled_available": compiled_available,
        "user_top_layer_keys": sorted(user_memory["top_layer"].keys()),
    }
