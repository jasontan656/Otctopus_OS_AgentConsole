from __future__ import annotations

from pathlib import Path

from managed_agents_text import is_agents_target_kind
from managed_paths import index_path


def _clean_preview_line(raw: str) -> str | None:
    line = raw.strip()
    if not line:
        return None
    if line in {"---", "```", "```text", "```md"}:
        return None
    if line.startswith("```"):
        return None
    return " ".join(line.split())


def build_preview(text: str, max_lines: int = 3) -> str:
    lines: list[str] = []
    for raw in text.splitlines():
        line = _clean_preview_line(raw)
        if line is None:
            continue
        lines.append(line)
        if len(lines) >= max_lines:
            break
    if not lines:
        return "N/A"
    return " | ".join(lines)


def write_index(skill_root: Path, entries: list[dict[str, str]]) -> None:
    path = index_path(skill_root)
    path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Managed Default Docs Index",
        "",
        f"- count: {len(entries)}",
        "- generated_by: collect",
        "",
    ]

    for entry in entries:
        managed = Path(entry["human_path"]) if is_agents_target_kind(entry["target_kind"]) else Path(entry["managed_path"])
        text = managed.read_text(encoding="utf-8") if managed.exists() else ""
        preview = build_preview(text)
        detail_lines = (
            [
                f"- human_path: `{entry['human_path']}`",
                f"- machine_path: `{entry['machine_path']}`",
            ]
            if is_agents_target_kind(entry["target_kind"])
            else [f"- managed_path: `{entry['managed_path']}`"]
        )
        lines.extend(
            [
                f"## {entry['source_path']}",
                f"- target_kind: `{entry['target_kind']}`",
                f"- source_path: `{entry['source_path']}`",
                f"- managed_dir: `{entry['managed_dir']}`",
                f"- managed_rel_path: `{entry['managed_rel_path']}`",
                *detail_lines,
                f"- preview: {preview}",
                "",
            ]
        )

    path.write_text("\n".join(lines), encoding="utf-8")
