from __future__ import annotations

import re
from pathlib import Path

from managed_agents_text import is_agents_target_kind


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
EXCLUDED_TOP_LEVEL_RELATIVE_DIRS = {
    "Octopus_OS",
}
AGENTS_HUMAN_FILENAME = "AGENTS_human.md"
AGENTS_MACHINE_FILENAME = "AGENTS_machine.json"


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


def _slugify(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", text)


def root_slug(source_root: Path) -> str:
    name = source_root.name.strip()
    if not name:
        return "root"
    return _slugify(name)


def legacy_root_slugs(source_root: Path) -> list[str]:
    slugs = [root_slug(source_root)]
    full_text = source_root.as_posix().strip("/")
    if full_text:
        full_slug = _slugify(full_text)
        if full_slug not in slugs:
            slugs.append(full_slug)
    return slugs


def legacy_managed_rel_paths(source_root: Path, source_path: Path) -> list[Path]:
    relative = source_path.relative_to(source_root)
    return [Path(slug) / relative for slug in legacy_root_slugs(source_root)]


def managed_rel_path(source_root: Path, source_path: Path) -> Path:
    return Path(root_slug(source_root)) / source_path.relative_to(source_root)


def managed_rel_dir(source_root: Path, source_path: Path) -> Path:
    return managed_rel_path(source_root, source_path).parent


def managed_dir_path(skill_root: Path, source_root: Path, source_path: Path) -> Path:
    return managed_root(skill_root) / managed_rel_dir(source_root, source_path)


def managed_file_path(skill_root: Path, source_root: Path, source_path: Path) -> Path:
    return managed_root(skill_root) / managed_rel_path(source_root, source_path)


def agents_human_path(skill_root: Path, source_root: Path, source_path: Path) -> Path:
    return managed_dir_path(skill_root, source_root, source_path) / AGENTS_HUMAN_FILENAME


def agents_machine_path(skill_root: Path, source_root: Path, source_path: Path) -> Path:
    return managed_dir_path(skill_root, source_root, source_path) / AGENTS_MACHINE_FILENAME


def asset_descriptor(
    skill_root: Path,
    source_root: Path,
    source_path: Path,
    target_kind: str,
) -> dict[str, str]:
    descriptor = {
        "managed_rel_path": managed_rel_path(source_root, source_path).as_posix(),
        "managed_rel_dir": managed_rel_dir(source_root, source_path).as_posix(),
        "managed_dir": str(managed_dir_path(skill_root, source_root, source_path)),
    }
    if is_agents_target_kind(target_kind):
        descriptor.update(
            {
                "human_path": str(agents_human_path(skill_root, source_root, source_path)),
                "machine_path": str(agents_machine_path(skill_root, source_root, source_path)),
            }
        )
    else:
        descriptor["managed_path"] = str(managed_file_path(skill_root, source_root, source_path))
    return descriptor


def explicit_target_paths(source_root: Path) -> list[Path]:
    return [(source_root / relative).resolve() for relative in EXPLICIT_TARGET_RELATIVE_PATHS]


def target_kind(source_root: Path, source_path: Path) -> str:
    relative = source_path.resolve().relative_to(source_root.resolve()).as_posix()
    for explicit in EXPLICIT_TARGET_RELATIVE_PATHS:
        if relative == explicit.as_posix():
            return explicit.name
    return source_path.name


def is_excluded_scan_path(candidate: Path, skill_root: Path, source_root: Path | None = None) -> bool:
    if ".git" in candidate.parts:
        return True
    if any(part in EXCLUDED_DIR_NAMES for part in candidate.parts):
        return True
    managed = managed_root(skill_root)
    if candidate.is_relative_to(managed):
        return True
    source_root = (source_root or DEFAULT_SOURCE_ROOT).resolve()
    resolved = candidate.resolve()
    if resolved.is_relative_to(source_root):
        relative = resolved.relative_to(source_root)
        if relative.parts and relative.parts[0] in EXCLUDED_TOP_LEVEL_RELATIVE_DIRS:
            return True
        if len(relative.parts) >= 3 and relative.parts[0] == "Codex_Skills_Mirror" and relative.parts[2] == "assets":
            return True
    return False
