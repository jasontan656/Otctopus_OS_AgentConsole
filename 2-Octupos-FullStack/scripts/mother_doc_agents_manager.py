from __future__ import annotations

import json
import shutil
from contextlib import contextmanager
from pathlib import Path

from mother_doc_navigation import AGENTS_FILENAME, LEGACY_AGENTS_FILENAME, sync_navigation_tree


ASSET_SUBDIR = Path("assets/mother_doc_agents")
RUNTIME_CONTRACT_REL = Path("references/mother_doc/agents_branch/runtime/AGENTS_BRANCH_CONTRACT.json")
DIRECTIVE_REL_ROOT = Path("references/mother_doc/agents_branch/stages")
ROOT_BRANCH = "octopus_os_root"
CONTAINER_BRANCH = "container_roots"
DOCS_BRANCH = "mother_doc_docs"

CONTAINER_DESCRIPTIONS = {
    "User_UI": "user-facing client container",
    "Admin_UI": "admin-facing client container and future operator surface",
    "API_Gateway": "unified ingress container for routing, auth forwarding, and traffic control",
    "Mother_Doc": "authoritative authored-document and OS_graph container",
    "Identity_Service": "identity and auth domain container",
    "Account_Service": "account and profile domain container",
    "Order_Service": "order domain container",
    "Payment_Service": "payment domain container",
    "Notification_Service": "notification domain container",
    "File_Service": "file domain container",
    "AI_Service": "AI domain container",
    "Postgres_DB": "relational database container",
    "Redis_Cache": "cache container",
    "MQ_Broker": "message broker container",
    "Object_Storage": "object storage container",
}


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
        "template_root": asset_root / "templates",
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


def _workspace_root_from_document_root(document_root: Path) -> Path:
    return document_root.parent.parent


def _container_dirs(workspace_root: Path) -> list[Path]:
    return sorted(
        [
            path
            for path in workspace_root.iterdir()
            if path.is_dir() and not path.name.startswith(".") and path.name != "__pycache__"
        ],
        key=lambda item: item.name.lower(),
    )


def _container_description(name: str) -> str:
    return CONTAINER_DESCRIPTIONS.get(name, f"`{name}` container scope")


def _root_template_relative() -> Path:
    return Path(ROOT_BRANCH) / AGENTS_FILENAME


def _container_template_relative(container_name: str) -> Path:
    return Path(CONTAINER_BRANCH) / container_name / AGENTS_FILENAME


def _docs_template_relative(target_path: Path, document_root: Path) -> Path:
    return Path(DOCS_BRANCH) / target_path.relative_to(document_root)


def build_octopus_root_agents(workspace_root: Path) -> str:
    lines = [
        "# AGENTS",
        "",
        "## 1. 目标",
        "- 当前层作用：`Octopus_OS` 总容器根，承载所有独立容器的总入口。",
        "- 先读 `README.md` 理解整体架构，再决定进入哪个容器。",
        "",
        "## 2. 同层入口",
        "- `README.md`: `Octopus_OS` 总介绍与当前顶层容器布局说明。",
        "",
        "## 3. 下一层入口",
    ]
    for container in _container_dirs(workspace_root):
        lines.append(f"- `{container.name}/`: {_container_description(container.name)}。")
    lines.extend(
        [
            "",
            "## 4. 选择规则",
            "- 先读当前层 `README.md`，确认目标容器或目标系统边界。",
            "- 只在用户需求命中该容器时进入对应容器路径，不跨到无关容器。",
            "",
            "## 5. 更新边界",
            "- 当前层只承担容器总索引，不承载各容器正文细节。",
            "- 各容器的说明、文档和后续索引必须在各容器自己的路径中维护。",
            "",
            "## 6. 索引契约",
            "- 当前根层 `AGENTS.md` 属于 `octopus_os_root` 分支。",
            "- 它必须固定指向 `README.md` 和所有当前顶层容器路径。",
            "",
            "## 7. 递归动作",
            "- 命中目标容器后，进入对应容器路径继续读取容器级 `AGENTS.md` 或 `README.md`。",
            "- 若目标属于文档树，再转入 `Mother_Doc/docs/**` 的递归索引链。",
            "",
        ]
    )
    return "\n".join(lines)


def build_container_root_agents(container_root: Path, document_root: Path) -> str:
    container_name = container_root.name
    doc_scope = document_root / container_name
    lines = [
        "# AGENTS",
        "",
        "## 1. 目标",
        f"- 当前层作用：`{container_name}` 容器根入口。",
        "- 先读 `README.md` 获取当前容器用途，再决定进入代码、文档或其他子路径。",
        "",
        "## 2. 同层入口",
        "- `README.md`: 当前容器用途说明。",
    ]
    if doc_scope.exists():
        lines.append(f"- `../Mother_Doc/docs/{container_name}/README.md`: 当前容器对应的 authored-doc 根说明。")
    lines.extend(
        [
            "",
            "## 3. 下一层入口",
        ]
    )
    children = sorted(
        [
            child
            for child in container_root.iterdir()
            if child.name not in {"README.md", AGENTS_FILENAME, LEGACY_AGENTS_FILENAME, "__pycache__"} and not child.name.startswith(".")
        ],
        key=lambda item: (item.is_file(), item.name.lower()),
    )
    if container_name == "Mother_Doc":
        lines.append("- `docs/`: Mother_Doc authored-doc 树根。")
        lines.append("- `graph/`: OS_graph 资产根。")
    elif doc_scope.exists():
        lines.append(f"- `../Mother_Doc/docs/{container_name}/`: 当前容器对应的文档树入口。")
    if children:
        for child in children:
            suffix = "/" if child.is_dir() else ""
            lines.append(f"- `{child.name}{suffix}`: 当前容器下的直接子路径。")
    if not children and container_name != "Mother_Doc" and not doc_scope.exists():
        lines.append("- `terminal`: 当前容器根尚无更深入口。")
    lines.extend(
        [
            "",
            "## 4. 选择规则",
            "- 先读当前层 `README.md`。",
            "- 若任务是文档设计、需求回写或结构浏览，优先转入对应的 `Mother_Doc/docs` 路径。",
            "- 若任务是容器根层结构或后续代码落点，再留在当前容器路径继续处理。",
            "",
            "## 5. 更新边界",
            "- 当前层只负责容器根入口，不替代容器内部正文。",
            "- 文档正文仍由 `Mother_Doc/docs` 承载，graph 资产由 `Mother_Doc/graph` 承载。",
            "",
            "## 6. 索引契约",
            "- 当前文件属于 `container_roots` 分支。",
            "- 每个顶层容器都必须有自己的容器根 `AGENTS.md` 模板与推送路径。",
            "",
            "## 7. 递归动作",
            "- 命中文档域时，进入对应 `Mother_Doc/docs` 容器路径。",
            "- 命中当前容器实际子路径时，继续进入对应子目录处理。",
            "",
        ]
    )
    return "\n".join(lines)


def _iter_managed_doc_dirs(document_root: Path) -> list[Path]:
    return sorted([document_root, *[path for path in document_root.rglob("*") if path.is_dir()]])


def _scan_entry(
    *,
    branch: str,
    target_path: Path,
    registry_key: Path,
    template_relative: Path,
    readme_present: bool,
    child_entry_count: int,
) -> dict[str, object]:
    return {
        "scope_branch": branch,
        "registry_key": str(registry_key),
        "relative_path": str(registry_key),
        "target_path": str(target_path),
        "template_relative_path": str(template_relative),
        "readme_present": readme_present,
        "child_entry_count": child_entry_count,
    }


def scan_agents_tree(skill_root: Path, document_root: Path) -> dict[str, object]:
    workspace_root = _workspace_root_from_document_root(document_root)
    entries: list[dict[str, object]] = []
    missing_agents: list[str] = []
    legacy_agents: list[str] = []

    root_agents = workspace_root / AGENTS_FILENAME
    if root_agents.exists():
        entries.append(
            _scan_entry(
                branch=ROOT_BRANCH,
                target_path=root_agents,
                registry_key=_root_template_relative(),
                template_relative=_root_template_relative(),
                readme_present=(workspace_root / "README.md").exists(),
                child_entry_count=len(_container_dirs(workspace_root)),
            )
        )
    else:
        missing_agents.append(str(root_agents))

    for container_root in _container_dirs(workspace_root):
        agents_path = container_root / AGENTS_FILENAME
        if agents_path.exists():
            children = [
                child
                for child in container_root.iterdir()
                if child.name not in {"README.md", AGENTS_FILENAME, LEGACY_AGENTS_FILENAME, "__pycache__"} and not child.name.startswith(".")
            ]
            entries.append(
                _scan_entry(
                    branch=CONTAINER_BRANCH,
                    target_path=agents_path,
                    registry_key=_container_template_relative(container_root.name),
                    template_relative=_container_template_relative(container_root.name),
                    readme_present=(container_root / "README.md").exists(),
                    child_entry_count=len(children),
                )
            )
        else:
            missing_agents.append(str(agents_path))

    for directory in _iter_managed_doc_dirs(document_root):
        rel_dir = directory.relative_to(document_root)
        agents_path = directory / AGENTS_FILENAME
        legacy_path = directory / LEGACY_AGENTS_FILENAME
        scope_doc = directory / ("Mother_Doc.md" if directory == document_root else f"{directory.name}.md")
        if legacy_path.exists():
            legacy_agents.append(str(legacy_path))
        if not agents_path.exists():
            missing_agents.append(str(agents_path))
            continue
        children = [
            child
            for child in directory.iterdir()
            if child.name not in {"README.md", AGENTS_FILENAME, LEGACY_AGENTS_FILENAME, scope_doc.name, "__pycache__"} and not child.name.startswith(".")
        ]
        registry_key = _docs_template_relative(agents_path, document_root)
        entries.append(
            _scan_entry(
                branch=DOCS_BRANCH,
                target_path=agents_path,
                registry_key=registry_key,
                template_relative=registry_key,
                readme_present=(directory / "README.md").exists(),
                child_entry_count=len(children),
            )
        )

    payload = {
        "branch": "mother_doc_agents",
        "managed_scopes": [ROOT_BRANCH, CONTAINER_BRANCH, DOCS_BRANCH],
        "entry_count": len(entries),
        "entries": entries,
        "missing_agents": missing_agents,
        "legacy_agents": legacy_agents,
        "workspace_root": str(workspace_root),
        "document_root": str(document_root),
        "managed_filename": AGENTS_FILENAME,
    }
    _write_json(asset_paths(skill_root)["scan_report_path"], payload)
    return payload


def _sync_template_tree(skill_root: Path, workspace_root: Path, document_root: Path) -> list[str]:
    paths = asset_paths(skill_root)
    template_root = paths["template_root"]
    _clear_tree(template_root)
    created: list[str] = []

    root_template = template_root / _root_template_relative()
    _write_text(root_template, build_octopus_root_agents(workspace_root))
    created.append(str(root_template))

    for container_root in _container_dirs(workspace_root):
        template_path = template_root / _container_template_relative(container_root.name)
        _write_text(template_path, build_container_root_agents(container_root, document_root))
        created.append(str(template_path))

    for directory in _iter_managed_doc_dirs(document_root):
        agents_path = directory / AGENTS_FILENAME
        template_path = template_root / _docs_template_relative(agents_path, document_root)
        _write_text(template_path, agents_path.read_text(encoding="utf-8"))
        created.append(str(template_path))

    return created


def _push_root_and_container_agents(workspace_root: Path, document_root: Path, *, dry_run: bool) -> list[str]:
    updated: list[str] = []
    root_agents = workspace_root / AGENTS_FILENAME
    updated.append(str(root_agents))
    if not dry_run:
        root_agents.write_text(build_octopus_root_agents(workspace_root), encoding="utf-8")

    for container_root in _container_dirs(workspace_root):
        agents_path = container_root / AGENTS_FILENAME
        updated.append(str(agents_path))
        if not dry_run:
            agents_path.write_text(build_container_root_agents(container_root, document_root), encoding="utf-8")
    return updated


def collect_from_scan(skill_root: Path) -> dict[str, object]:
    paths = asset_paths(skill_root)
    scan_report_path = paths["scan_report_path"]
    if not scan_report_path.exists():
        raise RuntimeError("scan_report.json missing; run mother-doc-agents-scan first")
    scan_report = _load_json(scan_report_path)
    entries = scan_report.get("entries", [])
    if not isinstance(entries, list) or not entries:
        raise RuntimeError("scan_report.json contains no entries; run mother-doc-agents-scan on a populated managed tree")

    collected_root = paths["collected_root"]
    _clear_tree(collected_root)
    collected_entries: list[dict[str, str]] = []
    index_lines = [
        "# Mother_Doc AGENTS Registry",
        "",
        "- This asset tree stores managed AGENTS templates and collected snapshots.",
        "- Managed branches: `octopus_os_root`, `container_roots`, `mother_doc_docs`.",
        "",
        "## Template Targets",
        "",
    ]

    for entry in entries:
        template_relative = Path(str(entry["template_relative_path"]))
        target_path = str(entry["target_path"])
        index_lines.append(f"- `{template_relative}` -> `{target_path}`")

    index_lines.extend(["", "## Collected Snapshots", ""])

    for entry in entries:
        source_path = Path(str(entry["target_path"]))
        rel_path = Path(str(entry["registry_key"]))
        target_path = collected_root / rel_path
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, target_path)
        collected_entries.append(
            {
                "scope_branch": str(entry["scope_branch"]),
                "relative_path": str(rel_path),
                "source_path": str(source_path),
                "collected_path": str(target_path),
                "template_relative_path": str(entry["template_relative_path"]),
            }
        )
        index_lines.append(f"- `{rel_path}`: collected snapshot for `{source_path}`.")

    registry_payload = {
        "branch": "mother_doc_agents",
        "managed_scopes": [ROOT_BRANCH, CONTAINER_BRANCH, DOCS_BRANCH],
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
        "template_root": str(paths["template_root"]),
        "entry_count": len(collected_entries),
        "entries": collected_entries,
    }


def load_registry(skill_root: Path) -> dict[str, object]:
    registry_path = asset_paths(skill_root)["registry_path"]
    if not registry_path.exists():
        return {
            "branch": "mother_doc_agents",
            "managed_scopes": [ROOT_BRANCH, CONTAINER_BRANCH, DOCS_BRANCH],
            "managed_filename": AGENTS_FILENAME,
            "entry_count": 0,
            "entries": [],
        }
    return _load_json(registry_path)


def push_agents_tree(skill_root: Path, document_root: Path, *, dry_run: bool) -> dict[str, object]:
    workspace_root = _workspace_root_from_document_root(document_root)
    navigation_sync = sync_navigation_tree(document_root, dry_run=dry_run)
    root_and_container_sync = _push_root_and_container_agents(workspace_root, document_root, dry_run=dry_run)
    template_paths: list[str] = []
    if not dry_run:
        template_paths = _sync_template_tree(skill_root, workspace_root, document_root)
    if dry_run:
        return {
            "workspace_root": str(workspace_root),
            "document_root": str(document_root),
            "navigation_sync": navigation_sync,
            "root_and_container_sync": root_and_container_sync,
            "template_sync": {"skipped": True, "reason": "dry_run"},
            "scan": {"skipped": True, "reason": "dry_run"},
            "collect": {"skipped": True, "reason": "dry_run"},
        }
    scan_payload = scan_agents_tree(skill_root, document_root)
    collect_payload = collect_from_scan(skill_root)
    return {
        "workspace_root": str(workspace_root),
        "document_root": str(document_root),
        "navigation_sync": navigation_sync,
        "root_and_container_sync": root_and_container_sync,
        "template_sync": {"created_or_updated": template_paths},
        "scan": scan_payload,
        "collect": collect_payload,
    }
