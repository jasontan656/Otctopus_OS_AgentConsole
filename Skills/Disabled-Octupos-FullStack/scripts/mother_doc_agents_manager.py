from __future__ import annotations

import json
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from agents_target_runtime import (
    DEFAULT_WORKSPACE_ROOT,
    build_default_machine_contract,
    extract_external_agents_part_a_body,
    extract_internal_part_a,
    managed_human_path,
    managed_machine_path,
    render_external_agents,
    render_internal_agents_human,
    root_source_path,
)


SCAN_REPORT_RELATIVE_PATH = Path("assets/mother_doc_agents/scan_report.json")
LOCK_RELATIVE_PATH = Path("runtime/locks/mother_doc_agents.lock")


def resolve_skill_root(raw_root: str | None) -> Path:
    if raw_root:
        return Path(raw_root).expanduser().resolve()
    return Path(__file__).resolve().parent.parent


def scan_report_path(skill_root: Path) -> Path:
    return skill_root / SCAN_REPORT_RELATIVE_PATH


def lock_path(skill_root: Path) -> Path:
    return skill_root / LOCK_RELATIVE_PATH


def obsolete_branch_paths(skill_root: Path) -> list[Path]:
    base = skill_root / "assets" / "mother_doc_agents"
    return [
        base / "index.md",
        base / "registry.json",
        base / "runtime_rules",
        base / "templates",
        base / "collected_tree",
    ]


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, object]) -> None:
    _ensure_parent(path)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_text(path: Path, content: str) -> None:
    _ensure_parent(path)
    path.write_text(content, encoding="utf-8")


def _infer_workspace_root(document_root: Path | None) -> Path:
    if document_root is None:
        return DEFAULT_WORKSPACE_ROOT
    resolved = document_root.resolve()
    if resolved.name == "docs" and resolved.parent.name == "Mother_Doc":
        return resolved.parent.parent
    return DEFAULT_WORKSPACE_ROOT


def _resolve_workspace_root(skill_root: Path) -> Path:
    report = scan_report_path(skill_root)
    if report.exists():
        payload = _load_json(report)
        raw_workspace_root = payload.get("workspace_root")
        if isinstance(raw_workspace_root, str):
            return Path(raw_workspace_root)
    sibling = skill_root.parent / "Octopus_OS"
    if (sibling / "AGENTS.md").exists():
        return sibling
    return DEFAULT_WORKSPACE_ROOT


def _delete_path(path: Path) -> None:
    if not path.exists():
        return
    if path.is_dir():
        for child in sorted(path.iterdir()):
            _delete_path(child)
        path.rmdir()
        return
    path.unlink()


def _cleanup_obsolete_branch_assets(skill_root: Path) -> list[str]:
    deleted: list[str] = []
    for path in obsolete_branch_paths(skill_root):
        if path.exists():
            deleted.append(str(path))
            _delete_path(path)
    return deleted


def _list_external_agents(workspace_root: Path) -> list[Path]:
    return sorted(workspace_root.rglob("AGENTS.md"))


def _list_extra_agents(workspace_root: Path) -> list[Path]:
    root_path = root_source_path(workspace_root)
    return [path for path in _list_external_agents(workspace_root) if path != root_path]


def _default_part_a_body() -> str:
    return "\n".join(
        [
            "1. 当前唯一受管外部 AGENTS 目标",
            "- `Octopus_OS/AGENTS.md` 是当前唯一允许存在的外部 AGENTS runtime entry。",
            "",
            "2. 运行时主源",
            "- 模型运行时以 CLI 返回的 JSON payload 为主源。",
            "- markdown 只作为写作载体，不作为分支索引或 README 治理层。",
            "",
            "3. 清理要求",
            "- `Octopus_OS` 其他目录下不得继续保留额外 `AGENTS.md`。",
            "",
            "4. 当前阶段说明",
            "- 当前只收敛这一个外部 AGENTS 目标，后续只继续设计它本身的内容。",
        ]
    )


def _root_part_a_body(workspace_root: Path) -> str:
    source = root_source_path(workspace_root)
    if source.exists():
        return extract_external_agents_part_a_body(source.read_text(encoding="utf-8"))
    return _default_part_a_body()


@contextmanager
def acquire_cli_lock(skill_root: Path, operation: str) -> Iterator[None]:
    path = lock_path(skill_root)
    _ensure_parent(path)
    path.write_text(operation + "\n", encoding="utf-8")
    try:
        yield
    finally:
        if path.exists():
            path.unlink()


def load_runtime_contract(skill_root: Path) -> dict[str, object]:
    payload = _load_json(
        skill_root / "references" / "mother_doc" / "agents_branch" / "runtime" / "AGENTS_BRANCH_CONTRACT.json"
    )
    payload["skill_root"] = str(skill_root)
    payload["scan_report_path"] = str(scan_report_path(skill_root))
    payload["managed_human_path"] = str(managed_human_path(skill_root))
    payload["managed_machine_path"] = str(managed_machine_path(skill_root))
    return payload


def load_stage_directive(skill_root: Path, stage: str) -> dict[str, object]:
    payload = _load_json(
        skill_root / "references" / "mother_doc" / "agents_branch" / "stages" / stage / "DIRECTIVE.json"
    )
    payload["skill_root"] = str(skill_root)
    return payload


def scan_agents_tree(skill_root: Path, document_root: Path) -> dict[str, object]:
    workspace_root = _infer_workspace_root(document_root)
    root_path = root_source_path(workspace_root)
    payload = {
        "schema_version": "3.0",
        "workspace_root": str(workspace_root),
        "managed_external_target": str(root_path),
        "root_agents_exists": root_path.exists(),
        "extra_agents": [str(path) for path in _list_extra_agents(workspace_root)],
        "obsolete_branch_assets": [str(path) for path in obsolete_branch_paths(skill_root) if path.exists()],
        "scan_report_path": str(scan_report_path(skill_root)),
    }
    _write_json(scan_report_path(skill_root), payload)
    return payload


def collect_from_scan(skill_root: Path) -> dict[str, object]:
    workspace_root = _resolve_workspace_root(skill_root)
    scan_payload = scan_agents_tree(skill_root, workspace_root / "Mother_Doc" / "docs")
    machine_payload = (
        _load_json(managed_machine_path(skill_root))
        if managed_machine_path(skill_root).exists()
        else build_default_machine_contract()
    )
    _write_json(managed_machine_path(skill_root), machine_payload)
    _write_text(
        managed_human_path(skill_root),
        render_internal_agents_human(_root_part_a_body(workspace_root), machine_payload),
    )
    deleted_assets = _cleanup_obsolete_branch_assets(skill_root)
    return {
        "schema_version": "3.0",
        "workspace_root": str(workspace_root),
        "source_path": str(root_source_path(workspace_root)),
        "managed_human_path": str(managed_human_path(skill_root)),
        "managed_machine_path": str(managed_machine_path(skill_root)),
        "removed_governance_assets": deleted_assets,
        "scan_summary": scan_payload,
    }


def push_agents_tree(skill_root: Path, document_root: Path, *, dry_run: bool) -> dict[str, object]:
    workspace_root = _infer_workspace_root(document_root)
    human_path = managed_human_path(skill_root)
    if not human_path.exists() and not dry_run:
        collect_from_scan(skill_root)

    if human_path.exists():
        part_a_body = extract_external_agents_part_a_body(extract_internal_part_a(human_path.read_text(encoding="utf-8")))
    else:
        part_a_body = _default_part_a_body()

    target_path = root_source_path(workspace_root)
    extra_agents = _list_extra_agents(workspace_root)
    obsolete_assets = [str(path) for path in obsolete_branch_paths(skill_root) if path.exists()]
    payload = {
        "schema_version": "3.0",
        "workspace_root": str(workspace_root),
        "pushed_root_agents": str(target_path),
        "deleted_external_agents": [str(path) for path in extra_agents],
        "removed_governance_assets": obsolete_assets,
        "managed_human_path": str(human_path),
        "managed_machine_path": str(managed_machine_path(skill_root)),
        "dry_run": dry_run,
    }
    if dry_run:
        return payload

    _write_text(target_path, render_external_agents(part_a_body))
    for path in extra_agents:
        _delete_path(path)
    payload["removed_governance_assets"] = _cleanup_obsolete_branch_assets(skill_root)
    payload["post_push_collect"] = collect_from_scan(skill_root)
    return payload
