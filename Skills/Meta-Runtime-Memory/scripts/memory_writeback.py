#!/usr/bin/env python3
from __future__ import annotations

from typing import Any


def _render_list(items: list[str]) -> list[str]:
    if not items:
        return ["- (empty)"]
    return [f"- {item}" for item in items]


def render_user_memory_md(payload: dict[str, Any]) -> str:
    top_layer = payload["top_layer"]
    sections = [
        "# USER_MEMORY",
        "",
        f"- updated_at: {payload['updated_at']}",
        "",
        "## Top Layer",
    ]
    for key in (
        "long_term_objectives",
        "communication_style",
        "work_style",
        "collaboration_style",
        "global_preferences",
        "habit_patterns",
        "stable_constraints",
    ):
        sections.append(f"### {key}")
        sections.extend(_render_list(top_layer[key]))
        sections.append("")
    return "\n".join(sections).rstrip() + "\n"


def render_task_memory_md(payload: dict[str, Any]) -> str:
    task_layer = payload["task_layer"]
    sections = [
        "# TASK_MEMORY",
        "",
        f"- task_id: {payload['task_id']}",
        f"- title: {payload['title']}",
        f"- status: {payload['status']}",
        f"- updated_at: {payload['updated_at']}",
        "",
        "## Task Layer",
        "### task_goal",
        f"- {task_layer['task_goal'] or '(empty)'}",
        "",
    ]
    for key in (
        "current_state",
        "working_style",
        "constraints",
        "mindset",
        "next_steps",
        "open_questions",
        "artifacts",
        "handoff_notes",
    ):
        sections.append(f"### {key}")
        sections.extend(_render_list(task_layer[key]))
        sections.append("")
    return "\n".join(sections).rstrip() + "\n"


def render_turn_delta_md(entries: list[dict[str, Any]]) -> str:
    sections = ["# TURN_DELTA", ""]
    if not entries:
        sections.extend(["- (empty)", ""])
        return "\n".join(sections)
    for entry in entries:
        sections.append(f"## {entry['timestamp']}")
        sections.append(f"- summary: {entry['summary']}")
        sections.append(f"- writeback_decision: {entry['writeback_decision']}")
        sections.append("- user_memory_updates:")
        sections.extend([f"  - {item}" for item in entry["user_memory_updates"]] or ["  - (empty)"])
        sections.append("- task_memory_updates:")
        sections.extend([f"  - {item}" for item in entry["task_memory_updates"]] or ["  - (empty)"])
        sections.append("- next_actions:")
        sections.extend([f"  - {item}" for item in entry["next_actions"]] or ["  - (empty)"])
        sections.append("")
    return "\n".join(sections).rstrip() + "\n"


def render_active_memory_md(payload: dict[str, Any]) -> str:
    sections = [
        "# ACTIVE_MEMORY",
        "",
        f"- compiled_at: {payload['compiled_at']}",
        f"- active_task_id: {payload['active_task_id'] or '(none)'}",
        f"- memory_definition: {payload['memory_definition']}",
        "",
        "## User Layer",
    ]
    for key, value in payload["user_memory"]["top_layer"].items():
        sections.append(f"### {key}")
        sections.extend(_render_list(value))
        sections.append("")
    sections.append("## Task Layer")
    if payload["task_memory"] is None:
        sections.extend(["- (none)", ""])
    else:
        task_layer = payload["task_memory"]["task_layer"]
        sections.extend(
            [
                f"- task_id: {payload['task_memory']['task_id']}",
                f"- title: {payload['task_memory']['title']}",
                "",
                "### task_goal",
                f"- {task_layer['task_goal'] or '(empty)'}",
                "",
            ]
        )
        for key in (
            "current_state",
            "working_style",
            "constraints",
            "mindset",
            "next_steps",
            "open_questions",
            "artifacts",
            "handoff_notes",
        ):
            sections.append(f"### {key}")
            sections.extend(_render_list(task_layer[key]))
            sections.append("")
    sections.append("## Ignore By Default")
    sections.extend(_render_list(payload["ignore_by_default"]))
    sections.append("")
    return "\n".join(sections).rstrip() + "\n"
