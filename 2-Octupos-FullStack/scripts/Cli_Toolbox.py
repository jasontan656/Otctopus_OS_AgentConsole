#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


DEFAULT_WORKSPACE_ROOT = Path("/home/jasontan656/AI_Projects/Octopus_OS")
DEFAULT_DOCUMENT_ROOT = DEFAULT_WORKSPACE_ROOT / "Mother_Doc"
VALID_NAME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")
DISCOURAGED_PREFIXES = ("Shared_", "Business_", "Runtime_")
PREFERRED_SUFFIXES = (
    "_UI",
    "_Gateway",
    "_Service",
    "_DB",
    "_Cache",
    "_Broker",
    "_Storage",
)


def validate_container_name(name: str) -> list[str]:
    warnings: list[str] = []
    if name == "Mother_Doc":
        raise ValueError("container name `Mother_Doc` is reserved")
    if not VALID_NAME_RE.fullmatch(name):
        raise ValueError(f"invalid container name: {name}")
    if any(name.startswith(prefix) for prefix in DISCOURAGED_PREFIXES):
        warnings.append(f"discouraged bucket-style name: {name}")
    if not any(name.endswith(suffix) for suffix in PREFERRED_SUFFIXES):
        warnings.append(f"name does not use a preferred stage-1 suffix: {name}")
    return warnings


def ensure_readme(path: Path, *, title: str, body_lines: list[str], dry_run: bool) -> bool:
    if path.exists():
        return False
    if dry_run:
        return True
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join([f"# {title}", "", *body_lines, ""]) , encoding="utf-8")
    return True


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

    for name in containers:
        warnings.extend(validate_container_name(name))

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

        ensure_readme(
            workspace_dir / "README.md",
            title=name,
            body_lines=[
                "Stage-1 container directory.",
                f"Corresponding Mother_Doc path: {document_dir}",
            ],
            dry_run=args.dry_run,
        )
        ensure_readme(
            document_dir / "README.md",
            title=name,
            body_lines=[
                "Mother_Doc entry for the same-named container.",
                f"Corresponding workspace path: {workspace_dir}",
            ],
            dry_run=args.dry_run,
        )

    payload = {
        "workspace_root": str(workspace_root),
        "document_root": str(document_root),
        "containers": containers,
        "created_workspace_dirs": created_workspace_dirs,
        "created_document_dirs": created_document_dirs,
        "existing_workspace_dirs": existing_workspace_dirs,
        "existing_document_dirs": existing_document_dirs,
        "warnings": warnings,
        "dry_run": bool(args.dry_run),
    }

    if args.json:
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
    materialize.add_argument(
        "--workspace-root",
        default=str(DEFAULT_WORKSPACE_ROOT),
        help="Octopus_OS workspace root",
    )
    materialize.add_argument(
        "--document-root",
        default=str(DEFAULT_DOCUMENT_ROOT),
        help="Mother_Doc root",
    )
    materialize.add_argument(
        "--container",
        action="append",
        default=[],
        help="container name; repeat for multiple containers",
    )
    materialize.add_argument("--dry-run", action="store_true")
    materialize.add_argument("--json", action="store_true")
    materialize.set_defaults(func=materialize_layout)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
