from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path


def _entry_header(kind: str) -> str:
    if kind == "implementation":
        return "implementation_batch"
    return "deployment_checkpoint"


def _resolve_log_path(document_root: Path, kind: str) -> Path:
    base = document_root / "Mother_Doc" / "common" / "development_logs"
    if kind == "implementation":
        return base / "implementation_batches.md"
    return base / "deployment_batches.md"


def append_log_entry(
    document_root: Path,
    *,
    kind: str,
    summary: str,
    doc_paths: list[str],
    code_paths: list[str],
    dry_run: bool,
) -> dict[str, object]:
    target = _resolve_log_path(document_root, kind)
    if not target.exists():
        raise FileNotFoundError(target)

    existing = target.read_text(encoding="utf-8")
    timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    lines = [
        f"### {timestamp}",
        f"- `entry_kind`: `{_entry_header(kind)}`",
        "- `comparison_order`: `read_code_then_read_updated_docs`",
        f"- `summary`: {summary}",
        "- `doc_paths`:",
    ]
    if doc_paths:
        lines.extend([f"  - `{value}`" for value in doc_paths])
    else:
        lines.append("  - `none`")
    lines.append("- `code_paths`:")
    if code_paths:
        lines.extend([f"  - `{value}`" for value in code_paths])
    else:
        lines.append("  - `none`")
    lines.append("")
    entry = "\n".join(lines)

    marker = "## Entries"
    if marker in existing:
        new_text = existing.rstrip() + "\n\n" + entry + "\n"
    else:
        new_text = existing.rstrip() + "\n\n## Entries\n\n" + entry + "\n"

    if not dry_run:
        target.write_text(new_text, encoding="utf-8")

    return {
        "kind": kind,
        "target": str(target),
        "summary": summary,
        "traceability_mode": "summary_equals_git_commit_message",
        "doc_paths": doc_paths,
        "code_paths": code_paths,
        "dry_run": dry_run,
    }
