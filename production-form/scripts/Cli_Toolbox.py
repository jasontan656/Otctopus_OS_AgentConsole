#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_ROOT = SKILL_ROOT / "references" / "runtime"
WORKING_CONTRACT_PATH = RUNTIME_ROOT / "WORKING_CONTRACT.json"
INTENT_PATH = RUNTIME_ROOT / "CURRENT_PRODUCT_INTENT.md"
LOG_PATH = RUNTIME_ROOT / "ITERATION_LOG.md"


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="production-form toolbox")
    subparsers = parser.add_subparsers(dest="command", required=True)

    working = subparsers.add_parser("working-contract")
    working.add_argument("--json", action="store_true")
    working.add_argument("--contract-path")

    intent = subparsers.add_parser("intent-snapshot")
    intent.add_argument("--json", action="store_true")
    intent.add_argument("--intent-path")

    latest = subparsers.add_parser("latest-log")
    latest.add_argument("--json", action="store_true")
    latest.add_argument("--log-path")
    latest.add_argument("--entry-count", type=int, default=1)

    append = subparsers.add_parser("append-iteration-log")
    append.add_argument("--json", action="store_true")
    append.add_argument("--log-path")
    append.add_argument("--title", required=True)
    append.add_argument("--summary", required=True)
    append.add_argument("--decision", action="append", default=[])
    append.add_argument("--affected-path", action="append", default=[])
    append.add_argument("--risk", action="append", default=[])
    append.add_argument("--next-step", action="append", default=[])
    append.add_argument("--author", default="codex")

    return parser


def _resolve_path(raw: str | None, default: Path) -> Path:
    if raw:
        return Path(raw).expanduser().resolve()
    return default


def _emit(payload: dict, as_json: bool) -> int:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(payload["summary"])
        for line in payload.get("details", []):
            print(line)
    return 0


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


def cmd_working_contract(args: argparse.Namespace) -> int:
    contract_path = _resolve_path(args.contract_path, WORKING_CONTRACT_PATH)
    payload = _read_json(contract_path)
    result = {
        "status": "ok",
        "action": "working_contract",
        "contract_path": str(contract_path),
        "payload": payload,
        "summary": f"loaded working contract from {contract_path}",
        "details": [],
    }
    return _emit(result, args.json)


def cmd_intent_snapshot(args: argparse.Namespace) -> int:
    intent_path = _resolve_path(args.intent_path, INTENT_PATH)
    content = intent_path.read_text(encoding="utf-8")
    result = {
        "status": "ok",
        "action": "intent_snapshot",
        "intent_path": str(intent_path),
        "content": content,
        "summary": f"loaded current product intent from {intent_path}",
        "details": [],
    }
    return _emit(result, args.json)


def cmd_latest_log(args: argparse.Namespace) -> int:
    log_path = _resolve_path(args.log_path, LOG_PATH)
    text = log_path.read_text(encoding="utf-8")
    entries = _split_log_entries(text)
    selected = entries[-args.entry_count :] if entries else []
    result = {
        "status": "ok",
        "action": "latest_log",
        "log_path": str(log_path),
        "entry_count": len(selected),
        "entries": selected,
        "summary": f"loaded {len(selected)} latest log entry(s) from {log_path}",
        "details": [entry.splitlines()[0] for entry in selected],
    }
    return _emit(result, args.json)


def cmd_append_iteration_log(args: argparse.Namespace) -> int:
    log_path = _resolve_path(args.log_path, LOG_PATH)
    timestamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%SZ")

    lines = [
        "",
        f"## {timestamp} - {args.title}",
        "",
        f"- author: `{args.author}`",
        f"- summary: {args.summary}",
    ]

    if args.decision:
        lines.append("- decisions:")
        for item in args.decision:
            lines.append(f"  - {item}")
    if args.affected_path:
        lines.append("- affected_paths:")
        for item in args.affected_path:
            lines.append(f"  - `{item}`")
    if args.risk:
        lines.append("- risks:")
        for item in args.risk:
            lines.append(f"  - {item}")
    if args.next_step:
        lines.append("- next_steps:")
        for item in args.next_step:
            lines.append(f"  - {item}")
    lines.append("")

    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write("\n".join(lines))

    result = {
        "status": "ok",
        "action": "append_iteration_log",
        "log_path": str(log_path),
        "title": args.title,
        "timestamp": timestamp,
        "summary": f"appended iteration log entry '{args.title}'",
        "details": [f"- log_path: {log_path}"],
    }
    return _emit(result, args.json)


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "working-contract":
        return cmd_working_contract(args)
    if args.command == "intent-snapshot":
        return cmd_intent_snapshot(args)
    if args.command == "latest-log":
        return cmd_latest_log(args)
    if args.command == "append-iteration-log":
        return cmd_append_iteration_log(args)
    raise ValueError(f"unsupported command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
