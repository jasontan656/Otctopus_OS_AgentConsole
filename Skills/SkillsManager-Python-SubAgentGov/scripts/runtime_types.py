from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TypeAlias
from typing import TypedDict


SKILL_NAME = "SkillsManager-Python-SubAgentGov"
DEFAULT_MAX_PARALLEL = 4
MAX_ALLOWED_PARALLEL = 4
DEFAULT_POLL_SECONDS = 10
RESULT_STATUSES = {"success_changed", "success_no_change"}
SKILL_EXCLUDE_NAMES = {".system", "_shared"}
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
DEFAULT_REPO_ROOT = SKILL_ROOT.parents[1]

JSONScalar: TypeAlias = str | int | float | bool | None
JSONValue: TypeAlias = JSONScalar | list["JSONValue"] | dict[str, "JSONValue"]
JSONDict: TypeAlias = dict[str, JSONValue]


@dataclass(frozen=True)
class RuntimeConfig:
    repo_root: Path
    skills_root: Path
    runtime_root: Path
    prompt_template_path: Path
    worker_session_template_path: Path
    python_executable: Path
    lint_script: Path
    git_tool: Path
    mirror_tool: Path
    max_parallel: int = DEFAULT_MAX_PARALLEL
    poll_seconds: int = DEFAULT_POLL_SECONDS
    include_self: bool = False


@dataclass(frozen=True)
class Worker:
    skill: str
    session_name: str
    runtime_dir: Path
    prompt_path: Path
    log_path: Path
    last_message_path: Path
    exit_code_path: Path
    state_path: Path
    result_json_path: Path
    result_md_path: Path
    closure_path: Path
    launched_at: float


class DiscoveryExclusion(TypedDict):
    skill_name: str
    reason: str


class DiscoveryPayload(TypedDict):
    status: str
    skills_root: str
    runtime_root: str
    selected_skills: list[str]
    include_self: bool
    discovered_skills: list[str]
    excluded_skills: list[DiscoveryExclusion]


class ActiveWorkerPayload(TypedDict):
    session_name: str
    state: str
    last_log: str


class StatusPayload(TypedDict):
    status: str
    skills_root: str
    runtime_root: str
    pending_count: int
    pending_skills: list[str]
    active: dict[str, ActiveWorkerPayload]
    completed_count: int
    completed_skills: list[str]
    excluded_skills: list[DiscoveryExclusion]
    selected_skills: list[str]


class PromptRenderPayload(TypedDict):
    status: str
    skill_name: str
    runtime_dir: str
    prompt_path: str
    result_json_path: str
    result_md_path: str


class VerificationSummary(TypedDict):
    lint: JSONValue | None
    pytest: JSONValue | None
    help: JSONValue | None


class ClosurePayload(TypedDict):
    skill: str
    status: str
    changed_files: list[str]
    verification: VerificationSummary
    commit_payload: JSONDict
    mirror_payload: JSONDict
    session_name: str
    session_closed: bool
    result_json_path: str
    result_md_path: str


class ControllerSnapshotPayload(TypedDict):
    status: str
    timestamp: int
    skills_root: str
    runtime_root: str
    pending_count: int
    pending_skills: list[str]
    active: dict[str, ActiveWorkerPayload]
    completed_count: int
    completed_skills: list[str]
    selected_skills: list[str]
    excluded_skills: list[DiscoveryExclusion]


class ControllerFinalPayload(TypedDict):
    status: str
    skills_root: str
    runtime_root: str
    completed_count: int
    skills: list[str]
    excluded_skills: list[DiscoveryExclusion]
