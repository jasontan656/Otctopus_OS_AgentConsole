---
doc_id: workflow_centralflow2_octppusos.path.development_loop.steps.mother_doc.steps.state_and_sync.contract
doc_type: action_contract_doc
topic: Mother doc state and sync contract
reading_chain:
- key: execution
  target: 20_EXECUTION.md
  hop: next
  reason: 进入当前步骤执行说明。
---

# state_and_sync 合同

## Contract Header
- `contract_name`: `workflow_centralflow2_mother_doc_state_and_sync_contract`
- `contract_version`: `1.0.0`
- `validation_mode`: `strict`
- `required_fields`:
  - `state_transition_rule`
  - `root_index_refresh_rule`
  - `client_mirror_sync_rule`
- `optional_fields`:
  - `notes`

- 文档状态只允许在受控转换中流动。
- 任何结构写入完成后都必须刷新根索引并同步 client mirror。

## 下一跳列表
- [execution]：`20_EXECUTION.md`
