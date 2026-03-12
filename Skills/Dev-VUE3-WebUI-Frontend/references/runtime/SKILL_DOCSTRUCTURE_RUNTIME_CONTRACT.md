---
doc_id: "runtime.docgraph.audit"
doc_type: "runtime_contract"
topic: "Audit version of the embedded doc-graph contract used by the frontend showroom"
anchors:
  - target: "SKILL_RUNTIME_CONTRACT.md"
    relation: "supports"
    direction: "upstream"
    reason: "The embedded doc-graph contract exists to support the staged frontend runtime contract."
  - target: "../../ui-dev/UI_DEV_ENTRY.md"
    relation: "implements"
    direction: "downstream"
    reason: "The showroom redevelopment docs define how future UI surfaces will consume the graph."
---

# Embedded Doc Graph Contract

## 作用
- 为 `ui-dev` 的 showroom redevelopment docs 与未来 runtime 提供稳定的 markdown graph 数据输入。
- 要求技能内 markdown 文档具备 frontmatter anchors。
- 让未来的 showroom runtime 能把当前技能自身渲染成可读的 graph。

## 最小合同
- 每个 markdown 文档至少一个 anchor。
- anchor 目标必须落在当前技能根目录内。
- `SKILL.md` 通过 `metadata.doc_structure` 暴露自身合同。
