---
doc_id: workflow_centralflow2_octppusos.path.development_loop.steps.mother_doc_audit.contract
doc_type: action_contract_doc
topic: Mother doc audit contract
reading_chain:
- key: tools
  target: 15_TOOLS.md
  hop: next
  reason: 先读 audit 合同，再看当前阶段工具。
---

# mother_doc_audit 阶段合同

## Contract Header
- `contract_name`: `workflow_centralflow2_mother_doc_audit_contract`
- `contract_version`: `1.0.0`
- `validation_mode`: `strict`
- `required_fields`:
  - `stage_order_position`
  - `entry_checks`
  - `blocking_growth_debt_policy`
- `optional_fields`:
  - `notes`

- `mother_doc_audit` 是进入 `mother_doc` 之前的固定前置治理阶段。
- 当前阶段先跑 `mother-doc-lint`，再跑 `mother-doc-audit`；协议脏树不得进入语义审计。
- 当前阶段只负责判断树是否干净、哪里存在 growth debt、哪些节点需要先拆，并产出 registry-backed 的 shadow split proposal；它不替代后续 `mother_doc` 的需求写回职责。
- 一旦发现 blocking 级 growth debt，必须先完成拆分/迁移、必要注册、根索引刷新与重审计，才能进入 `mother_doc`。

## 下一跳列表
- [tools]：`15_TOOLS.md`
