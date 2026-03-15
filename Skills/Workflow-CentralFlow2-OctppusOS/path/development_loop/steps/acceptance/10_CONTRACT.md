---
doc_id: workflow_centralflow2_octppusos.path.development_loop.steps.acceptance.contract
doc_type: action_contract_doc
topic: Acceptance contract
reading_chain:
- key: tools
  target: 15_TOOLS.md
  hop: next
  reason: 先读 acceptance 合同，再看工具。
---

# acceptance 阶段合同

- `acceptance` 不只是写报告；必须完成本地可控 bring-up、health、真实 witness 与 evidence closeout。
- `acceptance_matrix` 与 `acceptance_report` 固定落到当前 `mother_doc/acceptance/`。
- `acceptance-lint` 不通过时，不得宣称闭环完成。

## 下一跳列表
- [tools]：`15_TOOLS.md`
