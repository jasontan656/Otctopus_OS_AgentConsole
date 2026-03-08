#!/usr/bin/env python3
"""Governance audit logger for Meta-skills-tooling-governance.

This module writes auditable governance run records into:
Codex_Skill_Runtime/Meta-skills-tooling-governance/runtime/governance_audit
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
from typing import Any
import uuid

RUNTIME_NAMESPACE = "Meta-skills-tooling-governance"
AUDIT_DIR_NAME = "governance_audit"
RUNS_DIR_NAME = "runs"
TIMELINE_FILE = "GOVERNANCE_AUDIT_LOG.jsonl"
RUN_SCHEMA_VERSION = "mstg_governance_audit_run_v1"
EVENT_SCHEMA_VERSION = "mstg_governance_audit_event_v1"


def now_utc() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def utc_compact() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _slug(text: str) -> str:
    cleaned = []
    for ch in text.strip():
        if ch.isalnum():
            cleaned.append(ch.lower())
        elif ch in {"-", "_", "."}:
            cleaned.append("-")
    out = "".join(cleaned).strip("-")
    return out or "unknown"


def detect_runtime_root() -> Path:
    env_root = os.environ.get("MSTG_RUNTIME_ROOT", "").strip()
    if env_root:
        p = Path(env_root).expanduser().resolve()
        if p.is_dir():
            return p

    cwd = Path.cwd().resolve()
    for p in [cwd, *cwd.parents]:
        candidate = p / "Codex_Skill_Runtime"
        if candidate.is_dir():
            return candidate.resolve()

    home = Path.home().resolve()
    try:
        children = sorted(home.iterdir())
    except Exception:
        children = []
    for child in children:
        candidate = child / "Codex_Skill_Runtime"
        if candidate.is_dir():
            return candidate.resolve()

    return (home / "Codex_Skill_Runtime").resolve()


def audit_paths(runtime_root: Path | None = None) -> dict[str, Path]:
    rr = runtime_root.resolve() if runtime_root else detect_runtime_root()
    runtime_dir = rr / RUNTIME_NAMESPACE / "runtime"
    audit_dir = runtime_dir / AUDIT_DIR_NAME
    runs_dir = audit_dir / RUNS_DIR_NAME
    timeline = audit_dir / TIMELINE_FILE
    runs_dir.mkdir(parents=True, exist_ok=True)
    if not timeline.exists():
        timeline.write_text("", encoding="utf-8")
    return {
        "runtime_root": rr,
        "runtime_dir": runtime_dir,
        "audit_dir": audit_dir,
        "runs_dir": runs_dir,
        "timeline": timeline,
    }


def _run_file(run_id: str, paths: dict[str, Path]) -> Path:
    return paths["runs_dir"] / f"{run_id}.json"


def _load_run(run_id: str, paths: dict[str, Path]) -> dict[str, Any]:
    p = _run_file(run_id, paths)
    if not p.is_file():
        raise FileNotFoundError(f"audit run not found: {p}")
    payload = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError("audit run file must be json object")
    payload.setdefault("process_events", [])
    payload.setdefault("result", {})
    return payload


def _save_run(run_id: str, payload: dict[str, Any], paths: dict[str, Path]) -> Path:
    p = _run_file(run_id, paths)
    p.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return p


def _append_timeline(event: dict[str, Any], paths: dict[str, Path]) -> None:
    line = json.dumps(event, ensure_ascii=False, separators=(",", ":"))
    with paths["timeline"].open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def _next_event_id(run: dict[str, Any], run_id: str) -> str:
    idx = len(run.get("process_events", [])) + 1
    return f"{run_id}:{idx:04d}"


def start_run(
    *,
    source_script: str,
    governance_target_skill: str,
    governance_target_path: str,
    governance_objective: str,
    batch_mode: bool = False,
    metadata: dict[str, Any] | None = None,
    runtime_root: Path | None = None,
) -> dict[str, Any]:
    paths = audit_paths(runtime_root)
    run_id = (
        f"mstg-{_slug(Path(source_script).stem)}-{_slug(governance_target_skill)}-"
        f"{utc_compact()}-{uuid.uuid4().hex[:8]}"
    )
    ts = now_utc()
    run_payload: dict[str, Any] = {
        "schema_version": RUN_SCHEMA_VERSION,
        "run_id": run_id,
        "status": "IN_PROGRESS",
        "started_at_utc": ts,
        "ended_at_utc": "",
        "source_script": source_script,
        "governance_target": {
            "skill": governance_target_skill,
            "path": governance_target_path,
        },
        "governance_objective": governance_objective,
        "batch_mode": bool(batch_mode),
        "metadata": metadata or {},
        "process_events": [],
        "result": {},
    }
    _save_run(run_id, run_payload, paths)

    event = {
        "schema_version": EVENT_SCHEMA_VERSION,
        "event_type": "start",
        "event_id": f"{run_id}:0000",
        "run_id": run_id,
        "timestamp_utc": ts,
        "source_script": source_script,
        "status": "START",
        "step": "run_start",
        "message": governance_objective,
        "details": {
            "target_skill": governance_target_skill,
            "target_path": governance_target_path,
            "batch_mode": bool(batch_mode),
        },
    }
    _append_timeline(event, paths)

    return {
        "status": "PASS",
        "run_id": run_id,
        "run_file": str(_run_file(run_id, paths)),
        "timeline_file": str(paths["timeline"]),
        "runtime_root": str(paths["runtime_root"]),
    }


def append_step(
    *,
    run_id: str,
    step: str,
    status: str,
    message: str = "",
    details: dict[str, Any] | None = None,
    source_script: str = "",
    runtime_root: Path | None = None,
) -> dict[str, Any]:
    paths = audit_paths(runtime_root)
    run = _load_run(run_id, paths)
    ts = now_utc()
    event = {
        "schema_version": EVENT_SCHEMA_VERSION,
        "event_type": "step",
        "event_id": _next_event_id(run, run_id),
        "run_id": run_id,
        "timestamp_utc": ts,
        "source_script": source_script or run.get("source_script", ""),
        "status": status,
        "step": step,
        "message": message,
        "details": details or {},
    }
    run.setdefault("process_events", []).append(event)
    run["last_updated_at_utc"] = ts
    _save_run(run_id, run, paths)
    _append_timeline(event, paths)
    return {"status": "PASS", "run_id": run_id, "event_id": event["event_id"]}


def finish_run(
    *,
    run_id: str,
    status: str,
    summary: str,
    details: dict[str, Any] | None = None,
    source_script: str = "",
    runtime_root: Path | None = None,
) -> dict[str, Any]:
    paths = audit_paths(runtime_root)
    run = _load_run(run_id, paths)
    ts = now_utc()
    terminal = status.upper()
    if terminal not in {"PASS", "FAIL"}:
        raise ValueError("finish status must be PASS or FAIL")

    run["status"] = terminal
    run["ended_at_utc"] = ts
    run["last_updated_at_utc"] = ts
    run["result"] = {
        "status": terminal,
        "summary": summary,
        "details": details or {},
    }
    _save_run(run_id, run, paths)

    event = {
        "schema_version": EVENT_SCHEMA_VERSION,
        "event_type": "finish",
        "event_id": f"{run_id}:finish",
        "run_id": run_id,
        "timestamp_utc": ts,
        "source_script": source_script or run.get("source_script", ""),
        "status": terminal,
        "step": "run_finish",
        "message": summary,
        "details": details or {},
    }
    _append_timeline(event, paths)
    return {"status": "PASS", "run_id": run_id, "terminal_status": terminal}


def get_run_status(run_id: str, runtime_root: Path | None = None) -> dict[str, Any]:
    paths = audit_paths(runtime_root)
    run = _load_run(run_id, paths)
    return {
        "status": "PASS",
        "run_id": run_id,
        "run_status": run.get("status", ""),
        "run_file": str(_run_file(run_id, paths)),
        "timeline_file": str(paths["timeline"]),
        "event_count": len(run.get("process_events", [])),
    }


def _parse_json_arg(text: str) -> dict[str, Any]:
    raw = text.strip()
    if not raw:
        return {}
    obj = json.loads(raw)
    if not isinstance(obj, dict):
        raise ValueError("json argument must be an object")
    return obj


def main() -> int:
    parser = argparse.ArgumentParser(description="Governance audit logger")
    sub = parser.add_subparsers(dest="command", required=True)

    p_start = sub.add_parser("start")
    p_start.add_argument("--source-script", required=True)
    p_start.add_argument("--target-skill", required=True)
    p_start.add_argument("--target-path", default="")
    p_start.add_argument("--objective", required=True)
    p_start.add_argument("--batch-mode", action="store_true")
    p_start.add_argument("--metadata-json", default="{}")

    p_step = sub.add_parser("step")
    p_step.add_argument("--run-id", required=True)
    p_step.add_argument("--step", required=True)
    p_step.add_argument("--status", required=True)
    p_step.add_argument("--message", default="")
    p_step.add_argument("--details-json", default="{}")
    p_step.add_argument("--source-script", default="")

    p_finish = sub.add_parser("finish")
    p_finish.add_argument("--run-id", required=True)
    p_finish.add_argument("--status", required=True, choices=["PASS", "FAIL", "pass", "fail"])
    p_finish.add_argument("--summary", required=True)
    p_finish.add_argument("--details-json", default="{}")
    p_finish.add_argument("--source-script", default="")

    p_status = sub.add_parser("status")
    p_status.add_argument("--run-id", required=True)

    args = parser.parse_args()

    try:
        if args.command == "start":
            result = start_run(
                source_script=args.source_script,
                governance_target_skill=args.target_skill,
                governance_target_path=args.target_path,
                governance_objective=args.objective,
                batch_mode=args.batch_mode,
                metadata=_parse_json_arg(args.metadata_json),
            )
        elif args.command == "step":
            result = append_step(
                run_id=args.run_id,
                step=args.step,
                status=args.status,
                message=args.message,
                details=_parse_json_arg(args.details_json),
                source_script=args.source_script,
            )
        elif args.command == "finish":
            result = finish_run(
                run_id=args.run_id,
                status=args.status,
                summary=args.summary,
                details=_parse_json_arg(args.details_json),
                source_script=args.source_script,
            )
        else:
            result = get_run_status(args.run_id)
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False, indent=2))
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
