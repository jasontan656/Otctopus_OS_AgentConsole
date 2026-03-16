from __future__ import annotations

import argparse
import json
from pathlib import Path

from rootfile_runtime import (
    detect_paths,
    extract_external_agents_part_a,
    extract_internal_part_a,
    inject_owner_into_machine_payload,
    lint_external_entry,
    lint_managed_entry,
    load_machine_payload,
    managed_plain_copy_with_owner,
    match_scan_rules,
    prune_legacy_owner_meta_files,
    prune_legacy_managed_target_dirs,
    render_internal_agents_human,
    strip_owner_from_managed_plain_copy,
    sync_file_to_installed,
    upsert_frontmatter_owner,
    write_json,
    write_text,
)
from toolbox_support import build_operation, finalize_stage_report


def cmd_scan(args: argparse.Namespace) -> int:
    paths = detect_paths(__file__)
    entries = match_scan_rules(paths, args.only, args.source_path)
    lint_results = [
        {
            "source_path": entry["source_path"],
            "errors": lint_external_entry(paths, entry),
        }
        for entry in entries
    ]
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
            machine_payload = inject_owner_into_machine_payload(
                load_machine_payload(managed_machine),
                str(entry["owner"]),
            )
            external_text = source_path.read_text(encoding="utf-8")
            normalized_part_a = upsert_frontmatter_owner(
                extract_external_agents_part_a(external_text),
                str(entry["owner"]),
            )
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
            operations.append(
                build_operation(
                    entry,
                    source_path=str(source_path),
                    write_status="updated" if changed else "skipped",
                    managed_change_count=int(managed_human_changed) + int(managed_machine_changed),
                    installed_sync_count=int(installed_human_changed) + int(installed_machine_changed),
                )
            )
        else:
            managed_path = Path(entry["managed_mapped_path"])
            external_text = source_path.read_text(encoding="utf-8")
            managed_changed = write_text(
                managed_path,
                managed_plain_copy_with_owner(external_text, str(entry["owner"])),
                args.dry_run,
            )
            installed_changed = sync_file_to_installed(paths, managed_path, args.dry_run)
            changed = managed_changed or installed_changed
            operations.append(
                build_operation(
                    entry,
                    source_path=str(source_path),
                    write_status="updated" if changed else "skipped",
                    managed_change_count=int(managed_changed),
                    installed_sync_count=int(installed_changed),
                )
            )

        if operations[-1]["write_status"] == "updated":
            changed_operations += 1
        else:
            skipped_operations += 1

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
    entries = match_scan_rules(
        paths,
        args.only,
        args.source_path,
        include_missing=bool(args.source_path),
    )
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
            write_text(
                source_path,
                extract_internal_part_a(human_path.read_text(encoding="utf-8")),
                args.dry_run,
            )
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
        write_text(source_path, strip_owner_from_managed_plain_copy(managed_path.read_text(encoding="utf-8")), args.dry_run)
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
