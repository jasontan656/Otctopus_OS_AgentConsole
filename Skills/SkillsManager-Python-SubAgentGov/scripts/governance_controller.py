from __future__ import annotations

import json
import shlex
import shutil
import time
from pathlib import Path

from command_support import run_cmd
from result_support import read_tail
from result_support import worker_ready
from runtime_support import build_worker
from runtime_support import discover_skills
from runtime_support import ensure_runtime_layout
from runtime_support import render_prompt
from runtime_support import resume_state
from runtime_types import ControllerFinalPayload
from runtime_types import ControllerSnapshotPayload
from runtime_types import RuntimeConfig
from runtime_types import Worker

from closeout_support import process_completion


def _require_file(path: str, label: str) -> None:
    if not shutil.which(path) and label in {"codex", "tmux"}:
        raise RuntimeError(f"{label} command is not available in PATH")


def _require_asset(path: Path, label: str) -> None:
    if not path.exists():
        raise FileNotFoundError(f"{label} not found: {path}")


def validate_runtime_prerequisites(config: RuntimeConfig) -> None:
    for path, label in (
        (config.prompt_template_path, "prompt template"),
        (config.worker_session_template_path, "worker session template"),
        (config.python_executable, "skills backend python"),
        (config.lint_script, "Dev-PythonCode-Constitution lint entry"),
        (config.git_tool, "Meta-github-operation CLI"),
        (config.mirror_tool, "SkillsManager-Mirror-To-Codex CLI"),
    ):
        _require_asset(path, label)
    _require_file("codex", "codex")
    _require_file("tmux", "tmux")


def _render_worker_session_script(config: RuntimeConfig, worker: Worker) -> str:
    tmp_dir = worker.runtime_dir / "tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    script = config.worker_session_template_path.read_text(encoding="utf-8")
    substitutions = {
        "__REPO_ROOT__": shlex.quote(str(config.repo_root)),
        "__TMP_DIR__": shlex.quote(str(tmp_dir)),
        "__LAST_MESSAGE_PATH__": shlex.quote(str(worker.last_message_path)),
        "__PROMPT_PATH__": shlex.quote(str(worker.prompt_path)),
        "__LOG_PATH__": shlex.quote(str(worker.log_path)),
        "__EXIT_CODE_PATH__": shlex.quote(str(worker.exit_code_path)),
        "__STATE_PATH__": shlex.quote(str(worker.state_path)),
    }
    for placeholder, value in substitutions.items():
        script = script.replace(placeholder, value)
    return script


def _launch_worker(config: RuntimeConfig, skill: str) -> Worker:
    worker = build_worker(config, skill)
    worker.runtime_dir.mkdir(parents=True, exist_ok=True)
    render_prompt(config, skill)
    session_script = _render_worker_session_script(config, worker)
    run_cmd(["tmux", "new-session", "-d", "-s", worker.session_name, f"bash -lc {shlex.quote(session_script)}"], cwd=config.repo_root)
    return worker


def _write_controller_status(config: RuntimeConfig, payload: ControllerSnapshotPayload | ControllerFinalPayload) -> None:
    ensure_runtime_layout(config)
    status_path = config.runtime_root / "controller_status.json"
    status_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def govern(config: RuntimeConfig, *, skill_names: list[str] | None = None) -> ControllerFinalPayload:
    validate_runtime_prerequisites(config)
    ensure_runtime_layout(config)
    discovered = discover_skills(config, skill_names=skill_names)
    pending, active, completed = resume_state(config, list(discovered["discovered_skills"]))
    while pending and len(active) < config.max_parallel:
        skill = pending.pop(0)
        active[skill] = _launch_worker(config, skill)
    while pending or active:
        finished_now: list[str] = []
        for skill, worker in list(active.items()):
            if worker_ready(worker):
                process_completion(config, worker)
                completed.append(skill)
                finished_now.append(skill)
                del active[skill]
        for _ in finished_now:
            while pending and len(active) < config.max_parallel:
                skill = pending.pop(0)
                active[skill] = _launch_worker(config, skill)
        snapshot: ControllerSnapshotPayload = {
            "status": "running",
            "timestamp": int(time.time()),
            "skills_root": str(config.skills_root),
            "runtime_root": str(config.runtime_root),
            "pending_count": len(pending),
            "pending_skills": pending,
            "active": {
                skill: {
                    "session_name": worker.session_name,
                    "state": worker.state_path.read_text(encoding="utf-8").strip() if worker.state_path.exists() else "running",
                    "last_log": read_tail(worker.log_path),
                }
                for skill, worker in active.items()
            },
            "completed_count": len(completed),
            "completed_skills": completed[-10:],
            "selected_skills": list(discovered["selected_skills"]),
            "excluded_skills": list(discovered["excluded_skills"]),
        }
        _write_controller_status(config, snapshot)
        if pending or active:
            time.sleep(config.poll_seconds)
    final_payload: ControllerFinalPayload = {
        "status": "done",
        "skills_root": str(config.skills_root),
        "runtime_root": str(config.runtime_root),
        "completed_count": len(completed),
        "skills": completed,
        "excluded_skills": list(discovered["excluded_skills"]),
    }
    _write_controller_status(config, final_payload)
    return final_payload
