from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import TypedDict

from mother_doc_contract import (
    MOTHER_DOC_ALLOWED_DOC_ROLES,
    MOTHER_DOC_ANCHOR_FIELDS,
    MOTHER_DOC_DIRECTORY_NAME_PATTERN,
    MOTHER_DOC_FILE_BASENAME_PATTERN,
    MOTHER_DOC_FORBIDDEN_FRONTMATTER_FIELDS,
    MOTHER_DOC_FRONTMATTER_REQUIRED_FIELDS,
    MOTHER_DOC_REQUIRED_ENTRY_ALTERNATIVES,
    MOTHER_DOC_STATE_TRANSITIONS,
    MOTHER_DOC_WORK_STATES,
)


class StateViolation(TypedDict):
    doc_ref: str
    reason: str


EXCLUDED_MOTHER_DOC_ROOTS = {
    "execution_atom_plan_validation_packs",
    "acceptance",
    "graph",
}


def _parse_scalar(value: str) -> object:
    stripped = value.strip()
    if not stripped:
        return ""
    if stripped in {"true", "false", "null"} or stripped.startswith(("[", "{")):
        try:
            return json.loads(stripped)
        except json.JSONDecodeError:
            return stripped
    return stripped


def parse_frontmatter(path: Path) -> tuple[dict[str, object], str, list[str]]:
    content = path.read_text(encoding="utf-8")
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, content, ["missing_frontmatter_block"]

    closing_index = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            closing_index = index
            break
    if closing_index is None:
        return {}, content, ["unterminated_frontmatter_block"]

    metadata: dict[str, object] = {}
    current_key: str | None = None
    current_item_dict: dict[str, object] | None = None
    errors: list[str] = []
    for line_number, raw_line in enumerate(lines[1:closing_index], start=2):
        if not raw_line.strip():
            continue
        if raw_line.startswith("  ") and current_item_dict is not None:
            nested = raw_line.strip()
            if ":" not in nested:
                errors.append(f"line_{line_number}_expected_nested_key_value")
                continue
            nested_key, nested_value = nested.split(":", 1)
            current_item_dict[nested_key.strip()] = _parse_scalar(nested_value)
            continue
        if raw_line.startswith("  - ") or raw_line.startswith("- "):
            if current_key is None:
                errors.append(f"line_{line_number}_list_item_without_parent")
                continue
            existing = metadata.setdefault(current_key, [])
            if not isinstance(existing, list):
                errors.append(f"line_{line_number}_mixed_scalar_and_list_for_{current_key}")
                continue
            item_text = raw_line[4:].strip() if raw_line.startswith("  - ") else raw_line[2:].strip()
            if ":" in item_text and not item_text.startswith(("http://", "https://")):
                item_key, item_value = item_text.split(":", 1)
                current_item_dict = {item_key.strip(): _parse_scalar(item_value)}
                existing.append(current_item_dict)
            else:
                existing.append(item_text)
                current_item_dict = None
            continue
        if raw_line.startswith(" "):
            errors.append(f"line_{line_number}_unsupported_indentation")
            continue
        if ":" not in raw_line:
            errors.append(f"line_{line_number}_expected_key_value")
            current_key = None
            current_item_dict = None
            continue
        key, raw_value = raw_line.split(":", 1)
        key = key.strip()
        value = raw_value.strip()
        if not key:
            errors.append(f"line_{line_number}_empty_key")
            current_key = None
            current_item_dict = None
            continue
        current_key = key
        current_item_dict = None
        metadata[key] = _parse_scalar(value) if value else []

    body = "\n".join(lines[closing_index + 1 :])
    if content.endswith("\n"):
        body += "\n"
    return metadata, body, errors


def render_frontmatter(metadata: dict[str, object]) -> str:
    def render_scalar(value: object) -> str:
        if isinstance(value, bool) or value is None:
            return json.dumps(value)
        return str(value)

    lines = ["---"]
    for key, value in metadata.items():
        if isinstance(value, list):
            if not value:
                lines.append(f"{key}: []")
                continue
            lines.append(f"{key}:")
            for item in value:
                if isinstance(item, dict):
                    first = True
                    for item_key, item_value in item.items():
                        prefix = "- " if first else "  "
                        lines.append(f"{prefix}{item_key}: {render_scalar(item_value)}")
                        first = False
                    continue
                lines.append(f"  - {render_scalar(item)}")
            continue
        lines.append(f"{key}: {render_scalar(value)}")
    lines.append("---")
    return "\n".join(lines)


def write_frontmatter(path: Path, metadata: dict[str, object], body: str) -> None:
    rendered = render_frontmatter(metadata)
    body_text = body.lstrip("\n")
    content = f"{rendered}\n{body_text}"
    if not content.endswith("\n"):
        content += "\n"
    path.write_text(content, encoding="utf-8")


def required_entry_hits(root: Path) -> tuple[list[str], dict[str, list[str]]]:
    missing_entries: list[str] = []
    resolved_entries: dict[str, list[str]] = {}
    for entry_id, alternatives in MOTHER_DOC_REQUIRED_ENTRY_ALTERNATIVES.items():
        hits = [relative for relative in alternatives if (root / relative).exists()]
        if hits:
            resolved_entries[entry_id] = hits
            continue
        missing_entries.append(entry_id)
    return missing_entries, resolved_entries


def iter_atomic_markdown_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in sorted(root.rglob("*.md")):
        relative_parts = path.relative_to(root).parts
        if relative_parts and relative_parts[0] in EXCLUDED_MOTHER_DOC_ROOTS:
            continue
        files.append(path)
    return files


def find_docs_with_role(root: Path, role: str) -> list[Path]:
    matches: list[Path] = []
    for path in iter_atomic_markdown_files(root):
        metadata, _body, parse_errors = parse_frontmatter(path)
        if parse_errors:
            continue
        if metadata.get("doc_role") == role:
            matches.append(path)
    return matches


def _build_doc_id_index(root: Path) -> dict[str, str]:
    index: dict[str, str] = {}
    for path in iter_atomic_markdown_files(root):
        metadata, _body, parse_errors = parse_frontmatter(path)
        if parse_errors:
            continue
        doc_id = metadata.get("doc_id")
        if isinstance(doc_id, str) and doc_id and doc_id not in index:
            index[doc_id] = str(path.relative_to(root))
    return index


def resolve_doc_refs(root: Path, doc_refs: list[str]) -> tuple[list[str], list[StateViolation]]:
    doc_id_index = _build_doc_id_index(root)
    resolved: list[str] = []
    violations: list[StateViolation] = []
    seen: set[str] = set()
    for doc_ref in doc_refs:
        direct_path = (root / doc_ref).resolve()
        relative_doc = (
            doc_ref
            if direct_path.exists() and direct_path.is_file()
            else doc_id_index.get(doc_ref)
        )
        if relative_doc is None:
            violations.append({"doc_ref": doc_ref, "reason": "doc_missing"})
            continue
        if relative_doc in seen:
            continue
        seen.add(relative_doc)
        resolved.append(relative_doc)
    return resolved, violations


def validate_doc_metadata(metadata: dict[str, object]) -> list[str]:
    errors: list[str] = []
    forbidden_fields = [
        field for field in MOTHER_DOC_FORBIDDEN_FRONTMATTER_FIELDS if field in metadata
    ]
    if forbidden_fields:
        errors.append(f"forbidden_frontmatter_fields_present={forbidden_fields}")

    missing_fields = [
        field for field in MOTHER_DOC_FRONTMATTER_REQUIRED_FIELDS if field not in metadata
    ]
    if missing_fields:
        errors.append(f"missing_required_frontmatter_fields={missing_fields}")
        return errors

    state = metadata.get("doc_work_state")
    if state not in MOTHER_DOC_WORK_STATES:
        errors.append(
            f"invalid_doc_work_state={state}; allowed={','.join(MOTHER_DOC_WORK_STATES)}"
        )

    pack_refs = metadata.get("doc_pack_refs")
    if not isinstance(pack_refs, list):
        errors.append("doc_pack_refs_must_be_a_list")
    elif state in {"planned", "developed", "ref"} and not pack_refs:
        errors.append("doc_pack_refs_required_for_non_modified_state")

    thumb_title = metadata.get("thumb_title")
    if not isinstance(thumb_title, str) or not thumb_title.strip():
        errors.append("thumb_title_required_as_non_empty_string")

    thumb_summary = metadata.get("thumb_summary")
    if not isinstance(thumb_summary, str) or not thumb_summary.strip():
        errors.append("thumb_summary_required_as_non_empty_string")

    display_layer = metadata.get("display_layer")
    if not isinstance(display_layer, str) or not display_layer.strip():
        errors.append("display_layer_required_as_non_empty_string")

    always_read = metadata.get("always_read")
    if not isinstance(always_read, bool):
        errors.append("always_read_must_be_boolean")

    for anchor_field in MOTHER_DOC_ANCHOR_FIELDS:
        anchor_value = metadata.get(anchor_field)
        if not isinstance(anchor_value, list):
            errors.append(f"{anchor_field}_must_be_a_list")
            continue
        if any(not isinstance(item, str) or not item.strip() for item in anchor_value):
            errors.append(f"{anchor_field}_must_only_contain_non_empty_strings")

    doc_role = metadata.get("doc_role")
    if doc_role is not None and doc_role not in MOTHER_DOC_ALLOWED_DOC_ROLES:
        errors.append(
            f"invalid_doc_role={doc_role}; allowed={','.join(MOTHER_DOC_ALLOWED_DOC_ROLES)}"
        )
    return errors


def validate_doc_naming(root: Path, file_path: Path) -> list[str]:
    import re

    relative_parts = file_path.relative_to(root).parts
    basename = file_path.name
    file_pattern = re.compile(MOTHER_DOC_FILE_BASENAME_PATTERN)
    directory_pattern = re.compile(MOTHER_DOC_DIRECTORY_NAME_PATTERN)
    errors: list[str] = []

    if not file_pattern.match(basename):
        errors.append(f"invalid_file_basename={basename}")

    for directory_name in relative_parts[:-1]:
        if not directory_pattern.match(directory_name):
            errors.append(f"invalid_directory_name={directory_name}")

    return errors


def validate_transition(from_state: str, to_state: str) -> str | None:
    allowed = MOTHER_DOC_STATE_TRANSITIONS.get(from_state, [])
    if to_state not in allowed:
        return f"invalid_state_transition={from_state}->{to_state}"
    return None


def _git_repo_root(path: Path) -> Path:
    completed = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "--show-toplevel"],
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(f"git_repo_root_resolution_failed: {completed.stderr.strip()}")
    return Path(completed.stdout.strip()).resolve()


def _git_changed_paths(repo_root: Path, scope_root: Path) -> list[Path]:
    relative_scope = scope_root.resolve().relative_to(repo_root.resolve())
    completed = subprocess.run(
        [
            "git",
            "-C",
            str(repo_root),
            "status",
            "--short",
            "--porcelain=v1",
            "--untracked-files=all",
            "--",
            str(relative_scope),
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(f"git_status_failed: {completed.stderr.strip()}")

    changed_paths: list[Path] = []
    for line in completed.stdout.splitlines():
        if not line:
            continue
        path_text = line[3:]
        if " -> " in path_text:
            path_text = path_text.split(" -> ", 1)[1]
        changed_paths.append((repo_root / path_text).resolve())
    return changed_paths


def _impact_doc_refs(root: Path, changed_doc: Path) -> set[str]:
    impacted: set[str] = set()
    impacted.add(str(changed_doc.relative_to(root)))

    current = changed_doc.parent
    while current != root.parent and current.is_relative_to(root):
        index_path = current / "00_index.md"
        if index_path.exists():
            impacted.add(str(index_path.relative_to(root)))
        if current == root:
            break
        current = current.parent

    return impacted


def detect_git_modified_doc_refs(root: Path, repo_root: Path | None = None) -> dict[str, list[str]]:
    resolved_repo_root = repo_root or _git_repo_root(root)
    changed_paths = _git_changed_paths(resolved_repo_root, root)
    direct_doc_refs: set[str] = set()
    impact_doc_refs: set[str] = set()

    for changed_path in changed_paths:
        if not changed_path.exists():
            continue
        if changed_path.suffix != ".md" or not changed_path.is_relative_to(root):
            continue
        relative_doc = changed_path.relative_to(root)
        if relative_doc.parts and relative_doc.parts[0] in EXCLUDED_MOTHER_DOC_ROOTS:
            continue
        direct_doc_refs.add(str(relative_doc))
        impact_doc_refs.update(_impact_doc_refs(root, changed_path))

    return {
        "direct_doc_refs": sorted(direct_doc_refs),
        "impact_doc_refs": sorted(impact_doc_refs),
    }


def sync_doc_states(
    root: Path,
    doc_refs: list[str],
    from_state: str,
    to_state: str,
    pack_ref: str | None,
) -> dict[str, object]:
    transition_error = validate_transition(from_state, to_state)
    if transition_error is not None:
        return {"status": "fail", "reason": transition_error, "updated_docs": []}

    if to_state == "planned" and not pack_ref:
        return {
            "status": "fail",
            "reason": "planned_state_requires_pack_ref",
            "updated_docs": [],
        }

    resolved_doc_refs, violations = resolve_doc_refs(root, doc_refs)
    updated_docs: list[str] = []
    for relative_doc in resolved_doc_refs:
        path = (root / relative_doc).resolve()
        metadata, body, parse_errors = parse_frontmatter(path)
        if parse_errors:
            violations.append(
                {
                    "doc_ref": relative_doc,
                    "reason": f"frontmatter_parse_error:{','.join(parse_errors)}",
                }
            )
            continue
        current_state = metadata.get("doc_work_state")
        if current_state != from_state:
            violations.append(
                {
                    "doc_ref": relative_doc,
                    "reason": f"expected_state={from_state},found={current_state}",
                }
            )
            continue
        pack_refs = metadata.get("doc_pack_refs", [])
        if not isinstance(pack_refs, list):
            violations.append({"doc_ref": relative_doc, "reason": "doc_pack_refs_must_be_a_list"})
            continue
        if to_state == "modified":
            pack_refs = []
        elif pack_ref and pack_ref not in pack_refs:
            pack_refs.append(pack_ref)
        metadata["doc_pack_refs"] = pack_refs
        metadata["doc_work_state"] = to_state
        validation_errors = validate_doc_metadata(metadata)
        if validation_errors:
            violations.append(
                {
                    "doc_ref": relative_doc,
                    "reason": ",".join(validation_errors),
                }
            )
            continue
        write_frontmatter(path, metadata, body)
        updated_docs.append(relative_doc)

    return {
        "status": "pass" if not violations else "fail",
        "updated_docs": updated_docs,
        "selected_doc_refs": resolved_doc_refs,
        "violations": violations,
        "from_state": from_state,
        "to_state": to_state,
        "pack_ref": pack_ref,
    }


def mark_docs_modified(
    root: Path,
    doc_refs: list[str],
    *,
    repo_root: Path | None = None,
    auto_from_git: bool,
) -> dict[str, object]:
    explicit_doc_refs = sorted(set(doc_refs))
    detected = (
        detect_git_modified_doc_refs(root, repo_root)
        if auto_from_git
        else {"direct_doc_refs": [], "impact_doc_refs": []}
    )
    candidate_doc_refs = sorted(
        set(explicit_doc_refs)
        | set(detected["direct_doc_refs"])
        | set(detected["impact_doc_refs"])
    )
    if not candidate_doc_refs:
        return {
            "status": "fail",
            "reason": "no_doc_refs_selected_for_modified_mark",
            "explicit_doc_refs": explicit_doc_refs,
            "git_direct_doc_refs": detected["direct_doc_refs"],
            "git_impact_doc_refs": detected["impact_doc_refs"],
            "updated_docs": [],
        }

    resolved_doc_refs, violations = resolve_doc_refs(root, candidate_doc_refs)
    updated_docs: list[str] = []
    already_modified_docs: list[str] = []
    for relative_doc in resolved_doc_refs:
        path = (root / relative_doc).resolve()
        metadata, body, parse_errors = parse_frontmatter(path)
        if parse_errors:
            violations.append(
                {
                    "doc_ref": relative_doc,
                    "reason": f"frontmatter_parse_error:{','.join(parse_errors)}",
                }
            )
            continue
        pack_refs = metadata.get("doc_pack_refs", [])
        if not isinstance(pack_refs, list):
            violations.append({"doc_ref": relative_doc, "reason": "doc_pack_refs_must_be_a_list"})
            continue
        current_state = metadata.get("doc_work_state")
        if current_state == "modified" and pack_refs == []:
            already_modified_docs.append(relative_doc)
            continue
        metadata["doc_work_state"] = "modified"
        metadata["doc_pack_refs"] = []
        validation_errors = validate_doc_metadata(metadata)
        if validation_errors:
            violations.append({"doc_ref": relative_doc, "reason": ",".join(validation_errors)})
            continue
        write_frontmatter(path, metadata, body)
        updated_docs.append(relative_doc)

    return {
        "status": "pass" if not violations else "fail",
        "explicit_doc_refs": explicit_doc_refs,
        "git_direct_doc_refs": detected["direct_doc_refs"],
        "git_impact_doc_refs": detected["impact_doc_refs"],
        "selected_doc_refs": resolved_doc_refs,
        "updated_docs": updated_docs,
        "already_modified_docs": already_modified_docs,
        "violations": violations,
    }
