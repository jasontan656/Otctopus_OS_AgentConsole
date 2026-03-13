from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import TypedDict

from rootfile_runtime import (
    add_governed_source_path,
    build_entry,
    detect_paths,
    ensure_within_workspace,
    extract_external_agents_part_a,
    extract_internal_part_a,
    find_channel_by_file_kind,
    inject_owner_into_machine_payload,
    lint_external_entry,
    lint_managed_entry,
    load_machine_payload,
    match_scan_rules,
    prune_legacy_managed_target_dirs,
    resolve_target_contract,
    render_internal_agents_human,
    scaffold_external_agents,
    scaffold_internal_agents_human,
    scaffold_plain_external,
    is_markdown_owner_managed,
    strip_markdown_owner,
    upsert_markdown_owner,
    sync_file_to_installed,
    write_json,
    write_stage_report,
    write_text,
)


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


def cmd_scan(args: argparse.Namespace) -> int:
    paths = detect_paths(__file__)
    entries = match_scan_rules(paths, args.only, args.source_path)
    lint_results = []
    for entry in entries:
        lint_results.append(
            {
                "source_path": entry["source_path"],
                "errors": lint_external_entry(paths, entry),
            }
        )
    payload = {
        "stage": "scan",
        "dry_run": args.dry_run,
        "entry_count": len(entries),
        "entries": entries,
        "lint_results": lint_results,
        "summary": f"scan matched {len(entries)} governed file(s)",
        "details": [f"- {item['relative_path']} [{item['channel_id']}]" for item in entries],
    }
    finalize_stage_report(paths, args, "scan", payload)
    return 0


def cmd_lint(args: argparse.Namespace) -> int:
    paths = detect_paths(__file__)
    entries = match_scan_rules(paths, args.only, args.source_path)
    failed = []
    for entry in entries:
        errors = lint_managed_entry(paths, entry)
        if errors:
            failed.append(
                {
                    "source_path": entry["source_path"],
                    "channel_id": entry["channel_id"],
                    "errors": errors,
                }
            )
    payload = {
        "stage": "lint",
        "dry_run": args.dry_run,
        "checked_count": len(entries),
        "failed_count": len(failed),
        "failures": failed,
        "summary": f"lint checked {len(entries)} governed file(s), failures={len(failed)}",
        "details": [
            f"- {item['source_path']} [{item['channel_id']}]: {', '.join(item['errors'])}"
            for item in failed
        ],
    }
    finalize_stage_report(paths, args, "lint", payload)
    return 1 if failed else 0


def cmd_collect(args: argparse.Namespace) -> int:
    paths = detect_paths(__file__)
    removed_legacy_dirs = prune_legacy_managed_target_dirs(paths, args.dry_run)
    entries = match_scan_rules(paths, args.only, args.source_path)
    operations = []
    failures = []
    for entry in entries:
        source_path = Path(entry["source_path"])
        lint_errors = lint_external_entry(paths, entry)
        if lint_errors and not args.allow_invalid_external:
            failures.append(
                {
                    "source_path": str(source_path),
                    "channel_id": entry["channel_id"],
                    "errors": lint_errors,
                }
            )
            continue

        if entry["mapping_mode"] == "agents_ab":
            managed_human = Path(entry["managed_human_path"])
            managed_machine = Path(entry["managed_machine_path"])
            managed_owner_meta = Path(entry["managed_owner_meta_path"])
            machine_payload = load_machine_payload(managed_machine)
            machine_payload = inject_owner_into_machine_payload(machine_payload, str(entry["owner"]))
            external_text = source_path.read_text(encoding="utf-8")
            external_part_a = extract_external_agents_part_a(external_text)
            normalized_part_a = upsert_markdown_owner(external_part_a, str(entry["owner"]))
            new_human = render_internal_agents_human(normalized_part_a, machine_payload.as_dict())
            write_text(managed_human, new_human, args.dry_run)
            write_json(managed_machine, machine_payload.as_dict(), args.dry_run)
            write_json(managed_owner_meta, {"owner": entry["owner"]}, args.dry_run)
            sync_file_to_installed(paths, managed_human, args.dry_run)
            sync_file_to_installed(paths, managed_machine, args.dry_run)
            sync_file_to_installed(paths, managed_owner_meta, args.dry_run)
            operations.append(build_operation(entry, source_path=str(source_path)))
            continue

        managed_path = Path(entry["managed_mapped_path"])
        managed_owner_meta = Path(entry["managed_owner_meta_path"])
        external_text = source_path.read_text(encoding="utf-8")
        if is_markdown_owner_managed(str(entry["file_kind"])):
            external_text = upsert_markdown_owner(external_text, str(entry["owner"]))
        write_text(managed_path, external_text, args.dry_run)
        write_json(managed_owner_meta, {"owner": entry["owner"]}, args.dry_run)
        sync_file_to_installed(paths, managed_path, args.dry_run)
        sync_file_to_installed(paths, managed_owner_meta, args.dry_run)
        operations.append(build_operation(entry, source_path=str(source_path)))

    payload = {
        "stage": "collect",
        "dry_run": args.dry_run,
        "operation_count": len(operations),
        "operations": operations,
        "removed_legacy_dirs": removed_legacy_dirs,
        "failures": failures,
        "summary": f"collect prepared {len(operations)} managed file(s)",
        "details": [f"- {item['source_path']} [{item['channel_id']}]" for item in operations],
    }
    finalize_stage_report(paths, args, "collect", payload)
    return 1 if failures else 0


def cmd_push(args: argparse.Namespace) -> int:
    paths = detect_paths(__file__)
    removed_legacy_dirs = prune_legacy_managed_target_dirs(paths, args.dry_run)
    entries = match_scan_rules(paths, args.only, args.source_path, include_missing=True)
    operations = []
    failures = []
    for entry in entries:
        source_path = Path(entry["source_path"])
        if entry["mapping_mode"] == "agents_ab":
            human_path = Path(entry["managed_human_path"])
            errors = lint_managed_entry(paths, entry, include_external=False)
            if errors and not args.allow_invalid_internal:
                failures.append(
                    {
                        "source_path": str(source_path),
                        "channel_id": entry["channel_id"],
                        "errors": errors,
                    }
                )
                continue
            external_text = extract_internal_part_a(human_path.read_text(encoding="utf-8"))
            write_text(source_path, external_text, args.dry_run)
            operations.append(build_operation(entry, source_path=str(source_path)))
            continue

        managed_path = Path(entry["managed_mapped_path"])
        if not managed_path.exists():
            failures.append(
                {
                    "source_path": str(source_path),
                    "channel_id": entry["channel_id"],
                    "errors": ["missing_managed_mapping"],
                }
            )
            continue
        managed_text = managed_path.read_text(encoding="utf-8")
        if is_markdown_owner_managed(str(entry["file_kind"])):
            managed_text = strip_markdown_owner(managed_text)
        write_text(source_path, managed_text, args.dry_run)
        operations.append(build_operation(entry, source_path=str(source_path)))

    payload = {
        "stage": "push",
        "dry_run": args.dry_run,
        "operation_count": len(operations),
        "operations": operations,
        "removed_legacy_dirs": removed_legacy_dirs,
        "failures": failures,
        "summary": f"push prepared {len(operations)} external file(s)",
        "details": [f"- {item['source_path']} [{item['channel_id']}]" for item in operations],
    }
    finalize_stage_report(paths, args, "push", payload)
    return 1 if failures else 0


def cmd_target_contract(args: argparse.Namespace) -> int:
    paths = detect_paths(__file__)
    source_path = Path(args.source_path).resolve()
    try:
        result = resolve_target_contract(paths, source_path)
    except FileNotFoundError as exc:
        print(json.dumps({"error": str(exc), "source_path": str(source_path)}, ensure_ascii=False))
        return 1
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


def cmd_scaffold(args: argparse.Namespace) -> int:
    paths = detect_paths(__file__)
    removed_legacy_dirs = prune_legacy_managed_target_dirs(paths, args.dry_run)
    target_dirs = [ensure_within_workspace(paths, Path(item)) for item in args.target_dir]
    selected_kinds = sorted(
        set(args.file_kind or ([] if not args.all_governed else [channel["file_kind"] for _, channel in []]))
    )
    if args.all_governed:
        selected_kinds = sorted(
            {
                channel["file_kind"]
                for entry in match_scan_rules(paths, include_missing=True)
                for channel in [{"file_kind": entry["file_kind"]}]
            }
        )
    if not selected_kinds:
        selected_kinds = ["AGENTS.md"]

    operations = []
    failures = []
    for target_dir in target_dirs:
        for file_kind in selected_kinds:
            found = find_channel_by_file_kind(paths, file_kind)
            if found is None:
                failures.append(
                    {"target_dir": str(target_dir), "file_kind": file_kind, "errors": ["unsupported_file_kind"]}
                )
                continue
            channel_id, channel = found
            external_path = (target_dir / file_kind).resolve()
            scaffold_entry = build_entry(paths, external_path, channel_id, channel)
            managed_files = {key: Path(value) for key, value in scaffold_entry["managed_files"].items()}
            owner = str(scaffold_entry["owner"])
            collisions = []
            if not args.allow_existing:
                watch_paths = [external_path, *managed_files.values()]
                for path in watch_paths:
                    if path.exists():
                        collisions.append(str(path))
                if collisions:
                    failures.append(
                        {
                            "target_dir": str(target_dir),
                            "file_kind": file_kind,
                            "channel_id": channel_id,
                            "errors": ["target_already_exists"],
                            "collisions": collisions,
                        }
                    )
                    continue

            if channel["mapping_mode"] == "agents_ab":
                human_path = managed_files["human"]
                machine_path = managed_files["machine"]
                owner_meta_path = managed_files["owner_meta"]
                write_text(external_path, scaffold_external_agents(external_path, owner), args.dry_run)
                write_text(human_path, scaffold_internal_agents_human(external_path, owner), args.dry_run)
                write_json(machine_path, {"owner": owner}, args.dry_run)
                write_json(owner_meta_path, {"owner": owner}, args.dry_run)
                sync_file_to_installed(paths, human_path, args.dry_run)
                sync_file_to_installed(paths, machine_path, args.dry_run)
                sync_file_to_installed(paths, owner_meta_path, args.dry_run)
            else:
                mapped_path = managed_files["mapped"]
                owner_meta_path = managed_files["owner_meta"]
                content = scaffold_plain_external(file_kind)
                write_text(external_path, content, args.dry_run)
                if is_markdown_owner_managed(file_kind):
                    content = upsert_markdown_owner(content, owner)
                write_text(mapped_path, content, args.dry_run)
                write_json(owner_meta_path, {"owner": owner}, args.dry_run)
                sync_file_to_installed(paths, mapped_path, args.dry_run)
                sync_file_to_installed(paths, owner_meta_path, args.dry_run)

            add_governed_source_path(paths, external_path, file_kind, args.dry_run)
            operations.append(
                build_operation(
                    scaffold_entry,
                    target_dir=str(target_dir),
                    file_kind=file_kind,
                    external_path=str(external_path),
                    managed_files={key: str(value) for key, value in managed_files.items()},
                )
            )

    payload = {
        "stage": "scaffold",
        "dry_run": args.dry_run,
        "operation_count": len(operations),
        "operations": operations,
        "removed_legacy_dirs": removed_legacy_dirs,
        "failures": failures,
        "summary": f"scaffold prepared {len(operations)} governed file(s)",
        "details": [f"- {item['external_path']} [{item['channel_id']}]" for item in operations],
    }
    finalize_stage_report(paths, args, "scaffold", payload)
    return 1 if failures else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="Cli_Toolbox.py")
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan = subparsers.add_parser("scan")
    add_common_report_args(scan)
    scan.set_defaults(func=cmd_scan)

    lint = subparsers.add_parser("lint")
    add_common_report_args(lint)
    lint.set_defaults(func=cmd_lint)

    collect = subparsers.add_parser("collect")
    add_common_report_args(collect)
    collect.add_argument("--allow-invalid-external", action="store_true")
    collect.set_defaults(func=cmd_collect)

    push = subparsers.add_parser("push")
    add_common_report_args(push)
    push.add_argument("--allow-invalid-internal", action="store_true")
    push.set_defaults(func=cmd_push)

    scaffold = subparsers.add_parser("scaffold")
    add_common_report_args(scaffold)
    scaffold.add_argument(
        "--target-dir",
        action="append",
        required=True,
        help="External directory to place governed file skeletons into. Repeatable.",
    )
    scaffold.add_argument(
        "--file-kind", action="append", default=[], help="Governed filename to scaffold. Repeatable."
    )
    scaffold.add_argument("--all-governed", action="store_true", help="Scaffold all currently governed file kinds.")
    scaffold.add_argument("--allow-existing", action="store_true", help="Allow overwriting existing scaffold targets.")
    scaffold.set_defaults(func=cmd_scaffold)

    target_contract = subparsers.add_parser("target-contract")
    target_contract.add_argument("--source-path", required=True)
    target_contract.add_argument("--json", action="store_true", help="Compatibility flag; output is JSON.")
    target_contract.set_defaults(func=cmd_target_contract)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
