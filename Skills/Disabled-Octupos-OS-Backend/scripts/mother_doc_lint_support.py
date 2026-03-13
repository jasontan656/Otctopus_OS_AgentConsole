from __future__ import annotations

from pathlib import Path

from mother_doc_contract import (
    MOTHER_DOC_FORBIDDEN_TERMS,
    MOTHER_DOC_GUIDANCE_MARKERS,
    MOTHER_DOC_REQUIRED_FILES,
    MOTHER_DOC_REQUIRED_SIGNALS,
    MOTHER_DOC_REQUIRED_STAGE_IDS,
    MOTHER_DOC_STAGE_PLAN_MARKERS,
)


def _find_missing_signals(content: str) -> list[str]:
    lowered = content.lower()
    missing: list[str] = []
    for signal in MOTHER_DOC_REQUIRED_SIGNALS:
        if signal.lower() not in lowered:
            missing.append(signal)
    return missing


def _find_forbidden_terms(content: str) -> list[str]:
    lowered = content.lower()
    hits: list[str] = []
    for term in MOTHER_DOC_FORBIDDEN_TERMS:
        if term.lower() in lowered:
            hits.append(term)
    return hits


def _detect_mother_doc_root(path: Path) -> tuple[Path, bool]:
    resolved = path.resolve()
    if resolved.is_dir():
        return resolved, False
    if resolved.name == "00_index.md":
        return resolved.parent, False
    return resolved, resolved.name == "mother_doc.md"


def _required_file_paths(root: Path) -> list[Path]:
    return [root / relative_path for relative_path in MOTHER_DOC_REQUIRED_FILES]


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


def _aggregate_content(files: list[Path]) -> str:
    chunks: list[str] = []
    for file_path in files:
        if file_path.exists() and file_path.is_file():
            chunks.append(file_path.read_text(encoding="utf-8"))
    return "\n".join(chunks)


def mother_doc_lint_summary(path: Path) -> dict:
    root, single_file_input_detected = _detect_mother_doc_root(path)
    exists = root.exists()
    required_files = _required_file_paths(root)
    missing_files = [str(file_path.relative_to(root)) for file_path in required_files if not file_path.exists()] if exists else list(MOTHER_DOC_REQUIRED_FILES)
    aggregated_content = _aggregate_content(required_files) if exists and not single_file_input_detected else ""
    missing_signals = _find_missing_signals(aggregated_content) if aggregated_content else list(MOTHER_DOC_REQUIRED_SIGNALS)
    forbidden_term_hits = _find_forbidden_terms(aggregated_content) if aggregated_content else []
    replace_me_hits = _find_replace_me_hits(root, required_files) if exists and not single_file_input_detected else []
    guidance_hits = _find_guidance_hits(root, required_files) if exists and not single_file_input_detected else []
    stage_plan_path = root / "08_dev_execution_plan.md"
    stage_plan_content = stage_plan_path.read_text(encoding="utf-8") if stage_plan_path.exists() and stage_plan_path.is_file() else ""
    missing_stage_ids = [stage_id for stage_id in MOTHER_DOC_REQUIRED_STAGE_IDS if stage_id not in stage_plan_content]
    missing_stage_markers = [marker for marker in MOTHER_DOC_STAGE_PLAN_MARKERS if marker not in stage_plan_content]

    status = "pass"
    if single_file_input_detected:
        status = "fail"
    elif not exists or missing_files or missing_signals or forbidden_term_hits or replace_me_hits or guidance_hits or missing_stage_ids or missing_stage_markers:
        status = "fail"

    return {
        "path": str(path),
        "resolved_root": str(root),
        "exists": exists,
        "single_file_input_detected": single_file_input_detected,
        "status": status,
        "missing_required_files": missing_files,
        "missing_required_signals": missing_signals,
        "forbidden_term_hits": forbidden_term_hits,
        "files_with_replace_me": replace_me_hits,
        "files_with_template_guidance": guidance_hits,
        "missing_stage_ids": missing_stage_ids,
        "missing_stage_plan_markers": missing_stage_markers,
        "required_files": MOTHER_DOC_REQUIRED_FILES,
        "required_signals": MOTHER_DOC_REQUIRED_SIGNALS,
        "required_stage_ids": MOTHER_DOC_REQUIRED_STAGE_IDS,
        "required_stage_plan_markers": MOTHER_DOC_STAGE_PLAN_MARKERS,
        "guidance_markers": MOTHER_DOC_GUIDANCE_MARKERS,
        "forbidden_terms": MOTHER_DOC_FORBIDDEN_TERMS,
        "construction_plan_gate_allowed": status == "pass",
        "single_file_rejection_hint": ""
        if not single_file_input_detected
        else "single-file mother_doc.md is not accepted; run mother-doc-init and fill docs/mother_doc/ instead.",
    }
