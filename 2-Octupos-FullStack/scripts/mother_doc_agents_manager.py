from __future__ import annotations

import json
import shutil
from contextlib import contextmanager
from pathlib import Path

from mother_doc_navigation import AGENTS_FILENAME, LEGACY_AGENTS_FILENAME, sync_navigation_tree

README_FILENAME = "README.md"

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
        "- 当前层作用：`Octopus_OS` 总容器根，是 AI 进入项目开发与维护链路的第一站。",
        "- 项目相关介绍看同层 `README.md`；本文件不展开项目正文。",
        "- 本文件只负责把章鱼OS全栈技能锚点、代码去处、文档去处、graph 去处和工具入口说清楚。",
        "",
        "## 2. 同层入口",
        "- `README.md`: 当前总容器层的浓缩总结说明；可选阅读，但如果本层容器布局或维护入口发生变化，必须同步维护对应章节总结。",
        "",
        "## 3. 章鱼OS技能锚点",
        "- `/home/jasontan656/.codex/skills/2-Octupos-FullStack/SKILL.md`: 技能总门面。",
        "- `/home/jasontan656/.codex/skills/2-Octupos-FullStack/references/skill_native/01_FACADE_LOAD_MAP.md`: 技能总入口图与规则分流。",
        "- `/home/jasontan656/.codex/skills/2-Octupos-FullStack/references/stages/MOTHER_DOC_STAGE.md`: `mother_doc` 阶段入口。",
        "- `/home/jasontan656/.codex/skills/2-Octupos-FullStack/references/stages/IMPLEMENTATION_STAGE.md`: `implementation` 阶段入口。",
        "- `/home/jasontan656/.codex/skills/2-Octupos-FullStack/references/stages/EVIDENCE_STAGE.md`: `evidence` 阶段入口。",
        "- `/home/jasontan656/.codex/skills/2-Octupos-FullStack/scripts/Cli_Toolbox.py`: 统一 CLI 工具入口。",
        "",
        "## 4. 项目资产去处",
        "- `Octopus_OS/<Container_Name>/`: 各独立容器的代码与运行时根路径。",
        "- `Octopus_OS/Mother_Doc/docs/`: 所有容器的 authored-doc 文档树。",
        "- `Octopus_OS/Mother_Doc/graph/`: OS_graph 资产与 evidence graph runtime 根。",
        "",
        "## 5. 选择规则",
        "- 先看当前任务是否只需要技能锚点即可判断；若不足，再可选读取同层 `README.md`。",
        "- 再读章鱼OS全栈技能锚点，确认当前任务属于 `mother_doc`、`implementation` 还是 `evidence`。",
        "- 确认阶段后，再选择进入对应容器路径或 `Mother_Doc` 文档树，不跨到无关容器。",
        "- 如果本仓库在写入回合发生文件变动，则必须进行 GitHub 留痕；commit message 必须依据本轮实际变动内容编写。",
        "- 本仓库承担宪法技能与静态 lint 收口责任；写入本仓库时，必须对实际被修改的 concrete target root 运行 `Constitution-knowledge-base` static lint。",
        "- 禁止把 `/home/jasontan656/AI_Projects` 当作 lint 目标；若出现非零退出或 `status=fail`，必须声明 `violation` 并修复后重跑。",
        "",
        "## 6. 索引契约",
        "- 当前根层 `AGENTS.md` 属于 `octopus_os_root` 分支。",
        "- 它必须固定指向 `README.md` 和章鱼OS全栈技能锚点。",
        "- 它不负责展开具体文档正文或具体实现细节。",
        "- 当本层内容发生变更时，必须同时检查同层 `README.md` 是否需要更新总结。",
        "",
        "## 7. 递归动作",
    ]
    for container in _container_dirs(workspace_root):
        lines.append(f"- 进入 `{container.name}/`：{_container_description(container.name)}。")
    lines.extend(
        [
            "- 若目标属于文档树，则转入 `Mother_Doc/docs/**` 的递归索引链。",
            "- 若目标属于 graph 或 evidence，则转入 `Mother_Doc/graph/` 与技能 `evidence` 锚点继续处理。",
            "",
        ]
    )
    return "\n".join(lines)


def build_octopus_root_readme(workspace_root: Path) -> str:
    lines = [
        "# Octopus_OS",
        "",
        "<!-- replace_me: 这里写当前项目总容器层的浓缩总结，内容应来自当前各容器与 Mother_Doc 的实际状态。 -->",
        "",
        "## 1. 作用",
        "- 当前文件是 `Octopus_OS` 总容器层的浓缩总结说明。",
        "- 这里写人类和模型都能快速理解的顶层项目定位、容器分布和当前阶段概况。",
        "",
        "## 2. 阅读关系",
        "- 同层 `AGENTS.md` 是第一站索引与行动入口。",
        "- 当 `AGENTS.md` 的锚点和入口已经足够判断当前任务时，可以不读本文件。",
        "- 当本层容器布局、技能入口、代码去处、文档去处或 graph/evidence 去处发生变化时，必须维护本文件。",
        "",
        "## 3. 顶层容器摘要",
    ]
    for container in _container_dirs(workspace_root):
        lines.append(f"- `{container.name}/`: {_container_description(container.name)}.")
    lines.extend(
        [
            "",
            "## 4. 当前维护约束",
            "- 保持本文件为顶层总结，不在这里展开具体实现细节。",
            "- 需要具体开发或回写规则时，转到同层 `AGENTS.md` 指向的章鱼OS技能锚点。",
            "- 需要容器级细节时，进入对应容器目录下的 `README.md` 或 `Mother_Doc/docs/<Container_Name>/`。",
            "",
            "## 5. 待补内容",
            "- `replace_me`: 当前项目阶段总结。",
            "- `replace_me`: 当前最关键的开发目标或上线目标。",
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
        f"- 当前层作用：`{container_name}` 容器根的开发回写合同入口。",
        "- 本文件提醒模型遵守当前容器的抽象层通用规则、文档回写入口和 evidence 闭环要求。",
        "",
        "## 2. 同层入口",
        "- `README.md`: 当前容器项目的 AI-facing summary；可选阅读，但如果本容器发生了代码、文档或 evidence 相关落盘，必须考虑维护本文件。",
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
            "- 如果当前任务需要确认容器用途、维护范围或当前阶段总结，可选读取同层 `README.md`。",
            "- 若任务是文档设计、需求回写或结构浏览，优先转入对应的 `Mother_Doc/docs` 路径。",
            "- 若任务是代码落盘或运行时处理，则留在当前容器路径，并同时回看对应的 `Mother_Doc/docs/<Container_Name>/common/`。",
            "- 涉及前端开发、页面联调、浏览器测试或交互验证时，`User_UI` 与 `Admin_UI` 必须加载 `Meta-browser-operation`。",
            "",
            "## 5. 更新边界",
            "- 当前层只负责容器根入口与开发回写提醒，不替代容器内部正文。",
            "- 文档正文仍由 `Mother_Doc/docs` 承载，graph 资产由 `Mother_Doc/graph` 承载。",
            "- 若当前容器内容被修改，必须检查同层 `README.md` 是否需要更新总结。",
            "",
            "## 6. 索引契约",
            "- 当前文件属于 `container_roots` 分支。",
            "- 每个顶层容器都必须有自己的容器根 `AGENTS.md` 与 `README.md` 模板与推送路径。",
            "",
            "## 7. 递归动作",
            "- 命中文档域时，进入对应 `Mother_Doc/docs` 容器路径。",
            "- 命中当前容器实际子路径时，继续进入对应子目录处理。",
            "",
        ]
    )
    if container_name not in {"User_UI", "Admin_UI"}:
        lines.remove("- 涉及前端开发、页面联调、浏览器测试或交互验证时，`User_UI` 与 `Admin_UI` 必须加载 `Meta-browser-operation`。")
    return "\n".join(lines)


def build_container_root_readme(container_root: Path, document_root: Path) -> str:
    container_name = container_root.name
    doc_scope = document_root / container_name
    lines = [
        f"# {container_name}",
        "",
        f"<!-- replace_me: 这里写 `{container_name}` 当前容器项目的浓缩总结，内容应跟随容器代码、文档与 evidence 的实际状态更新。 -->",
        "",
        "## 1. 容器定位",
        f"- 当前文件是 `{container_name}` 容器根的 AI-facing README。",
        f"- 对应容器说明：{_container_description(container_name)}。",
        "",
        "## 2. 阅读关系",
        "- 同层 `AGENTS.md` 是当前容器的开发回写合同入口。",
        "- 如果 `AGENTS.md` 已经足够判断当前动作，可不先读本文件。",
        "- 如果当前容器发生代码、文档或 evidence 变更，则必须回看并维护本文件。",
        "",
        "## 3. 对应文档入口",
    ]
    if doc_scope.exists():
        lines.append(f"- `../Mother_Doc/docs/{container_name}/`: 当前容器对应的 authored-doc 根。")
        lines.append(f"- `../Mother_Doc/docs/{container_name}/README.md`: 当前容器文档域的浓缩总结。")
    else:
        lines.append("- `replace_me`: 当前容器对应的 authored-doc 根尚未补齐。")
    lines.extend(
        [
            "",
            "## 4. 当前维护摘要",
            "- `replace_me`: 当前容器主要职责。",
            "- `replace_me`: 当前容器最关键的代码/接口/运行点。",
            "- `replace_me`: 当前容器最近需要同步维护的总结信息。",
            "",
            "## 5. 边界",
            "- 本文件只做当前容器层的总结说明，不代替下层代码、API、文档正文。",
            "- 需要具体规则时，回到同层 `AGENTS.md`，再跳到对应 `Mother_Doc/docs` 或技能锚点。",
            "",
        ]
    )
    return "\n".join(lines)


def _iter_managed_doc_dirs(document_root: Path) -> list[Path]:
    return sorted([document_root, *[path for path in document_root.rglob("*") if path.is_dir()]])


def _scan_entry(
    *,
    branch: str,
    scope_path: Path,
    registry_dir: Path,
    agents_target_path: Path,
    agents_template_relative: Path,
    readme_target_path: Path,
    readme_template_relative: Path,
    readme_mode: str,
    child_entry_count: int,
) -> dict[str, object]:
    return {
        "scope_branch": branch,
        "registry_key": str(registry_dir),
        "relative_path": str(registry_dir),
        "scope_path": str(scope_path),
        "agents_target_path": str(agents_target_path),
        "agents_template_relative_path": str(agents_template_relative),
        "agents_present": agents_target_path.exists(),
        "readme_target_path": str(readme_target_path),
        "readme_template_relative_path": str(readme_template_relative),
        "readme_present": readme_target_path.exists(),
        "readme_management_mode": readme_mode,
        "child_entry_count": child_entry_count,
    }


def scan_agents_tree(skill_root: Path, document_root: Path) -> dict[str, object]:
    workspace_root = _workspace_root_from_document_root(document_root)
    entries: list[dict[str, object]] = []
    missing_agents: list[str] = []
    missing_readmes: list[str] = []
    legacy_agents: list[str] = []

    root_agents = workspace_root / AGENTS_FILENAME
    root_readme = workspace_root / README_FILENAME
    if root_agents.exists():
        entries.append(
            _scan_entry(
                branch=ROOT_BRANCH,
                scope_path=workspace_root,
                registry_dir=Path(ROOT_BRANCH),
                agents_target_path=root_agents,
                agents_template_relative=_root_template_relative(),
                readme_target_path=root_readme,
                readme_template_relative=Path(ROOT_BRANCH) / README_FILENAME,
                readme_mode="template_managed",
                child_entry_count=len(_container_dirs(workspace_root)),
            )
        )
    else:
        missing_agents.append(str(root_agents))
    if not root_readme.exists():
        missing_readmes.append(str(root_readme))

    for container_root in _container_dirs(workspace_root):
        agents_path = container_root / AGENTS_FILENAME
        readme_path = container_root / README_FILENAME
        if agents_path.exists():
            children = [
                child
                for child in container_root.iterdir()
                if child.name not in {README_FILENAME, AGENTS_FILENAME, LEGACY_AGENTS_FILENAME, "__pycache__"} and not child.name.startswith(".")
            ]
            entries.append(
                _scan_entry(
                    branch=CONTAINER_BRANCH,
                    scope_path=container_root,
                    registry_dir=Path(CONTAINER_BRANCH) / container_root.name,
                    agents_target_path=agents_path,
                    agents_template_relative=_container_template_relative(container_root.name),
                    readme_target_path=readme_path,
                    readme_template_relative=Path(CONTAINER_BRANCH) / container_root.name / README_FILENAME,
                    readme_mode="template_managed",
                    child_entry_count=len(children),
                )
            )
        else:
            missing_agents.append(str(agents_path))
        if not readme_path.exists():
            missing_readmes.append(str(readme_path))

    for directory in _iter_managed_doc_dirs(document_root):
        agents_path = directory / AGENTS_FILENAME
        readme_path = directory / README_FILENAME
        legacy_path = directory / LEGACY_AGENTS_FILENAME
        scope_doc = directory / ("Mother_Doc.md" if directory == document_root else f"{directory.name}.md")
        if legacy_path.exists():
            legacy_agents.append(str(legacy_path))
        if not agents_path.exists():
            missing_agents.append(str(agents_path))
            if not readme_path.exists():
                missing_readmes.append(str(readme_path))
            continue
        children = [
            child
            for child in directory.iterdir()
            if child.name not in {README_FILENAME, AGENTS_FILENAME, LEGACY_AGENTS_FILENAME, scope_doc.name, "__pycache__"} and not child.name.startswith(".")
        ]
        entries.append(
            _scan_entry(
                branch=DOCS_BRANCH,
                scope_path=directory,
                registry_dir=Path(DOCS_BRANCH) / directory.relative_to(document_root),
                agents_target_path=agents_path,
                agents_template_relative=_docs_template_relative(agents_path, document_root),
                readme_target_path=readme_path,
                readme_template_relative=Path(DOCS_BRANCH) / directory.relative_to(document_root) / README_FILENAME,
                readme_mode="collect_preserve",
                child_entry_count=len(children),
            )
        )
        if not readme_path.exists():
            missing_readmes.append(str(readme_path))

    payload = {
        "branch": "mother_doc_agents_readme",
        "managed_scopes": [ROOT_BRANCH, CONTAINER_BRANCH, DOCS_BRANCH],
        "entry_count": len(entries),
        "entries": entries,
        "missing_agents": missing_agents,
        "missing_readmes": missing_readmes,
        "legacy_agents": legacy_agents,
        "workspace_root": str(workspace_root),
        "document_root": str(document_root),
        "managed_filenames": [AGENTS_FILENAME, README_FILENAME],
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
    root_readme_template = template_root / ROOT_BRANCH / README_FILENAME
    _write_text(root_readme_template, build_octopus_root_readme(workspace_root))
    created.append(str(root_readme_template))

    for container_root in _container_dirs(workspace_root):
        template_path = template_root / _container_template_relative(container_root.name)
        _write_text(template_path, build_container_root_agents(container_root, document_root))
        created.append(str(template_path))
        readme_template_path = template_root / CONTAINER_BRANCH / container_root.name / README_FILENAME
        _write_text(readme_template_path, build_container_root_readme(container_root, document_root))
        created.append(str(readme_template_path))

    for directory in _iter_managed_doc_dirs(document_root):
        agents_path = directory / AGENTS_FILENAME
        if agents_path.exists():
            template_path = template_root / _docs_template_relative(agents_path, document_root)
            _write_text(template_path, agents_path.read_text(encoding="utf-8"))
            created.append(str(template_path))
        readme_path = directory / README_FILENAME
        if readme_path.exists():
            readme_template_path = template_root / DOCS_BRANCH / directory.relative_to(document_root) / README_FILENAME
            _write_text(readme_template_path, readme_path.read_text(encoding="utf-8"))
            created.append(str(readme_template_path))

    return created


def _push_root_and_container_assets(workspace_root: Path, document_root: Path, *, dry_run: bool) -> list[str]:
    updated: list[str] = []
    root_agents = workspace_root / AGENTS_FILENAME
    updated.append(str(root_agents))
    if not dry_run:
        root_agents.write_text(build_octopus_root_agents(workspace_root), encoding="utf-8")
    root_readme = workspace_root / README_FILENAME
    updated.append(str(root_readme))
    if not dry_run:
        root_readme.write_text(build_octopus_root_readme(workspace_root), encoding="utf-8")

    for container_root in _container_dirs(workspace_root):
        agents_path = container_root / AGENTS_FILENAME
        updated.append(str(agents_path))
        if not dry_run:
            agents_path.write_text(build_container_root_agents(container_root, document_root), encoding="utf-8")
        readme_path = container_root / README_FILENAME
        updated.append(str(readme_path))
        if not dry_run:
            readme_path.write_text(build_container_root_readme(container_root, document_root), encoding="utf-8")
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
        "# Mother_Doc AGENTS/README Registry",
        "",
        "- This asset tree stores managed AGENTS/README templates and collected snapshots.",
        "- Managed branches: `octopus_os_root`, `container_roots`, `mother_doc_docs`.",
        "",
        "## Template Targets",
        "",
    ]

    for entry in entries:
        agents_template = Path(str(entry["agents_template_relative_path"]))
        agents_target = str(entry["agents_target_path"])
        readme_template = Path(str(entry["readme_template_relative_path"]))
        readme_target = str(entry["readme_target_path"])
        readme_mode = str(entry["readme_management_mode"])
        index_lines.append(f"- `{agents_template}` -> `{agents_target}`")
        index_lines.append(f"- `{readme_template}` -> `{readme_target}` (`{readme_mode}`)")

    index_lines.extend(["", "## Collected Snapshots", ""])

    for entry in entries:
        rel_dir = Path(str(entry["registry_key"]))
        target_dir = collected_root / rel_dir
        target_dir.mkdir(parents=True, exist_ok=True)
        agents_source_path = Path(str(entry["agents_target_path"]))
        agents_target_path = target_dir / AGENTS_FILENAME
        shutil.copy2(agents_source_path, agents_target_path)
        readme_source_path = Path(str(entry["readme_target_path"]))
        readme_collected_path = None
        if readme_source_path.exists():
            readme_collected_path = target_dir / README_FILENAME
            shutil.copy2(readme_source_path, readme_collected_path)
        collected_entries.append(
            {
                "scope_branch": str(entry["scope_branch"]),
                "relative_path": str(rel_dir),
                "scope_path": str(entry["scope_path"]),
                "agents_source_path": str(agents_source_path),
                "agents_collected_path": str(agents_target_path),
                "agents_template_relative_path": str(entry["agents_template_relative_path"]),
                "readme_source_path": str(readme_source_path),
                "readme_collected_path": str(readme_collected_path) if readme_collected_path else "",
                "readme_template_relative_path": str(entry["readme_template_relative_path"]),
                "readme_management_mode": str(entry["readme_management_mode"]),
            }
        )
        index_lines.append(f"- `{rel_dir}`: collected snapshots for `{agents_source_path}` and peer `{readme_source_path}`.")

    registry_payload = {
        "branch": "mother_doc_agents_readme",
        "managed_scopes": [ROOT_BRANCH, CONTAINER_BRANCH, DOCS_BRANCH],
        "managed_filenames": [AGENTS_FILENAME, README_FILENAME],
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
            "branch": "mother_doc_agents_readme",
            "managed_scopes": [ROOT_BRANCH, CONTAINER_BRANCH, DOCS_BRANCH],
            "managed_filenames": [AGENTS_FILENAME, README_FILENAME],
            "entry_count": 0,
            "entries": [],
        }
    return _load_json(registry_path)


def push_agents_tree(skill_root: Path, document_root: Path, *, dry_run: bool) -> dict[str, object]:
    workspace_root = _workspace_root_from_document_root(document_root)
    navigation_sync = sync_navigation_tree(document_root, dry_run=dry_run)
    root_and_container_sync = _push_root_and_container_assets(workspace_root, document_root, dry_run=dry_run)
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
