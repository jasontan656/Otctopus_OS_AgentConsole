#!/usr/bin/env python3
from __future__ import annotations

import json

from memory_models import CompiledMemoryPayload
from memory_models import iso_now
from memory_models import validate_compiled_memory
from memory_store import compiled_active_memory_json_path
from memory_store import compiled_active_memory_md_path
from memory_store import compiled_root
from memory_store import load_active_task
from memory_store import load_task_memory
from memory_store import load_user_memory
from memory_writeback import render_active_memory_md


IGNORE_BY_DEFAULT = [
    "full transcript",
    "raw tool output",
    "stale branch detail",
    "low-signal repetition",
]


def compile_active_memory() -> CompiledMemoryPayload:
    compiled_root().mkdir(parents=True, exist_ok=True)
    active_task = load_active_task()
    user_memory = load_user_memory()
    task_memory = None
    if active_task["active_task_id"]:
        task_memory = load_task_memory(str(active_task["active_task_id"]))
    payload = {
        "skill_name": "Meta-Runtime-Memory",
        "compiled_at": iso_now(),
        "memory_definition": "Keep only long-term goals, current state, and stable behavior constraints.",
        "active_task_id": active_task["active_task_id"],
        "user_memory": user_memory,
        "task_memory": task_memory,
        "writeback_policy": {
            "turn_start": "mandatory_load",
            "turn_end": "mandatory_check_conditional_write",
        },
        "ignore_by_default": IGNORE_BY_DEFAULT,
    }
    validated = validate_compiled_memory(payload)
    compiled_active_memory_json_path().write_text(
        json.dumps(validated, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    compiled_active_memory_md_path().write_text(render_active_memory_md(validated), encoding="utf-8")
    return validated
