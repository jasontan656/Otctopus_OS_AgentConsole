#!/usr/bin/env python3
from __future__ import annotations

import argparse
import difflib
import json
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from memory_cli_parser import build_parser
from memory_bind_task import bind_task
from memory_compile import compile_active_memory
from memory_models import MemoryValidationError
from memory_models import iso_now
from memory_session_runtime import recall_memory
from memory_session_runtime import search_memory
from memory_session_runtime import watch_codex_sessions
from memory_models import validate_task_memory
from memory_models import validate_turn_delta_entries
from memory_models import validate_user_memory
from memory_store import active_runtime_path
from memory_store import active_task_path
from memory_store import compiled_active_memory_json_path
from memory_store import compiled_active_memory_md_path
from memory_store import deep_merge
from memory_store import ensure_store_exists
from memory_store import human_log_path
from memory_store import load_task_memory
from memory_store import load_turn_delta
from memory_store import load_user_memory
from memory_store import machine_log_path
from memory_store import resolve_task_id
from memory_store import result_root
from memory_store import runtime_root
from memory_store import save_task_memory
from memory_store import save_turn_delta
from memory_store import save_user_memory
from memory_store import turn_audit_json_path
from memory_store import task_memory_json_path
from memory_store import turn_delta_json_path
from memory_store import user_memory_json_path
from memory_store import watcher_state_json_path
from memory_validate import validate_store


SKILL_ROOT = SCRIPT_DIR.parent
PRODUCT_ROOT = SKILL_ROOT.parents[1]
WORKSPACE_ROOT = PRODUCT_ROOT.parent
RUNTIME_CONTRACTS_ROOT = SKILL_ROOT / "references" / "runtime_contracts"
CONTRACT_PATH = RUNTIME_CONTRACTS_ROOT / "SKILL_RUNTIME_CONTRACT.json"
DIRECTIVE_INDEX_PATH = RUNTIME_CONTRACTS_ROOT / "DIRECTIVE_INDEX.json"
SKILL_NAME = SKILL_ROOT.name

PLACEHOLDERS = {
    "__SKILL_NAME__": SKILL_NAME,
    "__SKILL_ROOT__": str(SKILL_ROOT),
    "__PRODUCT_ROOT__": str(PRODUCT_ROOT),
    "__WORKSPACE_ROOT__": str(WORKSPACE_ROOT),
    "__RUNTIME_ROOT__": str(runtime_root()),
    "__RESULT_ROOT__": str(result_root()),
}


def _replace_placeholders(value: Any) -> Any:
    if isinstance(value, str):
        rendered = value
        for placeholder, resolved in PLACEHOLDERS.items():
            rendered = rendered.replace(placeholder, resolved)
        return rendered
    if isinstance(value, list):
        return [_replace_placeholders(item) for item in value]
    if isinstance(value, dict):
        return {key: _replace_placeholders(item) for key, item in value.items()}
    return value


def _read_json_payload(path: Path) -> dict[str, Any]:
    return _replace_placeholders(json.loads(path.read_text(encoding="utf-8")))


def _read_directive_index() -> dict[str, dict[str, str]]:
    return json.loads(DIRECTIVE_INDEX_PATH.read_text(encoding="utf-8"))["topics"]


def _emit(payload: dict[str, Any], as_json: bool) -> int:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    for key, value in payload.items():
        if isinstance(value, (dict, list)):
            print(f"{key}:")
            print(json.dumps(value, ensure_ascii=False, indent=2))
        else:
            print(f"{key}: {value}")
    return 0


def _load_patch(args: argparse.Namespace) -> dict[str, Any]:
    if args.patch_json and args.payload_file:
        raise SystemExit("use either --patch-json or --payload-file, not both")
    if args.patch_json:
        payload = json.loads(args.patch_json)
    elif args.payload_file:
        payload = json.loads(Path(args.payload_file).read_text(encoding="utf-8"))
    else:
        raise SystemExit("one of --patch-json or --payload-file is required")
    if not isinstance(payload, dict):
        raise SystemExit("patch payload must be a JSON object")
    return payload


def _make_diff(before: str, after: str, path: Path) -> str:
    lines = difflib.unified_diff(
        before.splitlines(),
        after.splitlines(),
        fromfile=f"{path} (before)",
        tofile=f"{path} (after)",
        lineterm="",
    )
    return "\n".join(lines)


def _command_contract(args: argparse.Namespace) -> int:
    return _emit(_read_json_payload(CONTRACT_PATH), args.json)


def _command_directive(args: argparse.Namespace) -> int:
    directive_index = _read_directive_index()
    entry = directive_index.get(args.topic)
    if entry is None:
        available = ", ".join(sorted(directive_index))
        raise SystemExit(f"Unknown directive topic: {args.topic}. Available: {available}")
    return _emit(_read_json_payload(RUNTIME_CONTRACTS_ROOT / entry["json_path"]), args.json)


def _command_paths(args: argparse.Namespace) -> int:
    payload = {
        "skill_name": SKILL_NAME,
        "resolved_paths": {
            "skill_root": str(SKILL_ROOT),
            "product_root": str(PRODUCT_ROOT),
            "workspace_root": str(WORKSPACE_ROOT),
            "runtime_root": str(runtime_root()),
            "result_root": str(result_root()),
            "compiled_active_memory_json": str(compiled_active_memory_json_path()),
            "compiled_active_memory_md": str(compiled_active_memory_md_path()),
            "active_task_json": str(active_task_path()),
            "active_runtime_json": str(active_runtime_path()),
            "user_memory_json": str(user_memory_json_path()),
            "sessions_root": str(result_root() / "sessions"),
            "machine_log": str(machine_log_path()),
            "human_log": str(human_log_path()),
            "watcher_state_json": str(watcher_state_json_path()),
        },
        "environment_variables": {
            "CODEX_SKILL_RUNTIME_ROOT": "Optional base container override for the runtime root.",
            "CODEX_SKILL_RESULT_ROOT": "Optional base container override for the result root.",
            "CODEX_HOME": "Optional Codex session root override for session-stream watcher commands.",
        },
    }
    return _emit(payload, args.json)


def _command_init_store(args: argparse.Namespace) -> int:
    payload = ensure_store_exists()
    return _emit(payload, args.json)


def _command_bind_task(args: argparse.Namespace) -> int:
    ensure_store_exists()
    payload = bind_task(args.task_id, title=args.title, goal=args.goal)
    compile_payload = compile_active_memory()
    result = {
        "status": "bound",
        "task_id": payload["task_id"],
        "title": payload["title"],
        "active_task_path": str(active_task_path()),
        "task_memory_json": str(task_memory_json_path(payload["task_id"])),
        "turn_delta_json": str(turn_delta_json_path(payload["task_id"])),
        "compiled_active_memory_json": str(compiled_active_memory_json_path()),
        "compiled_at": compile_payload["compiled_at"],
    }
    return _emit(result, args.json)


def _command_compile_active_memory(args: argparse.Namespace) -> int:
    ensure_store_exists()
    payload = compile_active_memory()
    result = {
        "status": "compiled",
        "compiled_at": payload["compiled_at"],
        "active_task_id": payload["active_task_id"],
        "compiled_active_memory_json": str(compiled_active_memory_json_path()),
        "compiled_active_memory_md": str(compiled_active_memory_md_path()),
    }
    return _emit(result, args.json)


def _command_upsert_user_memory(args: argparse.Namespace) -> int:
    ensure_store_exists()
    current = load_user_memory()
    patch = _load_patch(args)
    merged = deep_merge(current, patch)
    merged["updated_at"] = iso_now()
    validate_user_memory(merged)
    before_text = json.dumps(current, ensure_ascii=False, indent=2) + "\n"
    after_text = json.dumps(merged, ensure_ascii=False, indent=2) + "\n"
    diff_text = _make_diff(before_text, after_text, user_memory_json_path())
    result = {
        "status": "dry_run" if args.dry_run else "written",
        "payload_path": str(user_memory_json_path()),
        "diff": diff_text,
    }
    if not args.dry_run:
        validated = save_user_memory(merged)
        result["updated_at"] = validated["updated_at"]
        compile_active_memory()
    return _emit(result, args.json)


def _command_upsert_task_memory(args: argparse.Namespace) -> int:
    ensure_store_exists()
    task_id = resolve_task_id(args.task_id)
    current = load_task_memory(task_id)
    patch = _load_patch(args)
    merged = deep_merge(current, patch)
    merged["task_id"] = task_id
    merged["updated_at"] = iso_now()
    validate_task_memory(merged)
    before_text = json.dumps(current, ensure_ascii=False, indent=2) + "\n"
    after_text = json.dumps(merged, ensure_ascii=False, indent=2) + "\n"
    diff_text = _make_diff(before_text, after_text, task_memory_json_path(task_id))
    result = {
        "status": "dry_run" if args.dry_run else "written",
        "task_id": task_id,
        "payload_path": str(task_memory_json_path(task_id)),
        "diff": diff_text,
    }
    if not args.dry_run:
        validated = save_task_memory(merged)
        result["updated_at"] = validated["updated_at"]
        compile_active_memory()
    return _emit(result, args.json)


def _build_turn_delta_entry(args: argparse.Namespace) -> dict[str, Any]:
    if args.entry_json and args.payload_file:
        raise SystemExit("use either --entry-json or --payload-file, not both")
    if args.entry_json:
        payload = json.loads(args.entry_json)
        if not isinstance(payload, dict):
            raise SystemExit("entry payload must be a JSON object")
        return payload
    if args.payload_file:
        payload = json.loads(Path(args.payload_file).read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise SystemExit("entry payload must be a JSON object")
        return payload
    if not args.summary:
        raise SystemExit("--summary is required unless --entry-json or --payload-file is provided")
    return {
        "timestamp": iso_now(),
        "summary": args.summary,
        "user_memory_updates": list(args.user_memory_update or []),
        "task_memory_updates": list(args.task_memory_update or []),
        "next_actions": list(args.next_action or []),
        "writeback_decision": args.writeback_decision,
    }


def _command_append_turn_delta(args: argparse.Namespace) -> int:
    ensure_store_exists()
    task_id = resolve_task_id(args.task_id)
    current_entries = load_turn_delta(task_id)
    entry = _build_turn_delta_entry(args)
    if "timestamp" not in entry:
        entry["timestamp"] = iso_now()
    before_text = json.dumps(current_entries, ensure_ascii=False, indent=2) + "\n"
    after_entries = [*current_entries, entry]
    validate_turn_delta_entries(after_entries)
    after_text = json.dumps(after_entries, ensure_ascii=False, indent=2) + "\n"
    diff_text = _make_diff(before_text, after_text, turn_delta_json_path(task_id))
    result = {
        "status": "dry_run" if args.dry_run else "written",
        "task_id": task_id,
        "payload_path": str(turn_delta_json_path(task_id)),
        "diff": diff_text,
    }
    if not args.dry_run:
        save_turn_delta(task_id, after_entries)
        compile_active_memory()
    return _emit(result, args.json)


def _command_validate_store(args: argparse.Namespace) -> int:
    ensure_store_exists()
    payload = validate_store()
    return _emit(payload, args.json)


def _command_watch_codex_sessions(args: argparse.Namespace) -> int:
    payload = watch_codex_sessions(
        codex_home_override=args.codex_home,
        poll_interval_ms=args.poll_interval_ms,
        idle_exit_seconds=args.idle_exit_seconds,
        once=args.once,
        session_id_filter=args.session_id,
    )
    return _emit(payload, args.json)


def _command_show_turn_audit(args: argparse.Namespace) -> int:
    ensure_store_exists()
    payload = json.loads(turn_audit_json_path(args.session_id, args.turn_id).read_text(encoding="utf-8"))
    return _emit(payload, args.json)


def _command_recall_memory(args: argparse.Namespace) -> int:
    payload = recall_memory(task_id=args.task_id, session_id=args.session_id, limit=args.limit)
    return _emit(payload, args.json)


def _command_search_memory(args: argparse.Namespace) -> int:
    payload = search_memory(args.query, limit=args.limit)
    return _emit(payload, args.json)


def main() -> int:
    parser = build_parser(
        command_contract=_command_contract,
        command_directive=_command_directive,
        command_paths=_command_paths,
        command_init_store=_command_init_store,
        command_bind_task=_command_bind_task,
        command_compile_active_memory=_command_compile_active_memory,
        command_upsert_user_memory=_command_upsert_user_memory,
        command_upsert_task_memory=_command_upsert_task_memory,
        command_append_turn_delta=_command_append_turn_delta,
        command_validate_store=_command_validate_store,
        command_watch_codex_sessions=_command_watch_codex_sessions,
        command_show_turn_audit=_command_show_turn_audit,
        command_recall_memory=_command_recall_memory,
        command_search_memory=_command_search_memory,
    )
    args = parser.parse_args()
    try:
        return args.func(args)
    except MemoryValidationError as exc:
        print(json.dumps({"status": "error", "error": "validation_failed", "message": str(exc)}, ensure_ascii=False))
        return 1
    except ValueError as exc:
        print(json.dumps({"status": "error", "error": "value_error", "message": str(exc)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
