from __future__ import annotations

import os
import re
import shutil
import subprocess
from pathlib import Path
from pathlib import PurePosixPath

from sync_payloads import build_rename_result


VALID_SKILL_SEGMENT_RE = re.compile(r"^[A-Za-z0-9._-]+$")
RSYNC_EXCLUDES = (
    ".git/",
    "__pycache__/",
    "*.pyc",
    "Codex_Skill_Runtime/",
)
SYSTEM_SKILL_NAMESPACE = ".system"
SYSTEM_SKILL_MARKER = ".codex-system-skills.marker"
SKILLS_DIR_NAME = "Skills"
CANONICAL_MIRROR_REPO_NAME = "Otctopus_OS_AgentConsole"
LEGACY_MIRROR_REPO_NAME = "Codex_Skills_Mirror"
FORBIDDEN_CODEX_ROOT_FILES = ("AGENTS.md",)


def _detect_repo_root() -> Path | None:
    script_path = Path(__file__).resolve()
    return next((parent for parent in script_path.parents if parent.name == CANONICAL_MIRROR_REPO_NAME), None)


def _resolve_codex_root(raw: str | None) -> Path:
    if raw:
        return Path(raw).expanduser().resolve()
    repo_root = _detect_repo_root()
    if repo_root is not None:
        local_codex_root = (repo_root.parent / ".codex" / "skills").resolve()
        if local_codex_root.exists():
            return local_codex_root
    env_root = os.environ.get("CODEX_SKILLS_ROOT")
    if env_root:
        return Path(env_root).expanduser().resolve()
    env_home = os.environ.get("CODEX_HOME")
    if env_home:
        return (Path(env_home).expanduser().resolve() / "skills").resolve()
    return (Path.home() / ".codex" / "skills").resolve()


def _discover_visible_mirror() -> Path | None:
    env_root = os.environ.get("CODEX_SKILLS_MIRROR_ROOT")
    if env_root:
        return Path(env_root).expanduser().resolve()

    for repo_name in (CANONICAL_MIRROR_REPO_NAME, LEGACY_MIRROR_REPO_NAME):
        for candidate in sorted(Path.home().glob(f"*/{repo_name}")):
            if candidate.is_dir():
                return candidate.resolve()
    return None


def _migrate_hidden_mirror_if_present() -> Path | None:
    for repo_name in (CANONICAL_MIRROR_REPO_NAME, LEGACY_MIRROR_REPO_NAME):
        for hidden in sorted(Path.home().glob(f"*/{repo_name}")):
            if not hidden.is_dir():
                continue
            visible = hidden.parent / CANONICAL_MIRROR_REPO_NAME
            if visible.exists() and visible.is_dir():
                return visible.resolve()
            os.replace(hidden, visible)
            return visible.resolve()
    return None


def _resolve_mirror_root(raw: str | None) -> Path:
    if raw:
        return Path(raw).expanduser().resolve()
    repo_root = _detect_repo_root()
    if repo_root is not None:
        return repo_root.resolve()

    visible = _discover_visible_mirror()
    if visible is not None:
        return visible

    migrated = _migrate_hidden_mirror_if_present()
    if migrated is not None:
        return migrated

    fallback = (Path.cwd() / CANONICAL_MIRROR_REPO_NAME).resolve()
    fallback.mkdir(parents=True, exist_ok=True)
    return fallback


def _resolve_skill_container(mirror_root: Path) -> Path:
    skills_root = mirror_root / SKILLS_DIR_NAME
    if skills_root.is_dir():
        return skills_root.resolve()
    return mirror_root.resolve()


def _normalize_skill_name(skill_name: str) -> str:
    normalized = str(skill_name or "").strip()
    if not normalized:
        raise ValueError("skill_name cannot be empty")
    if "\\" in normalized:
        raise ValueError("skill_name must use forward slashes")
    if normalized.startswith("/") or normalized.endswith("/"):
        raise ValueError("skill_name must be a relative skill path")

    posix_path = PurePosixPath(normalized)
    if posix_path.is_absolute():
        raise ValueError("skill_name must be a relative skill path")

    raw_parts = normalized.split("/")
    normalized_parts: list[str] = []
    for part in raw_parts:
        if not part:
            raise ValueError("skill_name contains empty path segments")
        if part in {".", ".."}:
            raise ValueError("skill_name cannot contain dot traversal segments")
        if not VALID_SKILL_SEGMENT_RE.match(part):
            raise ValueError("skill_name contains illegal characters")
        normalized_parts.append(part)
    return "/".join(normalized_parts)


def _posix_join(parts: list[str]) -> str:
    return "/".join(parts)


def _resolve_existing_source_skill_name(mirror_root: Path, normalized_skill_name: str) -> str:
    current = mirror_root
    actual_parts: list[str] = []
    for part in normalized_skill_name.split("/"):
        exact = current / part
        if exact.exists():
            actual_parts.append(part)
            current = exact
            continue

        try:
            children = list(current.iterdir())
        except FileNotFoundError as exc:
            raise FileNotFoundError(f"source does not exist: {mirror_root / normalized_skill_name}") from exc

        folded_matches = [child.name for child in children if child.name.casefold() == part.casefold()]
        if len(folded_matches) != 1:
            raise FileNotFoundError(f"source does not exist: {mirror_root / normalized_skill_name}")
        actual_part = folded_matches[0]
        actual_parts.append(actual_part)
        current = current / actual_part
    return _posix_join(actual_parts)


def _canonical_destination_skill_name(normalized_skill_name: str) -> str:
    parts = normalized_skill_name.split("/")
    if parts and parts[0] == SYSTEM_SKILL_NAMESPACE:
        return _posix_join([parts[0], *[part.lower() for part in parts[1:]]])
    return normalized_skill_name


def _resolve_destination_skill_path(codex_root: Path, normalized_skill_name: str) -> tuple[str, Path]:
    destination_skill_name = _canonical_destination_skill_name(normalized_skill_name)
    return destination_skill_name, codex_root / destination_skill_name


def _build_paths(
    codex_root: Path,
    mirror_root: Path,
    scope: str,
    skill_name: str | None,
) -> tuple[Path, Path, str | None, str | None, str | None]:
    skill_container = _resolve_skill_container(mirror_root)
    if scope == "skill":
        if not skill_name:
            raise ValueError("--skill-name is required when --scope=skill")
        normalized_skill_name = _normalize_skill_name(skill_name)
        source_skill_name = _resolve_existing_source_skill_name(skill_container, normalized_skill_name)
        destination_skill_name, dst = _resolve_destination_skill_path(codex_root, normalized_skill_name)
        src = skill_container / source_skill_name
        return src, dst, normalized_skill_name, source_skill_name, destination_skill_name
    return skill_container, codex_root, None, None, None


def _discover_syncable_roots(mirror_root: Path) -> list[tuple[str, Path, str]]:
    syncable: list[tuple[str, Path, str]] = []
    skill_container = _resolve_skill_container(mirror_root)
    for child in sorted(skill_container.iterdir(), key=lambda item: item.name.lower()):
        if not child.is_dir():
            continue
        if child.name == ".git":
            continue
        if child.name == SYSTEM_SKILL_NAMESPACE:
            if (child / SYSTEM_SKILL_MARKER).exists():
                syncable.append((child.name, child, child.name))
            continue
        if child.name.startswith("."):
            continue
        if (child / "SKILL.md").is_file():
            syncable.append((child.name, child, child.name))
    if not syncable:
        raise FileNotFoundError(f"no syncable skill roots found under mirror root: {skill_container}")
    return syncable


def _destination_exists(dst: Path, scope: str) -> bool:
    return True if scope == "all" else dst.exists()


def _rsync(src: Path, dst: Path, dry_run: bool) -> list[str]:
    if not src.exists():
        raise FileNotFoundError(f"source does not exist: {src}")

    dst.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["rsync", "-a", "--delete", "--delete-excluded", "--checksum"]
    for pattern in RSYNC_EXCLUDES:
        cmd.extend(["--exclude", pattern])
    if dry_run:
        cmd.append("--dry-run")

    cmd.extend([f"{src}/", f"{dst}/"])
    completed = subprocess.run(cmd, check=False, capture_output=True, text=True)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or "rsync failed")
    return cmd


def _remove_path(target: Path) -> None:
    if not target.exists():
        return
    if target.is_dir():
        shutil.rmtree(target)
        return
    target.unlink()


def _rsync_syncable_roots(
    mirror_root: Path,
    codex_root: Path,
    dry_run: bool,
) -> tuple[list[dict[str, str]], list[list[str]], list[str]]:
    synced_entries: list[dict[str, str]] = []
    commands: list[list[str]] = []
    for root_name, source_root, destination_name in _discover_syncable_roots(mirror_root):
        destination_root = codex_root / destination_name
        command = _rsync(src=source_root, dst=destination_root, dry_run=dry_run)
        synced_entries.append(
            {
                "root_name": root_name,
                "source": str(source_root),
                "destination": str(destination_root),
            }
        )
        commands.append(command)
    removed_forbidden_entries: list[str] = []
    for name in FORBIDDEN_CODEX_ROOT_FILES:
        target = codex_root / name
        if not target.exists():
            continue
        removed_forbidden_entries.append(str(target))
        if dry_run:
            continue
        _remove_path(target)
    return synced_entries, commands, removed_forbidden_entries


def _rename_push(
    *,
    src: Path,
    codex_root: Path,
    normalized_skill_name: str,
    source_skill_name: str,
    destination_skill_name: str,
    requested_skill_name: str | None,
    rename_from: str,
    dry_run: bool,
    mirror_root: Path,
) -> dict[str, object]:
    old_skill_name = _normalize_skill_name(rename_from)
    old_destination_skill_name, old_destination = _resolve_destination_skill_path(codex_root, old_skill_name)
    new_destination = codex_root / destination_skill_name

    if old_destination_skill_name == destination_skill_name:
        raise ValueError("--rename-from must differ from --skill-name")

    old_destination_exists = old_destination.exists()
    new_destination_exists = new_destination.exists()
    if not old_destination_exists and not new_destination_exists:
        raise FileNotFoundError(
            "rename target does not exist in codex root; use push/install instead of rename"
        )

    staged_destination = old_destination if old_destination_exists else new_destination
    command = _rsync(src=src, dst=staged_destination, dry_run=dry_run)

    renamed_path = False
    removed_new_destination = False
    if not dry_run and old_destination_exists and old_destination != new_destination:
        if new_destination.exists():
            _remove_path(new_destination)
            removed_new_destination = True
        new_destination.parent.mkdir(parents=True, exist_ok=True)
        os.replace(old_destination, new_destination)
        renamed_path = True

    return build_rename_result(
        skill_name=normalized_skill_name,
        requested_skill_name=requested_skill_name,
        source_skill_name=source_skill_name,
        destination_skill_name=destination_skill_name,
        src=src,
        destination=new_destination,
        mirror_root=mirror_root,
        skills_root=_resolve_skill_container(mirror_root),
        codex_root=codex_root,
        dry_run=bool(dry_run),
        rename_from=old_skill_name,
        rename_from_destination_skill_name=old_destination_skill_name,
        rename_from_destination=old_destination,
        staged_destination=staged_destination,
        rename_source_exists=old_destination_exists,
        rename_destination_preexisting=new_destination_exists,
        removed_existing_new_destination=removed_new_destination,
        renamed_path=renamed_path,
        command=command,
    )

