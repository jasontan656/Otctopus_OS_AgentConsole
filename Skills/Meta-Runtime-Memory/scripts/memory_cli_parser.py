#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections.abc import Callable


CommandHandler = Callable[[argparse.Namespace], int]


def build_parser(
    *,
    command_contract: CommandHandler,
    command_directive: CommandHandler,
    command_paths: CommandHandler,
    command_init_store: CommandHandler,
    command_bind_task: CommandHandler,
    command_compile_active_memory: CommandHandler,
    command_upsert_user_memory: CommandHandler,
    command_upsert_task_memory: CommandHandler,
    command_append_turn_delta: CommandHandler,
    command_validate_store: CommandHandler,
    command_watch_codex_sessions: CommandHandler,
    command_show_turn_audit: CommandHandler,
    command_recall_memory: CommandHandler,
    command_search_memory: CommandHandler,
) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Meta-Runtime-Memory CLI toolbox")
    subparsers = parser.add_subparsers(dest="command", required=True)

    contract_parser = subparsers.add_parser("runtime-contract", aliases=["contract"], help="Emit the runtime contract")
    contract_parser.add_argument("--json", action="store_true", help="Emit structured JSON")
    contract_parser.set_defaults(func=command_contract)

    directive_parser = subparsers.add_parser("directive", help="Emit a directive payload")
    directive_parser.add_argument("--topic", required=True, help="Directive topic name")
    directive_parser.add_argument("--json", action="store_true", help="Emit structured JSON")
    directive_parser.set_defaults(func=command_directive)

    paths_parser = subparsers.add_parser("paths", help="Resolve governed runtime and result paths")
    paths_parser.add_argument("--json", action="store_true", help="Emit structured JSON")
    paths_parser.set_defaults(func=command_paths)

    init_parser = subparsers.add_parser("init-store", help="Initialize the governed memory store")
    init_parser.add_argument("--json", action="store_true", help="Emit structured JSON")
    init_parser.set_defaults(func=command_init_store)

    bind_parser = subparsers.add_parser("bind-task", help="Bind the active task context")
    bind_parser.add_argument("--task-id", required=True, help="Task identifier or slug source")
    bind_parser.add_argument("--title", help="Task title")
    bind_parser.add_argument("--goal", help="Stable task goal")
    bind_parser.add_argument("--json", action="store_true", help="Emit structured JSON")
    bind_parser.set_defaults(func=command_bind_task)

    compile_parser = subparsers.add_parser("compile-active-memory", help="Compile runtime active memory")
    compile_parser.add_argument("--json", action="store_true", help="Emit structured JSON")
    compile_parser.set_defaults(func=command_compile_active_memory)

    upsert_user_parser = subparsers.add_parser("upsert-user-memory", help="Upsert durable user-layer memory")
    upsert_user_parser.add_argument("--patch-json", help="JSON object patch")
    upsert_user_parser.add_argument("--payload-file", help="Path to a JSON object patch")
    upsert_user_parser.add_argument("--dry-run", action="store_true", help="Preview the diff without writing")
    upsert_user_parser.add_argument("--json", action="store_true", help="Emit structured JSON")
    upsert_user_parser.set_defaults(func=command_upsert_user_memory)

    upsert_task_parser = subparsers.add_parser("upsert-task-memory", help="Upsert durable task-layer memory")
    upsert_task_parser.add_argument("--task-id", help="Target task id; defaults to ACTIVE_TASK")
    upsert_task_parser.add_argument("--patch-json", help="JSON object patch")
    upsert_task_parser.add_argument("--payload-file", help="Path to a JSON object patch")
    upsert_task_parser.add_argument("--dry-run", action="store_true", help="Preview the diff without writing")
    upsert_task_parser.add_argument("--json", action="store_true", help="Emit structured JSON")
    upsert_task_parser.set_defaults(func=command_upsert_task_memory)

    delta_parser = subparsers.add_parser("append-turn-delta", help="Append a turn delta entry")
    delta_parser.add_argument("--task-id", help="Target task id; defaults to ACTIVE_TASK")
    delta_parser.add_argument("--summary", help="Turn summary")
    delta_parser.add_argument("--user-memory-update", action="append", help="User-layer change summary")
    delta_parser.add_argument("--task-memory-update", action="append", help="Task-layer change summary")
    delta_parser.add_argument("--next-action", action="append", help="Next action summary")
    delta_parser.add_argument(
        "--writeback-decision",
        default="applied",
        choices=["applied", "skipped", "deferred"],
        help="Writeback decision for this turn",
    )
    delta_parser.add_argument("--entry-json", help="Full JSON object entry")
    delta_parser.add_argument("--payload-file", help="Path to a JSON object entry")
    delta_parser.add_argument("--dry-run", action="store_true", help="Preview the diff without writing")
    delta_parser.add_argument("--json", action="store_true", help="Emit structured JSON")
    delta_parser.set_defaults(func=command_append_turn_delta)

    validate_parser = subparsers.add_parser("validate-store", help="Validate the durable store and compiled memory")
    validate_parser.add_argument("--json", action="store_true", help="Emit structured JSON")
    validate_parser.set_defaults(func=command_validate_store)

    watch_parser = subparsers.add_parser("watch-codex-sessions", help="Watch Codex session logs and auto-apply memory hooks")
    watch_parser.add_argument("--codex-home", help="Override Codex home; defaults to workspace/.codex, $CODEX_HOME, or ~/.codex")
    watch_parser.add_argument("--poll-interval-ms", type=int, default=500, help="Polling interval for session log scan")
    watch_parser.add_argument("--idle-exit-seconds", type=float, help="Exit after idle time with no new session events")
    watch_parser.add_argument("--once", action="store_true", help="Scan available session logs once and exit")
    watch_parser.add_argument("--session-id", help="Optional session id filter")
    watch_parser.add_argument("--json", action="store_true", help="Emit structured JSON")
    watch_parser.set_defaults(func=command_watch_codex_sessions)

    turn_audit_parser = subparsers.add_parser("show-turn-audit", help="Read a persisted turn audit payload")
    turn_audit_parser.add_argument("--session-id", required=True, help="Codex session id")
    turn_audit_parser.add_argument("--turn-id", required=True, help="Codex turn id")
    turn_audit_parser.add_argument("--json", action="store_true", help="Emit structured JSON")
    turn_audit_parser.set_defaults(func=command_show_turn_audit)

    recall_parser = subparsers.add_parser("recall-memory", help="Read task or session memory plus recent audit history")
    recall_parser.add_argument("--task-id", help="Task identifier")
    recall_parser.add_argument("--session-id", help="Codex session id")
    recall_parser.add_argument("--limit", type=int, default=5, help="Maximum recent entries to return")
    recall_parser.add_argument("--json", action="store_true", help="Emit structured JSON")
    recall_parser.set_defaults(func=command_recall_memory)

    search_parser = subparsers.add_parser("search-memory", help="Search task memory and turn audits by substring")
    search_parser.add_argument("--query", required=True, help="Case-insensitive search text")
    search_parser.add_argument("--limit", type=int, default=10, help="Maximum hits per result set")
    search_parser.add_argument("--json", action="store_true", help="Emit structured JSON")
    search_parser.set_defaults(func=command_search_memory)
    return parser
