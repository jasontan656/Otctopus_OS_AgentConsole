from __future__ import annotations

from pathlib import Path

from mother_doc_contract import (
    MOTHER_DOC_FRONTMATTER_REQUIRED_FIELDS,
    MOTHER_DOC_REQUIRED_ENTRY_ALTERNATIVES,
    MOTHER_DOC_STATE_TRANSITIONS,
    MOTHER_DOC_WORK_STATES,
)


def _parse_scalar(value: str) -> object:
    stripped = value.strip()
    if stripped == "[]":
        return []
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
    errors: list[str] = []
    for line_number, raw_line in enumerate(lines[1:closing_index], start=2):
        if not raw_line.strip():
            continue
        if raw_line.startswith("  - "):
            if current_key is None:
                errors.append(f"line_{line_number}_list_item_without_parent")
                continue
            existing = metadata.setdefault(current_key, [])
            if not isinstance(existing, list):
                errors.append(f"line_{line_number}_mixed_scalar_and_list_for_{current_key}")
                continue
            existing.append(raw_line[4:].strip())
            continue
        if raw_line.startswith(" "):
            errors.append(f"line_{line_number}_unsupported_indentation")
            continue
        if ":" not in raw_line:
            errors.append(f"line_{line_number}_expected_key_value")
            current_key = None
            continue
        key, raw_value = raw_line.split(":", 1)
        key = key.strip()
        value = raw_value.strip()
        if not key:
            errors.append(f"line_{line_number}_empty_key")
            current_key = None
            continue
        current_key = key
        metadata[key] = _parse_scalar(value) if value else []

    body = "\n".join(lines[closing_index + 1 :])
    if content.endswith("\n"):
        body += "\n"
    return metadata, body, errors


def render_frontmatter(metadata: dict[str, object]) -> str:
    lines = ["---"]
    for key, value in metadata.items():
        if isinstance(value, list):
            if not value:
                lines.append(f"{key}: []")
                continue
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - {item}")
            continue
        lines.append(f"{key}: {value}")
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
    excluded_roots = {
        "execution_atom_plan_validation_packs",
        "acceptance",
        "graph",
    }
    files: list[Path] = []
    for path in sorted(root.rglob("*.md")):
        relative_parts = path.relative_to(root).parts
        if relative_parts and relative_parts[0] in excluded_roots:
            continue
        files.append(path)
    return files


def validate_doc_metadata(metadata: dict[str, object]) -> list[str]:
    errors: list[str] = []
    missing_fields = [
        field for field in MOTHER_DOC_FRONTMATTER_REQUIRED_FIELDS if field not in metadata
    ]
    if missing_fields:
        return [f"missing_required_frontmatter_fields={missing_fields}"]

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
    return errors


def validate_transition(from_state: str, to_state: str) -> str | None:
    allowed = MOTHER_DOC_STATE_TRANSITIONS.get(from_state, [])
    if to_state not in allowed:
        return f"invalid_state_transition={from_state}->{to_state}"
    return None


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

    updated_docs: list[str] = []
    violations: list[dict[str, str]] = []
    for relative_doc in doc_refs:
        path = (root / relative_doc).resolve()
        if not path.exists() or not path.is_file():
            violations.append({"doc_ref": relative_doc, "reason": "doc_missing"})
            continue
        metadata, body, parse_errors = parse_frontmatter(path)
        if parse_errors:
            violations.append(
                {"doc_ref": relative_doc, "reason": f"frontmatter_parse_error:{','.join(parse_errors)}"}
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
        if pack_ref and pack_ref not in pack_refs:
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
        "violations": violations,
        "from_state": from_state,
        "to_state": to_state,
        "pack_ref": pack_ref,
    }
