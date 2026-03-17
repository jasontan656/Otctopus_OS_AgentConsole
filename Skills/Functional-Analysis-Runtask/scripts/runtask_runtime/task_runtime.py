from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import os
import re
from typing import Any

import yaml

from .catalog import (
    DEFAULT_MANAGED_ROOT,
    DEFAULT_TASK_RUNTIME_ROOT,
    HUMENWORKZONE_COMMANDS,
    MANAGED_ROOT_ENV,
    NUMBERED_SLOT_RE,
    SKILL_ROOT,
    STAGE_ORDER,
    TASK_RUNTIME_ROOT_ENV,
)
from .types import BoundaryErrorPayload, OpenTaskPayload, TaskGateCheckPayload, TaskRuntimeScaffoldPayload


def managed_root() -> Path:
    return Path(os.environ.get(MANAGED_ROOT_ENV, str(DEFAULT_MANAGED_ROOT))).expanduser().resolve()


def task_runtime_root() -> Path:
    return Path(os.environ.get(TASK_RUNTIME_ROOT_ENV, str(DEFAULT_TASK_RUNTIME_ROOT))).expanduser().resolve()


def _is_relative_to(path: Path, other: Path) -> bool:
    try:
        path.relative_to(other)
        return True
    except ValueError:
        return False


def workspace_root_boundary_error(workspace_root: Path) -> BoundaryErrorPayload | None:
    governed_root = managed_root()
    if _is_relative_to(workspace_root, SKILL_ROOT):
        return {
            "status": "fail",
            "reason": "workspace_root_forbidden_under_skill_root",
            "workspace_root": str(workspace_root),
            "managed_root": str(governed_root),
            "message": "任务产物不得落到 Functional-Analysis-Runtask 技能目录内部；请先通过 Functional-HumenWorkZone-Manager 解析 Human_Work_Zone 受管落点。",
            "artifact_handoff_commands": HUMENWORKZONE_COMMANDS,
        }
    if not _is_relative_to(workspace_root, governed_root):
        return {
            "status": "fail",
            "reason": "workspace_root_must_be_under_managed_root",
            "workspace_root": str(workspace_root),
            "managed_root": str(governed_root),
            "message": "workspace_root 必须位于 Human_Work_Zone 受管根下；请先通过 Functional-HumenWorkZone-Manager 解析目标分区。",
            "artifact_handoff_commands": HUMENWORKZONE_COMMANDS,
        }
    return None


def task_gate_check_payload(task_runtime_root_override: Path | None = None) -> TaskGateCheckPayload:
    runtime_root = (task_runtime_root_override or task_runtime_root()).resolve()
    open_tasks: list[OpenTaskPayload] = []
    warnings = []
    if runtime_root.exists():
        for _prefix, _slug, task_dir in numbered_slot_entries(runtime_root):
            runtime_file = task_dir / "task_runtime.yaml"
            if not runtime_file.exists():
                open_tasks.append({"task_root": str(task_dir), "reason": "missing_task_runtime_file", "resume_hint": "补齐 task_runtime.yaml 后再继续。"})
                continue
            try:
                payload = yaml.safe_load(runtime_file.read_text(encoding="utf-8"))
            except yaml.YAMLError as exc:
                open_tasks.append(
                    {
                        "task_root": str(task_dir),
                        "reason": "task_runtime_yaml_parse_error",
                        "detail": str(exc),
                        "resume_hint": "修复 task_runtime.yaml 后再继续。",
                    }
                )
                continue
            if not isinstance(payload, dict):
                open_tasks.append({"task_root": str(task_dir), "reason": "invalid_task_runtime_root_type", "resume_hint": "task_runtime.yaml 根节点必须是映射。"})
                continue
            if _task_runtime_is_closed(payload):
                continue
            open_tasks.append(
                {
                    "task_root": str(task_dir),
                    "task_id": str(payload.get("task_id", "")),
                    "task_status": str(payload.get("task_status", "")),
                    "current_stage": str(payload.get("current_stage", "")),
                    "current_step": str(payload.get("current_step", "")),
                    "ended_stage": str(payload.get("ended_stage", "")),
                    "ended_step": str(payload.get("ended_step", "")),
                    "resume_hint": str(payload.get("resume_hint", "继续推进当前 task_runtime.yaml，直至全部阶段完成并 closed。")),
                }
            )
    if not runtime_root.exists():
        warnings.append({"code": "task_runtime_root_missing", "message": "task runtime root 尚未创建；当前允许启动首个任务。"})
    return {
        "status": "ok" if not open_tasks else "fail",
        "reason": "" if not open_tasks else "unfinished_task_exists",
        "task_runtime_root": str(runtime_root),
        "open_tasks": open_tasks,
        "warnings": warnings,
    }


def task_runtime_scaffold(task_name: str, workspace_root: Path | None = None, force: bool = False) -> TaskRuntimeScaffoldPayload | BoundaryErrorPayload | TaskGateCheckPayload:
    runtime_root = task_runtime_root()
    resolved_workspace_root = resolve_task_workspace_root(task_name, workspace_root, runtime_root)
    boundary_error = workspace_root_boundary_error(resolved_workspace_root)
    if boundary_error is not None:
        return boundary_error
    slug = slugify(task_name)
    prefix = resolve_shared_numbered_prefix(runtime_root, resolved_workspace_root.parent, slug)
    task_dir = runtime_root / f"{prefix}_{slug}"
    runtime_file = task_dir / "task_runtime.yaml"
    if runtime_file.exists() and not force:
        payload = yaml.safe_load(runtime_file.read_text(encoding="utf-8")) or {}
        return {
            "status": "ok",
            "task_root": str(task_dir),
            "task_runtime_file": str(runtime_file),
            "task_id": str(payload.get("task_id", f"{prefix}_{slug}")),
            "task_runtime_root": str(runtime_root),
            "workspace_root": str(payload.get("workspace_root", str(resolved_workspace_root))),
            "reused_existing": True,
        }
    gate_payload = task_gate_check_payload(runtime_root)
    if gate_payload["status"] != "ok":
        return gate_payload
    task_dir.mkdir(parents=True, exist_ok=True)
    resolved_workspace_root.mkdir(parents=True, exist_ok=True)
    payload = _task_runtime_template(f"{prefix}_{slug}", task_name, slug, resolved_workspace_root)
    runtime_file.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return {
        "status": "ok",
        "task_root": str(task_dir),
        "task_runtime_file": str(runtime_file),
        "task_id": payload["task_id"],
        "task_runtime_root": str(runtime_root),
        "workspace_root": str(resolved_workspace_root),
        "reused_existing": False,
    }


def _task_runtime_is_closed(payload: dict[str, Any]) -> bool:
    if payload.get("task_status") != "closed" or payload.get("ended_stage") != "final_delivery":
        return False
    stages = payload.get("stages")
    if not isinstance(stages, dict):
        return False
    return all(isinstance(stages.get(stage), dict) and stages[stage].get("status") == "completed" for stage in STAGE_ORDER)


def _task_runtime_template(task_id: str, task_name: str, task_slug: str, workspace_root: Path | None) -> dict[str, Any]:
    timestamp = datetime.now(timezone.utc).isoformat()
    stages = {
        stage: {"status": "in_progress" if index == 0 else "pending", "checklist": []}
        for index, stage in enumerate(STAGE_ORDER)
    }
    return {
        "task_id": task_id,
        "task_name": task_name,
        "task_slug": task_slug,
        "task_status": "in_progress",
        "workspace_root": "" if workspace_root is None else str(workspace_root.resolve()),
        "created_at": timestamp,
        "updated_at": timestamp,
        "current_stage": "research",
        "current_step": "",
        "ended_stage": "",
        "ended_step": "",
        "ended_reason": "",
        "resume_hint": "从 current_stage/current_step 指向的位置继续推进。",
        "stages": stages,
    }


def slugify(raw: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "_", raw.strip().lower())
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    return cleaned or "task"


def numbered_slot_entries(root: Path) -> list[tuple[int, str, Path]]:
    if not root.exists():
        return []
    entries = []
    for item in root.iterdir():
        if not item.is_dir():
            continue
        parsed = parse_numbered_slot_name(item.name)
        if parsed is not None:
            entries.append((*parsed, item))
    return sorted(entries, key=lambda entry: (entry[0], entry[1], entry[2].name))


def parse_numbered_slot_name(name: str) -> tuple[int, str] | None:
    match = NUMBERED_SLOT_RE.match(name)
    if match is None:
        return None
    return int(match.group("prefix")), match.group("slug")


def highest_numbered_prefix(root: Path) -> int:
    highest = 0
    for prefix, _slug, _path in numbered_slot_entries(root):
        highest = max(highest, prefix)
    return highest


def matching_numbered_prefixes(root: Path, slug: str) -> list[int]:
    return [prefix for prefix, entry_slug, _path in numbered_slot_entries(root) if entry_slug == slug]


def resolve_shared_numbered_prefix(runtime_root: Path, workspace_container: Path, slug: str) -> str:
    matches = matching_numbered_prefixes(runtime_root, slug) + matching_numbered_prefixes(workspace_container, slug)
    if matches:
        return f"{min(matches):03d}"
    next_prefix = max(highest_numbered_prefix(runtime_root), highest_numbered_prefix(workspace_container)) + 1
    return f"{next_prefix:03d}"


def normalize_numbered_workspace_root(workspace_root: Path) -> Path:
    workspace_root = workspace_root.resolve()
    if workspace_root_boundary_error(workspace_root) is not None or parse_numbered_slot_name(workspace_root.name) is not None:
        return workspace_root
    slug = slugify(workspace_root.name)
    container = workspace_root.parent
    matches = [path for _prefix, entry_slug, path in numbered_slot_entries(container) if entry_slug == slug]
    if matches:
        return matches[0]
    return container / f"{highest_numbered_prefix(container) + 1:03d}_{slug}"


def resolve_task_workspace_root(task_name: str, workspace_root: Path | None, runtime_root: Path) -> Path:
    task_slug = slugify(task_name)
    if workspace_root is None:
        container = (managed_root() / "Temporary_Files").resolve()
    else:
        requested_workspace_root = workspace_root.resolve()
        if workspace_root_boundary_error(requested_workspace_root) is not None:
            return requested_workspace_root
        container = requested_workspace_root.parent
    prefix = resolve_shared_numbered_prefix(runtime_root, container, task_slug)
    return container / f"{prefix}_{task_slug}"
