# 轻量化运行任务对象模型

## 核心对象
- `workspace_manifest.yaml`
  - 保存分析 id、目标范围、来源资产、执行模式、当前阶段、阶段状态、阶段产物路径与写回状态。
- `research/evidence_registry.yaml`
  - 保存证据入口、位置、用途与支持关系。
- `architect/assessment.yaml`
  - 保存 should / should_not 与结构变更评估结论。
- `preview/projection.yaml`
  - 保存未来形态、行为变化、失败模式与回滚阈值。
- `design/decisions.yaml`
  - 保存设计思路、抽象重整、增删改策略与 rewrite/replace/add 决策。
- `impact/impact_map.yaml`
  - 保存 direct / indirect / latent / regression 四类影响面。
- `plan/milestone_packages.yaml`
  - 保存 milestone package 合同。
- `implementation/turn_ledger.yaml`
  - 保存逐回合实现、验证、状态裁决与残余问题。
- `Codex_Skill_Runtime/Functional-Analysis-Runtask/NNN_task_slug/task_runtime.yaml`
  - 保存 AGENT 独立维护的运行态骨架、阶段 checklist、当前步骤、结束位置与任务闭合状态。

## 小型对象优先规则
- 证据、判断、计划、实现日志与状态必须拆开。
- 阶段沉淀文档负责汇总，不负责代替对象层。
- 阶段 lint 以对象层为主，不以聊天内容为校验依据。

## 状态约束
- `workspace_manifest.yaml` 是当前阶段状态真相源。
- `task_runtime.yaml` 是并发门禁、阶段推进位置与任务闭合判定真相源。
- `plan/milestone_packages.yaml` 只能存在 0 或 1 个 `active` package。
- `implementation/turn_ledger.yaml` 中发生真实实现或验证时，必须携带 `evidence_refs`。
