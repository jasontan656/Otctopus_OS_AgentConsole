from __future__ import annotations

import argparse
import json
from pathlib import Path

from container_scaffold import (
    build_document_readme,
    build_graph_readme,
    build_workspace_readme,
    detect_family,
    ensure_markdown,
    scaffold_content_tree,
    scaffold_common_tree,
    validate_container_name,
)
from development_log import append_log_entry
from mother_doc_navigation import sync_navigation_tree
from mother_doc_status import sync_status_tree, sync_status_tree_from_git


def _resolve_product_root() -> Path:
    script_path = Path(__file__).resolve()
    repo_root = next((parent for parent in script_path.parents if parent.name == "Otctopus_OS_AgentConsole"), None)
    if repo_root is None:
        raise RuntimeError("cannot resolve product root from Disabled-Octupos-FullStack script path")
    return repo_root.parent


DEFAULT_WORKSPACE_ROOT = (_resolve_product_root() / "Octopus_OS").resolve()
DEFAULT_DOCUMENT_ROOT = DEFAULT_WORKSPACE_ROOT / "Mother_Doc" / "docs"


def scaffold_graph_runtime_tree(graph_root: Path, *, dry_run: bool) -> list[str]:
    created: list[str] = []
    runtime_dirs = {
        "runtime": "OS_graph runtime root.",
        "runtime/registry": "Node registries for documents and evidence.",
        "runtime/indexes": "Edge indexes, bindings, and lifecycle-aware lookup data.",
        "runtime/reports": "Graph sync reports and change-detection outputs.",
        "runtime/maps": "Graph-derived resource and structural maps.",
        "runtime/wiki": "Local wiki bundles generated from graph resources.",
        "runtime/snapshots": "Future snapshot and compare artifacts.",
        "runtime/frontend_views": "Frontend-facing aggregated bundles derived from fragmented graph storage.",
    }
    for relative_path, description in runtime_dirs.items():
        target = graph_root / relative_path / "README.md"
        was_created = ensure_markdown(target, title=Path(relative_path).name, body_lines=[description], dry_run=dry_run)
        if was_created:
            created.append(str(target))
    return created


def emit_contract(payload: dict[str, object], *, as_json: bool) -> int:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for key, value in payload.items():
            print(f"{key}: {value}")
    return 0


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
        workspace_dir = workspace_root / name
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
        if name == "Mother_Doc":
            ensure_markdown(
                workspace_dir / "graph" / "README.md",
                title="graph",
                body_lines=build_graph_readme(),
                dry_run=args.dry_run,
            )
            created_document_files.extend(scaffold_graph_runtime_tree(workspace_dir / "graph", dry_run=args.dry_run))
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
        created_document_files.extend(
            scaffold_content_tree(
                container_name=name,
                document_dir=document_dir,
                family=family,
                dry_run=args.dry_run,
            )
        )

    payload = {
        "workspace_root": str(workspace_root),
        "document_root": str(document_root),
        "containers": containers,
        "created_workspace_dirs": created_workspace_dirs,
        "created_document_dirs": created_document_dirs,
        "existing_workspace_dirs": existing_workspace_dirs,
        "existing_document_dirs": existing_document_dirs,
        "created_document_files": created_document_files,
        "navigation_sync": sync_navigation_tree(document_root, dry_run=args.dry_run),
        "status_sync": sync_status_tree_from_git(
            document_root,
            repo_root=workspace_root,
            stage="mother_doc",
            block_ids=None,
            target_paths=[document_root / name for name in containers],
            dry_run=args.dry_run,
        ),
        "warnings": warnings,
        "dry_run": bool(args.dry_run),
    }
    return emit_contract(payload, as_json=args.json)


def sync_mother_doc_navigation(args: argparse.Namespace) -> int:
    document_root = Path(args.document_root).resolve()
    navigation_sync = sync_navigation_tree(document_root, dry_run=args.dry_run)
    touched_paths = [Path(path) for key in ("created_readmes", "created_scope_docs") for path in navigation_sync[key]]
    payload = {
        "document_root": str(document_root),
        **navigation_sync,
        "status_sync": sync_status_tree_from_git(
            document_root,
            repo_root=DEFAULT_WORKSPACE_ROOT,
            stage="mother_doc",
            block_ids=None,
            target_paths=touched_paths or None,
            dry_run=args.dry_run,
        ),
        "dry_run": bool(args.dry_run),
    }
    return emit_contract(payload, as_json=args.json)


def sync_mother_doc_status(args: argparse.Namespace) -> int:
    document_root = Path(args.document_root).resolve()
    target_paths = [Path(path) for path in args.path] if args.path else None
    payload = {
        "document_root": str(document_root),
        **sync_status_tree(
            document_root,
            stage=args.stage,
            lifecycle_state=args.lifecycle_state,
            block_ids=args.block_id or None,
            target_paths=target_paths,
            dry_run=args.dry_run,
        ),
    }
    return emit_contract(payload, as_json=args.json)


def sync_mother_doc_status_from_git(args: argparse.Namespace) -> int:
    document_root = Path(args.document_root).resolve()
    repo_root = Path(args.repo_root).resolve()
    target_paths = [Path(path) for path in args.path] if args.path else None
    payload = {
        "document_root": str(document_root),
        **sync_status_tree_from_git(
            document_root,
            repo_root=repo_root,
            stage=args.stage,
            block_ids=args.block_id or None,
            target_paths=target_paths,
            dry_run=args.dry_run,
        ),
    }
    return emit_contract(payload, as_json=args.json)


def append_development_log(args: argparse.Namespace) -> int:
    document_root = Path(args.document_root).resolve()
    payload = append_log_entry(
        document_root,
        kind=args.kind,
        summary=args.summary,
        doc_paths=args.doc_path,
        code_paths=args.code_path,
        dry_run=args.dry_run,
    )
    return emit_contract(payload, as_json=args.json)
