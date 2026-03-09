from __future__ import annotations

import subprocess
from pathlib import Path


STATUS_START = "<!-- octopus:status:start -->"
STATUS_END = "<!-- octopus:status:end -->"
AGENTS_FILENAME = "AGENTS.md"
LIFECYCLE_STATES = {"modified", "developed", "null"}
LEGACY_STATE_MAP = {
    "pending_implementation": "modified",
    "aligned": "developed",
}


def _bool_text(value: bool) -> str:
    return "true" if value else "false"


def _scope_doc_name(parent: Path, document_root: Path) -> str:
    return "Mother_Doc.md" if parent == document_root else f"{parent.name}.md"


def _requires_development(lifecycle_state: str) -> bool:
    return lifecycle_state == "modified"


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


def _extract_existing_block_ids(text: str) -> list[str]:
    block_ids: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- block_id:"):
            block_ids.append(stripped.split(":", 1)[1].strip())
    return block_ids or ["primary"]


def _extract_existing_state(text: str) -> str | None:
    for prefix in ("doc_lifecycle_state:", "doc_sync_status:"):
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith(prefix):
                value = stripped.split(":", 1)[1].strip()
                return LEGACY_STATE_MAP.get(value, value)
    return None


def _looks_null_payload(text: str) -> bool:
    body = _strip_existing_status("\n".join(text.splitlines()[1:]))
    if not body.strip():
        return True
    compact = "\n".join(line.strip() for line in body.splitlines() if line.strip())
    placeholder_tokens = {"replace_me", "null", "n/a", "todo"}
    return compact.lower() in placeholder_tokens


def build_status_block(
    *,
    path: Path,
    document_root: Path,
    stage: str,
    lifecycle_state: str,
    block_ids: list[str],
) -> str:
    requires_development = _requires_development(lifecycle_state)
    rel = path.relative_to(document_root)
    lines = [
        STATUS_START,
        "## Document Status",
        f"doc_path: {rel}",
        f"doc_role: {infer_doc_role(path, document_root)}",
        f"doc_lifecycle_state: {lifecycle_state}",
        f"doc_requires_development: {_bool_text(requires_development)}",
        f"doc_sync_status: {lifecycle_state}",
        f"last_updated_stage: {stage}",
        "change_detection_mode: block_registry",
        "",
        "## Block Registry",
    ]
    for block_id in block_ids:
        lines.extend(
            [
                f"- block_id: {block_id}",
                f"  lifecycle_state: {lifecycle_state}",
                f"  requires_development: {_bool_text(requires_development)}",
                f"  sync_status: {lifecycle_state}",
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
    lifecycle_state: str,
    block_ids: list[str] | None,
    dry_run: bool,
) -> bool:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines:
        return False
    title_line = lines[0]
    rest = "\n".join(lines[1:]).strip("\n")
    resolved_block_ids = block_ids or _extract_existing_block_ids(text)
    status_block = build_status_block(
        path=path,
        document_root=document_root,
        stage=stage,
        lifecycle_state=lifecycle_state,
        block_ids=resolved_block_ids,
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
        return sorted(path for path in document_root.rglob("*.md") if path.name != AGENTS_FILENAME)
    docs: set[Path] = set()
    for raw_path in target_paths:
        path = raw_path if raw_path.is_absolute() else document_root / raw_path
        if path.is_dir():
            docs.update(p for p in path.rglob("*.md") if p.name != AGENTS_FILENAME)
        elif path.suffix == ".md" and path.name != AGENTS_FILENAME:
            docs.add(path)
    return sorted(docs)


def _git_changed_docs(repo_root: Path, document_root: Path, docs: list[Path]) -> set[Path]:
    if not docs:
        return set()
    rel_paths = [str(path.relative_to(repo_root)) for path in docs]
    proc = subprocess.run(
        ["git", "-C", str(repo_root), "status", "--porcelain", "--", *rel_paths],
        check=True,
        capture_output=True,
        text=True,
    )
    changed: set[Path] = set()
    for line in proc.stdout.splitlines():
        if not line.strip():
            continue
        rel = line[3:].strip()
        candidate = repo_root / rel
        if candidate.suffix == ".md" and candidate.name != AGENTS_FILENAME and candidate.is_relative_to(document_root):
            changed.add(candidate)
    return changed


def sync_status_tree(
    document_root: Path,
    *,
    stage: str,
    lifecycle_state: str,
    block_ids: list[str] | None,
    target_paths: list[Path] | None,
    dry_run: bool,
) -> dict[str, object]:
    if lifecycle_state not in LIFECYCLE_STATES:
        raise ValueError(f"unsupported lifecycle_state: {lifecycle_state}")
    updated_files: list[str] = []
    unchanged_files: list[str] = []
    for path in _iter_target_docs(document_root, target_paths):
        changed = update_status_file(
            path=path,
            document_root=document_root,
            stage=stage,
            lifecycle_state=lifecycle_state,
            block_ids=block_ids,
            dry_run=dry_run,
        )
        (updated_files if changed else unchanged_files).append(str(path))
    return {
        "stage": stage,
        "lifecycle_state": lifecycle_state,
        "requires_development": _requires_development(lifecycle_state),
        "block_ids": block_ids or ["existing_or_primary"],
        "updated_files": updated_files,
        "unchanged_files": unchanged_files,
        "dry_run": dry_run,
    }


def sync_status_tree_from_git(
    document_root: Path,
    *,
    repo_root: Path,
    stage: str,
    block_ids: list[str] | None,
    target_paths: list[Path] | None,
    dry_run: bool,
) -> dict[str, object]:
    docs = _iter_target_docs(document_root, target_paths)
    changed_docs = _git_changed_docs(repo_root, document_root, docs)
    updated_files: list[str] = []
    unchanged_files: list[str] = []
    resolved_states: dict[str, str] = {}
    for path in docs:
        text = path.read_text(encoding="utf-8")
        if _looks_null_payload(text):
            lifecycle_state = "null"
        elif path in changed_docs:
            lifecycle_state = "modified"
        else:
            lifecycle_state = _extract_existing_state(text) or "developed"
        resolved_states[str(path)] = lifecycle_state
        changed = update_status_file(
            path=path,
            document_root=document_root,
            stage=stage,
            lifecycle_state=lifecycle_state,
            block_ids=block_ids,
            dry_run=dry_run,
        )
        (updated_files if changed else unchanged_files).append(str(path))
    return {
        "stage": stage,
        "repo_root": str(repo_root),
        "mode": "git_backed_lifecycle_sync",
        "changed_docs": sorted(str(path) for path in changed_docs),
        "resolved_states": resolved_states,
        "updated_files": updated_files,
        "unchanged_files": unchanged_files,
        "dry_run": dry_run,
    }
