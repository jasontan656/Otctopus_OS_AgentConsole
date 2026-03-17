# 轻量化运行任务对象模型

## 核心对象
- `workspace_manifest.yaml`
  - 保存分析 id、目标范围、来源资产、执行模式、当前阶段、阶段状态、阶段产物路径与写回状态。
- `research/evidence_registry.yaml`
  - 保存证据入口、位置、用途与支持关系。
- `architect/assessment.yaml`
  - 保存 consumed stage reports、问题框架、判断链、should / should_not、未收口问题、架构裁决与 evidence refs。
- `preview/projection.yaml`
  - 保存 consumed stage reports、问题框架、推演链、未来形态、行为变化、失败模式、回滚阈值与 evidence refs。
- `design/decisions.yaml`
  - 保存 consumed stage reports、问题框架、decision chain、selected strategy、候选路径取舍、rewrite/replace/add 决策与 evidence refs。
- `impact/impact_map.yaml`
  - 保存 consumed stage reports、问题框架、判断链、direct / indirect / latent / regression 四类影响面、confidence、evidence gaps 与 evidence refs。
- `plan/milestone_packages.yaml`
  - 保存 planning basis、package derivation chain，以及每个 milestone package 的 stage gates、writeback targets、evidence expectations 与 exit signals。
- `implementation/turn_ledger.yaml`
  - 保存逐回合承接输入、preflight checks、实现动作、验证动作、状态裁决、写回目标与残余问题。
- `Codex_Skill_Runtime/Functional-Analysis-Runtask/NNN_task_slug/task_runtime.yaml`
  - 保存 AGENT 独立维护的运行态骨架、阶段 checklist、当前步骤、结束位置与任务闭合状态。

## 小型对象优先规则
- 证据、判断、计划、实现日志与状态必须拆开。
- 阶段沉淀文档负责汇总，不负责代替对象层。
- 阶段 lint 以对象层为主，不以聊天内容为校验依据。
- 每个对象都必须显式写出 consumed stage reports、问题框架或推导链；不得只保留空壳字段。

## 状态约束
- `workspace_manifest.yaml` 是当前阶段状态真相源。
- `task_runtime.yaml` 是并发门禁、阶段推进位置与任务闭合判定真相源。
- `plan/milestone_packages.yaml` 只能存在 0 或 1 个 `active` package。
- `implementation/turn_ledger.yaml` 中发生真实实现或验证时，必须携带 `evidence_refs`。
- 任一后阶段对象若没有引用前序正式产物，视为阶段承接链断裂，不能标记完成。
