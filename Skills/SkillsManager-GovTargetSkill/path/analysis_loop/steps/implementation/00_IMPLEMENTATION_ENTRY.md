---
doc_id: skillsmanager_govtargetskill.path.analysis_loop.steps.implementation.entry
doc_type: action_entry_doc
topic: Implementation stage for governing a target skill
reading_chain:
- key: validation
  target: ../validation/00_VALIDATION_ENTRY.md
  hop: next
  reason: 完成真实落盘后，再进入验证收口。
---

# implementation

## 阶段目标
- 按已收敛的目标态直接改造目标技能的真实工件。

## 必须显式应用
- `Functional-Analysis-Runtask`：作为实施闭环的主线，不让计划与实施脱节。
- `Meta-keyword-first-edit`：优先采用删掉重写、整体替换、keyword first 替换；避免新增兼容壳。

## 若目标技能包含 CLI / runtime contract / tooling
- 使用 `SkillsManager-Tooling-CheckUp` 审计并收敛：
  - CLI surface
  - runtime contract
  - artifact policy
  - remediation gate

## 若目标技能包含 Python
- 使用 `Dev-PythonCode-Constitution` 约束：
  - 模块拆分
  - lint 规则
  - pytest 基线
  - runtime safety
  - 工具文档同步

## 阶段产物
- 已落盘修改
- 同步更新的文档 / contract / tooling / tests
- 与目标态一致的最终承载结构
- 回填 `stage_runtime_checklist`，并把 implementation 写回结果作为 `validation` 的唯一前置输入
