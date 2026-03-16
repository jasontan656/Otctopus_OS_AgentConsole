---
doc_id: workflow_centralflow2_octppusos.path.development_loop.steps.mother_doc.steps.scope_and_runtime.contract
doc_type: action_contract_doc
topic: Mother doc scope and runtime contract
reading_chain:
- key: execution
  target: 20_EXECUTION.md
  hop: next
  reason: 进入当前步骤执行说明。
---

# scope_and_runtime 合同

## Contract Header
- `contract_name`: `workflow_centralflow2_mother_doc_scope_and_runtime_contract`
- `contract_version`: `1.0.0`
- `validation_mode`: `strict`
- `required_fields`:
  - `runtime_preflight`
  - `docs_root_rule`
  - `archive_read_rule`
- `optional_fields`:
  - `notes`

- 先运行 `target-runtime-contract`。
- 当前 `docs_root` 必须真实存在；不存在时拒绝服务或先 `target-scaffold`。
- 若存在编号归档，先读取最新归档再开始本轮回填。

## 下一跳列表
- [execution]：`20_EXECUTION.md`
