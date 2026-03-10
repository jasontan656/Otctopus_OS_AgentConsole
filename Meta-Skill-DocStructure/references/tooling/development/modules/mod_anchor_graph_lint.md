---
doc_id: "tooling.module.anchor_graph_lint"
doc_type: "module_doc"
topic: "Anchor graph build and lint module behavior in Meta-Skill-DocStructure"
anchors:
  - target: "../../Cli_Toolbox_USAGE.md"
    relation: "explains_commands_for"
    direction: "upstream"
    reason: "Usage doc is the primary human-facing surface for these commands."
  - target: "../../../runtime/SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT.md"
    relation: "implements"
    direction: "upstream"
    reason: "This module enforces the runtime contract rules."
---

# anchor_graph_lint 模块

## 职责
- 扫描 target skill root 下全部 markdown 文档。
- 解析 frontmatter anchors。
- 构建 JSON graph。
- 用 `anchor_query_matrix.json` 产生 atomicity warnings。
- 在自技能模式下回写 `self_anchor_graph.json`。

## 失败模式
- target 不是 skill root
- 某文档缺 frontmatter 或必填字段
- 某文档没有 anchors
- 某 anchor target 不存在或不是 markdown
