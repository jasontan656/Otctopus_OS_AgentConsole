from __future__ import annotations

import argparse
import json
from typing import TypedDict

from rootfile_runtime import write_stage_report


class StageReportPayload(TypedDict, total=False):
    stage: str
    dry_run: bool
    summary: str
    details: list[str]
    runtime_report_path: str


def add_common_report_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON to stdout.")
    parser.add_argument("--write-runtime-report", action="store_true", help="Write a JSON report into Codex_Skill_Runtime/<skill>/<stage>/latest.json.")
    parser.add_argument("--only", action="append", default=[], help="Limit operation to source paths containing this substring. Repeatable.")
    parser.add_argument("--source-path", action="append", default=[], help="Limit operation to an exact external source path. Repeatable.")
    parser.add_argument("--report-path", help="Optional custom JSON report path. When set, also writes the report there.")


def emit(report: dict[str, object], as_json: bool) -> None:
    if as_json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return
    print(report["summary"])
    for line in report.get("details", []):
        print(line)


def finalize_stage_report(
    paths: object,
    args: argparse.Namespace,
    stage: str,
    payload: StageReportPayload,
) -> None:
    if args.json or args.write_runtime_report or args.report_path:
        runtime_path = write_stage_report(paths, stage, payload, args.dry_run, args.report_path)
        payload["runtime_report_path"] = str(runtime_path)
    emit(payload, args.json)


def build_operation(entry: dict[str, object], **extra: object) -> dict[str, object]:
    return {
        **extra,
        "channel_id": entry["channel_id"],
        "owner": entry["owner"],
        "managed_files": entry["managed_files"],
    }
