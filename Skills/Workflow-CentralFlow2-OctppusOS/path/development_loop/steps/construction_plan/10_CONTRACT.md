---
doc_id: workflow_centralflow2_octppusos.path.development_loop.steps.construction_plan.contract
doc_type: action_contract_doc
topic: Construction plan contract
reading_chain:
- key: tools
  target: 15_TOOLS.md
  hop: next
  reason: 先读 packs 合同，再看当前阶段工具。
---

# construction_plan 阶段合同

- `construction_plan` 必须从已通过 `mother-doc-lint` 的文档树正式生成。
- official plan 与 preview skeleton 必须显式区分。
- 每个 pack 都要声明 `source_mother_doc_refs`。

## 下一跳列表
- [tools]：`15_TOOLS.md`
