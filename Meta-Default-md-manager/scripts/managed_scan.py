from __future__ import annotations

import json
from pathlib import Path

from managed_paths import asset_descriptor
from managed_paths import (
    RECURSIVE_TARGET_BASENAMES,
    explicit_target_paths,
    is_excluded_scan_path,
    managed_root,
    resolve_source_root,
    root_slug,
    scan_report_path,
    target_kind,
)


def _discover_targets(source_root: Path, skill_root: Path) -> list[Path]:
    results: set[Path] = set()
    for basename in RECURSIVE_TARGET_BASENAMES:
        for candidate in source_root.rglob(basename):
            if is_excluded_scan_path(candidate, skill_root, source_root):
                continue
            results.add(candidate.resolve())
    for candidate in explicit_target_paths(source_root):
        if not candidate.exists():
            continue
        if is_excluded_scan_path(candidate, skill_root, source_root):
            continue
        results.add(candidate.resolve())
    return sorted(results, key=lambda path: path.as_posix())


def write_scan_report(skill_root: Path, source_root: Path) -> dict[str, object]:
    discovered = _discover_targets(source_root, skill_root)
    entries: list[dict[str, str]] = []
    for source_path in discovered:
        resolved_target_kind = target_kind(source_root, source_path)
        entries.append(
            {
                "source_root": str(source_root),
                "source_path": str(source_path),
                "target_kind": resolved_target_kind,
                **asset_descriptor(skill_root, source_root, source_path, resolved_target_kind),
            }
        )

    payload = {
        "version": 3,
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
    normalized_entries: list[dict[str, str]] = []
    report_source_root = Path(str(payload["source_root"])).resolve()
    for entry in entries:
        source_path = Path(str(entry["source_path"])).resolve()
        resolved_target_kind = target_kind(report_source_root, source_path)
        normalized_entries.append(
            {
                "source_root": str(report_source_root),
                "source_path": str(source_path),
                "target_kind": resolved_target_kind,
                **asset_descriptor(skill_root, report_source_root, source_path, resolved_target_kind),
            }
        )
    payload["source_root"] = str(report_source_root)
    payload["root_slug"] = root_slug(report_source_root)
    payload["managed_root"] = str(managed_root(skill_root))
    payload["count"] = len(normalized_entries)
    payload["entries"] = normalized_entries
    return payload


def resolve_scan_source_root(raw: str | None) -> Path:
    return resolve_source_root(raw)
