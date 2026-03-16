# AGENTS Payload Structure

本文件是 `AGENTS_payload_structure.json` 的人类可读镜像。

## 顶层结构
- `Part B` 顶层不是一个扁平 payload。
- `Part B` 聚合后的顶层 key 固定为：
  - `hook_identity`
  - `turn_start`
  - `runtime_constraints`
  - `execution_modes`
  - `repo_handoff`
  - `turn_end`

## 每个域 block 的固定形态
- `read_command_preview`
- `contract`

## 各域合同
- `hook_identity.contract`
  - `entry_role`
  - `contract_scope`
  - `secondary_contract_source`
- `turn_start.contract`
  - `required_actions`
- `runtime_constraints.contract`
  - `rules`
- `execution_modes.contract`
  - `READ_EXEC.goal`
  - `READ_EXEC.default_actions`
  - `WRITE_EXEC.goal`
  - `WRITE_EXEC.default_actions`
- `repo_handoff.contract`
  - `rules`
- `turn_end.contract`
  - `required_actions`

## 结构门禁
- 每个域必须独立成块。
- 每块必须带 `domain_id`，且 `domain_id` 必须是第一字段。
- 所有标准域必须完整出现一次。
- `WRITE_EXEC` 固定块必须保持标准值。

## 语义门禁
- `read_command_preview` 必须指向 `agents-domain-contract`。
- `contract` 只允许机器可执行语义。
- 禁止把 repo 摘要、技能顺序、技术栈说明、Markdown 叙事等软语义塞入 `Part B`。
