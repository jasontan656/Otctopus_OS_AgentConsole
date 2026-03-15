---
doc_id: skillsmanager_doc_structure.path.primary_flow.target_shape
doc_type: topic_atom
topic: Target skill shape resolution in the primary governance flow
anchors:
- target: 20_EXECUTION.md
  relation: implements
  direction: upstream
  reason: Shape resolution is the first execution step.
- target: 22_PATH_CHAINING.md
  relation: routes_to
  direction: downstream
  reason: Path chaining is checked after shape resolution.
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
- [路径衔接检查]：`22_PATH_CHAINING.md`
