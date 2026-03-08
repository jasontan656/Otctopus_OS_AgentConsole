from __future__ import annotations

from pathlib import Path

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
        "# Managed AGENTS Index",
        "",
        f"- count: {len(entries)}",
        "- generated_by: scan-collect",
        "",
    ]

    for entry in entries:
        managed = Path(entry["managed_path"])
        text = managed.read_text(encoding="utf-8") if managed.exists() else ""
        preview = build_preview(text)
        lines.extend(
            [
                f"## {entry['source_path']}",
                f"- source_path: `{entry['source_path']}`",
                f"- managed_path: `{entry['managed_path']}`",
                f"- managed_rel_path: `{entry['managed_rel_path']}`",
                f"- preview: {preview}",
                "",
            ]
        )

    path.write_text("\n".join(lines), encoding="utf-8")
