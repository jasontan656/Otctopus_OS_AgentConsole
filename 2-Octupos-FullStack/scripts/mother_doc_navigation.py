from __future__ import annotations

from pathlib import Path


AGENTS_FILENAME = "AGENTS.md"
LEGACY_AGENTS_FILENAME = "agents.md"

DOMAIN_DESCRIPTIONS = {
    "common": "current container's abstract layer root; choose one abstract domain below",
    "overview": "human-readable overview scope for the current container; start here when you need top-level comprehension",
    "features": "feature document scope for the current container; choose the affected requirement or unresolved question slice below",
    "shared": "shared integration scope for the current container; choose APIs, events, contracts, or cross-container dependencies below",
    "writing_guides": "authored-doc writing rules for the current container",
    "code_abstractions": "code abstraction root for the current container; choose one code-facing abstract domain below",
    "architecture": "architecture abstraction scope under code abstractions for the current container",
    "stack": "technology stack abstraction scope under code abstractions for the current container",
    "naming": "naming rules abstraction scope under code abstractions for the current container",
    "contracts": "contract rules abstraction scope under code abstractions for the current container",
    "operations": "operations and maintenance abstraction scope under code abstractions for the current container",
    "dev_canon": "recovered development canon scope for the current container",
    "development_logs": "development and deployment log scope for the Mother_Doc container",
    "docs": "authored-document root for the Mother_Doc container itself",
    "graph": "OS_graph asset root for the Mother_Doc container",
}


def titleize(name: str) -> str:
    return name.replace("_", " ")


def scope_doc_name(path: Path, document_root: Path) -> str:
    if path == document_root:
        return "Mother_Doc.md"
    return f"{path.name}.md"


def describe_directory(path: Path, document_root: Path) -> str:
    rel = path.relative_to(document_root)
    parts = rel.parts
    if not parts:
        return "root navigation scope for Mother_Doc docs; choose the container documentation scope to enter"
    if len(parts) == 1:
        if parts[0] == "Mother_Doc":
            return "self-description container scope for the Mother_Doc container itself"
        return f"container documentation scope for `{parts[0]}`"
    if parts[-1] in DOMAIN_DESCRIPTIONS:
        return DOMAIN_DESCRIPTIONS[parts[-1]]
    if len(parts) >= 2 and parts[-2] == "common":
        return f"leaf abstract domain scope for `{parts[-1]}` under the current container"
    return f"nested documentation scope for `{parts[-1]}`"


def describe_leaf_file(path: Path, document_root: Path) -> str:
    if path.name == "README.md":
        return "peer purpose document for the current scope"
    if path.name == AGENTS_FILENAME:
        return "navigation index for the current scope"
    if path.name == scope_doc_name(path.parent, document_root):
        return "scope-entity document for the current directory itself"
    stem = path.stem
    parent = path.parent.name
    if parent in DOMAIN_DESCRIPTIONS:
        return f"`{titleize(stem)}` leaf rule file inside the `{parent}` abstract domain"
    return f"`{titleize(stem)}` leaf markdown file for the current scope"


def build_directory_readme(path: Path, document_root: Path) -> str:
    rel = path.relative_to(document_root)
    title = rel.name if rel.parts else "Mother_Doc"
    description = describe_directory(path, document_root)
    peer_scope_doc = scope_doc_name(path, document_root)
    lines = [
        f"# {title}",
        "",
        f"<!-- replace_me: 这里写当前目录 `{title}` 的浓缩总结，内容应跟随本目录和子目录文档实际状态更新。 -->",
        "",
        "## 1. 作用",
        f"- 当前目录用途：{description}。",
        "- 本文件负责当前层的总结说明，不承担递归索引职责。",
        "",
        "## 2. 阅读关系",
        f"- 同层 `{AGENTS_FILENAME}` 是当前层索引入口；当索引足够判断时，可不先读本文件。",
        f"- 同层 `{peer_scope_doc}` 是当前目录自身的实体说明。",
        "- 如果本目录或其子路径的内容发生变化，必须考虑维护本文件。",
        "",
        "## 3. 当前层摘要",
        "- `replace_me`: 当前目录承载内容的总结。",
        "- `replace_me`: 当前目录下最重要的子域或关键文档。",
        "",
        "## 4. 边界",
        "- 保持本文件聚焦当前层的用途与范围，不在这里展开完整子路径索引。",
        "- 需要下一步入口时，回到同层 `AGENTS.md`。",
        "",
    ]
    return "\n".join(lines)


def build_scope_entity_doc(path: Path, document_root: Path) -> str:
    rel = path.relative_to(document_root)
    scope_label = str(rel) if rel.parts else "Mother_Doc"
    title = "Mother_Doc" if path == document_root else path.name
    if path.name == "contracts":
        lines = [
            "# contracts",
            "",
            "- `contract_name`: current_scope_contract_domain",
            "- `contract_version`: 1.0.0",
            "- `validation_mode`: static_minimal",
            "- `required_fields`: contract_name, contract_version, validation_mode, domain_scope",
            "- `optional_fields`: notes",
            "",
            f"- `domain_scope`: `{scope_label}`",
            "- This file is the scope-entity contract for the current `contracts/` directory itself.",
            "- Keep it aligned with the contract files and contract semantics that live under this directory.",
            "",
        ]
        return "\n".join(lines)
    lines = [
        f"# {title}",
        "",
        f"This file is the scope-entity document for `{scope_label}`.",
        "It describes the directory itself as a module, parent scope, black-box container, or authored documentation carrier.",
        "Keep the content aligned with the actual code and document structure for the same scope.",
        "",
    ]
    return "\n".join(lines)


def build_agents_index(path: Path, document_root: Path) -> str:
    rel = path.relative_to(document_root)
    scope_label = str(rel) if rel.parts else "Mother_Doc"
    peer_scope_doc = scope_doc_name(path, document_root)
    children = sorted(
        [
            child
            for child in path.iterdir()
            if child.name not in {"README.md", AGENTS_FILENAME, LEGACY_AGENTS_FILENAME, peer_scope_doc, "__pycache__"}
        ],
        key=lambda item: (item.is_file(), item.name.lower()),
    )
    lines = [
        "# AGENTS",
        "",
        "## 1. 目标",
        f"- 当前层作用：{describe_directory(path, document_root)}。",
        "- 本文件只承担当前层入口索引与递归选域，不承载正文细节。",
        "",
        "## 2. 同层入口",
        "- `README.md`: 当前层用途说明；可选阅读，但如果当前目录内容发生变更，则必须考虑维护它。",
        f"- `{peer_scope_doc}`: 当前层目录实体说明。",
        "",
        "## 3. 下一层入口",
    ]
    if not children:
        lines.append("- `terminal`: 当前层没有更深入口。")
    else:
        for child in children:
            child_rel = child.relative_to(document_root)
            description = describe_directory(child, document_root) if child.is_dir() else describe_leaf_file(child, document_root)
            lines.append(f"- `{child_rel}`: {description}.")
    lines.extend(
        [
            "",
            "## 4. 选择规则",
            "- 若当前 `AGENTS.md` 的索引不足以判断，再读取当前层 `README.md` 与同名实体文档。",
            f"- 再从当前 `{AGENTS_FILENAME}` 的入口中选择下一层或目标叶子。",
            "- 选择时只依据强化后的用户意图，不跨到无关域。",
            "",
            "## 5. 更新边界",
            "- 当前层只负责把下一步入口说清楚，不负责替代下层正文。",
            "- 当前层不得把别的域的规则、workflow 或实现细节混写进来。",
            "- 如果当前目录本身或其下子路径被修改，必须同时检查同层 `README.md` 是否需要维护。",
            "",
            "## 6. 索引契约",
            f"- 当前文件属于 `mother_doc_docs` 分支；总容器根与容器根的 `{AGENTS_FILENAME}` 由同一 AGENTS/README manager 的其他分支管理。",
            "- 当前层索引必须同时指向同层用途文档、同层实体文档和下一层入口。",
            "- 子路径说明必须简短且可判断作用域。",
            "",
            "## 7. 递归动作",
            "- 命中目标后进入下一层，重复当前链路。",
            "- 直到完整影响面被覆盖，再执行文档覆盖写回或规则读取。",
            "",
        ]
    )
    return "\n".join(lines)


def sync_navigation_tree(document_root: Path, *, dry_run: bool) -> dict[str, list[str]]:
    created_readmes: list[str] = []
    created_scope_docs: list[str] = []
    updated_agents: list[str] = []
    removed_legacy_indexes: list[str] = []
    removed_legacy_agents: list[str] = []

    for legacy in sorted(document_root.rglob("00_INDEX.md")):
        removed_legacy_indexes.append(str(legacy))
        if not dry_run:
            legacy.unlink()

    for legacy_agents in sorted(document_root.rglob(LEGACY_AGENTS_FILENAME)):
        removed_legacy_agents.append(str(legacy_agents))
        if not dry_run:
            legacy_agents.unlink()

    dirs = sorted([path for path in document_root.rglob("*") if path.is_dir()], key=lambda item: (len(item.parts), str(item)))
    dirs.insert(0, document_root)
    seen: set[Path] = set()
    ordered_dirs: list[Path] = []
    for path in dirs:
        if path not in seen:
            seen.add(path)
            ordered_dirs.append(path)

    for directory in ordered_dirs:
        readme_path = directory / "README.md"
        if not readme_path.exists():
            created_readmes.append(str(readme_path))
            if not dry_run:
                readme_path.write_text(build_directory_readme(directory, document_root), encoding="utf-8")
        scope_doc_path = directory / scope_doc_name(directory, document_root)
        if not scope_doc_path.exists():
            created_scope_docs.append(str(scope_doc_path))
            if not dry_run:
                scope_doc_path.write_text(build_scope_entity_doc(directory, document_root), encoding="utf-8")
        agents_path = directory / AGENTS_FILENAME
        updated_agents.append(str(agents_path))
        if not dry_run:
            agents_path.write_text(build_agents_index(directory, document_root), encoding="utf-8")

    return {
        "created_readmes": created_readmes,
        "created_scope_docs": created_scope_docs,
        "updated_agents": updated_agents,
        "removed_legacy_indexes": removed_legacy_indexes,
        "removed_legacy_agents": removed_legacy_agents,
    }
