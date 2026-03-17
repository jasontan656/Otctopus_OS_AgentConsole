---
doc_id: skillsmanager_python_subagentgov.references.routing.task_routing
doc_type: routing_guide
topic: Route Python subagent governance tasks to the correct CLI entry
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: The routing guide explains how to enter the governed toolbox.
---

# Task Routing

## 1. 进入时机
- 当任务目标是“对多个技能目录逐个做 Python 代码规范治理，并且每个技能都要保留独立 evidence / commit / mirror closeout”时，进入本技能。
- 当任务只想查看哪些技能会被纳入或排除时，使用 `list-targets`。
- 当任务是恢复中断治理、检查有哪些技能已经完成 closeout、还有哪些仍在跑时，使用 `status`。
- 当任务要核对单技能 subagent 实际 prompt 与结果文件落点时，使用 `render-prompt`。
- 当任务要真正启动或恢复治理主控时，使用 `govern`。

## 2. 命令路由
- `contract`
  - 用途：读取 machine-readable runtime contract，确认默认并发度、runtime artifact 路径规则、subagent 固定模型和 closeout 顺序。
- `directive --topic execution_boundary`
  - 用途：确认单技能 subagent 的可写边界、主控和 subagent 的职责切分，以及行为保持底线。
- `directive --topic runtime_layout`
  - 用途：确认 `Codex_Skill_Runtime/SkillsManager-Python-SubAgentGov/` 下每个技能的 evidence 布局。
- `directive --topic closeout_sequence`
  - 用途：确认 `verify -> git traceability -> mirror sync -> session closeout` 只能串行执行。
- `list-targets`
  - 用途：预览本轮会治理哪些技能，以及哪些技能因保留目录、缺少 `SKILL.md` 或自治理边界而被排除。
- `status`
  - 用途：读取当前 runtime 目录的 `pending/active/completed` 状态，不重新启动任何 subagent。
- `render-prompt --skill-name <name>`
  - 用途：为单技能生成当前主控会提交给 subagent 的固定 prompt 文件。
- `govern`
  - 用途：正式启动或恢复治理闭环。

## 3. 自治理路由
- 默认批量发现会排除 `SkillsManager-Python-SubAgentGov` 自身，因为运行中的主控不应被隐式自修改。
- 若确实要治理本技能自身，必须显式指定：
  - `govern --skill-name SkillsManager-Python-SubAgentGov`
  - 或 `render-prompt --skill-name SkillsManager-Python-SubAgentGov`
- 不要在 `all-scope` 批处理里同时把主控自身作为后台 subagent 目标。
