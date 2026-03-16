from __future__ import annotations

from pathlib import Path


def write_files(target_root: Path, files: dict[str, str], overwrite: bool) -> list[str]:
    written: list[str] = []
    for relative_path, content in files.items():
        destination = target_root / relative_path
        if destination.exists() and not overwrite:
            raise FileExistsError(f"file already exists: {destination}")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")
        written.append(relative_path)
    return sorted(written)
