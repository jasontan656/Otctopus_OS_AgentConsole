from __future__ import annotations

import json
import hashlib
from pathlib import Path

from managed_paths import asset_descriptor, registry_path


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def normalize_entry(skill_root: Path, entry: dict[str, object]) -> dict[str, str]:
    source_root = Path(str(entry["source_root"]))
    source_path = Path(str(entry["source_path"]))
    target_kind = str(entry["target_kind"])
    normalized = {
        "source_root": str(source_root),
        "source_path": str(source_path),
        "target_kind": target_kind,
        "sha256": str(entry.get("sha256", "")),
    }
    normalized.update(asset_descriptor(skill_root, source_root, source_path, target_kind))
    return normalized


def load_registry(
    skill_root: Path,
    *,
    require_existing: bool = False,
    require_entries: bool = False,
) -> dict[str, object]:
    path = registry_path(skill_root)
    if not path.exists():
        if require_existing:
            raise FileNotFoundError(f"registry missing: {path}")
        return {"version": 2, "entries": []}
    raw = path.read_text(encoding="utf-8")
    if not raw.strip():
        raise ValueError(f"registry file is empty: {path}")
    payload = json.loads(raw)
    entries = [normalize_entry(skill_root, entry) for entry in payload.get("entries", [])]
    if require_entries and not entries:
        raise ValueError(f"registry has no entries: {path}")
    return {"version": 3, "entries": entries}


def write_registry(skill_root: Path, payload: dict[str, object]) -> None:
    path = registry_path(skill_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def build_entry(
    *,
    skill_root: Path,
    source_root: Path,
    source_path: Path,
    target_kind: str,
    sha256: str,
) -> dict[str, str]:
    entry = {
        "source_root": str(source_root),
        "source_path": str(source_path),
        "target_kind": target_kind,
        "sha256": sha256,
    }
    entry.update(asset_descriptor(skill_root, source_root, source_path, target_kind))
    return entry
