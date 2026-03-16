---
doc_id: skillsmanager_govtargetskill.path.analysis_loop.workflow_index
doc_type: workflow_index_doc
topic: Analysis loop workflow index for governing a target skill
reading_chain:
- key: research_baseline
  target: steps/research_baseline/00_RESEARCH_BASELINE_ENTRY.md
  hop: next
  reason: 先建立目标技能当前真实状态与证据基线。
---

# analysis_loop 阶段索引

## 固定阶段顺序
1. `research_baseline`
2. `architecture_convergence`
3. `plan`
4. `implementation`
5. `validation`

## 当前闭环规则
- 阶段顺序固定，不跳步进入实现。
- `Skills_runtime_checklist` 约束技能编排 flow；`workflow_runtime_checklist` 约束 analysis_loop；`stage_runtime_checklist` 约束当前阶段内原子步骤。
- 每个阶段都继续依托 `Functional-Analysis-Runtask` 组织证据与收敛动作。
- 每个阶段继续前，都必须先消费上一阶段产物与对应 checklist 回填结果。
- 若目标技能包含 CLI 或 Python 工件，tooling 与 Python 治理链必须在后续阶段显式启用。
- `SkillsManager-RunStates-Manager` 固定在 `SkillsManager-Tooling-CheckUp` 之前执行。

## 下一跳列表
- [research_baseline]：`steps/research_baseline/00_RESEARCH_BASELINE_ENTRY.md`
