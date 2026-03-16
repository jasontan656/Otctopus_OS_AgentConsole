---
doc_id: workflow_centralflow2_octppusos.path.development_loop.steps.mother_doc.steps.impact_and_codegraph.contract
doc_type: action_contract_doc
topic: Mother doc impact and codegraph contract
reading_chain:
- key: execution
  target: 20_EXECUTION.md
  hop: next
  reason: 进入当前步骤执行说明。
---

# impact_and_codegraph 合同

## Contract Header
- `contract_name`: `workflow_centralflow2_mother_doc_impact_and_codegraph_contract`
- `contract_version`: `1.0.0`
- `validation_mode`: `strict`
- `required_fields`:
  - `write_intent_scope`
  - `graph_runtime_rule`
  - `graph_gap_disclosure_rule`
- `optional_fields`:
  - `notes`

- mother_doc 默认属于 `WRITE_INTENT`；进入文档树写回前，必须先用 `Meta-Impact-Investigation` 建立：
  - `direct_scope`
  - `indirect_scope`
  - `latent_related`
  - `validation_or_evidence`
- 若 repo 已有实质代码，必须先检查 `Meta-code-graph-base` runtime；缺图时先初始化，再读 graph context。
- graph 只负责校准当前代码现实，不得替代需求源，也不得决定 mother_doc 应该长成什么形态。
- 若当前 repo 近空或 graph 尚未初始化，允许继续，但必须显式记录“当前图谱证据缺口”。

## 下一跳列表
- [execution]：`20_EXECUTION.md`
