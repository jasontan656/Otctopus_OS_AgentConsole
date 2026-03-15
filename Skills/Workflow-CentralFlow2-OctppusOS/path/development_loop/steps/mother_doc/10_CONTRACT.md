---
doc_id: workflow_centralflow2_octppusos.path.development_loop.steps.mother_doc.contract
doc_type: action_contract_doc
topic: Mother doc contract
reading_chain:
- key: tools
  target: 15_TOOLS.md
  hop: next
  reason: 先读 mother_doc 合同，再看本阶段工具面。
---

# mother_doc 阶段合同

- `mother_doc` 是唯一需求源；graph 只能补充现状，不得替代需求源。
- `00_index.md` 是固定根入口，必须由 `mother-doc-refresh-root-index` 自动生成。
- 原子文档协议至少包含：
  - `doc_work_state`
  - `doc_pack_refs`
  - `thumb_title`
  - `thumb_summary`
  - `display_layer`
  - `always_read`
  - `anchors_down`
  - `anchors_support`
- 进入 `construction_plan` 之前，`mother-doc-lint` 必须通过。

## 下一跳列表
- [tools]：`15_TOOLS.md`
