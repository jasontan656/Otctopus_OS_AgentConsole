# Implementation Log Rules

适用阶段：`evidence`

## Core Rule

- implementation batch 只允许在 `evidence` 阶段追加。
- 允许的触发形态只有两种：
  - 纯 `evidence` 回合
  - `implementation -> evidence` 联动回合

## Input Rule

- implementation 必须先产出已对齐的文档范围、代码范围与差异摘要。
- evidence 读取这些 implementation 结果后，再把它们写成 implementation batch。
- `mother_doc` 阶段不得直接写该日志。

## Log Location

- 日志固定落在：
  - `Octopus_OS/Mother_Doc/docs/Mother_Doc/common/development_logs/implementation_batches.md`

## Entry Semantics

- 每条 implementation batch 必须绑定：
  - 对应的文档范围
  - 对应的代码范围
  - `read_code_then_read_updated_docs` 的比较顺序
- `implementation_batches.md` 不是规划文档，而是 implementation 完成后的摘要时间线。
- 日志只保留摘要，不复制具体实现 diff 或文件级修改内容。
- 每条日志的 `summary` 必须等于同轮 Git 提交 message；具体修改内容交由 Git / GitHub 追踪。
