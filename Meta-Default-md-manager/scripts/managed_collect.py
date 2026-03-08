from __future__ import annotations

from pathlib import Path

from managed_index import write_index
from managed_paths import managed_root, root_slug
from managed_registry import build_entry, load_registry, sha256_text, write_registry
from managed_scan import load_scan_report


def _prune_missing(skill_root: Path, source_root: Path, live_rel_paths: set[str]) -> None:
    namespace_root = managed_root(skill_root) / root_slug(source_root)
    if not namespace_root.exists():
        return

    for target in sorted(namespace_root.rglob("*")):
        if not target.is_file():
            continue
        rel_path = target.relative_to(managed_root(skill_root)).as_posix()
        if rel_path in live_rel_paths:
            continue
        target.unlink()

    for candidate in sorted(namespace_root.rglob("*"), reverse=True):
        if candidate.is_dir() and not any(candidate.iterdir()):
            candidate.rmdir()
    if namespace_root.exists() and not any(namespace_root.iterdir()):
        namespace_root.rmdir()


def collect_from_scan(skill_root: Path, source_root: str | None = None) -> dict[str, object]:
    scan_report = load_scan_report(skill_root)
    report_source_root = str(Path(scan_report["source_root"]).resolve())
    if source_root is not None:
        wanted_source_root = str(Path(source_root).expanduser().resolve())
        if wanted_source_root != report_source_root:
            raise ValueError(
                f"scan report source_root mismatch: wanted {wanted_source_root}, got {report_source_root}"
            )

    source_root_path = Path(report_source_root)
    payload = load_registry(skill_root)
    other_entries = [
        entry for entry in payload.get("entries", [])
        if entry["source_root"] != report_source_root
    ]
    new_entries: list[dict[str, str]] = []
    live_rel_paths: set[str] = set()

    for scanned in scan_report.get("entries", []):
        source_path = Path(scanned["source_path"])
        if not source_path.exists():
            raise FileNotFoundError(f"scanned source file missing: {source_path}")
        managed_path = Path(scanned["managed_path"])
        text = source_path.read_text(encoding="utf-8")
        managed_path.parent.mkdir(parents=True, exist_ok=True)
        managed_path.write_text(text, encoding="utf-8")
        live_rel_paths.add(scanned["managed_rel_path"])
        new_entries.append(
            build_entry(
                source_root=source_root_path,
                source_path=source_path,
                managed_path=managed_path,
                managed_rel_path=Path(scanned["managed_rel_path"]),
                target_kind=str(scanned["target_kind"]),
                sha256=sha256_text(text),
            )
        )

    _prune_missing(skill_root, source_root_path, live_rel_paths)
    merged = sorted(other_entries + new_entries, key=lambda item: item["source_path"])
    write_registry(skill_root, {"version": 2, "entries": merged})
    write_index(skill_root, merged)
    return {
        "status": "ok",
        "action": "collect",
        "source_root": report_source_root,
        "managed_root": str(managed_root(skill_root)),
        "count": len(new_entries),
        "entries": merged,
    }
