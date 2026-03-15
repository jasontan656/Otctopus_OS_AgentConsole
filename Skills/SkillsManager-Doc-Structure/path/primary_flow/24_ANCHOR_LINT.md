---
doc_id: skillsmanager_doc_structure.path.primary_flow.anchor_lint
doc_type: topic_atom
topic: Anchor lint in the primary governance flow
anchors:
- target: 23_DOC_WRITING.md
  relation: implements
  direction: upstream
  reason: Anchor lint follows doc-writing checks.
- target: 30_VALIDATION.md
  relation: routes_to
  direction: downstream
  reason: Final validation closes the governance flow.
---

# Anchor Lint

## 当前动作
- 抽取目标技能中所有 markdown frontmatter 的 `anchors`。
- 检查每个 `target` 是否存在。
- 检查 anchors 是否仍然连接在当前物理链路允许的范围内。

## 当前动作必须满足什么
- anchor 目标必须存在。
- anchor 不能把读者直接拉回已经被废弃的旧主组织轴。
- anchor 的作用是补充必要关系，而不是代替物理目录结构。

## 下一跳列表
- [最终校验]：`30_VALIDATION.md`
