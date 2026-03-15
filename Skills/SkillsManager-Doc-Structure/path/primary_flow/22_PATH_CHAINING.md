---
doc_id: skillsmanager_doc_structure.path.primary_flow.path_chaining
doc_type: topic_atom
topic: Path chaining rules in the primary governance flow
anchors:
- target: 21_TARGET_SHAPE.md
  relation: implements
  direction: upstream
  reason: Path chaining follows shape resolution.
- target: 22A_NEXT_HOP_RULES.md
  relation: routes_to
  direction: downstream
  reason: Path chaining semantic rules are read before node-writing checks.
---

# 路径衔接检查

## 当前动作
- 检查 `SKILL.md` 是否只指向 `path/00_SKILL_ENTRY.md`。
- 检查 `path/00_SKILL_ENTRY.md` 是否只暴露入口层，而不是越级暴露深层正文。
- 检查每个入口目录是否物理下沉到自己的链路，而不是多个阶段文件平铺在同一层靠内联控制。

## 当前动作必须满足什么
- 单线路径型内部不能再出现子目录分叉。
- 复合路径型必须把 workflow index 和 step 目录物理下沉。
- 任何入口内的下一跳都必须是当前步骤真正要看的内容。

## 下一跳列表
- [下一跳规则]：`22A_NEXT_HOP_RULES.md`
- [单线路径链路规则]：`22B_LINEAR_CHAIN_RULES.md`
- [复合路径链路规则]：`22C_COMPOUND_CHAIN_RULES.md`
