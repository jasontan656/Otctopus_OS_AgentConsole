from __future__ import annotations

from pathlib import Path

from managed_paths import is_excluded_scan_path, managed_file_path, managed_rel_path, managed_root, root_slug
from managed_registry import build_entry, load_registry, sha256_text, write_registry


def _discover_agents(source_root: Path, skill_root: Path) -> list[Path]:
    results: list[Path] = []
    for candidate in source_root.rglob("AGENTS.md"):
        if is_excluded_scan_path(candidate, skill_root):
            continue
        results.append(candidate.resolve())
    return sorted(results)


def _prune_missing(skill_root: Path, source_root: Path, live_rel_paths: set[str]) -> None:
    namespace_root = managed_root(skill_root) / root_slug(source_root)
    if not namespace_root.exists():
        return

    for target in sorted(namespace_root.rglob("AGENTS.md")):
        rel_path = target.relative_to(managed_root(skill_root)).as_posix()
        if rel_path in live_rel_paths:
            continue
        target.unlink()

    for candidate in sorted(namespace_root.rglob("*"), reverse=True):
        if candidate.is_dir() and not any(candidate.iterdir()):
            candidate.rmdir()
    if namespace_root.exists() and not any(namespace_root.iterdir()):
        namespace_root.rmdir()


def collect_agents(skill_root: Path, source_root: Path) -> dict[str, object]:
    discovered = _discover_agents(source_root, skill_root)
    payload = load_registry(skill_root)
    other_entries = [
        entry for entry in payload.get("entries", [])
        if entry["source_root"] != str(source_root)
    ]
    new_entries: list[dict[str, str]] = []
    live_rel_paths: set[str] = set()

    for source_path in discovered:
        text = source_path.read_text(encoding="utf-8")
        managed_path = managed_file_path(skill_root, source_root, source_path)
        managed_path.parent.mkdir(parents=True, exist_ok=True)
        managed_path.write_text(text, encoding="utf-8")
        rel_path = managed_rel_path(source_root, source_path)
        live_rel_paths.add(rel_path.as_posix())
        new_entries.append(
            build_entry(
                source_root=source_root,
                source_path=source_path,
                managed_path=managed_path,
                managed_rel_path=rel_path,
                sha256=sha256_text(text),
            )
        )

    _prune_missing(skill_root, source_root, live_rel_paths)
    merged = sorted(other_entries + new_entries, key=lambda item: item["source_path"])
    write_registry(skill_root, {"version": 1, "entries": merged})
    return {
        "status": "ok",
        "action": "scan_collect",
        "source_root": str(source_root),
        "managed_root": str(managed_root(skill_root)),
        "count": len(new_entries),
        "entries": merged,
    }
