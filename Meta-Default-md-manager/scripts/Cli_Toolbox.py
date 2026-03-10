from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from mdm_runtime import (
    add_governed_source_path,
    detect_paths,
    ensure_within_workspace,
    extract_external_agents_part_a,
    extract_internal_part_a,
    lint_discovered_entry,
    load_machine_payload,
    match_scan_rules,
    read_json,
    render_internal_agents_human,
    report_path,
    scaffold_external_agents,
    scaffold_internal_agents_human,
    sync_file_to_installed,
    validate_internal_human_agents,
    validate_machine_json,
    write_stage_report,
    write_json,
    write_text,
)


def add_common_report_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON to stdout.")
    parser.add_argument(
        "--write-runtime-report",
        action="store_true",
        help="Write a JSON report into Codex_Skill_Runtime/<skill>/<stage>/latest.json.",
    )
    parser.add_argument(
        "--only",
        action="append",
        default=[],
        help="Limit operation to source paths containing this substring. Repeatable.",
    )
    parser.add_argument(
        "--source-path",
        action="append",
        default=[],
        help="Limit operation to an exact external source path. Repeatable.",
    )
    parser.add_argument(
        "--report-path",
        help="Optional custom JSON report path. When set, also writes the report there.",
    )


def emit(payload: dict, as_json: bool) -> None:
    if as_json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return
    print(payload["summary"])
    for line in payload.get("details", []):
        print(line)


def cmd_scan(args: argparse.Namespace) -> int:
    paths = detect_paths(__file__)
    entries = match_scan_rules(paths, args.only, args.source_path)
    lint_results = []
    for entry in entries:
        lint_results.append(
            {
                "source_path": entry["source_path"],
                "errors": lint_discovered_entry(paths, entry),
            }
        )
    payload = {
        "stage": "scan",
        "dry_run": args.dry_run,
        "entry_count": len(entries),
        "entries": entries,
        "lint_results": lint_results,
        "summary": f"scan matched {len(entries)} governed file(s)",
        "details": [f"- {item['relative_path']}" for item in entries],
    }
    if args.json or args.write_runtime_report or args.report_path:
        runtime_path = write_stage_report(paths, "scan", payload, args.dry_run, args.report_path)
        payload["runtime_report_path"] = str(runtime_path)
    emit(payload, args.json)
    return 0


def cmd_lint(args: argparse.Namespace) -> int:
    paths = detect_paths(__file__)
    entries = match_scan_rules(paths, args.only, args.source_path)
    failed = []
    for entry in entries:
        errors = lint_discovered_entry(paths, entry)
        if errors:
            failed.append({"source_path": entry["source_path"], "errors": errors})
    payload = {
        "stage": "lint",
        "dry_run": args.dry_run,
        "checked_count": len(entries),
        "failed_count": len(failed),
        "failures": failed,
        "summary": f"lint checked {len(entries)} governed file(s), failures={len(failed)}",
        "details": [
            f"- {item['source_path']}: {', '.join(item['errors'])}" for item in failed
        ],
    }
    if args.json or args.write_runtime_report or args.report_path:
        runtime_path = write_stage_report(paths, "lint", payload, args.dry_run, args.report_path)
        payload["runtime_report_path"] = str(runtime_path)
    emit(payload, args.json)
    return 1 if failed else 0


def cmd_collect(args: argparse.Namespace) -> int:
    paths = detect_paths(__file__)
    entries = match_scan_rules(paths, args.only, args.source_path)
    operations = []
    failures = []
    for entry in entries:
        source_path = Path(entry["source_path"])
        if source_path.name != "AGENTS.md":
            continue
        lint_errors = lint_discovered_entry(paths, entry)
        if lint_errors and not args.allow_invalid_external:
            failures.append({"source_path": str(source_path), "errors": lint_errors})
            continue
        managed_human = Path(entry["managed_human_path"])
        managed_machine = Path(entry["managed_machine_path"])
        machine_payload = load_machine_payload(managed_machine)
        external_text = source_path.read_text(encoding="utf-8")
        external_part_a = extract_external_agents_part_a(external_text)
        new_human = render_internal_agents_human(external_part_a, machine_payload)
        write_text(managed_human, new_human, args.dry_run)
        if not managed_machine.exists() and not args.dry_run:
            managed_machine.parent.mkdir(parents=True, exist_ok=True)
            managed_machine.write_text("{}\n", encoding="utf-8")
        sync_file_to_installed(paths, managed_human, args.dry_run)
        if managed_machine.exists():
            sync_file_to_installed(paths, managed_machine, args.dry_run)
        operations.append(
            {
                "source_path": str(source_path),
                "managed_human_path": str(managed_human),
                "managed_machine_path": str(managed_machine),
                "legacy_part_a_marker_detected": "[PART A]" in external_text,
            }
        )
    payload = {
        "stage": "collect",
        "dry_run": args.dry_run,
        "operation_count": len(operations),
        "operations": operations,
        "failures": failures,
        "summary": f"collect prepared {len(operations)} managed file(s)",
        "details": [f"- {item['source_path']} -> {item['managed_human_path']}" for item in operations],
    }
    if args.json or args.write_runtime_report or args.report_path:
        runtime_path = write_stage_report(paths, "collect", payload, args.dry_run, args.report_path)
        payload["runtime_report_path"] = str(runtime_path)
    emit(payload, args.json)
    return 1 if failures else 0


def iter_managed_humans(paths, only_filters, source_paths):
    root = paths.managed_targets_root
    normalized_source_paths = {str(Path(item).expanduser().resolve()) for item in (source_paths or [])}
    for human_path in root.rglob("AGENTS_human.md"):
        human_path = human_path.resolve()
        if only_filters and not any(token in str(human_path) for token in only_filters):
            continue
        external_rel_parent = human_path.parent.relative_to(paths.managed_targets_root)
        if str(external_rel_parent) == ".":
            external_path = paths.workspace_root / "AGENTS.md"
        else:
            external_path = paths.workspace_root / external_rel_parent / "AGENTS.md"
        if normalized_source_paths and str(external_path.resolve()) not in normalized_source_paths:
            continue
        yield human_path, external_path


def cmd_push(args: argparse.Namespace) -> int:
    paths = detect_paths(__file__)
    operations = []
    failures = []
    for human_path, external_path in iter_managed_humans(paths, args.only, args.source_path):
        errors = validate_internal_human_agents(human_path.read_text(encoding="utf-8"))
        errors.extend(validate_machine_json(human_path.with_name("AGENTS_machine.json")))
        if errors and not args.allow_invalid_internal:
            failures.append({"managed_human_path": str(human_path), "errors": errors})
            continue
        external_text = extract_internal_part_a(human_path.read_text(encoding="utf-8"))
        write_text(external_path, external_text, args.dry_run)
        operations.append(
            {
                "managed_human_path": str(human_path),
                "external_path": str(external_path),
            }
        )
    payload = {
        "stage": "push",
        "dry_run": args.dry_run,
        "operation_count": len(operations),
        "operations": operations,
        "failures": failures,
        "summary": f"push prepared {len(operations)} external file(s)",
        "details": [f"- {item['managed_human_path']} -> {item['external_path']}" for item in operations],
    }
    if args.json or args.write_runtime_report or args.report_path:
        runtime_path = write_stage_report(paths, "push", payload, args.dry_run, args.report_path)
        payload["runtime_report_path"] = str(runtime_path)
    emit(payload, args.json)
    return 1 if failures else 0


def cmd_target_contract(args: argparse.Namespace) -> int:
    paths = detect_paths(__file__)
    source_path = Path(args.source_path).resolve()
    relative = source_path.relative_to(paths.workspace_root)
    managed_dir = paths.managed_targets_root / relative.parent if str(relative.parent) != "." else paths.managed_targets_root
    human_path = managed_dir / "AGENTS_human.md"
    machine_path = managed_dir / "AGENTS_machine.json"
    if not machine_path.exists():
        print(json.dumps({"error": "managed_machine_json_not_found", "source_path": str(source_path)}, ensure_ascii=False))
        return 1
    payload = read_json(machine_path)
    result = {
        "source_path": str(source_path),
        "managed_human_path": str(human_path),
        "managed_machine_path": str(machine_path),
        "payload": payload,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


def cmd_scaffold(args: argparse.Namespace) -> int:
    paths = detect_paths(__file__)
    target_dirs = [ensure_within_workspace(paths, Path(item)) for item in args.target_dir]
    selected_kinds = sorted(set(args.file_kind or ([] if not args.all_governed else ["AGENTS.md"])))
    if not selected_kinds:
        selected_kinds = ["AGENTS.md"]

    operations = []
    failures = []
    for target_dir in target_dirs:
        for file_kind in selected_kinds:
            if file_kind != "AGENTS.md":
                failures.append({"target_dir": str(target_dir), "file_kind": file_kind, "errors": ["unsupported_file_kind"]})
                continue
            external_path = (target_dir / file_kind).resolve()
            managed_dir = paths.managed_targets_root / external_path.relative_to(paths.workspace_root).parent
            human_path = managed_dir / "AGENTS_human.md"
            machine_path = managed_dir / "AGENTS_machine.json"
            if not args.allow_existing:
                collisions = []
                for path in (external_path, human_path, machine_path):
                    if path.exists():
                        collisions.append(str(path))
                if collisions:
                    failures.append(
                        {
                            "target_dir": str(target_dir),
                            "file_kind": file_kind,
                            "errors": ["target_already_exists"],
                            "collisions": collisions,
                        }
                    )
                    continue

            write_text(external_path, scaffold_external_agents(external_path), args.dry_run)
            write_text(human_path, scaffold_internal_agents_human(external_path), args.dry_run)
            write_json(machine_path, {}, args.dry_run)
            add_governed_source_path(paths, external_path, args.dry_run)
            sync_file_to_installed(paths, human_path, args.dry_run)
            sync_file_to_installed(paths, machine_path, args.dry_run)
            operations.append(
                {
                    "target_dir": str(target_dir),
                    "file_kind": file_kind,
                    "external_path": str(external_path),
                    "managed_human_path": str(human_path),
                    "managed_machine_path": str(machine_path),
                }
            )

    payload = {
        "stage": "scaffold",
        "dry_run": args.dry_run,
        "operation_count": len(operations),
        "operations": operations,
        "failures": failures,
        "summary": f"scaffold prepared {len(operations)} governed file(s)",
        "details": [f"- {item['external_path']} -> {item['managed_human_path']}" for item in operations],
    }
    if args.json or args.write_runtime_report or args.report_path:
        runtime_path = write_stage_report(paths, "scaffold", payload, args.dry_run, args.report_path)
        payload["runtime_report_path"] = str(runtime_path)
    emit(payload, args.json)
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
    scaffold.add_argument("--target-dir", action="append", required=True, help="External directory to place governed file skeletons into. Repeatable.")
    scaffold.add_argument("--file-kind", action="append", default=[], help="Governed filename to scaffold. Repeatable.")
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
