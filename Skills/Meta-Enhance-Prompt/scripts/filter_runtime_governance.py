#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import json
import os
from pathlib import Path
from typing import TypedDict


SKILL_NAME = "Meta-Enhance-Prompt"
MACHINE_LOG_NAME = "machine.jsonl"
HUMAN_LOG_NAME = "human.log"


class RuntimeLogPaths(TypedDict):
    machine_log_path: str
    human_log_path: str


class RuntimePayloadRecord(TypedDict, total=False):
    mode_decision: str
    filter_exit_code: int
    filter_exit_message: str
    publish_blocked: bool
    final_prompt_copy_paste: str
    final_skill_read_directive: str
    intent_summary: str
    chat_publish_policy: str
    run_id: str
    output_path: str
    runtime_logs: RuntimeLogPaths


def _repo_root_from_script() -> Path | None:
    script_path = Path(__file__).resolve()
    return next((parent for parent in script_path.parents if parent.name == "Otctopus_OS_AgentConsole"), None)


def _workspace_root_from_cwd() -> Path | None:
    cwd = Path.cwd().resolve()
    for parent in [cwd, *cwd.parents]:
        if (parent / "Codex_Skill_Runtime").exists() or (parent / "Codex_Skills_Result").exists():
            return parent
    return None


def resolve_workspace_root() -> Path:
    env_root = os.environ.get("META_ENHANCE_PROMPT_WORKSPACE_ROOT", "").strip()
    if env_root:
        return Path(env_root).expanduser().resolve()
    repo_root = _repo_root_from_script()
    if repo_root is not None:
        return repo_root.parent.resolve()
    cwd_root = _workspace_root_from_cwd()
    if cwd_root is not None:
        return cwd_root
    codex_home = os.environ.get("CODEX_HOME", "").strip()
    if codex_home:
        return Path(codex_home).expanduser().resolve()
    return (Path.home() / ".codex").resolve()


def governed_runtime_root() -> Path:
    base = resolve_workspace_root()
    return (base / "Codex_Skill_Runtime" / SKILL_NAME).resolve()


def governed_result_root() -> Path:
    base = resolve_workspace_root()
    return (base / "Codex_Skills_Result" / SKILL_NAME).resolve()


def new_run_id(mode: str) -> str:
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    normalized_mode = str(mode or "active_invoke").strip().lower() or "active_invoke"
    return f"meta-enhance-prompt-{normalized_mode}-{stamp}"


def default_output_path(*, mode: str) -> Path:
    filename = "latest.txt"
    return (governed_result_root() / mode / filename).resolve()


def write_output_artifact(*, mode: str, rendered_output: str, output_path: str | None) -> Path:
    target = Path(output_path).expanduser().resolve() if output_path else default_output_path(mode=mode)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(rendered_output, encoding="utf-8")
    return target


def attach_runtime_logs(
    *,
    run_id: str,
    mode: str,
    status: str,
    output_path: Path,
    payload: RuntimePayloadRecord,
) -> RuntimeLogPaths:
    log_dir = (governed_runtime_root() / "logs" / mode).resolve()
    log_dir.mkdir(parents=True, exist_ok=True)
    machine_path = log_dir / MACHINE_LOG_NAME
    human_path = log_dir / HUMAN_LOG_NAME

    machine_event = {
        "run_id": run_id,
        "mode": mode,
        "status": status,
        "output_path": str(output_path),
        "payload_keys": sorted(payload.keys()),
    }
    with machine_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(machine_event, ensure_ascii=False) + "\n")

    human_lines = [
        f"run_id: {run_id}",
        f"mode: {mode}",
        f"status: {status}",
        f"output_path: {output_path}",
        f"payload_keys: {', '.join(sorted(payload.keys()))}",
    ]
    with human_path.open("a", encoding="utf-8") as handle:
        handle.write("\n".join(human_lines) + "\n\n")

    return {
        "machine_log_path": str(machine_path),
        "human_log_path": str(human_path),
    }
