#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import NotRequired, TypedDict

from production_form_runtime import compile_reading_chain
from production_form_runtime import runtime_payload
from production_form_runtime import working_contract_payload


SKILL_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = SKILL_ROOT.parents[1]
PRODUCT_ROOT = REPO_ROOT.parent
DEFAULT_SKILL_RUNTIME_ROOT = (PRODUCT_ROOT / "Codex_Skill_Runtime").resolve()
DEFAULT_SKILL_RESULT_ROOT = (PRODUCT_ROOT / "Codex_Skills_Result").resolve()
INTENT_PATH = SKILL_ROOT / "path" / "current_intent" / "20_EXECUTION.md"
DEFAULT_SEED_LOG_PATH = SKILL_ROOT / "path" / "latest_log" / "25_LOG_SEED.md"
LEGACY_LOG_PATH = Path(
    os.environ.get("SKILL_PRODUCTION_FORM_LEGACY_LOG_PATH", str(DEFAULT_SEED_LOG_PATH))
).expanduser().resolve()
SKILL_RUNTIME_ROOT = (
    Path(os.environ.get("CODEX_SKILL_RUNTIME_ROOT", str(DEFAULT_SKILL_RUNTIME_ROOT))).expanduser().resolve()
    / "SkillsManager-Production-Form"
)
SKILL_RESULT_ROOT = (
    Path(os.environ.get("CODEX_SKILLS_RESULT_ROOT", str(DEFAULT_SKILL_RESULT_ROOT))).expanduser().resolve()
    / "SkillsManager-Production-Form"
)
DEFAULT_LOG_PATH = SKILL_RUNTIME_ROOT / "ITERATION_LOG.md"


class RuntimeContractCommandPayload(TypedDict):
    status: str
    skill_name: str
    skill_mode: str
    runtime_entry: str
    root_shape: list[str]
    governed_scope: list[str]
    commands: list[str]
    notes: list[str]


class WorkingContractCommandPayload(TypedDict):
    status: str
    action: str
    payload: object
    summary: str
    details: list[str]


class IntentSnapshotCommandPayload(TypedDict):
    status: str
    action: str
    intent_path: str
    content: str
    summary: str
    details: list[str]


class LatestLogCommandPayload(TypedDict):
    status: str
    action: str
    log_path: str
    runtime_root: str
    result_root: str
    entry_count: int
    entries: list[str]
    summary: str
    details: list[str]
    migrated_legacy_log: NotRequired[bool]


class AppendIterationLogCommandPayload(TypedDict):
    status: str
    action: str
    log_path: str
    runtime_root: str
    result_root: str
    title: str
    timestamp: str
    summary: str
    details: list[str]
    migrated_legacy_log: NotRequired[bool]


CliPayload = (
    RuntimeContractCommandPayload
    | WorkingContractCommandPayload
    | IntentSnapshotCommandPayload
    | LatestLogCommandPayload
    | AppendIterationLogCommandPayload
    | dict[str, object]
)


def _resolve_path(raw: str | None, default: Path) -> Path:
    if raw:
        return Path(raw).expanduser().resolve()
    return default


def _emit(payload: CliPayload, *, as_json: bool) -> int:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    print(payload.get("summary", payload.get("status", "ok")))
    for line in payload.get("details", []):
        print(line)
    return 0


def _seed_runtime_log_if_needed(path: Path) -> bool:
    if path != DEFAULT_LOG_PATH:
        return False
    if path.exists() or not LEGACY_LOG_PATH.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(LEGACY_LOG_PATH.read_text(encoding="utf-8"), encoding="utf-8")
    return True


def _split_log_entries(text: str) -> list[str]:
    sections = text.split("\n## ")
    if not sections:
        return []
    entries: list[str] = []
    for index, section in enumerate(sections):
        if index == 0:
            continue
        entries.append("## " + section.strip())
    return entries


def _append_markdown_section(
    *,
    title: str,
    summary: str,
    decisions: list[str],
    affected_paths: list[str],
    risks: list[str],
    next_steps: list[str],
    author: str,
) -> tuple[str, list[str]]:
    timestamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%SZ")
    lines = [
        "",
        f"## {timestamp} - {title}",
        "",
        f"- author: `{author}`",
        f"- summary: {summary}",
    ]
    if decisions:
        lines.append("- decisions:")
        for item in decisions:
            lines.append(f"  - {item}")
    if affected_paths:
        lines.append("- affected_paths:")
        for item in affected_paths:
            lines.append(f"  - `{item}`")
    if risks:
        lines.append("- risks:")
        for item in risks:
            lines.append(f"  - {item}")
    if next_steps:
        lines.append("- next_steps:")
        for item in next_steps:
            lines.append(f"  - {item}")
    lines.append("")
    return timestamp, lines


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="SkillsManager-Production-Form toolbox")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for name in ("runtime-contract", "contract"):
        sub = subparsers.add_parser(name, help="Read the local runtime payload")
        sub.add_argument("--json", action="store_true")

    sub = subparsers.add_parser("working-contract", help="Read the working contract payload")
    sub.add_argument("--json", action="store_true")

    for name in ("read-path-context", "read-contract-context"):
        sub = subparsers.add_parser(name, help="Compile one local production-form chain into one context")
        sub.add_argument("--entry", required=True)
        sub.add_argument("--selection", default="")
        sub.add_argument("--json", action="store_true")

    sub = subparsers.add_parser("intent-snapshot", help="Read the current intent markdown")
    sub.add_argument("--json", action="store_true")
    sub.add_argument("--intent-path")

    sub = subparsers.add_parser("latest-log", help="Read latest runtime log entries")
    sub.add_argument("--json", action="store_true")
    sub.add_argument("--log-path")
    sub.add_argument("--entry-count", type=int, default=1)

    sub = subparsers.add_parser("append-iteration-log", help="Append one iteration log entry")
    sub.add_argument("--title", required=True)
    sub.add_argument("--summary", required=True)
    sub.add_argument("--json", action="store_true")
    sub.add_argument("--log-path")
    sub.add_argument("--decision", action="append", default=[])
    sub.add_argument("--affected-path", action="append", default=[])
    sub.add_argument("--risk", action="append", default=[])
    sub.add_argument("--next-step", action="append", default=[])
    sub.add_argument("--author", default="codex")

    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    if args.command in {"runtime-contract", "contract"}:
        payload: RuntimeContractCommandPayload = runtime_payload()
        return _emit(payload, as_json=args.json)

    if args.command == "working-contract":
        payload: WorkingContractCommandPayload = {
            "status": "ok",
            "action": "working_contract",
            "payload": working_contract_payload(),
            "summary": "loaded current production-form working contract",
            "details": [
                f"- runtime_root: {SKILL_RUNTIME_ROOT}",
                f"- result_root: {SKILL_RESULT_ROOT}",
            ],
        }
        return _emit(payload, as_json=args.json)

    if args.command in {"read-path-context", "read-contract-context"}:
        selection_keys = [item.strip() for item in args.selection.split(",") if item.strip()]
        payload = compile_reading_chain(SKILL_ROOT, args.entry, selection_keys)
        return _emit(payload, as_json=args.json)

    if args.command == "intent-snapshot":
        resolved_intent_path = _resolve_path(args.intent_path, INTENT_PATH)
        payload: IntentSnapshotCommandPayload = {
            "status": "ok",
            "action": "intent_snapshot",
            "intent_path": str(resolved_intent_path),
            "content": resolved_intent_path.read_text(encoding="utf-8"),
            "summary": f"loaded current console product intent from {resolved_intent_path}",
            "details": [],
        }
        return _emit(payload, as_json=args.json)

    if args.command == "latest-log":
        resolved_log_path = _resolve_path(args.log_path, DEFAULT_LOG_PATH)
        migrated = _seed_runtime_log_if_needed(resolved_log_path)
        entries = _split_log_entries(resolved_log_path.read_text(encoding="utf-8"))
        selected = entries[-args.entry_count :] if entries else []
        payload: LatestLogCommandPayload = {
            "status": "ok",
            "action": "latest_log",
            "log_path": str(resolved_log_path),
            "runtime_root": str(SKILL_RUNTIME_ROOT),
            "result_root": str(SKILL_RESULT_ROOT),
            "entry_count": len(selected),
            "entries": selected,
            "summary": f"loaded {len(selected)} latest log entry(s) from {resolved_log_path}",
            "details": [
                f"- runtime_root: {SKILL_RUNTIME_ROOT}",
                f"- result_root: {SKILL_RESULT_ROOT}",
                *[entry.splitlines()[0] for entry in selected],
            ],
        }
        if migrated:
            payload["migrated_legacy_log"] = True
            payload["details"].append(f"- migrated legacy log seed from: {LEGACY_LOG_PATH}")
        return _emit(payload, as_json=args.json)

    if args.command == "append-iteration-log":
        resolved_log_path = _resolve_path(args.log_path, DEFAULT_LOG_PATH)
        migrated = _seed_runtime_log_if_needed(resolved_log_path)
        timestamp, lines = _append_markdown_section(
            title=args.title,
            summary=args.summary,
            decisions=list(args.decision or []),
            affected_paths=list(args.affected_path or []),
            risks=list(args.risk or []),
            next_steps=list(args.next_step or []),
            author=args.author,
        )
        resolved_log_path.parent.mkdir(parents=True, exist_ok=True)
        with resolved_log_path.open("a", encoding="utf-8") as handle:
            handle.write("\n".join(lines))
        payload: AppendIterationLogCommandPayload = {
            "status": "ok",
            "action": "append_iteration_log",
            "log_path": str(resolved_log_path),
            "runtime_root": str(SKILL_RUNTIME_ROOT),
            "result_root": str(SKILL_RESULT_ROOT),
            "title": args.title,
            "timestamp": timestamp,
            "summary": f"appended iteration log entry '{args.title}'",
            "details": [
                f"- runtime_root: {SKILL_RUNTIME_ROOT}",
                f"- result_root: {SKILL_RESULT_ROOT}",
                f"- log_path: {resolved_log_path}",
            ],
        }
        if migrated:
            payload["migrated_legacy_log"] = True
            payload["details"].append(f"- migrated legacy log seed from: {LEGACY_LOG_PATH}")
        return _emit(payload, as_json=args.json)

    raise ValueError(f"unsupported command: {args.command}")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2))
        raise SystemExit(1)
