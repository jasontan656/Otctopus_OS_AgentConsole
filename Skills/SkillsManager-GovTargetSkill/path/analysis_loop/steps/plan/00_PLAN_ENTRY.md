---
doc_id: skillsmanager_govtargetskill.path.analysis_loop.steps.plan.entry
doc_type: action_entry_doc
topic: Plan stage for governing a target skill
reading_chain:
- key: implementation
  target: ../implementation/00_IMPLEMENTATION_ENTRY.md
  hop: next
  reason: 先排定迁移顺序与验证路径，再进入真实施工。
---

# plan

## 阶段目标
- 生成一个以最终形态为导向的实施计划，而不是兼容式修补清单。

## 必须显式应用
- `Functional-Analysis-Runtask`：组织迁移顺序、影响面、验证路径与风险边界。
- `Meta-keyword-first-edit`：把计划中的改造动作收敛成删除、替换、重写优先，而不是新增包裹层。

## 若目标技能包含 CLI / Python
- 必须先经过 `SkillsManager-RunStates-Manager`，确认 runstate scaffold、成功判定与模板要求已经成立，再进入 tooling 审计与整改顺序。
- 必须把 `SkillsManager-Tooling-CheckUp` 纳入审计与整改顺序。
- 必须把 `Dev-PythonCode-Constitution` 纳入 lint、pytest、runtime safety 与文档同步计划。

## 阶段产物
- 实施步骤
- 影响面与依赖链
- 验证清单
- 风险边界与回滚判断
- 回填 `stage_runtime_checklist`，并把 plan 产物作为 `implementation` 唯一允许消费的施工输入
