#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, TypedDict, cast

from session_context_support import SessionContextError, print_json, read_session_context, render_session_context_text

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
RUNTIME_CONTRACTS_ROOT = SKILL_ROOT / "references" / "runtime_contracts"
CONTRACT_PATH = RUNTIME_CONTRACTS_ROOT / "SKILL_RUNTIME_CONTRACT.json"
DIRECTIVE_INDEX_PATH = RUNTIME_CONTRACTS_ROOT / "DIRECTIVE_INDEX.json"


class ToolEntry(TypedDict):
    script: str
    commands: dict[str, str]


class DirectiveTopic(TypedDict):
    topic: str
    doc_kind: str
    use_when: str


class ContractPayload(TypedDict):
    contract_name: str
    contract_version: str
    skill_name: str
    runtime_source_policy: dict[str, object]
    tool_entry: ToolEntry
    must_use_sequence: list[str]
    directive_topics: list[DirectiveTopic]
    hard_constraints: list[str]
    runtime_output_policy: dict[str, str]


class DirectivePayload(TypedDict):
    directive_name: str
    directive_version: str
    doc_kind: str
    topic: str
    purpose: str
    instruction: list[str]
    workflow: list[str]
    rules: list[str]


class DirectiveIndexEntry(TypedDict):
    doc_kind: str
    json_path: str
    human_path: str


class DirectiveIndex(TypedDict):
    topics: dict[str, DirectiveIndexEntry]


Payload = dict[str, Any]


def read_json(path: Path) -> Payload:
    return cast(Payload, json.loads(path.read_text(encoding="utf-8")))


def read_directive_index(path: Path) -> DirectiveIndex:
    return cast(DirectiveIndex, json.loads(path.read_text(encoding="utf-8")))


def emit(payload: Payload, as_json: bool) -> int:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    if "directive_name" in payload:
        print(payload["directive_name"])
        print(f"purpose: {payload['purpose']}")
        for section in ("instruction", "workflow", "rules"):
            values = payload.get(section, [])
            if not values:
                continue
            print(f"{section}:")
            for item in values:
                print(f"- {item}")
        return 0
    print(payload["contract_name"])
    print(f"version: {payload['contract_version']}")
    print("tool_entry:")
    for name, command in payload["tool_entry"]["commands"].items():
        print(f"- {name}: {command}")
    print("directive_topics:")
    for item in payload["directive_topics"]:
        print(f"- {item['topic']}: {item['doc_kind']}")
    return 0


def cmd_contract(args: argparse.Namespace) -> int:
    return emit(read_json(CONTRACT_PATH), args.json)


def _resolve_directive_path(topic: str) -> Path:
    index = read_directive_index(DIRECTIVE_INDEX_PATH)
    directive = index.get("topics", {}).get(topic)
    if not directive:
        raise KeyError(topic)
    return RUNTIME_CONTRACTS_ROOT / directive["json_path"]


def cmd_directive(args: argparse.Namespace) -> int:
    try:
        payload = read_json(_resolve_directive_path(args.topic))
    except KeyError:
        print(
            json.dumps(
                {
                    "status": "error",
                    "error": "unknown_directive_topic",
                    "topic": args.topic,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1
    return emit(payload, args.json)


def _resolve_lookup(args: argparse.Namespace) -> tuple[str, str]:
    if args.codex_id:
        return "codex_id", str(args.codex_id)
    if args.session_id:
        return "session_id", str(args.session_id)
    if args.resume_id:
        return "resume_id", str(args.resume_id)
    return str(args.lookup_key or ""), str(args.lookup_value or "")


def cmd_read_session_context(args: argparse.Namespace) -> int:
    lookup_key, lookup_value = _resolve_lookup(args)
    try:
        payload = read_session_context(
            lookup_key=lookup_key,
            lookup_value=lookup_value,
            codex_home_override=args.codex_home,
            match_mode=args.lookup_match_mode,
            case_sensitive=bool(args.case_sensitive),
            message_role=str(args.message_role or "assistant"),
            message_key=str(args.message_key or "") or None,
            message_query=str(args.message_query or "") or None,
            message_match_mode=str(args.message_match_mode or "contains"),
            select_mode=str(args.select_mode or "latest"),
            context_mode=str(args.context_mode or "paired_turn"),
            window_before=int(args.window_before or 0),
            window_after=int(args.window_after or 0),
            include_roles=list(args.include_role or []),
            trim_chars=int(args.trim_chars or 0),
        )
    except SessionContextError as exc:
        if args.json:
            print_json(exc.payload)
        else:
            print(str(exc))
        return exc.code

    if args.json:
        print_json(payload)
    else:
        print(render_session_context_text(payload), end="")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Meta-Enhance-Prompt unified toolbox")
    subparsers = parser.add_subparsers(dest="command", required=True)

    contract = subparsers.add_parser("contract")
    contract.add_argument("--json", action="store_true")
    contract.set_defaults(func=cmd_contract)

    directive = subparsers.add_parser("directive")
    directive.add_argument("--topic", required=True)
    directive.add_argument("--json", action="store_true")
    directive.set_defaults(func=cmd_directive)

    session_context = subparsers.add_parser("read-session-context")
    session_context.add_argument("--lookup-key", default="")
    session_context.add_argument("--lookup-id", "--lookup-value", dest="lookup_value", default="")
    session_context.add_argument("--codex-id", default="")
    session_context.add_argument("--session-id", default="")
    session_context.add_argument("--resume-id", default="")
    session_context.add_argument("--codex-home", default=None)
    session_context.add_argument("--lookup-match-mode", choices=("exact", "contains"), default="exact")
    session_context.add_argument("--message-role", default="assistant")
    session_context.add_argument("--message-key", default="")
    session_context.add_argument("--message-query", default="")
    session_context.add_argument("--message-match-mode", choices=("exact", "contains"), default="contains")
    session_context.add_argument("--select-mode", choices=("latest", "first"), default="latest")
    session_context.add_argument("--context-mode", choices=("paired_turn", "window", "all"), default="paired_turn")
    session_context.add_argument("--window-before", type=int, default=1)
    session_context.add_argument("--window-after", type=int, default=1)
    session_context.add_argument("--include-role", action="append", default=[])
    session_context.add_argument("--trim-chars", type=int, default=4000)
    session_context.add_argument("--case-sensitive", action="store_true")
    session_context.add_argument("--json", action="store_true")
    session_context.set_defaults(func=cmd_read_session_context)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
