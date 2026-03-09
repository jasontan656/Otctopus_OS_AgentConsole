# Mother_Doc Document Status Rules

适用阶段：`mother_doc`

## Core Rule

- `AGENTS.md` 之外的 `Mother_Doc` markdown 必须带有机械可读的状态块。
- 状态机固定只使用三种生命周期值：
  - `modified`
  - `developed`
  - `null`
- 任意文档区块被 `mother_doc` 更新后，必须通过本地 `git` 差异判定脚本刷新生命周期状态。
- 文档级状态与区块级状态必须同时可读，供后续 `implementation` 与 `evidence` 机械探测。

## Fixed Shape

- 每个非 `AGENTS.md` 文档都必须包含：
  - `## Document Status`
  - `## Block Registry`
- `Document Status` 至少固定包含：
  - `doc_path`
  - `doc_role`
  - `doc_lifecycle_state`
  - `doc_requires_development`
  - `doc_sync_status`
  - `last_updated_stage`
- `Block Registry` 至少固定包含：
  - `block_id`
  - `lifecycle_state`
  - `requires_development`
  - `sync_status`
  - `last_updated_stage`

## Lifecycle Semantics

- `modified`
  - `mother_doc` 发生覆盖写回，且本地 `git` 差异显示该文档已变更。
  - `requires_development: true`
- `developed`
  - 当前文档对应能力已经完成代码落盘，并在 `evidence` 阶段完成闭环回写。
  - `requires_development: false`
- `null`
  - 当前文档暂时不适用、有效正文为空，或仍停留在空占位状态。
  - `requires_development: false`
- 当前文档如果尚未细分多个区块，默认使用单一 `block_id: primary`。
