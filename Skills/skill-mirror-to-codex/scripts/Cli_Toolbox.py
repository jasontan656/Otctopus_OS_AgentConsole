#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from pathlib import Path
from pathlib import PurePosixPath
from typing import List

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
CANONICAL_MIRROR_REPO_NAME = "octopus-os-agent-console"
LEGACY_MIRROR_REPO_NAME = "Codex_Skills_Mirror"


def _resolve_codex_root(raw: str | None) -> Path:
    if raw:
        return Path(raw).expanduser().resolve()
    env_root = os.environ.get("CODEX_SKILLS_ROOT")
    if env_root:
        return Path(env_root).expanduser().resolve()
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
        destination_skill_name = _canonical_destination_skill_name(normalized_skill_name)
        src = skill_container / source_skill_name
        dst = codex_root / destination_skill_name
        return src, dst, normalized_skill_name, source_skill_name, destination_skill_name

    return skill_container, codex_root, None, None, None


def _discover_syncable_roots(mirror_root: Path) -> list[tuple[str, Path, Path]]:
    syncable: list[tuple[str, Path, Path]] = []
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
    if scope == "all":
        return True
    return dst.exists()


def _rsync(src: Path, dst: Path, dry_run: bool) -> List[str]:
    if not src.exists():
        raise FileNotFoundError(f"source does not exist: {src}")

    dst.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["rsync", "-a", "--delete"]
    for pattern in RSYNC_EXCLUDES:
        cmd.extend(["--exclude", pattern])
    if dry_run:
        cmd.append("--dry-run")

    cmd.extend([f"{src}/", f"{dst}/"])
    completed = subprocess.run(cmd, check=False, capture_output=True, text=True)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or "rsync failed")
    return cmd


def _rsync_syncable_roots(
    mirror_root: Path,
    codex_root: Path,
    dry_run: bool,
) -> tuple[list[dict[str, str]], list[list[str]]]:
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
    return synced_entries, commands


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Skill-Mirror-to-Codex toolbox (one-way: mirror -> codex)"
    )
    parser.add_argument("--scope", choices=["all", "skill"], default="all")
    parser.add_argument("--skill-name")
    parser.add_argument("--mode", choices=["auto", "push", "install"], default="auto")
    parser.add_argument("--codex-root")
    parser.add_argument("--mirror-root")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    codex_root = _resolve_codex_root(args.codex_root)
    mirror_root = _resolve_mirror_root(args.mirror_root)

    if not codex_root.exists():
        raise FileNotFoundError(f"codex root does not exist: {codex_root}")

    src, dst, normalized_skill_name, source_skill_name, destination_skill_name = _build_paths(
        codex_root=codex_root,
        mirror_root=mirror_root,
        scope=args.scope,
        skill_name=args.skill_name,
    )
    if not src.exists():
        raise FileNotFoundError(f"source does not exist: {src}")

    if args.mode == "install" and args.scope != "skill":
        raise ValueError("--mode=install only supports --scope=skill")

    destination_exists = _destination_exists(dst=dst, scope=args.scope)
    if args.mode == "push":
        resolved_mode = "push"
    elif args.mode == "install":
        resolved_mode = "install"
    else:
        resolved_mode = "push" if destination_exists else "install"

    if resolved_mode == "install":
        payload = {
            "status": "route_required",
            "action": "install_via_external_skills",
            "scope": args.scope,
            "skill_name": normalized_skill_name,
            "requested_skill_name": args.skill_name,
            "source_skill_name": source_skill_name,
            "destination_skill_name": destination_skill_name,
            "resolved_mode": "install",
            "source": str(src),
            "destination": str(dst),
            "mirror_root": str(mirror_root),
            "skills_root": str(_resolve_skill_container(mirror_root)),
            "codex_root": str(codex_root),
            "dry_run": bool(args.dry_run),
            "destination_exists": destination_exists,
            "next_skills": [
                "Skill-creator",
                "Skill-installer",
            ],
            "next_steps": [
                "Use Skill-creator to validate the skill folder format and fix issues if needed.",
                "Use Skill-installer to install the skill into the codex skills directory.",
            ],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    payload: dict[str, object] = {
        "status": "ok",
        "action": "mirror_to_codex",
        "scope": args.scope,
        "skill_name": normalized_skill_name,
        "requested_skill_name": args.skill_name,
        "source_skill_name": source_skill_name,
        "destination_skill_name": destination_skill_name,
        "resolved_mode": "push",
        "source": str(src),
        "destination": str(dst),
        "mirror_root": str(mirror_root),
        "skills_root": str(_resolve_skill_container(mirror_root)),
        "codex_root": str(codex_root),
        "dry_run": bool(args.dry_run),
        "destination_exists": destination_exists,
    }

    if args.scope == "all":
        synced_entries, commands = _rsync_syncable_roots(
            mirror_root=mirror_root,
            codex_root=codex_root,
            dry_run=args.dry_run,
        )
        payload["synced_entries"] = synced_entries
        payload["commands"] = commands
    else:
        command = _rsync(src=src, dst=dst, dry_run=args.dry_run)
        payload["command"] = command
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2))
        raise SystemExit(1)
