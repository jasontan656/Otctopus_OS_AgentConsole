---
doc_id: skill_creation_template.path.template_creation.executable.contract
doc_type: topic_atom
topic: Contract for executable_workflow_skill template creation
reading_chain:
- key: template
  target: 12_TEMPLATE.md
  hop: next
  reason: The target-state template follows the contract.
---

# Executable Workflow Contract

## 当前动作要完成什么
- 产出入口内承载复合 workflow 的 `executable_workflow_skill` 模板形态。

## 当前动作必须满足什么
- 输出至少包含：
  - `SKILL.md`
  - `path/primary_flow/00_PRIMARY_FLOW_ENTRY.md`
  - `path/primary_flow/10_CONTRACT.md`
  - `path/primary_flow/15_TOOLS.md`
  - `path/primary_flow/20_WORKFLOW_INDEX.md`
  - `path/primary_flow/30_VALIDATION.md`
  - `path/primary_flow/steps/step_01/`
  - `path/primary_flow/steps/step_02/`
  - `path/primary_flow/steps/step_03/`
  - `agents/openai.yaml`
  - `scripts/Cli_Toolbox.py`
  - `scripts/test_skill_layout.py`
- 复合步骤规则不能回填到门面。
- 不得生成：
  - `references/`
  - `assets/`
  - `tests/`

## 下一跳列表
- [template]：`12_TEMPLATE.md`
