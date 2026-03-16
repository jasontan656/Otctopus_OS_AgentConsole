---
doc_id: skillsmanager_govtargetskill.references.routing.task_routing
doc_type: topic_atom
topic: Task routing for SkillsManager-GovTargetSkill
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This routing note explains when to use the single analysis_loop workflow.
---

# Task Routing

## 何时使用本技能
- 当任务对象是“一个具体目标技能”，且目标是对它执行一次完整治理闭环时使用。
- 当任务要求同时覆盖现状调研、目标态收敛、实施计划、真实施工与验证收口时使用。

## 何时不要使用本技能
- 只是在讨论技能理论、命名、局部文案或单一文件小修时，不应强行进入本闭环。
- 没有明确目标技能时，不应触发本技能。

## 固定路由
- 当前技能只有一个入口：`path/analysis_loop/00_ANALYSIS_LOOP_ENTRY.md`
- 当前闭环主依托：`Functional-Analysis-Runtask`
- 当前治理约束源：
  - `SkillsManager-Creation-Template`
  - `Dev-ProjectStructure-Constitution`
  - `SkillsManager-RunStates-Manager`
  - `SkillsManager-Tooling-CheckUp`
  - `Dev-PythonCode-Constitution`
  - `Meta-keyword-first-edit`

## 固定治理顺序
- `SkillsManager-Creation-Template`
- `SkillsManager-Doc-Structure`
- `SkillsManager-RunStates-Manager`
- `SkillsManager-Tooling-CheckUp`
