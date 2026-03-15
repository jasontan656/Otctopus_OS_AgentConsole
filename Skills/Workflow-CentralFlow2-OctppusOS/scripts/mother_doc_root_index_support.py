from __future__ import annotations

from pathlib import Path

from mother_doc_contract import MOTHER_DOC_REQUIRED_ROOT_INDEX_RULES


def _iter_visible_directories(root: Path) -> list[Path]:
    directories: list[Path] = []
    for path in sorted(root.rglob("*")):
        if not path.is_dir() or path == root:
            continue
        relative = path.relative_to(root)
        if any(part.startswith(".") for part in relative.parts):
            continue
        directories.append(path)
    return directories


def folder_refs(root: Path) -> list[str]:
    return [f"{path.relative_to(root).as_posix()}/" for path in _iter_visible_directories(root)]


def _tree_lines(root: Path) -> list[str]:
    visible_children: dict[Path, list[Path]] = {}
    for directory in _iter_visible_directories(root):
        visible_children.setdefault(directory.parent, []).append(directory)

    for children in visible_children.values():
        children.sort(key=lambda item: item.relative_to(root).as_posix())

    lines = ["mother_doc/"]

    def walk(parent: Path, prefix: str) -> None:
        children = visible_children.get(parent, [])
        for index, child in enumerate(children):
            is_last = index == len(children) - 1
            connector = "└── " if is_last else "├── "
            lines.append(f"{prefix}{connector}{child.name}/")
            walk(child, prefix + ("    " if is_last else "│   "))

    walk(root, "")
    return lines


def render_root_index_body(root: Path) -> str:
    folder_list = folder_refs(root)
    folder_lines = [f"- `{folder_ref}`" for folder_ref in folder_list] or ["- 当前尚无子目录。"]
    tree_block = "\n".join(_tree_lines(root))

    body_lines = [
        "# Mother Doc Root Index",
        "",
        "## 当前职责",
        "- 作为 `mother_doc` 的固定根入口存在。",
        "- 本文件由 `mother-doc-refresh-root-index` 自动维护，只展示目录级结构，不展示文件。",
        "- 根入口不承载具体设计细节，只承载最小根说明与脚本挂点。",
        "",
        "## 自动目录结构图",
        "```text",
        tree_block,
        "```",
        "",
        "## 自动目录清单",
        *folder_lines,
        "",
        "## 根入口约束",
        "- `doc_role` 必须保持为 `root_index`。",
        "- `always_read` 必须保持为 `true`。",
        "- 所有 `anchors_*` 必须保持空数组。",
        "- 根入口不手工维护文件级清单，结构变更应重新运行自动刷新脚本。",
        "",
    ]

    return "\n".join(body_lines)


def render_root_index_content(root: Path) -> str:
    frontmatter_lines = [
        "---",
        "doc_work_state: modified",
        "doc_pack_refs: []",
        f"doc_role: {MOTHER_DOC_REQUIRED_ROOT_INDEX_RULES['doc_role']}",
        "thumb_title: Root Index",
        "thumb_summary: 顶层常驻根入口，自动维护目录级结构图，不展示文件清单。",
        "display_layer: overview",
        "always_read: true",
        "anchors_down: []",
        "anchors_support: []",
        "---",
        "",
    ]

    return "\n".join(frontmatter_lines + [render_root_index_body(root)])


def refresh_root_index_result(root: Path) -> tuple[dict[str, object], int]:
    root.mkdir(parents=True, exist_ok=True)
    index_path = root / MOTHER_DOC_REQUIRED_ROOT_INDEX_RULES["relative_path"]
    content = render_root_index_content(root)
    index_path.write_text(content if content.endswith("\n") else f"{content}\n", encoding="utf-8")
    folders = folder_refs(root)
    return (
        {
            "status": "pass",
            "root": str(root),
            "index_path": str(index_path),
            "folder_count": len(folders),
            "folder_refs": folders,
        },
        0,
    )
