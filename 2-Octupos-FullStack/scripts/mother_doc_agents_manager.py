from __future__ import annotations

import json
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from agents_target_runtime import (
    DEFAULT_WORKSPACE_ROOT,
    ROOT_RELATIVE_PATH,
    build_default_machine_payload,
    extract_external_agents_part_a_body,
    extract_internal_part_a,
    managed_human_path,
    managed_machine_path,
    registry_path,
    render_external_agents,
    render_internal_agents_human,
    root_source_path,
)


SCAN_REPORT_RELATIVE_PATH = Path("assets/mother_doc_agents/scan_report.json")
INDEX_RELATIVE_PATH = Path("assets/mother_doc_agents/index.md")
LOCK_RELATIVE_PATH = Path("runtime/locks/mother_doc_agents.lock")
MANAGED_TARGET_NAME = "Octopus_OS"


def resolve_skill_root(raw_root: str | None) -> Path:
    if raw_root:
        return Path(raw_root).expanduser().resolve()
    return Path(__file__).resolve().parent.parent


def scan_report_path(skill_root: Path) -> Path:
    return skill_root / SCAN_REPORT_RELATIVE_PATH


def index_path(skill_root: Path) -> Path:
    return skill_root / INDEX_RELATIVE_PATH


def lock_path(skill_root: Path) -> Path:
    return skill_root / LOCK_RELATIVE_PATH


def legacy_asset_roots(skill_root: Path) -> list[Path]:
    base = skill_root / "assets" / "mother_doc_agents"
    return [
        base / "runtime_rules",
        base / "templates",
        base / "collected_tree",
    ]


def _infer_workspace_root(document_root: Path | None) -> Path:
    if document_root is None:
        return DEFAULT_WORKSPACE_ROOT
    resolved = document_root.resolve()
    if resolved.name == "docs" and resolved.parent.name == "Mother_Doc":
        return resolved.parent.parent
    return DEFAULT_WORKSPACE_ROOT


def _resolve_workspace_root(skill_root: Path) -> Path:
    scan_path = scan_report_path(skill_root)
    if scan_path.exists():
        payload = _load_json(scan_path)
        raw_workspace_root = payload.get("workspace_root")
        if isinstance(raw_workspace_root, str):
            return Path(raw_workspace_root)
    reg_path = registry_path(skill_root)
    if reg_path.exists():
        payload = _load_json(reg_path)
        entries = payload.get("entries")
        if isinstance(entries, list) and entries:
            source_path = entries[0].get("source_path")
            if isinstance(source_path, str):
                return Path(source_path).parent
    sibling = skill_root.parent / "Octopus_OS"
    if (sibling / "AGENTS.md").exists():
        return sibling
    return DEFAULT_WORKSPACE_ROOT


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


def _list_external_agents(workspace_root: Path) -> list[Path]:
    return sorted(workspace_root.rglob("AGENTS.md"))


def _list_extra_agents(workspace_root: Path) -> list[Path]:
    root_path = root_source_path(workspace_root)
    return [path for path in _list_external_agents(workspace_root) if path != root_path]


def _registry_entry(skill_root: Path, workspace_root: Path) -> dict[str, object]:
    return {
        "target_name": MANAGED_TARGET_NAME,
        "relative_path": ROOT_RELATIVE_PATH,
        "source_path": str(root_source_path(workspace_root)),
        "managed_human_path": str(managed_human_path(skill_root)),
        "managed_machine_path": str(managed_machine_path(skill_root)),
        "governance_mode": "root_only_payload_managed",
        "payload_navigation": {
            "target_contract_command": (
                "python3 scripts/Cli_Toolbox.py mother-doc-agents-target-contract "
                '--relative-path "octopus_os_root" --file-kind agents --json'
            ),
            "branch_registry_command": "python3 scripts/Cli_Toolbox.py mother-doc-agents-registry --json",
        },
    }


def _registry_payload(skill_root: Path, workspace_root: Path) -> dict[str, object]:
    entry = _registry_entry(skill_root, workspace_root)
    return {
        "schema_version": "2.0",
        "branch_name": "mother_doc_agents_manager",
        "machine_index_semantics": "registry_json_is_primary_machine_index",
        "human_index_role": "index_md_is_human_audit_only",
        "entries": [entry],
    }


def _index_markdown(skill_root: Path, workspace_root: Path) -> str:
    entry = _registry_entry(skill_root, workspace_root)
    return "\n".join(
        [
            "# Mother_Doc AGENTS Branch Index",
            "",
            "- 分支目标：仅治理一个外部 AGENTS 目标，即 `Octopus_OS/AGENTS.md`。",
            "- 机器主索引：`assets/mother_doc_agents/registry.json`。",
            "- 人类审计索引：本文件只用于阅读，不作为模型运行时主源。",
            "",
            "## Managed Target",
            f"- `relative_path`: `{entry['relative_path']}`",
            f"- `source_path`: `{entry['source_path']}`",
            f"- `managed_human_path`: `{entry['managed_human_path']}`",
            f"- `managed_machine_path`: `{entry['managed_machine_path']}`",
            "- 外部形态：仅保留 `Part A`。",
            "- 内部形态：`AGENTS_human.md` 为 `Part A + Part B`，`AGENTS_machine.json` 为 `Part B only`。",
            "",
        ]
    ) + "\n"


def _default_part_a_body() -> str:
    return "\n".join(
        [
            "1. 当前唯一受管外部 AGENTS 目标",
            "- `Octopus_OS/AGENTS.md` 是当前唯一允许存在的外部 AGENTS runtime entry。",
            "",
            "2. 运行时主源",
            "- 模型运行时以 CLI 返回的 JSON payload 为主源。",
            "- markdown 只作为人类可读审计或写作载体，不是第一运行时规则源。",
            "",
            "3. 清理要求",
            "- `Octopus_OS` 其他目录下不得继续保留额外 `AGENTS.md`。",
            "- 若需要扩展治理范围，应先在 mirror 的 managed payload 中定义，再由统一 push 写回。",
            "",
            "4. 当前阶段说明",
            "- 当前处于 root-only bootstrap 阶段，后续由用户继续设计根 `AGENTS.md` 的 payload 内容。",
        ]
    )


def _root_part_a_body(workspace_root: Path) -> str:
    source = root_source_path(workspace_root)
    if source.exists():
        return extract_external_agents_part_a_body(source.read_text(encoding="utf-8"))
    return _default_part_a_body()


def _persist_registry(skill_root: Path, workspace_root: Path) -> None:
    _write_json(registry_path(skill_root), _registry_payload(skill_root, workspace_root))
    _write_text(index_path(skill_root), _index_markdown(skill_root, workspace_root))


def _delete_path(path: Path) -> None:
    if not path.exists():
        return
    if path.is_dir():
        for child in sorted(path.iterdir()):
            _delete_path(child)
        path.rmdir()
        return
    path.unlink()


def _delete_legacy_assets(skill_root: Path) -> list[str]:
    deleted: list[str] = []
    for legacy_path in legacy_asset_roots(skill_root):
        if legacy_path.exists():
            deleted.append(str(legacy_path))
            _delete_path(legacy_path)
    return deleted


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
    payload["registry_path"] = str(registry_path(skill_root))
    payload["index_path"] = str(index_path(skill_root))
    payload["scan_report_path"] = str(scan_report_path(skill_root))
    return payload


def load_stage_directive(skill_root: Path, stage: str) -> dict[str, object]:
    payload = _load_json(
        skill_root / "references" / "mother_doc" / "agents_branch" / "stages" / stage / "DIRECTIVE.json"
    )
    payload["skill_root"] = str(skill_root)
    return payload


def load_registry(skill_root: Path) -> dict[str, object]:
    path = registry_path(skill_root)
    if not path.exists():
        return _registry_payload(skill_root, _resolve_workspace_root(skill_root))
    return _load_json(path)


def scan_agents_tree(skill_root: Path, document_root: Path) -> dict[str, object]:
    workspace_root = _infer_workspace_root(document_root)
    root_path = root_source_path(workspace_root)
    extra_agents = _list_extra_agents(workspace_root)
    payload = {
        "schema_version": "2.0",
        "workspace_root": str(workspace_root),
        "managed_external_targets": [str(root_path)],
        "root_agents_exists": root_path.exists(),
        "extra_agents": [str(path) for path in extra_agents],
        "legacy_asset_paths": [str(path) for path in legacy_asset_roots(skill_root) if path.exists()],
        "registry_path": str(registry_path(skill_root)),
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
        else build_default_machine_payload()
    )
    part_a_body = _root_part_a_body(workspace_root)
    _write_json(managed_machine_path(skill_root), machine_payload)
    _write_text(
        managed_human_path(skill_root),
        render_internal_agents_human(part_a_body, machine_payload),
    )
    _persist_registry(skill_root, workspace_root)
    return {
        "schema_version": "2.0",
        "workspace_root": str(workspace_root),
        "source_path": str(root_source_path(workspace_root)),
        "managed_human_path": str(managed_human_path(skill_root)),
        "managed_machine_path": str(managed_machine_path(skill_root)),
        "registry_path": str(registry_path(skill_root)),
        "index_path": str(index_path(skill_root)),
        "scan_summary": scan_payload,
    }


def push_agents_tree(skill_root: Path, document_root: Path, *, dry_run: bool) -> dict[str, object]:
    workspace_root = _infer_workspace_root(document_root)
    human_path = managed_human_path(skill_root)
    machine_path = managed_machine_path(skill_root)
    if not human_path.exists() and not dry_run:
        collect_from_scan(skill_root)
    part_a_text = (
        extract_internal_part_a(human_path.read_text(encoding="utf-8"))
        if human_path.exists()
        else render_external_agents(_default_part_a_body())
    )
    part_a_body = extract_external_agents_part_a_body(part_a_text)
    target_path = root_source_path(workspace_root)
    extra_agents = _list_extra_agents(workspace_root)
    deleted_legacy_assets = [str(path) for path in legacy_asset_roots(skill_root) if path.exists()]
    payload = {
        "schema_version": "2.0",
        "workspace_root": str(workspace_root),
        "pushed_root_agents": str(target_path),
        "deleted_external_agents": [str(path) for path in extra_agents],
        "deleted_legacy_assets": deleted_legacy_assets,
        "managed_human_path": str(human_path),
        "managed_machine_path": str(machine_path),
        "dry_run": dry_run,
    }
    if dry_run:
        return payload

    _write_text(target_path, render_external_agents(part_a_body))
    for extra_path in extra_agents:
        _delete_path(extra_path)
    payload["deleted_legacy_assets"] = _delete_legacy_assets(skill_root)
    refreshed = collect_from_scan(skill_root)
    payload["post_push_collect"] = refreshed
    return payload
