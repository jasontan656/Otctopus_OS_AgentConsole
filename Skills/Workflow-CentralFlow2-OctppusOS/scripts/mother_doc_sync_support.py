from __future__ import annotations

import shutil
from pathlib import Path


def mother_doc_sync_result(source_root: Path, mirror_root: Path) -> tuple[dict[str, object], int]:
    resolved_source = source_root.resolve()
    resolved_mirror = mirror_root.resolve()

    if not resolved_source.exists():
        return {
            "status": "fail",
            "reason": "source_mother_doc_missing",
            "source_root": str(resolved_source),
            "mirror_root": str(resolved_mirror),
        }, 1

    if not resolved_source.is_dir():
        return {
            "status": "fail",
            "reason": "source_mother_doc_not_directory",
            "source_root": str(resolved_source),
            "mirror_root": str(resolved_mirror),
        }, 1

    if resolved_source == resolved_mirror:
        return {
            "status": "fail",
            "reason": "source_and_mirror_identical",
            "source_root": str(resolved_source),
            "mirror_root": str(resolved_mirror),
        }, 1

    file_count = sum(1 for path in resolved_source.rglob("*") if path.is_file())
    if resolved_mirror.exists():
        shutil.rmtree(resolved_mirror)
    resolved_mirror.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(resolved_source, resolved_mirror)

    return {
        "status": "pass",
        "source_root": str(resolved_source),
        "mirror_root": str(resolved_mirror),
        "copied_file_count": file_count,
    }, 0
