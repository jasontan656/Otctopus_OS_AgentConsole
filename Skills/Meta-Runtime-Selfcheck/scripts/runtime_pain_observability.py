from __future__ import annotations

import datetime as dt
import json
import os
from pathlib import Path
from typing import Any

MACHINE_LOG_NAME = "machine.jsonl"
HUMAN_LOG_NAME = "human.log"
HUMAN_SUMMARY_KEY = "octopus_human_summary"
HUMAN_RENDERER = "rich_compatible_plaintext"


def normalize_text(value: str, *, limit: int = 320) -> str:
    flat = " ".join((value or "").split())
    if len(flat) <= limit:
        return flat
    return flat[: max(0, limit - 3)] + "..."


def new_run_id(mode: str) -> str:
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    normalized_mode = str(mode or "diagnose").strip().lower() or "diagnose"
    return f"runtime-pain-batch-{normalized_mode}-{stamp}"


def _is_blocked_runtime_parent(path: Path) -> bool:
    text = str(path.resolve()).replace("\\", "/")
    return (
        "/.codex/skills" in text
        or "/octopus-os-agent-console" in text
        or "/Codex_Skills_Mirror" in text
    )


def _discover_runtime_root_from_cwd() -> Path | None:
    cwd = Path.cwd().resolve()
    for parent in [cwd, *cwd.parents]:
        candidate = (parent / "Codex_Skill_Runtime").resolve()
        if not candidate.exists():
            continue
        if _is_blocked_runtime_parent(candidate.parent):
            continue
        return candidate
    return None


def _discover_runtime_root_from_repo() -> Path | None:
    script_path = Path(__file__).resolve()
    repo_root = next((parent for parent in script_path.parents if parent.name == "octopus-os-agent-console"), None)
    if repo_root is None:
        return None
    candidate = (repo_root.parent / "Codex_Skill_Runtime").resolve()
    if _is_blocked_runtime_parent(candidate.parent):
        return None
    return candidate


def _default_runtime_root() -> Path:
    repo_runtime_root = _discover_runtime_root_from_repo()
    if repo_runtime_root is not None:
        return repo_runtime_root
    discovered = _discover_runtime_root_from_cwd()
    if discovered is not None:
        return discovered
    return (Path.home() / ".codex" / "Codex_Skill_Runtime").resolve()


def _resolve_runtime_log_dir(run_id: str) -> Path:
    runtime_root = os.environ.get("CODEX_SKILL_RUNTIME_ROOT", "").strip()
    if runtime_root:
        base = Path(runtime_root).expanduser().resolve()
    else:
        base = _default_runtime_root()
    return (base / "Meta-Runtime-Selfcheck" / "logs" / "runtime_pain_batch" / run_id).resolve()


def attach_observability_logs(*, run_id: str, mode: str, output: dict[str, Any]) -> dict[str, Any]:
    payload = (
        output.get("runtime_pain_batch_selfcheck_v1", {})
        if isinstance(output.get("runtime_pain_batch_selfcheck_v1", {}), dict)
        else {}
    )
    queue_summary = payload.get("queue_summary", {}) if isinstance(payload.get("queue_summary", {}), dict) else {}
    group_summary = payload.get("group_summary", {}) if isinstance(payload.get("group_summary", {}), dict) else {}
    log_dir = _resolve_runtime_log_dir(run_id)
    machine_path = log_dir / MACHINE_LOG_NAME
    human_path = log_dir / HUMAN_LOG_NAME

    try:
        log_dir.mkdir(parents=True, exist_ok=True)
        machine_event = {
            "run_id": run_id,
            "mode": mode,
            "status": str(output.get("status", "ok") or "ok"),
            "queue_summary": queue_summary,
            "group_summary": group_summary,
        }
        with machine_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(machine_event, ensure_ascii=False) + "\n")

        human_lines = [
            f"run_id: {run_id}",
            f"mode: {mode}",
            f"status: {output.get('status', 'ok')}",
            (
                "queue: "
                f"total={int(queue_summary.get('total_items', 0) or 0)}, "
                f"pending={int(queue_summary.get('pending_items', 0) or 0)}, "
                f"resolved={int(queue_summary.get('resolved_items', 0) or 0)}"
            ),
            (
                "groups: "
                f"total={int(group_summary.get('group_count', 0) or 0)}, "
                f"pending={int(group_summary.get('pending_group_count', 0) or 0)}"
            ),
            f"human_renderer: {HUMAN_RENDERER}",
        ]
        human_path.write_text("\n".join(human_lines) + "\n", encoding="utf-8")
        return {
            "status": "ok",
            "run_id": run_id,
            "machine_log_path": str(machine_path),
            "human_log_path": str(human_path),
            "human_renderer": HUMAN_RENDERER,
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "status": "error",
            "run_id": run_id,
            "error": normalize_text(str(exc), limit=240),
            "machine_log_path": str(machine_path),
            "human_log_path": str(human_path),
            "human_renderer": HUMAN_RENDERER,
        }
