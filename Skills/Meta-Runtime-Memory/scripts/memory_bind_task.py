#!/usr/bin/env python3
from __future__ import annotations

import re

from memory_store import create_task_memory
from memory_store import save_active_task
from memory_store import save_task_memory
from memory_store import task_memory_json_path


TASK_ID_RE = re.compile(r"[^a-z0-9]+")


def normalize_task_id(value: str) -> str:
    lowered = value.strip().lower()
    normalized = TASK_ID_RE.sub("-", lowered).strip("-")
    if not normalized:
        raise ValueError("task_id resolved to empty after normalization")
    return normalized


def bind_task(task_id: str, title: str | None = None, goal: str | None = None) -> dict[str, object]:
    normalized_task_id = normalize_task_id(task_id)
    normalized_title = (title or task_id).strip() or normalized_task_id
    task_memory = create_task_memory(normalized_task_id, normalized_title)
    if goal is not None and goal.strip() and task_memory["task_layer"]["task_goal"] != goal.strip():
        task_memory["task_layer"]["task_goal"] = goal.strip()
        task_memory = save_task_memory(task_memory)
    active_payload = save_active_task(normalized_task_id)
    return {
        "task_id": normalized_task_id,
        "title": task_memory["title"],
        "task_memory_path": str(task_memory_json_path(normalized_task_id)),
        "active_task": active_payload,
    }
