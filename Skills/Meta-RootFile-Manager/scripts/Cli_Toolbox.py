from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from toolbox_contracts import build_agents_payload_contract, load_skill_runtime_contract
from toolbox_support import add_common_report_args, build_operation, finalize_stage_report
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
    managed_plain_copy_with_owner,
    match_scan_rules,
    prune_legacy_owner_meta_files,
    prune_legacy_managed_target_dirs,
    resolve_target_contract,
    render_internal_agents_human,
    scaffold_agents_machine_payload,
    scaffold_external_agents,
    scaffold_internal_agents_human,
    scaffold_plain_external,
    strip_owner_from_managed_plain_copy,
    upsert_frontmatter_owner,
    sync_file_to_installed,
    validate_agents_writeback_completion,
    write_json,
    write_text,
)


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
    removed_legacy_owner_meta_files = prune_legacy_owner_meta_files(paths, args.dry_run)
    entries = match_scan_rules(paths, args.only, args.source_path)
    operations = []
    failures = []
    changed_operations = 0
    skipped_operations = 0
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
            machine_payload = load_machine_payload(managed_machine)
            machine_payload = inject_owner_into_machine_payload(machine_payload, str(entry["owner"]))
            external_text = source_path.read_text(encoding="utf-8")
            external_part_a = extract_external_agents_part_a(external_text)
            normalized_part_a = upsert_frontmatter_owner(external_part_a, str(entry["owner"]))
            new_human = render_internal_agents_human(normalized_part_a, machine_payload.as_dict())
            managed_human_changed = write_text(managed_human, new_human, args.dry_run)
            managed_machine_changed = write_json(managed_machine, machine_payload.as_dict(), args.dry_run)
            installed_human_changed = sync_file_to_installed(paths, managed_human, args.dry_run)
            installed_machine_changed = sync_file_to_installed(paths, managed_machine, args.dry_run)
            changed = any(
                (
                    managed_human_changed,
                    managed_machine_changed,
                    installed_human_changed,
                    installed_machine_changed,
                )
            )
            if changed:
                changed_operations += 1
            else:
                skipped_operations += 1
            operations.append(
                build_operation(
                    entry,
                    source_path=str(source_path),
                    write_status="updated" if changed else "skipped",
                    managed_change_count=int(managed_human_changed) + int(managed_machine_changed),
                    installed_sync_count=int(installed_human_changed) + int(installed_machine_changed),
                )
            )
            continue

        managed_path = Path(entry["managed_mapped_path"])
        external_text = source_path.read_text(encoding="utf-8")
        managed_changed = write_text(
            managed_path,
            managed_plain_copy_with_owner(external_text, str(entry["owner"])),
            args.dry_run,
        )
        installed_changed = sync_file_to_installed(paths, managed_path, args.dry_run)
        changed = managed_changed or installed_changed
        if changed:
            changed_operations += 1
        else:
            skipped_operations += 1
        operations.append(
            build_operation(
                entry,
                source_path=str(source_path),
                write_status="updated" if changed else "skipped",
                managed_change_count=int(managed_changed),
                installed_sync_count=int(installed_changed),
            )
        )

    payload = {
        "stage": "collect",
        "dry_run": args.dry_run,
        "operation_count": len(operations),
        "changed_operation_count": changed_operations,
        "skipped_operation_count": skipped_operations,
        "operations": operations,
        "removed_legacy_dirs": removed_legacy_dirs,
        "removed_legacy_owner_meta_files": removed_legacy_owner_meta_files,
        "failures": failures,
        "summary": (
            f"collect prepared {len(operations)} managed file(s); "
            f"{changed_operations} updated, {skipped_operations} skipped"
        ),
        "details": [
            f"- {item['source_path']} [{item['channel_id']}] -> {item['write_status']}"
            for item in operations
        ],
    }
    finalize_stage_report(paths, args, "collect", payload)
    return 1 if failures else 0


def cmd_push(args: argparse.Namespace) -> int:
    paths = detect_paths(__file__)
    removed_legacy_dirs = prune_legacy_managed_target_dirs(paths, args.dry_run)
    removed_legacy_owner_meta_files = prune_legacy_owner_meta_files(paths, args.dry_run)
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
        managed_text = strip_owner_from_managed_plain_copy(managed_path.read_text(encoding="utf-8"))
        write_text(source_path, managed_text, args.dry_run)
        operations.append(build_operation(entry, source_path=str(source_path)))

    payload = {
        "stage": "push",
        "dry_run": args.dry_run,
        "operation_count": len(operations),
        "operations": operations,
        "removed_legacy_dirs": removed_legacy_dirs,
        "removed_legacy_owner_meta_files": removed_legacy_owner_meta_files,
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


def cmd_contract(args: argparse.Namespace) -> int:
    payload = load_skill_runtime_contract()
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def cmd_agents_payload_contract(args: argparse.Namespace) -> int:
    paths = detect_paths(__file__)
    source_path = Path(args.source_path).resolve()
    try:
        payload = build_agents_payload_contract(paths, source_path)
    except FileNotFoundError as exc:
        print(json.dumps({"error": str(exc), "source_path": str(source_path)}, ensure_ascii=False))
        return 1
    except ValueError as exc:
        print(
            json.dumps(
                {
                    "status": "error",
                    "error": str(exc),
                    "source_path": str(source_path),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def cmd_scaffold(args: argparse.Namespace) -> int:
    paths = detect_paths(__file__)
    removed_legacy_dirs = prune_legacy_managed_target_dirs(paths, args.dry_run)
    removed_legacy_owner_meta_files = prune_legacy_owner_meta_files(paths, args.dry_run)
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
                machine_payload = scaffold_agents_machine_payload(paths, external_path, owner)
                write_text(external_path, scaffold_external_agents(external_path, owner), args.dry_run)
                write_text(
                    human_path,
                    scaffold_internal_agents_human(paths, external_path, owner, machine_payload),
                    args.dry_run,
                )
                write_json(machine_path, machine_payload, args.dry_run)
                sync_file_to_installed(paths, human_path, args.dry_run)
                sync_file_to_installed(paths, machine_path, args.dry_run)
            else:
                mapped_path = managed_files["mapped"]
                content = scaffold_plain_external(file_kind)
                write_text(external_path, content, args.dry_run)
                write_text(mapped_path, managed_plain_copy_with_owner(content, owner), args.dry_run)
                sync_file_to_installed(paths, mapped_path, args.dry_run)

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
        "removed_legacy_owner_meta_files": removed_legacy_owner_meta_files,
        "failures": failures,
        "summary": f"scaffold prepared {len(operations)} governed file(s)",
        "details": [f"- {item['external_path']} [{item['channel_id']}]" for item in operations],
    }
    finalize_stage_report(paths, args, "scaffold", payload)
    return 1 if failures else 0


def cmd_new_writeback(args: argparse.Namespace) -> int:
    paths = detect_paths(__file__)
    removed_legacy_dirs = prune_legacy_managed_target_dirs(paths, args.dry_run)
    removed_legacy_owner_meta_files = prune_legacy_owner_meta_files(paths, args.dry_run)
    entries = match_scan_rules(paths, source_paths=args.source_path)
    operations = []
    failures = []
    for entry in entries:
        source_path = Path(entry["source_path"])
        if entry["mapping_mode"] != "agents_ab":
            failures.append(
                {
                    "source_path": str(source_path),
                    "channel_id": entry["channel_id"],
                    "errors": ["new_writeback_requires_agents_target"],
                }
            )
            continue
        managed_human = Path(entry["managed_human_path"])
        managed_machine = Path(entry["managed_machine_path"])
        if not source_path.exists():
            failures.append(
                {
                    "source_path": str(source_path),
                    "channel_id": entry["channel_id"],
                    "errors": ["missing_external_source"],
                }
            )
            continue
        try:
            machine_payload = load_machine_payload(managed_machine)
        except json.JSONDecodeError as exc:
            failures.append(
                {
                    "source_path": str(source_path),
                    "channel_id": entry["channel_id"],
                    "errors": [f"invalid_machine_json:{exc.msg}"],
                }
            )
            continue
        external_text = source_path.read_text(encoding="utf-8")
        errors = lint_external_entry(paths, entry)
        errors.extend(validate_agents_writeback_completion(external_text, machine_payload))
        if errors:
            failures.append(
                {
                    "source_path": str(source_path),
                    "channel_id": entry["channel_id"],
                    "errors": errors,
                }
            )
            continue

        machine_payload = inject_owner_into_machine_payload(machine_payload, str(entry["owner"]))
        normalized_part_a = upsert_frontmatter_owner(extract_external_agents_part_a(external_text), str(entry["owner"]))
        new_human = render_internal_agents_human(normalized_part_a, machine_payload.as_dict())
        write_text(managed_human, new_human, args.dry_run)
        write_json(managed_machine, machine_payload.as_dict(), args.dry_run)
        sync_file_to_installed(paths, managed_human, args.dry_run)
        sync_file_to_installed(paths, managed_machine, args.dry_run)

        post_errors = lint_managed_entry(paths, entry)
        if post_errors:
            failures.append(
                {
                    "source_path": str(source_path),
                    "channel_id": entry["channel_id"],
                    "errors": post_errors,
                }
            )
            continue
        operations.append(build_operation(entry, source_path=str(source_path)))

    payload = {
        "stage": "new_writeback",
        "dry_run": args.dry_run,
        "operation_count": len(operations),
        "operations": operations,
        "removed_legacy_dirs": removed_legacy_dirs,
        "removed_legacy_owner_meta_files": removed_legacy_owner_meta_files,
        "failures": failures,
        "summary": f"new_writeback finalized {len(operations)} governed file(s)",
        "details": [f"- {item['source_path']} [{item['channel_id']}]" for item in operations],
    }
    finalize_stage_report(paths, args, "new_writeback", payload)
    return 1 if failures else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="Cli_Toolbox.py")
    subparsers = parser.add_subparsers(dest="command", required=True)

    contract = subparsers.add_parser("contract")
    contract.add_argument("--json", action="store_true", help="Compatibility flag; output is JSON.")
    contract.set_defaults(func=cmd_contract)

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

    new_writeback = subparsers.add_parser("new-writeback")
    new_writeback.add_argument("--dry-run", action="store_true")
    new_writeback.add_argument("--json", action="store_true", help="Print machine-readable JSON to stdout.")
    new_writeback.add_argument(
        "--write-runtime-report",
        action="store_true",
        help="Write latest result JSON into Codex_Skill_Runtime/<skill>/artifacts/<stage>/latest.json and append a timestamped runtime log under logs/<stage>/.",
    )
    new_writeback.add_argument("--report-path", help="Optional custom JSON report path. When set, also writes the report there.")
    new_writeback.add_argument("--source-path", action="append", required=True, help="Exact external AGENTS path to finalize. Repeatable.")
    new_writeback.set_defaults(func=cmd_new_writeback)

    target_contract = subparsers.add_parser("target-contract")
    target_contract.add_argument("--source-path", required=True)
    target_contract.add_argument("--json", action="store_true", help="Compatibility flag; output is JSON.")
    target_contract.set_defaults(func=cmd_target_contract)

    agents_payload_contract = subparsers.add_parser("agents-payload-contract")
    agents_payload_contract.add_argument("--source-path", required=True)
    agents_payload_contract.add_argument("--json", action="store_true", help="Compatibility flag; output is JSON.")
    agents_payload_contract.set_defaults(func=cmd_agents_payload_contract)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
