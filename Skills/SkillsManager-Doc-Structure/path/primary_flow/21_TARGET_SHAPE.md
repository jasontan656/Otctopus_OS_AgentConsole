---
doc_id: skillsmanager_doc_structure.path.primary_flow.target_shape
doc_type: topic_atom
topic: Target skill shape resolution in the primary governance flow
reading_chain:
- key: facade_only
  target: 21A_FACADE_ONLY_RULES.md
  hop: branch
  reason: Read the facade-only rule branch when the target is a minimal facade skill.
- key: linear_path
  target: 21B_LINEAR_PATH_RULES.md
  hop: branch
  reason: Read the linear-path rule branch when the target is a single-line path skill.
- key: compound_path
  target: 21C_COMPOUND_PATH_RULES.md
  hop: branch
  reason: Read the compound-path rule branch when the target is a compound workflow skill.
---

# 目标技能形态判定

## 当前动作
- 把目标技能先判定为三种抽象形态之一：
  - `最小门面型`
  - `单线路径型`
  - `复合路径型`
- 这一步只解决“目录应该长什么样”，不讨论业务语义。

## 当前动作必须满足什么
- `最小门面型`：根目录只允许 `SKILL.md / agents`。
- `单线路径型`：根目录只允许 `SKILL.md / path / agents / scripts`，每个入口进入后单线到底。
- `复合路径型`：根目录同样只允许 `SKILL.md / path / agents / scripts`，但入口内允许 workflow index 和步骤子闭环继续下沉。

## 下一跳列表
- [最小门面型规则]：`21A_FACADE_ONLY_RULES.md`
- [单线路径型规则]：`21B_LINEAR_PATH_RULES.md`
- [复合路径型规则]：`21C_COMPOUND_PATH_RULES.md`
