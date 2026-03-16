---
doc_id: workflow_centralflow2_octppusos.path.development_loop.steps.mother_doc.steps.lint_and_exit.contract
doc_type: action_contract_doc
topic: Mother doc lint and exit contract
reading_chain:
- key: execution
  target: 20_EXECUTION.md
  hop: next
  reason: 进入当前步骤执行说明。
---

# lint_and_exit 合同

## Contract Header
- `contract_name`: `workflow_centralflow2_mother_doc_lint_and_exit_contract`
- `contract_version`: `1.0.0`
- `validation_mode`: `strict`
- `required_fields`:
  - `lint_gate`
  - `placeholder_cleanup_rule`
- `optional_fields`:
  - `notes`

- 未通过 `mother-doc-lint` 不得进入 `construction_plan`。
- 不得保留 `replace_me` 与未完成的阶段断言。

## 下一跳列表
- [execution]：`20_EXECUTION.md`
