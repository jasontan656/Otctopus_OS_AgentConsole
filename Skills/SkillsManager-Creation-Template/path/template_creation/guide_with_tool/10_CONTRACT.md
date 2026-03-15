---
doc_id: skill_creation_template.path.template_creation.guide_with_tool.contract
doc_type: topic_atom
topic: Contract for guide_with_tool template creation
reading_chain:
- key: template
  target: 12_TEMPLATE.md
  hop: next
  reason: The target-state template follows the contract.
---

# Guide With Tool/Lint Contract

## 当前动作要完成什么
- 产出带 `path/`、`scripts/` 能力面与单线入口闭环的 `guide_with_tool` 模板形态。
- 该形态允许多个平行入口，但每个入口进入后必须单线到底。
- `scripts/` 可以承载工具、lint，或两者之一；不要求每个目标技能都同时具备两者。

## 当前动作必须满足什么
- 输出至少包含：
  - `SKILL.md`
  - `path/primary_flow/00_PRIMARY_FLOW_ENTRY.md`
  - `path/primary_flow/10_CONTRACT.md`
  - `path/primary_flow/15_TOOLS.md`
  - `path/primary_flow/20_EXECUTION.md`
  - `path/primary_flow/30_VALIDATION.md`
  - `agents/openai.yaml`
  - `scripts/Cli_Toolbox.py`
  - `scripts/test_skill_layout.py`
- 门面保持极简，不回填深规则正文。
- 入口层可以后续扩展为多入口索引，但任何入口内部都不得再次分叉。
- `15_TOOLS.md` 节点承载当前入口自己的 tool/lint 说明；若该技能只有 lint，也仍然在这里写清楚。
- 不得生成：
  - `references/`
  - `assets/`
  - `tests/`

## 下一跳列表
- [template]：`12_TEMPLATE.md`
