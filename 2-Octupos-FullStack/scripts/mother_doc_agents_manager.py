from __future__ import annotations

import json
import shutil
from contextlib import contextmanager
from pathlib import Path

from mother_doc_navigation import AGENTS_FILENAME, sync_navigation_tree


ASSET_SUBDIR = Path("assets/mother_doc_agents")
RUNTIME_CONTRACT_REL = Path("references/mother_doc/agents_branch/runtime/AGENTS_BRANCH_CONTRACT.json")
DIRECTIVE_REL_ROOT = Path("references/mother_doc/agents_branch/stages")


def resolve_skill_root(raw_root: str | None) -> Path:
    if raw_root:
        return Path(raw_root).resolve()
    return Path(__file__).resolve().parent.parent


def asset_paths(skill_root: Path) -> dict[str, Path]:
    asset_root = skill_root / ASSET_SUBDIR
    return {
        "asset_root": asset_root,
        "lock_path": asset_root / ".cli.lock",
        "index_path": asset_root / "index.md",
        "registry_path": asset_root / "registry.json",
        "scan_report_path": asset_root / "scan_report.json",
        "collected_root": asset_root / "collected_tree",
    }


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_runtime_contract(skill_root: Path) -> dict[str, object]:
    payload = _load_json(skill_root / RUNTIME_CONTRACT_REL)
    payload["skill_root"] = str(skill_root)
    return payload


def load_stage_directive(skill_root: Path, stage: str) -> dict[str, object]:
    payload = _load_json(skill_root / DIRECTIVE_REL_ROOT / stage / "DIRECTIVE.json")
    payload["skill_root"] = str(skill_root)
    return payload


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _clear_tree(target: Path) -> None:
    if not target.exists():
        return
    for path in sorted(target.rglob("*"), key=lambda item: (len(item.parts), str(item)), reverse=True):
        if path.is_file() or path.is_symlink():
            path.unlink()
        elif path.is_dir():
            path.rmdir()
    if target.exists():
        target.rmdir()


@contextmanager
def acquire_cli_lock(skill_root: Path, stage: str):
    paths = asset_paths(skill_root)
    lock_path = paths["lock_path"]
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    if lock_path.exists():
        raise RuntimeError(f"mother_doc_agents lock already held: {lock_path}")
    lock_path.write_text(stage + "\n", encoding="utf-8")
    try:
        yield
    finally:
        if lock_path.exists():
            lock_path.unlink()


def _iter_managed_dirs(document_root: Path) -> list[Path]:
    dirs = sorted([document_root, *[path for path in document_root.rglob("*") if path.is_dir()]])
    return dirs


def scan_agents_tree(skill_root: Path, document_root: Path) -> dict[str, object]:
    entries: list[dict[str, object]] = []
    missing_agents_dirs: list[str] = []
    legacy_agents: list[str] = []
    for directory in _iter_managed_dirs(document_root):
        rel_dir = directory.relative_to(document_root)
        agents_path = directory / AGENTS_FILENAME
        legacy_path = directory / LEGACY_AGENTS_FILENAME
        scope_doc = directory / ("Mother_Doc.md" if directory == document_root else f"{directory.name}.md")
        if legacy_path.exists():
            legacy_agents.append(str(legacy_path))
        if not agents_path.exists():
            missing_agents_dirs.append(str(rel_dir) if rel_dir.parts else ".")
            continue
        entries.append(
            {
                "relative_dir": "." if not rel_dir.parts else str(rel_dir),
                "relative_path": str(agents_path.relative_to(document_root)),
                "agents_path": str(agents_path),
                "readme_present": (directory / "README.md").exists(),
                "scope_doc_present": scope_doc.exists(),
                "child_entry_count": len(
                    [
                        child
                        for child in directory.iterdir()
                        if child.name not in {"README.md", AGENTS_FILENAME, LEGACY_AGENTS_FILENAME, "__pycache__"}
                    ]
                ),
            }
        )

    payload = {
        "branch": "mother_doc_agents",
        "document_root": str(document_root),
        "managed_filename": AGENTS_FILENAME,
        "entry_count": len(entries),
        "entries": entries,
        "missing_agents_dirs": missing_agents_dirs,
        "legacy_agents": legacy_agents,
    }
    _write_json(asset_paths(skill_root)["scan_report_path"], payload)
    return payload


def collect_from_scan(skill_root: Path) -> dict[str, object]:
    paths = asset_paths(skill_root)
    scan_report_path = paths["scan_report_path"]
    if not scan_report_path.exists():
        raise RuntimeError("scan_report.json missing; run mother-doc-agents-scan first")
    scan_report = _load_json(scan_report_path)
    entries = scan_report.get("entries", [])
    if not isinstance(entries, list) or not entries:
        raise RuntimeError("scan_report.json contains no entries; run mother-doc-agents-scan on a populated Mother_Doc tree")

    collected_root = paths["collected_root"]
    _clear_tree(collected_root)
    collected_entries: list[dict[str, str]] = []
    index_lines = [
        "# Mother_Doc AGENTS Registry",
        "",
        "- This asset tree stores collected `AGENTS.md` snapshots from `Octopus_OS/Mother_Doc/docs/**`.",
        "- Use `scan` to discover managed AGENTS paths.",
        "- Use `collect` to pull current AGENTS files back into the skill-side managed registry.",
        "- Use `push` to regenerate AGENTS files from the skill-side template and sync the tree again.",
        "",
        "## Entries",
        "",
    ]

    for entry in entries:
        source_path = Path(str(entry["agents_path"]))
        rel_path = Path(str(entry["relative_path"]))
        target_path = collected_root / rel_path
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, target_path)
        collected_entries.append(
            {
                "relative_path": str(rel_path),
                "source_path": str(source_path),
                "collected_path": str(target_path),
            }
        )
        index_lines.append(f"- `{rel_path}`: collected snapshot for `{source_path.parent.name}`.")

    registry_payload = {
        "branch": "mother_doc_agents",
        "managed_filename": AGENTS_FILENAME,
        "entry_count": len(collected_entries),
        "entries": collected_entries,
    }
    _write_json(paths["registry_path"], registry_payload)
    _write_text(paths["index_path"], "\n".join(index_lines) + "\n")
    return {
        "registry_path": str(paths["registry_path"]),
        "index_path": str(paths["index_path"]),
        "collected_root": str(collected_root),
        "entry_count": len(collected_entries),
        "entries": collected_entries,
    }


def load_registry(skill_root: Path) -> dict[str, object]:
    registry_path = asset_paths(skill_root)["registry_path"]
    if not registry_path.exists():
        return {
            "branch": "mother_doc_agents",
            "managed_filename": AGENTS_FILENAME,
            "entry_count": 0,
            "entries": [],
        }
    return _load_json(registry_path)


def push_agents_tree(skill_root: Path, document_root: Path, *, dry_run: bool) -> dict[str, object]:
    navigation_sync = sync_navigation_tree(document_root, dry_run=dry_run)
    if dry_run:
        return {
            "document_root": str(document_root),
            "navigation_sync": navigation_sync,
            "scan": {
                "skipped": True,
                "reason": "dry_run",
            },
            "collect": {
                "skipped": True,
                "reason": "dry_run",
            },
        }
    scan_payload = scan_agents_tree(skill_root, document_root)
    collect_payload = collect_from_scan(skill_root)
    return {
        "document_root": str(document_root),
        "navigation_sync": navigation_sync,
        "scan": scan_payload,
        "collect": collect_payload,
    }
LEGACY_AGENTS_FILENAME = "agents.md"
