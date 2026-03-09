# Implementation Log Rules

适用阶段：`implementation`

## Core Rule

- 每次批量文档更新进入实现后，都必须追加一条 implementation batch 日志。
- 对比顺序固定为：
  1. 先读当前代码
  2. 再读更新后的 `Mother_Doc`
  3. 以差异作为本轮实现与修复的依据

## Log Location

- 日志固定落在：
  - `Octopus_OS/Mother_Doc/Mother_Doc/common/development_logs/implementation_batches.md`

## Entry Semantics

- 日志承担项目内部的开发时间线与版本控制语义。
- 即使项目内部文档不区分版本，implementation batch 仍必须按追加方式保留。
- 首次无代码时，也必须写日志；此时日志描述“当前文档领先于空代码基线”的状态。

## Status Flip Rule

- 当实现已经覆盖对应文档变更时，必须把对应文档与区块的 `requires_development` 从 `true` 翻回 `false`，并把 `sync_status` 改为 `aligned`。
