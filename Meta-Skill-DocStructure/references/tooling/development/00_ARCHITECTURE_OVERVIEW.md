---
doc_id: "tooling.architecture.overview"
doc_type: "tooling_architecture"
topic: "Architecture overview of Meta-Skill-DocStructure tooling"
anchors:
  - target: "../../runtime/SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT.md"
    relation: "implements"
    direction: "upstream"
    reason: "Architecture exists to implement the runtime contract."
  - target: "modules/mod_anchor_graph_lint.md"
    relation: "decomposes_into"
    direction: "downstream"
    reason: "The lint module doc explains the main execution path."
---

# 架构总览

## 组件
- `scripts/Cli_Toolbox.py`
  - 统一 CLI 入口。
- `references/runtime/SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT.json`
  - machine-readable 合同。
- `assets/runtime/anchor_query_matrix.json`
  - keyword-based split signals 与 anchor query semantics。
- `assets/runtime/self_anchor_graph.json`
  - 本技能自身文档图谱快照。

## 执行面
- `runtime-contract`
- `lint-doc-anchors`
- `build-anchor-graph`
- `rebuild-self-graph`

## 设计取向
- 把 skill 内部 markdown 文档视为 graph nodes。
- 把 frontmatter anchors 视为 graph edges。
- 把 atomicity keyword matrix 作为“是否继续拆分”的机械辅助，而非最终裁决者。
