#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from container_scaffold import (
    build_document_readme,
    build_workspace_readme,
    detect_family,
    ensure_markdown,
    scaffold_common_tree,
    validate_container_name,
)
from mother_doc_navigation import sync_navigation_tree
from stage_contract_support import (
    get_stage_checklist,
    get_stage_command_contract,
    get_stage_doc_contract,
    get_stage_graph_contract,
)
from stage_runtime import emit_stage_payload


DEFAULT_WORKSPACE_ROOT = Path("/home/jasontan656/AI_Projects/Octopus_OS")
DEFAULT_DOCUMENT_ROOT = DEFAULT_WORKSPACE_ROOT / "Mother_Doc"


def materialize_layout(args: argparse.Namespace) -> int:
    workspace_root = Path(args.workspace_root).resolve()
    document_root = Path(args.document_root).resolve()
    containers = list(dict.fromkeys(args.container))
    if not containers:
        raise SystemExit("at least one --container is required")

    warnings: list[str] = []
    created_workspace_dirs: list[str] = []
    created_document_dirs: list[str] = []
    existing_workspace_dirs: list[str] = []
    existing_document_dirs: list[str] = []
    created_document_files: list[str] = []

    for name in containers:
        warnings.extend(validate_container_name(name))
        family = detect_family(name)
        workspace_dir = document_root if name == "Mother_Doc" else workspace_root / name
        document_dir = document_root / name

        if workspace_dir.exists():
            existing_workspace_dirs.append(str(workspace_dir))
        else:
            created_workspace_dirs.append(str(workspace_dir))
            if not args.dry_run:
                workspace_dir.mkdir(parents=True, exist_ok=True)

        if document_dir.exists():
            existing_document_dirs.append(str(document_dir))
        else:
            created_document_dirs.append(str(document_dir))
            if not args.dry_run:
                document_dir.mkdir(parents=True, exist_ok=True)

        ensure_markdown(
            workspace_dir / "README.md",
            title=name,
            body_lines=build_workspace_readme(name, document_dir),
            dry_run=args.dry_run,
        )
        ensure_markdown(
            document_dir / "README.md",
            title=name,
            body_lines=build_document_readme(name, workspace_dir, family),
            dry_run=args.dry_run,
        )
        created_document_files.extend(
            scaffold_common_tree(
                container_name=name,
                document_dir=document_dir,
                family=family,
                dry_run=args.dry_run,
            )
        )

    navigation_sync = sync_navigation_tree(document_root, dry_run=args.dry_run)

    payload = {
        "workspace_root": str(workspace_root),
        "document_root": str(document_root),
        "containers": containers,
        "created_workspace_dirs": created_workspace_dirs,
        "created_document_dirs": created_document_dirs,
        "existing_workspace_dirs": existing_workspace_dirs,
        "existing_document_dirs": existing_document_dirs,
        "created_document_files": created_document_files,
        "navigation_sync": navigation_sync,
        "warnings": warnings,
        "dry_run": bool(args.dry_run),
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for key, value in payload.items():
            print(f"{key}: {value}")
    return 0


def sync_mother_doc_navigation(args: argparse.Namespace) -> int:
    document_root = Path(args.document_root).resolve()
    payload = {
        "document_root": str(document_root),
        **sync_navigation_tree(document_root, dry_run=args.dry_run),
        "dry_run": bool(args.dry_run),
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for key, value in payload.items():
            print(f"{key}: {value}")
    return 0


def emit_contract(payload: dict[str, object], *, as_json: bool) -> int:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for key, value in payload.items():
            print(f"{key}: {value}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="2-Octupos-FullStack toolbox")
    subparsers = parser.add_subparsers(dest="command", required=True)

    materialize = subparsers.add_parser(
        "materialize-container-layout",
        help="create workspace and Mother_Doc directories for already-decided containers",
    )
    materialize.add_argument("--workspace-root", default=str(DEFAULT_WORKSPACE_ROOT), help="Octopus_OS workspace root")
    materialize.add_argument("--document-root", default=str(DEFAULT_DOCUMENT_ROOT), help="Mother_Doc root")
    materialize.add_argument("--container", action="append", default=[], help="container name; repeat for multiple containers")
    materialize.add_argument("--dry-run", action="store_true")
    materialize.add_argument("--json", action="store_true")
    materialize.set_defaults(func=materialize_layout)

    navigation = subparsers.add_parser(
        "sync-mother-doc-navigation",
        help="refresh recursive README.md and agents.md navigation files for Mother_Doc",
    )
    navigation.add_argument("--document-root", default=str(DEFAULT_DOCUMENT_ROOT), help="Mother_Doc root")
    navigation.add_argument("--dry-run", action="store_true")
    navigation.add_argument("--json", action="store_true")
    navigation.set_defaults(func=sync_mother_doc_navigation)

    checklist = subparsers.add_parser(
        "stage-checklist",
        help="print the checklist for a specific stage",
    )
    checklist.add_argument("--stage", choices=("mother_doc", "implementation", "evidence"), required=True)
    checklist.add_argument("--json", action="store_true")
    checklist.set_defaults(func=lambda args: emit_contract(get_stage_checklist(args.stage), as_json=args.json))

    doc_contract = subparsers.add_parser(
        "stage-doc-contract",
        help="print the document-loading contract for a specific stage",
    )
    doc_contract.add_argument("--stage", choices=("mother_doc", "implementation", "evidence"), required=True)
    doc_contract.add_argument("--json", action="store_true")
    doc_contract.set_defaults(func=lambda args: emit_contract(get_stage_doc_contract(args.stage), as_json=args.json))

    command_contract = subparsers.add_parser(
        "stage-command-contract",
        help="print the command contract for a specific stage",
    )
    command_contract.add_argument("--stage", choices=("mother_doc", "implementation", "evidence"), required=True)
    command_contract.add_argument("--json", action="store_true")
    command_contract.set_defaults(func=lambda args: emit_contract(get_stage_command_contract(args.stage), as_json=args.json))

    graph_contract = subparsers.add_parser(
        "stage-graph-contract",
        help="print the graph contract for a specific stage",
    )
    graph_contract.add_argument("--stage", choices=("mother_doc", "implementation", "evidence"), required=True)
    graph_contract.add_argument("--json", action="store_true")
    graph_contract.set_defaults(func=lambda args: emit_contract(get_stage_graph_contract(args.stage), as_json=args.json))

    mother_doc = subparsers.add_parser(
        "mother-doc-stage",
        help="print scope and carry-forward requirements for the mother_doc stage",
    )
    mother_doc.add_argument("--json", action="store_true")
    mother_doc.set_defaults(func=lambda args: emit_stage_payload("mother_doc", as_json=args.json))

    implementation = subparsers.add_parser(
        "implementation-stage",
        help="print scope and carry-forward requirements for the implementation stage",
    )
    implementation.add_argument("--json", action="store_true")
    implementation.set_defaults(func=lambda args: emit_stage_payload("implementation", as_json=args.json))

    evidence = subparsers.add_parser(
        "evidence-stage",
        help="print scope and carry-forward requirements for the evidence stage",
    )
    evidence.add_argument("--json", action="store_true")
    evidence.set_defaults(func=lambda args: emit_stage_payload("evidence", as_json=args.json))
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
