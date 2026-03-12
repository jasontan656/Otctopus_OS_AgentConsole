#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Annotated, NotRequired, TypedDict

import typer


SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SKILL_RUNTIME_ROOT = Path("/home/jasontan656/AI_Projects/Codex_Skill_Runtime")
DEFAULT_SKILL_RESULT_ROOT = Path("/home/jasontan656/AI_Projects/Codex_Skills_Result")
REPO_RUNTIME_ROOT = SKILL_ROOT / "references" / "runtime"
WORKING_CONTRACT_PATH = REPO_RUNTIME_ROOT / "WORKING_CONTRACT.json"
INTENT_PATH = REPO_RUNTIME_ROOT / "CURRENT_PRODUCT_INTENT.md"
LEGACY_LOG_PATH = Path(
    os.environ.get("SKILL_PRODUCTION_FORM_LEGACY_LOG_PATH", str(REPO_RUNTIME_ROOT / "ITERATION_LOG.md"))
).expanduser().resolve()
SKILL_RUNTIME_ROOT = (
    Path(os.environ.get("CODEX_SKILL_RUNTIME_ROOT", str(DEFAULT_SKILL_RUNTIME_ROOT))).expanduser().resolve()
    / "skill-production-form"
)
SKILL_RESULT_ROOT = (
    Path(os.environ.get("CODEX_SKILLS_RESULT_ROOT", str(DEFAULT_SKILL_RESULT_ROOT))).expanduser().resolve()
    / "skill-production-form"
)
DEFAULT_LOG_PATH = SKILL_RUNTIME_ROOT / "ITERATION_LOG.md"


class WorkingContractCommandPayload(TypedDict):
    status: str
    action: str
    contract_path: str
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
    WorkingContractCommandPayload
    | IntentSnapshotCommandPayload
    | LatestLogCommandPayload
    | AppendIterationLogCommandPayload
)

app = typer.Typer(add_completion=False, pretty_exceptions_enable=False)


def _read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def _resolve_path(raw: str | None, default: Path) -> Path:
    if raw:
        return Path(raw).expanduser().resolve()
    return default


def _seed_runtime_log_if_needed(path: Path) -> bool:
    if path != DEFAULT_LOG_PATH:
        return False
    if path.exists() or not LEGACY_LOG_PATH.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(LEGACY_LOG_PATH.read_text(encoding="utf-8"), encoding="utf-8")
    return True


def _emit(payload: CliPayload, *, as_json: bool) -> None:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    print(payload["summary"])
    for line in payload.get("details", []):
        print(line)


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


@app.command("working-contract")
def working_contract_command(
    json_output: Annotated[bool, typer.Option("--json")] = False,
    contract_path: Annotated[str | None, typer.Option("--contract-path")] = None,
) -> None:
    resolved_contract_path = _resolve_path(contract_path, WORKING_CONTRACT_PATH)
    payload: WorkingContractCommandPayload = {
        "status": "ok",
        "action": "working_contract",
        "contract_path": str(resolved_contract_path),
        "payload": _read_json(resolved_contract_path),
        "summary": f"loaded working contract from {resolved_contract_path}",
        "details": [],
    }
    _emit(payload, as_json=json_output)


@app.command("intent-snapshot")
def intent_snapshot_command(
    json_output: Annotated[bool, typer.Option("--json")] = False,
    intent_path: Annotated[str | None, typer.Option("--intent-path")] = None,
) -> None:
    resolved_intent_path = _resolve_path(intent_path, INTENT_PATH)
    payload: IntentSnapshotCommandPayload = {
        "status": "ok",
        "action": "intent_snapshot",
        "intent_path": str(resolved_intent_path),
        "content": resolved_intent_path.read_text(encoding="utf-8"),
        "summary": f"loaded current console product intent from {resolved_intent_path}",
        "details": [],
    }
    _emit(payload, as_json=json_output)


@app.command("latest-log")
def latest_log_command(
    json_output: Annotated[bool, typer.Option("--json")] = False,
    log_path: Annotated[str | None, typer.Option("--log-path")] = None,
    entry_count: Annotated[int, typer.Option("--entry-count")] = 1,
) -> None:
    resolved_log_path = _resolve_path(log_path, DEFAULT_LOG_PATH)
    migrated = _seed_runtime_log_if_needed(resolved_log_path)
    entries = _split_log_entries(resolved_log_path.read_text(encoding="utf-8"))
    selected = entries[-entry_count:] if entries else []
    payload: LatestLogCommandPayload = {
        "status": "ok",
        "action": "latest_log",
        "log_path": str(resolved_log_path),
        "runtime_root": str(SKILL_RUNTIME_ROOT),
        "result_root": str(SKILL_RESULT_ROOT),
        "entry_count": len(selected),
        "entries": selected,
        "summary": f"loaded {len(selected)} latest log entry(s) from {resolved_log_path}",
        "details": [f"- runtime_root: {SKILL_RUNTIME_ROOT}", f"- result_root: {SKILL_RESULT_ROOT}", *[entry.splitlines()[0] for entry in selected]],
    }
    if migrated:
        payload["migrated_legacy_log"] = True
        payload["details"].append(f"- migrated legacy log seed from: {LEGACY_LOG_PATH}")
    _emit(payload, as_json=json_output)


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


@app.command("append-iteration-log")
def append_iteration_log_command(
    title: Annotated[str, typer.Option("--title")] = ...,
    summary: Annotated[str, typer.Option("--summary")] = ...,
    json_output: Annotated[bool, typer.Option("--json")] = False,
    log_path: Annotated[str | None, typer.Option("--log-path")] = None,
    decisions: Annotated[list[str] | None, typer.Option("--decision")] = None,
    affected_paths: Annotated[list[str] | None, typer.Option("--affected-path")] = None,
    risks: Annotated[list[str] | None, typer.Option("--risk")] = None,
    next_steps: Annotated[list[str] | None, typer.Option("--next-step")] = None,
    author: Annotated[str, typer.Option("--author")] = "codex",
) -> None:
    resolved_log_path = _resolve_path(log_path, DEFAULT_LOG_PATH)
    migrated = _seed_runtime_log_if_needed(resolved_log_path)
    timestamp, lines = _append_markdown_section(
        title=title,
        summary=summary,
        decisions=list(decisions or []),
        affected_paths=list(affected_paths or []),
        risks=list(risks or []),
        next_steps=list(next_steps or []),
        author=author,
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
        "title": title,
        "timestamp": timestamp,
        "summary": f"appended iteration log entry '{title}'",
        "details": [
            f"- runtime_root: {SKILL_RUNTIME_ROOT}",
            f"- result_root: {SKILL_RESULT_ROOT}",
            f"- log_path: {resolved_log_path}",
        ],
    }
    if migrated:
        payload["migrated_legacy_log"] = True
        payload["details"].append(f"- migrated legacy log seed from: {LEGACY_LOG_PATH}")
    _emit(payload, as_json=json_output)


def main() -> int:
    app()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
