from __future__ import annotations

import json
import re
from pathlib import Path


def fill_directory_placeholders(root: Path) -> None:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        content = path.read_text(encoding="utf-8")
        if path.suffix == ".md":
            content = re.sub(r"```python\n.*?```\n\n", "", content, flags=re.S)
        content = content.replace("replace_me", "resolved_value")
        path.write_text(content + "\n", encoding="utf-8")


def write_protocol_doc(
    root: Path,
    relative_path: str,
    *,
    title: str,
    summary: str,
    layer: str,
    doc_id: str | None = None,
    doc_role: str | None = None,
    doc_kind: str | None = None,
    content_family: str | None = None,
    branch_family: str | None = None,
    state: str = "modified",
    pack_refs: list[str] | None = None,
    always_read: bool = False,
    anchors_down: list[str] | None = None,
    anchors_support: list[str] | None = None,
    body_lines: list[str] | None = None,
) -> Path:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    if doc_role == "root_index":
        inferred_doc_kind = doc_kind or "trunk_node"
        inferred_content_family = content_family or "root_index_auto"
        inferred_branch_family = None
    else:
        if layer == "overview":
            inferred_doc_kind = doc_kind or "trunk_node"
            inferred_content_family = content_family or "overview_narrative"
            inferred_branch_family = branch_family
        elif layer == "entry":
            inferred_doc_kind = doc_kind or "branch_root"
            inferred_content_family = content_family or "branch_overview"
            inferred_branch_family = branch_family or "domain_branch"
        elif layer == "resolution":
            inferred_doc_kind = doc_kind or "branch_root"
            inferred_content_family = content_family or "layer_taxonomy_root"
            inferred_branch_family = branch_family or "framework_branch"
        elif layer == "capability":
            inferred_doc_kind = doc_kind or "trunk_node"
            inferred_content_family = content_family or "layer_item_doc"
            inferred_branch_family = branch_family
        else:
            inferred_doc_kind = doc_kind or "trunk_node"
            inferred_content_family = content_family or "container_item_doc"
            inferred_branch_family = branch_family
    frontmatter_lines = [
        "---",
        f"doc_work_state: {state}",
        f"doc_pack_refs: {json.dumps(pack_refs or [], ensure_ascii=False)}",
    ]
    if doc_id is not None:
        frontmatter_lines.append(f"doc_id: {doc_id}")
    if doc_role is not None:
        frontmatter_lines.append(f"doc_role: {doc_role}")
    frontmatter_lines.extend(
        [
            f"doc_kind: {inferred_doc_kind}",
            f"content_family: {inferred_content_family}",
            *( [f"branch_family: {inferred_branch_family}"] if inferred_branch_family else [] ),
            f"thumb_title: {title}",
            f"thumb_summary: {summary}",
            f"display_layer: {layer}",
            f"always_read: {'true' if always_read else 'false'}",
            f"anchors_down: {json.dumps(anchors_down or [], ensure_ascii=False)}",
            f"anchors_support: {json.dumps(anchors_support or [], ensure_ascii=False)}",
            "---",
            "",
        ]
    )
    default_body = body_lines or [
        f"# {title}",
        "",
        "## 来源",
        "- `test_fixture`",
        "",
        "## 当前节点职责",
        f"- {summary}",
        "",
        "## 当前内容",
        f"- {summary}",
        "",
        "## 当前延伸规则",
        "- 当前 fixture 允许继续按注册规则扩展。",
        "",
        "## 当前延伸边界",
        "- 当前 fixture 不跨同层互连。",
        "",
        "## 当前承载边界",
        "- 当前 fixture 只承载本节点语义。",
        "",
        "## 当前规则",
        f"- {summary}",
        "",
        "## 当前配置",
        "- `fixture: true`",
        "",
    ]
    if inferred_content_family == "root_index_auto":
        default_body = [
            f"# {title}",
            "",
            "## 当前职责",
            "- 作为测试 fixture 的根入口。",
            "",
            "## 自动目录结构图",
            "```text",
            "mother_doc/",
            "```",
            "",
            "## 自动目录清单",
            "- `fixture/`",
            "",
        ]
    path.write_text("\n".join(frontmatter_lines + default_body) + "\n", encoding="utf-8")
    return path
