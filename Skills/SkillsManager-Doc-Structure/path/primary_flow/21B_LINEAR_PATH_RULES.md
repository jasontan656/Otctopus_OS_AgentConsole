---
doc_id: skillsmanager_doc_structure.path.primary_flow.linear_path_rules
doc_type: topic_atom
topic: Semantic rules for linear-path target skills
anchors:
- target: 21_TARGET_SHAPE.md
  relation: implements
  direction: upstream
  reason: This file refines the linear-path shape branch.
- target: 22_PATH_CHAINING.md
  relation: routes_to
  direction: downstream
  reason: Path chaining checks follow shape-specific semantic review.
---

# 单线路径型规则

## 语义审查规则
- 根目录必须是 `SKILL.md / path / agents / scripts`。
- 允许存在多个入口，但任一入口进入后必须单线到底。
- 入口内部应只承载当前入口自己的闭环，不得再拆成平级分叉。

## 不合格信号
- 某个入口内又出现新的平级分流目录。
- 把多个后续层级文件平铺在同一目录，仅靠内联链接强控读序。
- 把规则重新拉回全局总则，而不是挂在当前入口链路上。

## 下一跳列表
- [路径衔接检查]：`22_PATH_CHAINING.md`
