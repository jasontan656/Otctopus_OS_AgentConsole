from __future__ import annotations

from pathlib import Path
from typing import Iterable


STATUS_START = "<!-- octopus:status:start -->"
STATUS_END = "<!-- octopus:status:end -->"


def _bool_text(value: bool) -> str:
    return "true" if value else "false"


def _scope_doc_name(parent: Path, document_root: Path) -> str:
    if parent == document_root:
        return "Mother_Doc.md"
    return f"{parent.name}.md"


def infer_doc_role(path: Path, document_root: Path) -> str:
    if path.name == "README.md":
        return "scope_purpose"
    if path.name == _scope_doc_name(path.parent, document_root):
        return "scope_entity"
    rel = path.relative_to(document_root)
    if "contracts" in rel.parts:
        return "contract_leaf"
    if "common" in rel.parts:
        return "abstraction_leaf"
    return "authored_leaf"


def _strip_existing_status(body: str) -> str:
    if STATUS_START not in body:
        return body.strip("\n")
    before, _sep, rest = body.partition(STATUS_START)
    _managed, _sep2, after = rest.partition(STATUS_END)
    return "\n".join([before.rstrip(), after.lstrip()]).strip("\n")


def build_status_block(
    *,
    path: Path,
    document_root: Path,
    stage: str,
    requires_development: bool,
    sync_status: str,
    block_ids: Iterable[str],
) -> str:
    rel = path.relative_to(document_root)
    lines = [
        STATUS_START,
        "## Document Status",
        f"doc_path: {rel}",
        f"doc_role: {infer_doc_role(path, document_root)}",
        f"doc_requires_development: {_bool_text(requires_development)}",
        f"doc_sync_status: {sync_status}",
        f"last_updated_stage: {stage}",
        "change_detection_mode: block_registry",
        "",
        "## Block Registry",
    ]
    for block_id in block_ids:
        lines.extend(
            [
                f"- block_id: {block_id}",
                f"  requires_development: {_bool_text(requires_development)}",
                f"  sync_status: {sync_status}",
                f"  last_updated_stage: {stage}",
            ]
        )
    lines.extend([STATUS_END, ""])
    return "\n".join(lines)


def update_status_file(
    *,
    path: Path,
    document_root: Path,
    stage: str,
    requires_development: bool,
    sync_status: str,
    block_ids: list[str],
    dry_run: bool,
) -> bool:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines:
        return False
    title_line = lines[0]
    rest = "\n".join(lines[1:]).strip("\n")
    status_block = build_status_block(
        path=path,
        document_root=document_root,
        stage=stage,
        requires_development=requires_development,
        sync_status=sync_status,
        block_ids=block_ids,
    )
    normalized_rest = _strip_existing_status(rest)
    new_text = "\n".join([title_line, "", status_block, normalized_rest]).rstrip() + "\n"
    if new_text == text:
        return False
    if not dry_run:
        path.write_text(new_text, encoding="utf-8")
    return True


def _iter_target_docs(document_root: Path, target_paths: list[Path] | None) -> list[Path]:
    if not target_paths:
        return sorted(
            [
                path
                for path in document_root.rglob("*.md")
                if path.name != "agents.md"
            ]
        )

    docs: set[Path] = set()
    for raw_path in target_paths:
        path = raw_path if raw_path.is_absolute() else document_root / raw_path
        if path.is_dir():
            docs.update(p for p in path.rglob("*.md") if p.name != "agents.md")
        elif path.suffix == ".md" and path.name != "agents.md":
            docs.add(path)
    return sorted(docs)


def sync_status_tree(
    document_root: Path,
    *,
    stage: str,
    requires_development: bool,
    sync_status: str,
    block_ids: list[str],
    target_paths: list[Path] | None,
    dry_run: bool,
) -> dict[str, object]:
    updated_files: list[str] = []
    unchanged_files: list[str] = []
    for path in _iter_target_docs(document_root, target_paths):
        changed = update_status_file(
            path=path,
            document_root=document_root,
            stage=stage,
            requires_development=requires_development,
            sync_status=sync_status,
            block_ids=block_ids,
            dry_run=dry_run,
        )
        if changed:
            updated_files.append(str(path))
        else:
            unchanged_files.append(str(path))
    return {
        "stage": stage,
        "requires_development": requires_development,
        "sync_status": sync_status,
        "block_ids": block_ids,
        "updated_files": updated_files,
        "unchanged_files": unchanged_files,
        "dry_run": dry_run,
    }
