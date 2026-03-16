---
doc_id: skillsmanager_runstates_manager.references.routing.task_routing
doc_type: topic_atom
topic: Task routing for SkillsManager-RunStates-Manager
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This routing note explains the stable entry points for runstate governance.
---

# Task Routing

## 何时使用本技能
- 当任务要判断一个目标技能是否需要 workflow/stage/skill-flow 运行态文件方法时，运行 `inspect`。
- 当任务要为一个目标技能补齐 runstate contract、三层 checklist 模板与成功判定模板时，运行 `scaffold`。
- 当任务要审计一个目标技能是否真正满足 runstate 方法要求时，运行 `audit`。
- 当任务处于技能创建或技能治理链内时，把本技能固定插入在 `SkillsManager-Tooling-CheckUp` 之前。

## 何时不要使用本技能
- 只是在治理 skill 骨架拓扑时，不应替代 `SkillsManager-Doc-Structure`。
- 只是在创建技能空骨架时，不应替代 `SkillsManager-Creation-Template`。
- 只是在治理 contract/tooling surface/tests 时，不应替代 `SkillsManager-Tooling-CheckUp`。

## 固定治理顺序
1. `SkillsManager-Creation-Template`
2. `SkillsManager-Doc-Structure`
3. `SkillsManager-RunStates-Manager`
4. `SkillsManager-Tooling-CheckUp`

## governed_type 收敛
- `not_applicable`
  - 目标技能不属于 workflow-bearing skill，不应伪造中间态要求。
- `workflow_runtime`
  - 目标技能具备 workflow/stage 两层运行态要求。
- `skill_flow_orchestrator`
  - 目标技能除了 workflow/stage 外，还必须治理技能编排 flow 级运行态，因此三层 checklist 全部必需。
