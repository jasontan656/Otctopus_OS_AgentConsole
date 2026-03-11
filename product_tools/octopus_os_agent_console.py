#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path


RSYNC_EXCLUDES = (
    ".git/",
    "__pycache__/",
    "*.pyc",
    ".tooling_runtime/",
    ".product_runtime/",
)
SYSTEM_SKILL_NAMESPACE = ".system"
SYSTEM_SKILL_MARKER = ".codex-system-skills.marker"
WORKSPACE_MARKER = ".octopus_os_workspace_install.json"


def _resolve_repo_root(raw: str | None) -> Path:
    if raw:
        return Path(raw).expanduser().resolve()
    return Path(__file__).resolve().parents[1]


def _resolve_codex_root(raw: str | None) -> Path:
    if raw:
        return Path(raw).expanduser().resolve()
    env_root = os.environ.get("CODEX_SKILLS_ROOT")
    if env_root:
        return Path(env_root).expanduser().resolve()
    return (Path.home() / ".codex" / "skills").resolve()


def _resolve_workspace_root(raw: str | None) -> Path:
    if raw:
        return Path(raw).expanduser().resolve()
    return (Path.home() / "Octopus_OS_Agent_Console").resolve()


def _resolve_state_root(raw: str | None) -> Path:
    if raw:
        return Path(raw).expanduser().resolve()
    return (Path.home() / ".octopus-os-agent-console" / "install_sessions").resolve()


def _discover_skill_roots(repo_root: Path) -> list[dict[str, str]]:
    skills: list[dict[str, str]] = []
    for child in sorted(repo_root.iterdir(), key=lambda item: item.name.lower()):
        if not child.is_dir():
            continue
        if child.name == ".git":
            continue
        if child.name == SYSTEM_SKILL_NAMESPACE:
            if (child / SYSTEM_SKILL_MARKER).exists():
                skills.append(
                    {
                        "name": child.name,
                        "source": str(child.resolve()),
                        "destination_name": child.name,
                    }
                )
            continue
        if child.name.startswith("."):
            continue
        if (child / "SKILL.md").is_file():
            skills.append(
                {
                    "name": child.name,
                    "source": str(child.resolve()),
                    "destination_name": child.name,
                }
            )
    if not skills:
        raise FileNotFoundError(f"no syncable skill roots found under repo root: {repo_root}")
    return skills


def _rsync(src: Path, dst: Path) -> list[str]:
    dst.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["rsync", "-a", "--delete"]
    for pattern in RSYNC_EXCLUDES:
        cmd.extend(["--exclude", pattern])
    cmd.extend([f"{src}/", f"{dst}/"])
    completed = subprocess.run(cmd, check=False, capture_output=True, text=True)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or "rsync failed")
    return cmd


def _copy_tree(source: Path, destination: Path) -> None:
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination)


def _build_plan(repo_root: Path, codex_root: Path, workspace_root: Path) -> dict[str, object]:
    skills: list[dict[str, object]] = []
    overwrite_skills: list[str] = []
    for skill in _discover_skill_roots(repo_root):
        destination = codex_root / skill["destination_name"]
        exists = destination.exists()
        if exists:
            overwrite_skills.append(skill["name"])
        skills.append(
            {
                **skill,
                "destination": str(destination),
                "destination_exists": exists,
            }
        )
    return {
        "repo_root": str(repo_root),
        "codex_root": str(codex_root),
        "workspace_root": str(workspace_root),
        "skills": skills,
        "overwrite_skills": overwrite_skills,
        "workspace_exists": workspace_root.exists(),
    }


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _load_manifest(state_root: Path, session_id: str | None) -> tuple[Path, dict[str, object]]:
    if session_id:
        manifest_path = state_root / session_id / "install_manifest.json"
        if not manifest_path.exists():
            raise FileNotFoundError(f"manifest does not exist: {manifest_path}")
        return manifest_path, json.loads(manifest_path.read_text(encoding="utf-8"))

    manifest_paths = sorted(state_root.glob("*/install_manifest.json"))
    if not manifest_paths:
        raise FileNotFoundError(f"no install manifest found under state root: {state_root}")
    manifest_path = manifest_paths[-1]
    return manifest_path, json.loads(manifest_path.read_text(encoding="utf-8"))


def plan_command(args: argparse.Namespace) -> int:
    repo_root = _resolve_repo_root(args.repo_root)
    codex_root = _resolve_codex_root(args.codex_root)
    workspace_root = _resolve_workspace_root(args.workspace_root)
    payload = {
        "status": "ok",
        "action": "plan",
        "product_name": "章鱼 OS - 自然语言驱动的多 Agent 控制台",
        "plan": _build_plan(repo_root, codex_root, workspace_root),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def install_command(args: argparse.Namespace) -> int:
    repo_root = _resolve_repo_root(args.repo_root)
    codex_root = _resolve_codex_root(args.codex_root)
    workspace_root = _resolve_workspace_root(args.workspace_root)
    state_root = _resolve_state_root(args.state_root)
    plan = _build_plan(repo_root, codex_root, workspace_root)

    if plan["overwrite_skills"] and not args.allow_overwrite_skills:
        raise ValueError(
            "overwrite required for existing codex skills; rerun with --allow-overwrite-skills"
        )
    if workspace_root.exists() and any(workspace_root.iterdir()) and not args.allow_replace_workspace:
        raise ValueError(
            "workspace root already exists and is not empty; rerun with --allow-replace-workspace"
        )

    session_id = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    session_root = state_root / session_id
    backup_root = session_root / "backups"
    codex_root.mkdir(parents=True, exist_ok=True)

    installed_entries: list[dict[str, object]] = []
    for skill in plan["skills"]:
        source = Path(str(skill["source"]))
        destination = Path(str(skill["destination"]))
        backup_path = None
        if destination.exists():
            backup_path = backup_root / str(skill["name"])
            _copy_tree(destination, backup_path)
        command = _rsync(source, destination)
        installed_entries.append(
            {
                "name": skill["name"],
                "source": str(source),
                "destination": str(destination),
                "had_existing_destination": bool(skill["destination_exists"]),
                "backup_path": str(backup_path) if backup_path else None,
                "command": command,
            }
        )

    if workspace_root.exists():
        shutil.rmtree(workspace_root)
    _rsync(repo_root, workspace_root)

    workspace_marker = workspace_root / WORKSPACE_MARKER
    _write_json(
        workspace_marker,
        {
            "session_id": session_id,
            "repo_root": str(repo_root),
            "workspace_root": str(workspace_root),
        },
    )

    manifest = {
        "session_id": session_id,
        "product_name": "章鱼 OS - 自然语言驱动的多 Agent 控制台",
        "repo_root": str(repo_root),
        "codex_root": str(codex_root),
        "workspace_root": str(workspace_root),
        "installed_entries": installed_entries,
        "workspace_marker": str(workspace_marker),
    }
    manifest_path = session_root / "install_manifest.json"
    _write_json(manifest_path, manifest)

    payload = {
        "status": "ok",
        "action": "install",
        "manifest_path": str(manifest_path),
        "session_id": session_id,
        "overwrite_skills": plan["overwrite_skills"],
        "workspace_root": str(workspace_root),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def uninstall_command(args: argparse.Namespace) -> int:
    state_root = _resolve_state_root(args.state_root)
    manifest_path, manifest = _load_manifest(state_root, args.session_id)
    workspace_root = Path(str(manifest["workspace_root"]))

    restored_backups: list[str] = []
    removed_entries: list[str] = []

    for entry in reversed(list(manifest["installed_entries"])):
        destination = Path(str(entry["destination"]))
        backup_path_raw = entry.get("backup_path")
        if destination.exists():
            shutil.rmtree(destination)
            removed_entries.append(str(destination))
        if backup_path_raw:
            backup_path = Path(str(backup_path_raw))
            if backup_path.exists():
                _copy_tree(backup_path, destination)
                restored_backups.append(str(destination))

    workspace_removed = False
    marker_path = workspace_root / WORKSPACE_MARKER
    if workspace_root.exists() and marker_path.exists():
        marker = json.loads(marker_path.read_text(encoding="utf-8"))
        if marker.get("session_id") == manifest.get("session_id"):
            shutil.rmtree(workspace_root)
            workspace_removed = True

    payload = {
        "status": "ok",
        "action": "uninstall",
        "manifest_path": str(manifest_path),
        "session_id": manifest["session_id"],
        "removed_entries": removed_entries,
        "restored_backups": restored_backups,
        "workspace_removed": workspace_removed,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Octopus OS product installer and cleanup entrypoint"
    )
    parser.add_argument("action", choices=["plan", "install", "uninstall"])
    parser.add_argument("--repo-root")
    parser.add_argument("--codex-root")
    parser.add_argument("--workspace-root")
    parser.add_argument("--state-root")
    parser.add_argument("--session-id")
    parser.add_argument("--allow-overwrite-skills", action="store_true")
    parser.add_argument("--allow-replace-workspace", action="store_true")
    args = parser.parse_args()

    if args.action == "plan":
        return plan_command(args)
    if args.action == "install":
        return install_command(args)
    return uninstall_command(args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2))
        raise SystemExit(1)
