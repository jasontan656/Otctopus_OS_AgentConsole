from __future__ import annotations

import json
from pathlib import Path

from managed_paths import (
    is_excluded_scan_path,
    managed_file_path,
    managed_rel_path,
    managed_root,
    resolve_source_root,
    root_slug,
    scan_report_path,
)


def _discover_agents(source_root: Path, skill_root: Path) -> list[Path]:
    results: list[Path] = []
    for candidate in source_root.rglob("AGENTS.md"):
        if is_excluded_scan_path(candidate, skill_root):
            continue
        results.append(candidate.resolve())
    return sorted(results)


def write_scan_report(skill_root: Path, source_root: Path) -> dict[str, object]:
    discovered = _discover_agents(source_root, skill_root)
    entries: list[dict[str, str]] = []
    for source_path in discovered:
        entries.append(
            {
                "source_root": str(source_root),
                "source_path": str(source_path),
                "managed_rel_path": managed_rel_path(source_root, source_path).as_posix(),
                "managed_path": str(managed_file_path(skill_root, source_root, source_path)),
            }
        )

    payload = {
        "version": 1,
        "action": "scan",
        "source_root": str(source_root),
        "root_slug": root_slug(source_root),
        "managed_root": str(managed_root(skill_root)),
        "count": len(entries),
        "entries": entries,
    }
    path = scan_report_path(skill_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def load_scan_report(skill_root: Path) -> dict[str, object]:
    path = scan_report_path(skill_root)
    if not path.exists():
        raise FileNotFoundError(f"scan report missing: {path}")
    raw = path.read_text(encoding="utf-8")
    if not raw.strip():
        raise ValueError(f"scan report file is empty: {path}")
    payload = json.loads(raw)
    entries = payload.get("entries", [])
    if not entries:
        raise ValueError(f"scan report has no entries: {path}")
    return payload


def resolve_scan_source_root(raw: str | None) -> Path:
    return resolve_source_root(raw)
