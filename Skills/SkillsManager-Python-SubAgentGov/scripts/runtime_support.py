from __future__ import annotations

import time
from pathlib import Path

from command_support import tmux_exists
from runtime_types import ActiveWorkerPayload
from runtime_types import DEFAULT_MAX_PARALLEL
from runtime_types import DEFAULT_POLL_SECONDS
from runtime_types import DEFAULT_REPO_ROOT
from runtime_types import DiscoveryExclusion
from runtime_types import DiscoveryPayload
from runtime_types import MAX_ALLOWED_PARALLEL
from runtime_types import PromptRenderPayload
from runtime_types import RuntimeConfig
from runtime_types import SKILL_EXCLUDE_NAMES
from runtime_types import SKILL_NAME
from runtime_types import StatusPayload
from runtime_types import Worker
from result_support import read_tail


def build_config(
    *,
    repo_root: Path | None = None,
    skills_root: Path | None = None,
    runtime_root: Path | None = None,
    include_self: bool = False,
    max_parallel: int = DEFAULT_MAX_PARALLEL,
    poll_seconds: int = DEFAULT_POLL_SECONDS,
) -> RuntimeConfig:
    repo_root = (repo_root or DEFAULT_REPO_ROOT).resolve()
    skills_root = (skills_root or (repo_root / "Skills")).resolve()
    runtime_root = (runtime_root or (repo_root.parent / "Codex_Skill_Runtime" / SKILL_NAME)).resolve()
    if not (1 <= max_parallel <= MAX_ALLOWED_PARALLEL):
        raise ValueError(f"max_parallel must be between 1 and {MAX_ALLOWED_PARALLEL}")
    if poll_seconds < 1:
        raise ValueError("poll_seconds must be at least 1 second")
    return RuntimeConfig(
        repo_root=repo_root,
        skills_root=skills_root,
        runtime_root=runtime_root,
        prompt_template_path=(repo_root / "Skills" / SKILL_NAME / "assets" / "prompt_template.md").resolve(),
        worker_session_template_path=(
            repo_root / "Skills" / SKILL_NAME / "assets" / "worker_session_template.sh"
        ).resolve(),
        python_executable=(repo_root / ".venv_backend_skills" / "bin" / "python3").resolve(),
        lint_script=(repo_root / "Skills" / "Dev-PythonCode-Constitution" / "scripts" / "run_python_code_lints.py").resolve(),
        git_tool=(repo_root / "Skills" / "Meta-github-operation" / "scripts" / "Cli_Toolbox.py").resolve(),
        mirror_tool=(repo_root / "Skills" / "SkillsManager-Mirror-To-Codex" / "scripts" / "Cli_Toolbox.py").resolve(),
        max_parallel=max_parallel,
        poll_seconds=poll_seconds,
        include_self=include_self,
    )


def ensure_runtime_layout(config: RuntimeConfig) -> None:
    config.runtime_root.mkdir(parents=True, exist_ok=True)


def normalize_selected_skills(skill_names: list[str] | None) -> list[str] | None:
    if not skill_names:
        return None
    normalized: list[str] = []
    for item in skill_names:
        value = item.strip()
        if value and value not in normalized:
            normalized.append(value)
    return normalized or None


def safe_session_name(skill: str) -> str:
    return f"pygov_{skill.lower().replace('-', '_')}"[:80]


def build_worker(config: RuntimeConfig, skill: str) -> Worker:
    runtime_dir = config.runtime_root / skill
    return Worker(
        skill=skill,
        session_name=safe_session_name(skill),
        runtime_dir=runtime_dir,
        prompt_path=runtime_dir / "prompt.md",
        log_path=runtime_dir / "codex.jsonl",
        last_message_path=runtime_dir / "last_message.txt",
        exit_code_path=runtime_dir / "exit_code.txt",
        state_path=runtime_dir / "state.txt",
        result_json_path=runtime_dir / "result.json",
        result_md_path=runtime_dir / "result.md",
        closure_path=runtime_dir / "closure.json",
        launched_at=time.time(),
    )


def render_prompt(config: RuntimeConfig, skill: str) -> PromptRenderPayload:
    worker = build_worker(config, skill)
    worker.runtime_dir.mkdir(parents=True, exist_ok=True)
    prompt = config.prompt_template_path.read_text(encoding="utf-8")
    for placeholder, value in {
        "__SKILL_NAME__": skill,
        "__REPO_ROOT__": str(config.repo_root),
        "__RUNTIME_DIR__": str(worker.runtime_dir),
        "__RESULT_JSON__": str(worker.result_json_path),
        "__RESULT_MD__": str(worker.result_md_path),
    }.items():
        prompt = prompt.replace(placeholder, value)
    worker.prompt_path.write_text(prompt, encoding="utf-8")
    return {
        "status": "ok",
        "skill_name": skill,
        "runtime_dir": str(worker.runtime_dir),
        "prompt_path": str(worker.prompt_path),
        "result_json_path": str(worker.result_json_path),
        "result_md_path": str(worker.result_md_path),
    }


def discover_skills(config: RuntimeConfig, *, skill_names: list[str] | None = None) -> DiscoveryPayload:
    selected = normalize_selected_skills(skill_names)
    if not config.skills_root.exists():
        raise FileNotFoundError(f"skills root does not exist: {config.skills_root}")
    skill_dirs = {path.name: path for path in sorted(config.skills_root.iterdir()) if path.is_dir()}
    requested = selected if selected is not None else sorted(skill_dirs)
    discovered: list[str] = []
    excluded: list[DiscoveryExclusion] = []
    for name in requested:
        path = skill_dirs.get(name)
        if path is None:
            raise FileNotFoundError(f"target skill does not exist under skills root: {name}")
        if name in SKILL_EXCLUDE_NAMES:
            excluded.append({"skill_name": name, "reason": "reserved_skill_container"})
            continue
        if not (path / "SKILL.md").exists():
            excluded.append({"skill_name": name, "reason": "missing_skill_facade"})
            continue
        if name == SKILL_NAME and selected is None and not config.include_self:
            excluded.append({"skill_name": name, "reason": "self_governance_requires_explicit_target"})
            continue
        discovered.append(name)
    return {
        "status": "ok",
        "skills_root": str(config.skills_root),
        "runtime_root": str(config.runtime_root),
        "selected_skills": selected or [],
        "include_self": config.include_self,
        "discovered_skills": discovered,
        "excluded_skills": excluded,
    }


def resume_state(config: RuntimeConfig, skills: list[str]) -> tuple[list[str], dict[str, Worker], list[str]]:
    pending: list[str] = []
    active: dict[str, Worker] = {}
    completed: list[str] = []
    for skill in skills:
        worker = build_worker(config, skill)
        if worker.closure_path.exists():
            completed.append(skill)
        elif worker.exit_code_path.exists() or worker.result_json_path.exists() or tmux_exists(worker.session_name):
            active[skill] = worker
        else:
            pending.append(skill)
    return pending, active, completed


def status_payload(config: RuntimeConfig, *, skill_names: list[str] | None = None) -> StatusPayload:
    discovered = discover_skills(config, skill_names=skill_names)
    pending, active_workers, completed = resume_state(config, list(discovered["discovered_skills"]))
    active: dict[str, ActiveWorkerPayload] = {}
    for skill, worker in active_workers.items():
        state = worker.state_path.read_text(encoding="utf-8").strip() if worker.state_path.exists() else "running"
        active[skill] = {"session_name": worker.session_name, "state": state, "last_log": read_tail(worker.log_path)}
    return {
        "status": "ok",
        "skills_root": str(config.skills_root),
        "runtime_root": str(config.runtime_root),
        "pending_count": len(pending),
        "pending_skills": pending,
        "active": active,
        "completed_count": len(completed),
        "completed_skills": completed,
        "excluded_skills": list(discovered["excluded_skills"]),
        "selected_skills": list(discovered["selected_skills"]),
    }
