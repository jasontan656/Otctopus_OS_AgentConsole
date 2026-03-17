#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from mirror_to_codex_runtime import compile_reading_chain
from mirror_to_codex_runtime import runtime_payload
from sync_payloads import build_install_route
from sync_payloads import build_push_result
from sync_runtime_support import _build_paths
from sync_runtime_support import _destination_exists
from sync_runtime_support import _rename_push
from sync_runtime_support import _resolve_codex_root
from sync_runtime_support import _resolve_mirror_root
from sync_runtime_support import _resolve_skill_container
from sync_runtime_support import _rsync
from sync_runtime_support import _rsync_syncable_roots

SKILL_ROOT = Path(__file__).resolve().parents[1]


def _print_payload(payload: dict[str, object], as_json: bool) -> int:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    print(payload.get("status", "ok"))
    return 0


def _build_runtime_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="SkillsManager-Mirror-To-Codex runtime toolbox")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for name in ("runtime-contract", "contract"):
        sub = subparsers.add_parser(name, help="Read the local runtime payload")
        sub.add_argument("--json", action="store_true")

    for name in ("read-path-context", "read-contract-context"):
        sub = subparsers.add_parser(name, help="Compile one local mirror-to-codex chain into one context")
        sub.add_argument("--entry", required=True, help="Top-level entry key declared under SKILL.md section 2")
        sub.add_argument("--selection", default="", help="Comma-separated branch keys used when the chain hits a branch node")
        sub.add_argument("--json", action="store_true")

    return parser


def _handle_runtime_command(argv: list[str]) -> int:
    parser = _build_runtime_parser()
    args = parser.parse_args(argv)
    if args.command in {"runtime-contract", "contract"}:
        return _print_payload(runtime_payload(), args.json)
    if args.command in {"read-path-context", "read-contract-context"}:
        selection = [item.strip() for item in args.selection.split(",") if item.strip()]
        return _print_payload(compile_reading_chain(SKILL_ROOT, args.entry, selection), args.json)
    raise ValueError(f"unsupported command: {args.command}")


def _build_sync_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="SkillsManager-Mirror-To-Codex toolbox (one-way: mirror -> codex)"
    )
    parser.add_argument("--scope", choices=["all", "skill"], default="all")
    parser.add_argument("--skill-name")
    parser.add_argument("--mode", choices=["auto", "push", "install", "rename"], default="auto")
    parser.add_argument("--rename-from")
    parser.add_argument("--codex-root")
    parser.add_argument("--mirror-root")
    parser.add_argument("--dry-run", action="store_true")
    return parser


def _handle_sync_command(argv: list[str]) -> int:
    parser = _build_sync_parser()
    args = parser.parse_args(argv)

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
    if args.mode == "rename":
        if args.scope != "skill":
            raise ValueError("--mode=rename only supports --scope=skill")
        if not args.rename_from:
            raise ValueError("--rename-from is required when --mode=rename")
        payload = _rename_push(
            src=src,
            codex_root=codex_root,
            normalized_skill_name=normalized_skill_name or "",
            source_skill_name=source_skill_name or "",
            destination_skill_name=destination_skill_name or "",
            requested_skill_name=args.skill_name,
            rename_from=args.rename_from,
            dry_run=args.dry_run,
            mirror_root=mirror_root,
        )
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    destination_exists = _destination_exists(dst=dst, scope=args.scope)
    if args.mode == "push":
        resolved_mode = "push"
    elif args.mode == "install":
        resolved_mode = "install"
    else:
        resolved_mode = "push" if destination_exists else "install"

    if resolved_mode == "install":
        payload = build_install_route(
            scope=args.scope,
            skill_name=normalized_skill_name,
            requested_skill_name=args.skill_name,
            source_skill_name=source_skill_name,
            destination_skill_name=destination_skill_name,
            src=src,
            dst=dst,
            mirror_root=mirror_root,
            skills_root=_resolve_skill_container(mirror_root),
            codex_root=codex_root,
            dry_run=bool(args.dry_run),
            destination_exists=destination_exists,
        )
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    payload = build_push_result(
        scope=args.scope,
        skill_name=normalized_skill_name,
        requested_skill_name=args.skill_name,
        source_skill_name=source_skill_name,
        destination_skill_name=destination_skill_name,
        src=src,
        dst=dst,
        mirror_root=mirror_root,
        skills_root=_resolve_skill_container(mirror_root),
        codex_root=codex_root,
        dry_run=bool(args.dry_run),
        destination_exists=destination_exists,
    )

    if args.scope == "all":
        synced_entries, commands, removed_forbidden_entries = _rsync_syncable_roots(
            mirror_root=mirror_root,
            codex_root=codex_root,
            dry_run=args.dry_run,
        )
        payload["synced_entries"] = synced_entries
        payload["commands"] = commands
        payload["removed_forbidden_entries"] = removed_forbidden_entries
    else:
        command = _rsync(src=src, dst=dst, dry_run=args.dry_run)
        payload["command"] = command
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    runtime_commands = {"runtime-contract", "contract", "read-path-context", "read-contract-context"}
    if args and args[0] in runtime_commands:
        return _handle_runtime_command(args)
    return _handle_sync_command(args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2))
        raise SystemExit(1)
