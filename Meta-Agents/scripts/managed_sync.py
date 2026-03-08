from __future__ import annotations

import shutil
from pathlib import Path

from managed_registry import load_registry, sha256_text, write_registry


def sync_out(
    skill_root: Path,
    target_source_paths: list[str],
    sync_all: bool,
) -> dict[str, object]:
    payload = load_registry(skill_root)
    entries = payload.get("entries", [])
    if sync_all:
        selected = entries
    else:
        wanted = {str(Path(item).expanduser().resolve()) for item in target_source_paths}
        selected = [entry for entry in entries if entry["source_path"] in wanted]
        missing = sorted(wanted - {entry["source_path"] for entry in selected})
        if missing:
            raise ValueError(f"unknown source paths: {missing}")

    synced: list[dict[str, str]] = []
    for entry in selected:
        source = Path(entry["managed_path"])
        target = Path(entry["source_path"])
        if not source.exists():
            raise FileNotFoundError(f"managed copy missing: {source}")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        text = source.read_text(encoding="utf-8")
        entry["sha256"] = sha256_text(text)
        synced.append(
            {
                "source_path": entry["source_path"],
                "managed_path": entry["managed_path"],
            }
        )

    write_registry(skill_root, payload)
    return {
        "status": "ok",
        "action": "sync_out",
        "count": len(synced),
        "entries": synced,
    }
