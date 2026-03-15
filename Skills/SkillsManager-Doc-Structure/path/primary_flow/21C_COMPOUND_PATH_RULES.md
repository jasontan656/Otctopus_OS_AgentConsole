---
doc_id: skillsmanager_doc_structure.path.primary_flow.compound_path_rules
doc_type: topic_atom
topic: Semantic rules for compound-path target skills
anchors:
- target: 21_TARGET_SHAPE.md
  relation: implements
  direction: upstream
  reason: This file refines the compound-path shape branch.
- target: 22_PATH_CHAINING.md
  relation: routes_to
  direction: downstream
  reason: Path chaining checks follow shape-specific semantic review.
---

# 复合路径型规则

## 语义审查规则
- 根目录必须是 `SKILL.md / path / agents / scripts`。
- 入口进入后允许先到 `workflow index`，再进入步骤级闭环。
- 每个步骤都必须物理下沉到自己的 step 目录，而不是把步骤正文平铺在 workflow 层。

## 不合格信号
- 复合技能缺少 `workflow index`，直接把所有 step 内容压在一层。
- step 没有自己的局部闭环，只是一个大段混写正文。
- workflow index 直接承担 step 级正文。

## 下一跳列表
- [路径衔接检查]：`22_PATH_CHAINING.md`
