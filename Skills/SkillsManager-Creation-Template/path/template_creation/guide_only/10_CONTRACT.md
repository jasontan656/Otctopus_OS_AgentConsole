---
doc_id: skill_creation_template.path.template_creation.guide_only.contract
doc_type: topic_atom
topic: Contract for guide_only template creation
reading_chain:
- key: template
  target: 12_TEMPLATE.md
  hop: next
  reason: The target-state template follows the guide_only contract.
---

# Guide Only Contract

## 当前动作要完成什么
- 产出最小形态的 `guide_only` 模板。
- 该模板根目录只保留：`SKILL.md`、`agents/`。

## 当前动作必须满足什么
- 生成结果至少包含：
  - `SKILL.md`
  - `agents/openai.yaml`
- 不得生成：
  - `path/`
  - `scripts/`
  - `references/`
  - `assets/`
  - `tests/`
- `SKILL.md` 必须自己承载完整技能正文，不再外跳其他文档。

## 下一跳列表
- [template]：`12_TEMPLATE.md`
