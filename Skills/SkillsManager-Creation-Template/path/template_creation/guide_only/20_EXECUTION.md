---
doc_id: skill_creation_template.path.template_creation.guide_only.execution
doc_type: topic_atom
topic: Execution for guide_only template creation
reading_chain:
- key: validation
  target: 30_VALIDATION.md
  hop: next
  reason: Validation closes the guide_only action loop.
---

# Guide Only Execution

## 当前动作怎么做
1. 明确目标 skill 的真实业务主轴。
2. 先对照 `12_TEMPLATE.md` 确认目标技能的最终骨架。
3. 直接渲染完整 `SKILL.md` 正文。
4. 只补 `agents/openai.yaml`，不要再生成 `path/` 或 `scripts/`。
5. 确保完整说明直接留在 `SKILL.md`，不再把技能拆成外跳链路。

## 下一跳列表
- [validation]：`30_VALIDATION.md`
