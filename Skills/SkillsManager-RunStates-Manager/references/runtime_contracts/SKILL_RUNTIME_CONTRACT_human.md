---
doc_id: skillsmanager_runstates_manager.references.runtime_contracts.skill_runtime_contract
doc_type: topic_atom
topic: Runtime contract for SkillsManager-RunStates-Manager
---

# Skill Runtime Contract

- `inspect`：判定 target skill 的 `governed_type`，并返回该类型需要满足的 runstate 层级。
- `scaffold`：把 runstate contract、三层 checklist 模板与成功判定文档写入 target skill。
- `audit`：验证 target skill 是否已经具备、落盘并真正消费这些 runstate 方法。
- 本技能的新增位置固定为：
  - `SkillsManager-Creation-Template`
  - `SkillsManager-Doc-Structure`
  - `SkillsManager-RunStates-Manager`
  - `SkillsManager-Tooling-CheckUp`
- `Skills_runtime_checklist` 是 runstate contract schema 字段，不属于 `metadata.skill_profile`。
