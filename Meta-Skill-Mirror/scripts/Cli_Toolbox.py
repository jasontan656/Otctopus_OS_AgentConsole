#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from pathlib import Path
from typing import List

VALID_SKILL_RE = re.compile(r"^[A-Za-z0-9._-]+$")
RSYNC_EXCLUDES = (
    ".git/",
    "__pycache__/",
    "*.pyc",
    "Codex_Skill_Runtime/",
)


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

    for candidate in sorted(Path.home().glob("*/Codex_Skills_Mirror")):
        if candidate.is_dir():
            return candidate.resolve()
    return None


def _migrate_hidden_mirror_if_present() -> Path | None:
    for hidden in sorted(Path.home().glob("*/Codex_Skills_Mirror")):
        if not hidden.is_dir():
            continue
        visible = hidden.parent / "Codex_Skills_Mirror"
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

    fallback = (Path.cwd() / "Codex_Skills_Mirror").resolve()
    fallback.mkdir(parents=True, exist_ok=True)
    return fallback


def _validate_skill_name(skill_name: str) -> None:
    if not VALID_SKILL_RE.match(skill_name):
        raise ValueError("skill_name contains illegal characters")


def _build_paths(codex_root: Path, mirror_root: Path, scope: str, skill_name: str | None) -> tuple[Path, Path]:
    if scope == "skill":
        if not skill_name:
            raise ValueError("--skill-name is required when --scope=skill")
        _validate_skill_name(skill_name)
        src = mirror_root / skill_name
        dst = codex_root / skill_name
        return src, dst

    return mirror_root, codex_root


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


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Meta-Skill-Mirror toolbox (one-way: mirror -> codex)"
    )
    parser.add_argument("--scope", choices=["all", "skill"], default="all")
    parser.add_argument("--skill-name")
    parser.add_argument("--codex-root")
    parser.add_argument("--mirror-root")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    codex_root = _resolve_codex_root(args.codex_root)
    mirror_root = _resolve_mirror_root(args.mirror_root)

    if not codex_root.exists():
        raise FileNotFoundError(f"codex root does not exist: {codex_root}")

    src, dst = _build_paths(
        codex_root=codex_root,
        mirror_root=mirror_root,
        scope=args.scope,
        skill_name=args.skill_name,
    )

    command = _rsync(src=src, dst=dst, dry_run=args.dry_run)
    payload = {
        "status": "ok",
        "action": "mirror_to_codex",
        "scope": args.scope,
        "skill_name": args.skill_name,
        "source": str(src),
        "destination": str(dst),
        "mirror_root": str(mirror_root),
        "codex_root": str(codex_root),
        "dry_run": bool(args.dry_run),
        "command": command,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2))
        raise SystemExit(1)
