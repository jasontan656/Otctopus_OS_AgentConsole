---
doc_id: skill_creation_template.path.template_creation.guide_only.template
doc_type: topic_atom
topic: Template blueprint for guide_only template creation
anchors:
- target: 10_CONTRACT.md
  relation: implements
  direction: upstream
  reason: The target-state template follows the guide_only contract.
- target: 20_EXECUTION.md
  relation: routes_to
  direction: downstream
  reason: Execution follows after the target-state template is confirmed.
---

# Guide Only Target State

## 根目录结构
```text
<skill-name>/
├── SKILL.md
└── agents/
    └── openai.yaml
```

## 门面目标
- `SKILL.md` 同时承担门面与完整技能正文。
- `SKILL.md` 不再外跳 `path/` 或 `scripts/`。
- 所有目标技能说明都直接留在 `SKILL.md` 内。

## 正文目标
- `SKILL.md` 直接承载完整技能约束、正文与执行说明。
- 当前模式不生成：
  - `path/`
  - `scripts/`

## 下一跳列表
- [execution]：`20_EXECUTION.md`
