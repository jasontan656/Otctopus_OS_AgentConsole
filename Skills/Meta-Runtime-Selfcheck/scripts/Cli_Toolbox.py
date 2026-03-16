#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from runtime_selfcheck_store import ensure_store_exists
from runtime_selfcheck_store import load_turn_audit
from runtime_selfcheck_store import turn_audit_json_path
from runtime_selfcheck_store import watcher_state_json_path
from runtime_selfcheck_turn_hook import run_turn_hook
from runtime_selfcheck_turn_hook import watch_codex_sessions

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
PRODUCT_ROOT = SKILL_ROOT.parents[1]
WORKSPACE_ROOT = PRODUCT_ROOT.parent
RUNTIME_CONTRACTS_ROOT = SKILL_ROOT / "references" / "runtime_contracts"
CONTRACT_PATH = RUNTIME_CONTRACTS_ROOT / "SKILL_RUNTIME_CONTRACT.json"
DIRECTIVE_INDEX_PATH = RUNTIME_CONTRACTS_ROOT / "DIRECTIVE_INDEX.json"
SKILL_NAME = SKILL_ROOT.name
RUNTIME_ROOT = WORKSPACE_ROOT / "Codex_Skill_Runtime" / SKILL_NAME
RESULT_ROOT = WORKSPACE_ROOT / "Codex_Skills_Result" / SKILL_NAME
DEFAULT_HISTORY_PATH = (WORKSPACE_ROOT / ".codex" / "history.jsonl").resolve()

PLACEHOLDERS = {
    "__SKILL_NAME__": SKILL_NAME,
    "__SKILL_ROOT__": str(SKILL_ROOT),
    "__PRODUCT_ROOT__": str(PRODUCT_ROOT),
    "__WORKSPACE_ROOT__": str(WORKSPACE_ROOT),
    "__RUNTIME_ROOT__": str(RUNTIME_ROOT),
    "__RESULT_ROOT__": str(RESULT_ROOT),
    "__DEFAULT_HISTORY_PATH__": str(DEFAULT_HISTORY_PATH),
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
    payload = json.loads(path.read_text(encoding="utf-8"))
    return _replace_placeholders(payload)


def _read_directive_index() -> dict[str, dict[str, str]]:
    payload = json.loads(DIRECTIVE_INDEX_PATH.read_text(encoding="utf-8"))
    return payload["topics"]


def _emit(payload: dict[str, Any], as_json: bool) -> int:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    if "directive_name" in payload:
        print(payload["directive_name"])
        print(f"purpose: {payload['purpose']}")
        for section in ("instruction", "workflow", "rules"):
            items = payload.get(section, [])
            if not items:
                continue
            print(f"{section}:")
            for item in items:
                print(f"- {item}")
        return 0

    if "resolved_paths" in payload:
        for key, value in payload["resolved_paths"].items():
            print(f"{key}: {value}")
        return 0

    print(payload["contract_name"])
    print(f"version: {payload['contract_version']}")
    print("tool_entry:")
    for name, command in payload["tool_entry"]["commands"].items():
        print(f"- {name}: {command}")
    return 0


def _command_contract(args: argparse.Namespace) -> int:
    return _emit(_read_json_payload(CONTRACT_PATH), args.json)


def _command_directive(args: argparse.Namespace) -> int:
    directive_index = _read_directive_index()
    entry = directive_index.get(args.topic)
    if entry is None:
        available = ", ".join(sorted(directive_index))
        raise SystemExit(f"Unknown directive topic: {args.topic}. Available: {available}")
    payload = _read_json_payload(RUNTIME_CONTRACTS_ROOT / entry["json_path"])
    return _emit(payload, args.json)


def _command_paths(args: argparse.Namespace) -> int:
    ensure_store_exists()
    payload = {
        "skill_name": SKILL_NAME,
        "resolved_paths": {
            "skill_root": str(SKILL_ROOT),
            "product_root": str(PRODUCT_ROOT),
            "workspace_root": str(WORKSPACE_ROOT),
            "runtime_root": str(RUNTIME_ROOT),
            "result_root": str(RESULT_ROOT),
            "default_history_path": str(DEFAULT_HISTORY_PATH),
            "watcher_state_json": str(watcher_state_json_path()),
            "session_turn_audits_root": str((RUNTIME_ROOT / "sessions").resolve()),
        },
        "environment_variables": {
            "CODEX_RUNTIME_PAIN_PROVIDER": "Optional. If absent, runtime selfcheck falls back to Codex session evidence.",
            "CODEX_HOME": "Optional override for history.jsonl discovery and session-stream watcher commands.",
            "CODEX_SKILL_RUNTIME_ROOT": "Optional override for runtime log base root.",
        },
    }
    return _emit(payload, args.json)


def _command_run_turn_hook(args: argparse.Namespace) -> int:
    payload = run_turn_hook(
        codex_home_override=args.codex_home,
        session_id=args.session_id,
        turn_id=args.turn_id,
        mode=args.mode,
        auto_repair=bool(args.auto_repair),
        auto_repair_limit=args.auto_repair_limit,
    )
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
    payload = load_turn_audit(args.session_id, args.turn_id)
    payload["turn_audit_path"] = str(turn_audit_json_path(args.session_id, args.turn_id))
    return _emit(payload, args.json)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Meta-Runtime-Selfcheck CLI toolbox")
    subparsers = parser.add_subparsers(dest="command", required=True)

    contract_parser = subparsers.add_parser(
        "runtime-contract",
        aliases=["contract"],
        help="Emit the runtime contract payload",
    )
    contract_parser.add_argument("--json", action="store_true", help="Emit structured JSON")
    contract_parser.set_defaults(func=_command_contract)

    directive_parser = subparsers.add_parser("directive", help="Emit a directive payload")
    directive_parser.add_argument("--topic", required=True, help="Directive topic name")
    directive_parser.add_argument("--json", action="store_true", help="Emit structured JSON")
    directive_parser.set_defaults(func=_command_directive)

    paths_parser = subparsers.add_parser("paths", help="Resolve governed runtime and result paths")
    paths_parser.add_argument("--json", action="store_true", help="Emit structured JSON")
    paths_parser.set_defaults(func=_command_paths)

    hook_parser = subparsers.add_parser(
        "run-turn-hook",
        help="Run the governed turn hook against the latest or targeted Codex turn and persist a turn audit",
    )
    hook_parser.add_argument("--codex-home", help="Override Codex home; defaults to workspace/.codex, $CODEX_HOME, or ~/.codex")
    hook_parser.add_argument("--session-id", help="Optional session id filter")
    hook_parser.add_argument("--turn-id", help="Optional turn id filter")
    hook_parser.add_argument("--mode", choices=["diagnose", "repair"], default="diagnose")
    hook_parser.add_argument("--auto-repair", action=argparse.BooleanOptionalAction, default=False)
    hook_parser.add_argument("--auto-repair-limit", type=int, default=3)
    hook_parser.add_argument("--json", action="store_true", help="Emit structured JSON")
    hook_parser.set_defaults(func=_command_run_turn_hook)

    watch_parser = subparsers.add_parser("watch-codex-sessions", help="Watch Codex session logs and auto-emit selfcheck turn audits")
    watch_parser.add_argument("--codex-home", help="Override Codex home; defaults to workspace/.codex, $CODEX_HOME, or ~/.codex")
    watch_parser.add_argument("--poll-interval-ms", type=int, default=500, help="Polling interval for session log scan")
    watch_parser.add_argument("--idle-exit-seconds", type=float, help="Exit after idle time with no new session events")
    watch_parser.add_argument("--once", action="store_true", help="Scan available session logs once and exit")
    watch_parser.add_argument("--session-id", help="Optional session id filter")
    watch_parser.add_argument("--json", action="store_true", help="Emit structured JSON")
    watch_parser.set_defaults(func=_command_watch_codex_sessions)

    turn_audit_parser = subparsers.add_parser("show-turn-audit", help="Read a persisted turn audit payload")
    turn_audit_parser.add_argument("--session-id", required=True, help="Codex session id")
    turn_audit_parser.add_argument("--turn-id", required=True, help="Codex turn id")
    turn_audit_parser.add_argument("--json", action="store_true", help="Emit structured JSON")
    turn_audit_parser.set_defaults(func=_command_show_turn_audit)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
