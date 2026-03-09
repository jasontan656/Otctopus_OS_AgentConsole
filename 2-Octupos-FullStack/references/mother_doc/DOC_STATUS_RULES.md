# Mother_Doc Document Status Rules

适用阶段：`mother_doc`

## Core Rule

- `AGENTS.md` 之外的 `Mother_Doc` markdown 必须带有机械可读的状态块。
- 任意文档区块被 `mother_doc` 更新后，必须显式把对应区块标记为 `requires_development: true`。
- 文档级状态与区块级状态必须同时可读，供后续 `implementation` 与 `evidence` 机械探测。

## Fixed Shape

- 每个非 `AGENTS.md` 文档都必须包含：
  - `## Document Status`
  - `## Block Registry`
- `Document Status` 至少固定包含：
  - `doc_path`
  - `doc_role`
  - `doc_requires_development`
  - `doc_sync_status`
  - `last_updated_stage`
- `Block Registry` 至少固定包含：
  - `block_id`
  - `requires_development`
  - `sync_status`
  - `last_updated_stage`

## Default State

- `mother_doc` 更新后默认写入：
  - `doc_requires_development: true`
  - `doc_sync_status: pending_implementation`
  - `requires_development: true`
  - `sync_status: pending_implementation`
- 当前文档如果尚未细分多个区块，默认使用单一 `block_id: primary`。
