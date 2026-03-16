from __future__ import annotations

import argparse
import json
from pathlib import Path

from agents_maintain_runtime import maintain_agents
from rootfile_runtime import (
    add_governed_source_path,
    build_entry,
    detect_paths,
    ensure_within_workspace,
    extract_external_agents_part_a,
    find_channel_by_file_kind,
    graft_frontmatter_from_template,
    lint_external_entry,
    lint_managed_entry,
    load_machine_payload,
    managed_plain_copy_with_owner,
    match_scan_rules,
    prune_legacy_agents_machine_files,
    prune_legacy_owner_meta_files,
    prune_legacy_managed_target_dirs,
    prune_runtime_ephemeral_managed_targets,
    render_internal_agents_human,
    scaffold_agents_machine_payload,
    scaffold_external_agents,
    scaffold_internal_agents_human,
    scaffold_plain_external,
    sync_managed_targets_tree_to_installed,
    sync_file_to_installed,
    upsert_frontmatter_owner,
    validate_agents_writeback_completion,
    write_text,
)
from toolbox_support import build_operation, finalize_stage_report


def cmd_agents_maintain(args: argparse.Namespace) -> int:
    paths = detect_paths(__file__)
    payload = maintain_agents(paths, args.intent, dry_run=args.dry_run)
    finalize_stage_report(paths, args, "agents_maintain", payload)
    return 1 if payload.get("write_status") == "blocked" else 0


def cmd_scaffold(args: argparse.Namespace) -> int:
    paths = detect_paths(__file__)
    removed_legacy_dirs = prune_legacy_managed_target_dirs(paths, args.dry_run)
    removed_legacy_owner_meta_files = prune_legacy_owner_meta_files(paths, args.dry_run)
    removed_legacy_agents_machine_files = prune_legacy_agents_machine_files(paths, args.dry_run)
    removed_runtime_ephemeral_managed_targets = prune_runtime_ephemeral_managed_targets(paths, args.dry_run)
    target_dirs = [ensure_within_workspace(paths, Path(item)) for item in args.target_dir]
    selected_kinds = sorted(set(args.file_kind))
    if args.all_governed:
        selected_kinds = sorted(
            {
                entry["file_kind"]
                for entry in match_scan_rules(paths, include_missing=True)
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
                    {
                        "target_dir": str(target_dir),
                        "file_kind": file_kind,
                        "errors": ["unsupported_file_kind"],
                    }
                )
                continue
            channel_id, channel = found
            external_path = (target_dir / file_kind).resolve()
            scaffold_entry = build_entry(paths, external_path, channel_id, channel)
            managed_files = {key: Path(value) for key, value in scaffold_entry["managed_files"].items()}
            owner = str(scaffold_entry["owner"])
            collisions = []
            if not args.allow_existing:
                for path in [external_path, *managed_files.values()]:
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
                machine_payload = scaffold_agents_machine_payload(paths, external_path, owner)
                write_text(external_path, scaffold_external_agents(external_path, owner), args.dry_run)
                write_text(
                    human_path,
                    scaffold_internal_agents_human(paths, external_path, owner, machine_payload),
                    args.dry_run,
                )
                sync_file_to_installed(paths, human_path, args.dry_run)
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
        "removed_legacy_agents_machine_files": removed_legacy_agents_machine_files,
        "removed_runtime_ephemeral_managed_targets": removed_runtime_ephemeral_managed_targets,
        "failures": failures,
        "summary": f"scaffold prepared {len(operations)} governed file(s)",
        "details": [f"- {item['external_path']} [{item['channel_id']}]" for item in operations],
    }
    payload["installed_managed_targets_sync"] = sync_managed_targets_tree_to_installed(paths, args.dry_run)
    finalize_stage_report(paths, args, "scaffold", payload)
    return 1 if failures else 0


def cmd_new_writeback(args: argparse.Namespace) -> int:
    paths = detect_paths(__file__)
    removed_legacy_dirs = prune_legacy_managed_target_dirs(paths, args.dry_run)
    removed_legacy_owner_meta_files = prune_legacy_owner_meta_files(paths, args.dry_run)
    removed_legacy_agents_machine_files = prune_legacy_agents_machine_files(paths, args.dry_run)
    removed_runtime_ephemeral_managed_targets = prune_runtime_ephemeral_managed_targets(paths, args.dry_run)
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
            machine_payload = load_machine_payload(managed_human)
        except (json.JSONDecodeError, ValueError) as exc:
            failures.append(
                {
                    "source_path": str(source_path),
                    "channel_id": entry["channel_id"],
                    "errors": [f"invalid_internal_payload:{exc}"],
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

        normalized_part_a = upsert_frontmatter_owner(
            graft_frontmatter_from_template(
                extract_external_agents_part_a(external_text),
                managed_human.read_text(encoding="utf-8"),
            ),
            str(entry["owner"]),
        )
        write_text(
            managed_human,
            render_internal_agents_human(normalized_part_a, machine_payload),
            args.dry_run,
        )
        sync_file_to_installed(paths, managed_human, args.dry_run)

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
        "removed_legacy_agents_machine_files": removed_legacy_agents_machine_files,
        "removed_runtime_ephemeral_managed_targets": removed_runtime_ephemeral_managed_targets,
        "failures": failures,
        "summary": f"new_writeback finalized {len(operations)} governed file(s)",
        "details": [f"- {item['source_path']} [{item['channel_id']}]" for item in operations],
    }
    payload["installed_managed_targets_sync"] = sync_managed_targets_tree_to_installed(paths, args.dry_run)
    finalize_stage_report(paths, args, "new_writeback", payload)
    return 1 if failures else 0
