from __future__ import annotations

import re
from pathlib import Path


DEFAULT_SOURCE_ROOT = Path("/home/jasontan656/AI_Projects")
RECURSIVE_TARGET_BASENAMES = ("AGENTS.md", ".gitignore")
EXPLICIT_TARGET_RELATIVE_PATHS = (
    Path("Octopus_CodeBase_Backend/README.md"),
    Path("Octopus_CodeBase_Backend/Deployment_Guide.md"),
)
EXCLUDED_DIR_NAMES = {
    "Human_Work_Zone",
    "Codex_Skills_Result",
    "Codex_Skill_Runtime",
    "__pycache__",
    ".pytest_cache",
    "node_modules",
    ".venv",
    "venv",
}


def resolve_skill_root(raw: str | None) -> Path:
    if raw:
        return Path(raw).expanduser().resolve()
    return Path(__file__).resolve().parents[1]


def resolve_source_root(raw: str | None) -> Path:
    if raw:
        return Path(raw).expanduser().resolve()
    return DEFAULT_SOURCE_ROOT


def managed_root(skill_root: Path) -> Path:
    return skill_root / "assets" / "managed_targets"


def registry_path(skill_root: Path) -> Path:
    return managed_root(skill_root) / "registry.json"


def index_path(skill_root: Path) -> Path:
    return managed_root(skill_root) / "index.md"


def scan_report_path(skill_root: Path) -> Path:
    return managed_root(skill_root) / "scan_report.json"


def lock_path(skill_root: Path) -> Path:
    return managed_root(skill_root) / ".cli.lock"


def root_slug(source_root: Path) -> str:
    text = source_root.as_posix().strip("/")
    if not text:
        return "root"
    return re.sub(r"[^A-Za-z0-9._-]+", "_", text)


def managed_rel_path(source_root: Path, source_path: Path) -> Path:
    return Path(root_slug(source_root)) / source_path.relative_to(source_root)


def managed_file_path(skill_root: Path, source_root: Path, source_path: Path) -> Path:
    return managed_root(skill_root) / managed_rel_path(source_root, source_path)


def explicit_target_paths(source_root: Path) -> list[Path]:
    return [(source_root / relative).resolve() for relative in EXPLICIT_TARGET_RELATIVE_PATHS]


def target_kind(source_root: Path, source_path: Path) -> str:
    relative = source_path.resolve().relative_to(source_root.resolve()).as_posix()
    for explicit in EXPLICIT_TARGET_RELATIVE_PATHS:
        if relative == explicit.as_posix():
            return explicit.name
    return source_path.name


def is_excluded_scan_path(candidate: Path, skill_root: Path) -> bool:
    if ".git" in candidate.parts:
        return True
    if any(part in EXCLUDED_DIR_NAMES for part in candidate.parts):
        return True
    managed = managed_root(skill_root)
    return candidate.is_relative_to(managed)
