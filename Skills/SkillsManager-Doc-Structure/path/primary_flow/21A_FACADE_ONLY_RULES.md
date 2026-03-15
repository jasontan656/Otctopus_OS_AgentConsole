---
doc_id: skillsmanager_doc_structure.path.primary_flow.facade_only_rules
doc_type: topic_atom
topic: Semantic rules for facade-only target skills
anchors:
- target: 21_TARGET_SHAPE.md
  relation: implements
  direction: upstream
  reason: This file refines the facade-only shape branch.
- target: 22_PATH_CHAINING.md
  relation: routes_to
  direction: downstream
  reason: Path chaining checks follow shape-specific semantic review.
---

# 最小门面型规则

## 语义审查规则
- 只允许 `SKILL.md` 承载完整正文，不允许再假设 `path/` 或 `scripts/`。
- `SKILL.md` 既是门面也是正文，因此不能再额外制造“外跳正文”。
- `agents/` 只承载 agent runtime config，不承载文档治理内容。

## 不合格信号
- 根目录出现 `path/`、`scripts/` 或任何额外主组织轴。
- `SKILL.md` 把读者继续送向外部链路。
- 规则被拆出到平级额外 markdown 文件中。

## 下一跳列表
- [路径衔接检查]：`22_PATH_CHAINING.md`
