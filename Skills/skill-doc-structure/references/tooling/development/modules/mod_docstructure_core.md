---
doc_id: "tooling.module.docstructure_core"
doc_type: "module_doc"
topic: "Core TS docstructure engine behind lint and graph workspace building"
anchors:
  - target: "../../../runtime/SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT.md"
    relation: "implements"
    direction: "upstream"
    reason: "This module enforces the runtime contract."
  - target: "../../Cli_Toolbox_DEVELOPMENT.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This module doc belongs to the tooling development tree."
---

# docstructure_core 模块

## 职责
- 扫描 markdown 文档。
- 解析 frontmatter anchor 合同。
- 读取 runtime contract 中的知识轨、workflow 轨与 metadata 字段。
- 产出 lint 结果、graph JSON 与 doc graph workspace。
- 在当前 skill 模式下回写 `self_anchor_graph.json`。
