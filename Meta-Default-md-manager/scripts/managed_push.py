from __future__ import annotations

import shutil
from pathlib import Path

from managed_agents_text import compose_external_agents, is_agents_target_kind
from managed_registry import load_registry, sha256_text, write_registry


def push_out(
    skill_root: Path,
    target_source_paths: list[str],
    push_all: bool,
) -> dict[str, object]:
    payload = load_registry(skill_root, require_existing=True, require_entries=True)
    entries = payload.get("entries", [])
    if push_all:
        selected = entries
    else:
        wanted = {str(Path(item).expanduser().resolve()) for item in target_source_paths}
        selected = [entry for entry in entries if entry["source_path"] in wanted]
        missing = sorted(wanted - {entry["source_path"] for entry in selected})
        if missing:
            raise ValueError(f"unknown source paths: {missing}")

    pushed: list[dict[str, str]] = []
    for entry in selected:
        target = Path(entry["source_path"])
        target.parent.mkdir(parents=True, exist_ok=True)
        if is_agents_target_kind(entry["target_kind"]):
            source = Path(entry["human_path"])
            if not source.exists():
                raise FileNotFoundError(f"managed human asset missing: {source}")
            if source.stat().st_size == 0:
                raise ValueError(f"managed human asset is empty: {source}")
            text = compose_external_agents(source.read_text(encoding="utf-8"))
            target.write_text(text, encoding="utf-8")
            asset_path = entry["human_path"]
        else:
            source = Path(entry["managed_path"])
            if not source.exists():
                raise FileNotFoundError(f"managed copy missing: {source}")
            if source.stat().st_size == 0:
                raise ValueError(f"managed copy is empty: {source}")
            shutil.copyfile(source, target)
            text = source.read_text(encoding="utf-8")
            asset_path = entry["managed_path"]
        entry["sha256"] = sha256_text(text)
        pushed.append(
            {
                "source_path": entry["source_path"],
                "asset_path": asset_path,
            }
        )

    write_registry(skill_root, payload)
    return {
        "status": "ok",
        "action": "push",
        "count": len(pushed),
        "entries": pushed,
    }
