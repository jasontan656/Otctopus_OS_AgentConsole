---
doc_id: skillsmanager_govtargetskill.path.analysis_loop.steps.validation.entry
doc_type: action_entry_doc
topic: Validation stage for governing a target skill
reading_chain:
- key: global_validation
  target: ../../30_VALIDATION.md
  hop: next
  reason: 阶段验证完成后，再回到 analysis_loop 的全局退出条件。
---

# validation

## 阶段目标
- 验证目标技能已经从当前真实状态收敛到目标态，并记录残余风险。

## 必须显式应用
- `Functional-Analysis-Runtask`：整理验证证据与闭环结论。
- `SkillsManager-Tooling-CheckUp`：若目标技能有 tooling surface，则验证审计问题已闭合。
- `Dev-PythonCode-Constitution`：若触及 Python，则运行 lint / pytest 或说明未运行原因。

## 最低验证要求
- 结构验证：门面、references、workflow_path 是否与目标 profile 一致
- tooling 验证：contract、CLI、artifact policy 是否一致
- Python 验证：lint、pytest、runtime safety 是否满足当前改造范围
- 行为保持验证：原有有效用途未退化，且至少获得一个显式工程质量增益
