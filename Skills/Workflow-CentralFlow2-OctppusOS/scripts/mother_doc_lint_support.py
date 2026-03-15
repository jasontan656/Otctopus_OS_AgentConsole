from __future__ import annotations
from pathlib import Path

from mother_doc_contract import (
    MOTHER_DOC_ANCHOR_FIELDS,
    MOTHER_DOC_FRONTMATTER_REQUIRED_FIELDS,
    MOTHER_DOC_GUIDANCE_MARKERS,
    MOTHER_DOC_HEADING_MAX_DEPTH,
    MOTHER_DOC_REQUIRED_DESIGN_PLAN_ROLE,
    MOTHER_DOC_REQUIRED_ENTRY_ALTERNATIVES,
    MOTHER_DOC_REQUIRED_ROOT_INDEX_RULES,
    MOTHER_DOC_ROOT_REQUIRED_FILES,
    MOTHER_DOC_REQUIRED_STAGE_IDS,
    MOTHER_DOC_STAGE_PLAN_MARKERS,
    MOTHER_DOC_WORK_STATES,
)
from mother_doc_root_index_support import render_root_index_body
from mother_doc_state_support import (
    find_docs_with_role,
    iter_atomic_markdown_files,
    parse_frontmatter,
    required_entry_hits,
    validate_doc_naming,
    validate_doc_metadata,
)


def _detect_mother_doc_root(path: Path) -> tuple[Path, bool]:
    resolved = path.resolve()
    if resolved.is_dir():
        return resolved, False
    if resolved.name == "00_index.md":
        return resolved.parent, False
    return resolved, resolved.name == "mother_doc.md"


def _find_replace_me_hits(root: Path, files: list[Path]) -> list[str]:
    hits: list[str] = []
    for file_path in files:
        if not file_path.exists() or not file_path.is_file():
            continue
        if "replace_me" in file_path.read_text(encoding="utf-8"):
            hits.append(str(file_path.relative_to(root)))
    return hits


def _find_guidance_hits(root: Path, files: list[Path]) -> list[str]:
    hits: list[str] = []
    for file_path in files:
        if not file_path.exists() or not file_path.is_file():
            continue
        content = file_path.read_text(encoding="utf-8")
        if any(marker in content for marker in MOTHER_DOC_GUIDANCE_MARKERS):
            hits.append(str(file_path.relative_to(root)))
    return hits


def _heading_violations(root: Path, files: list[Path]) -> dict[str, list[str]]:
    violations: dict[str, list[str]] = {}
    for file_path in files:
        errors: list[str] = []
        heading_count = 0
        for line_number, raw_line in enumerate(file_path.read_text(encoding="utf-8").splitlines(), start=1):
            if not raw_line.startswith("#"):
                continue
            prefix = raw_line.split(" ", 1)[0]
            level = len(prefix)
            heading_count += 1
            if level > MOTHER_DOC_HEADING_MAX_DEPTH:
                errors.append(f"line_{line_number}_heading_depth_exceeds_{MOTHER_DOC_HEADING_MAX_DEPTH}")
        if heading_count == 0:
            errors.append("missing_heading_structure")
        if errors:
            violations[str(file_path.relative_to(root))] = errors
    return violations


def _anchor_violations(root: Path, files: list[Path]) -> dict[str, list[str]]:
    violations: dict[str, list[str]] = {}
    for file_path in files:
        metadata, _body, parse_errors = parse_frontmatter(file_path)
        if parse_errors:
            continue
        errors: list[str] = []
        relative_doc = str(file_path.relative_to(root))
        for anchor_field in MOTHER_DOC_ANCHOR_FIELDS:
            anchor_value = metadata.get(anchor_field)
            if not isinstance(anchor_value, list):
                continue
            for target in anchor_value:
                target_path = root / str(target)
                if not target_path.exists():
                    errors.append(f"{anchor_field}_target_missing={target}")
                if str(target) == relative_doc:
                    errors.append(f"{anchor_field}_self_reference_forbidden={target}")
        if errors:
            violations[relative_doc] = errors
    return violations


_DISPLAY_LAYER_ORDER = {
    "overview": 0,
    "entry": 1,
    "resolution": 2,
    "capability": 3,
    "support": 4,
}


def _traversal_violations(root: Path, files: list[Path]) -> dict[str, list[str]]:
    violations: dict[str, list[str]] = {}
    metadata_by_doc: dict[str, dict[str, object]] = {}
    parent_hits: dict[str, list[str]] = {}

    for file_path in files:
        metadata, _body, parse_errors = parse_frontmatter(file_path)
        if parse_errors:
            continue
        metadata_by_doc[str(file_path.relative_to(root))] = metadata

    for relative_doc, metadata in metadata_by_doc.items():
        errors: list[str] = []
        display_layer = str(metadata.get("display_layer") or "")
        display_layer_index = _DISPLAY_LAYER_ORDER.get(display_layer, 99)
        local_targets: set[str] = set()

        for anchor_field in MOTHER_DOC_ANCHOR_FIELDS:
            anchor_value = metadata.get(anchor_field)
            if not isinstance(anchor_value, list):
                continue

            for target in anchor_value:
                target_ref = str(target).strip()
                if not target_ref:
                    continue
                if target_ref in local_targets:
                    errors.append(f"duplicate_traversal_target={target_ref}")
                    continue
                local_targets.add(target_ref)
                parent_hits.setdefault(target_ref, []).append(f"{relative_doc}:{anchor_field}")

                target_metadata = metadata_by_doc.get(target_ref)
                if target_metadata is None:
                    continue

                target_layer = str(target_metadata.get("display_layer") or "")
                target_layer_index = _DISPLAY_LAYER_ORDER.get(target_layer, 99)
                if anchor_field == "anchors_down" and target_layer_index <= display_layer_index:
                    errors.append(f"anchors_down_target_not_deeper={target_ref}")
                if anchor_field == "anchors_support" and target_layer_index < display_layer_index:
                    errors.append(f"anchors_support_target_cannot_be_higher={target_ref}")

        if errors:
            violations[relative_doc] = errors

    for target_ref, parents in parent_hits.items():
        if len(parents) <= 1:
            continue
        for parent in parents:
            parent_doc = parent.split(":", 1)[0]
            violations.setdefault(parent_doc, []).append(
                f"multi_parent_target_forbidden={target_ref}; parents={sorted(parents)}"
            )

    return violations


def _root_index_violations(root: Path, resolved_entries: dict[str, list[str]]) -> list[str]:
    hits = resolved_entries.get("root_index", [])
    if not hits:
        return ["root_index_missing"]
    root_index_path = root / hits[0]
    metadata, _body, parse_errors = parse_frontmatter(root_index_path)
    if parse_errors:
        return [f"root_index_frontmatter_parse_error={error}" for error in parse_errors]

    errors: list[str] = []
    if metadata.get("doc_role") != MOTHER_DOC_REQUIRED_ROOT_INDEX_RULES["doc_role"]:
        errors.append("root_index_doc_role_must_be_root_index")
    if metadata.get("always_read") is not MOTHER_DOC_REQUIRED_ROOT_INDEX_RULES["always_read"]:
        errors.append("root_index_always_read_must_be_true")
    if MOTHER_DOC_REQUIRED_ROOT_INDEX_RULES["anchor_fields_must_be_empty"]:
        for anchor_field in MOTHER_DOC_ANCHOR_FIELDS:
            if metadata.get(anchor_field) not in ([], None):
                errors.append(f"root_index_{anchor_field}_must_be_empty")
    _metadata, current_body, _current_parse_errors = parse_frontmatter(root_index_path)
    expected_body = render_root_index_body(root)
    if current_body.lstrip("\n").rstrip() != expected_body.rstrip():
        errors.append("root_index_out_of_sync_with_folder_structure")
    return errors


def _design_plan_violations(root: Path) -> dict[str, object]:
    design_plan_docs = find_docs_with_role(root, MOTHER_DOC_REQUIRED_DESIGN_PLAN_ROLE)
    if not design_plan_docs:
        return {
            "design_plan_docs": [],
            "complete_design_plan_docs": [],
            "incomplete_design_plan_docs": {},
            "violations": [],
        }

    complete_docs: list[str] = []
    incomplete_docs: dict[str, list[str]] = {}
    for file_path in design_plan_docs:
        content = file_path.read_text(encoding="utf-8")
        missing_items = [
            *[f"missing_stage_id={stage_id}" for stage_id in MOTHER_DOC_REQUIRED_STAGE_IDS if stage_id not in content],
            *[
                f"missing_stage_plan_marker={marker}"
                for marker in MOTHER_DOC_STAGE_PLAN_MARKERS
                if marker not in content
            ],
        ]
        relative_doc = str(file_path.relative_to(root))
        if missing_items:
            incomplete_docs[relative_doc] = missing_items
            continue
        complete_docs.append(relative_doc)

    violations: list[str] = []
    if design_plan_docs and not complete_docs:
        violations.append("design_plan_docs_present_but_missing_stage_contract_markers")

    return {
        "design_plan_docs": [str(path.relative_to(root)) for path in design_plan_docs],
        "complete_design_plan_docs": complete_docs,
        "incomplete_design_plan_docs": incomplete_docs,
        "violations": violations,
    }


def mother_doc_lint_summary(path: Path) -> dict:
    root, single_file_input_detected = _detect_mother_doc_root(path)
    exists = root.exists()
    missing_entry_ids, resolved_entries = required_entry_hits(root) if exists else (
        list(MOTHER_DOC_REQUIRED_ENTRY_ALTERNATIVES),
        {},
    )
    atomic_docs = iter_atomic_markdown_files(root) if exists and not single_file_input_detected else []
    replace_me_hits = _find_replace_me_hits(root, atomic_docs) if exists and not single_file_input_detected else []
    guidance_hits = _find_guidance_hits(root, atomic_docs) if exists and not single_file_input_detected else []
    frontmatter_violations: dict[str, list[str]] = {}
    naming_violations: dict[str, list[str]] = {}
    for file_path in atomic_docs:
        metadata, _body, parse_errors = parse_frontmatter(file_path)
        errors = list(parse_errors)
        errors.extend(validate_doc_metadata(metadata) if not parse_errors else [])
        if errors:
            frontmatter_violations[str(file_path.relative_to(root))] = errors
        naming_errors = validate_doc_naming(root, file_path)
        if naming_errors:
            naming_violations[str(file_path.relative_to(root))] = naming_errors

    heading_violations = _heading_violations(root, atomic_docs) if exists and not single_file_input_detected else {}
    anchor_violations = _anchor_violations(root, atomic_docs) if exists and not single_file_input_detected else {}
    traversal_violations = _traversal_violations(root, atomic_docs) if exists and not single_file_input_detected else {}
    root_index_violations = _root_index_violations(root, resolved_entries) if exists and not single_file_input_detected else []
    design_plan_summary = _design_plan_violations(root) if exists and not single_file_input_detected else {
        "design_plan_docs": [],
        "complete_design_plan_docs": [],
        "incomplete_design_plan_docs": {},
        "violations": [],
    }

    status = "pass"
    if single_file_input_detected:
        status = "fail"
    elif (
        not exists
        or missing_entry_ids
        or replace_me_hits
        or guidance_hits
        or frontmatter_violations
        or naming_violations
        or heading_violations
        or anchor_violations
        or traversal_violations
        or root_index_violations
    ):
        status = "fail"

    return {
        "path": str(path),
        "resolved_root": str(root),
        "exists": exists,
        "single_file_input_detected": single_file_input_detected,
        "status": status,
        "missing_required_files": list(MOTHER_DOC_ROOT_REQUIRED_FILES) if not exists else missing_entry_ids,
        "required_entry_alternatives": MOTHER_DOC_REQUIRED_ENTRY_ALTERNATIVES,
        "resolved_required_entries": resolved_entries,
        "files_with_replace_me": replace_me_hits,
        "files_with_template_guidance": guidance_hits,
        "frontmatter_violations": frontmatter_violations,
        "naming_violations": naming_violations,
        "heading_violations": heading_violations,
        "anchor_violations": anchor_violations,
        "traversal_violations": traversal_violations,
        "root_index_violations": root_index_violations,
        "design_plan_summary": design_plan_summary,
        "frontmatter_required_fields": MOTHER_DOC_FRONTMATTER_REQUIRED_FIELDS,
        "doc_work_states": MOTHER_DOC_WORK_STATES,
        "required_files": MOTHER_DOC_ROOT_REQUIRED_FILES,
        "required_stage_ids": MOTHER_DOC_REQUIRED_STAGE_IDS,
        "required_stage_plan_markers": MOTHER_DOC_STAGE_PLAN_MARKERS,
        "guidance_markers": MOTHER_DOC_GUIDANCE_MARKERS,
        "construction_plan_gate_allowed": status == "pass",
        "single_file_rejection_hint": ""
        if not single_file_input_detected
        else "single-file mother_doc.md is not accepted; run mother-doc-init and fill docs/mother_doc/ instead.",
    }
