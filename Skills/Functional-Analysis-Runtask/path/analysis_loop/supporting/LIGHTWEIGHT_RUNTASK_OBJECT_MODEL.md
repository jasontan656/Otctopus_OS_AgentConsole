# 轻量化运行任务对象模型

## 核心对象
- `workspace_manifest.yaml`
  - 保存分析 id、目标范围、来源资产、执行模式、当前阶段、阶段状态与写回状态。
- `research/evidence_registry.yaml`
  - 保存证据入口、位置、用途与支持关系。
- `design/architecture_decisions.yaml`
  - 保存架构收敛判断、沿用旧资产关系、目标形态与阶段门禁。
- `plan/slices.yaml`
  - 保存最小切片合同。
- `implementation/turn_ledger.yaml`
  - 保存逐回合实现、验证、状态裁决与残余问题。

## 小型对象优先规则
- 证据、判断、计划、实现日志与状态必须拆开。
- 阶段沉淀文档负责汇总，不负责代替对象层。
- 阶段 lint 以对象层为主，不以聊天内容为校验依据。

## 状态约束
- `workspace_manifest.yaml` 是当前阶段状态真相源。
- `plan/slices.yaml` 只能存在 0 或 1 个 `active` 切片。
- `implementation/turn_ledger.yaml` 中发生真实实现或验证时，必须携带 `evidence_refs`。
