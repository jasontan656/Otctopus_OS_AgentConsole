from __future__ import annotations

import json
import hashlib
from pathlib import Path

from managed_paths import registry_path


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


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
        return {"version": 1, "entries": []}
    raw = path.read_text(encoding="utf-8")
    if not raw.strip():
        raise ValueError(f"registry file is empty: {path}")
    payload = json.loads(raw)
    entries = payload.get("entries", [])
    if require_entries and not entries:
        raise ValueError(f"registry has no entries: {path}")
    return payload


def write_registry(skill_root: Path, payload: dict[str, object]) -> None:
    path = registry_path(skill_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def build_entry(
    *,
    source_root: Path,
    source_path: Path,
    managed_path: Path,
    managed_rel_path: Path,
    sha256: str,
) -> dict[str, str]:
    return {
        "source_root": str(source_root),
        "source_path": str(source_path),
        "managed_rel_path": managed_rel_path.as_posix(),
        "managed_path": str(managed_path),
        "sha256": sha256,
    }
