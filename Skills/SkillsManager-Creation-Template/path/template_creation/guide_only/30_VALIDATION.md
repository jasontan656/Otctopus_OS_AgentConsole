---
doc_id: skill_creation_template.path.template_creation.guide_only.validation
doc_type: topic_atom
topic: Validation for guide_only template creation
---

# Guide Only Validation

## 当前动作如何校验
- 结果目录只包含 `SKILL.md`、`agents/`。
- `SKILL.md` 顶层含 `skill_mode: guide_only`。
- 不存在 `path/`、`scripts/`、`references/`、`assets/`、`tests/`。
- 文案没有把“创建技能流程”误写成目标 skill 的业务目标。

## 当前动作完成后
- guide_only 线路到此闭环完成；若继续工作，应返回上层再选择新的行为线路。
