---
doc_id: skill_creation_template.asset.stage_index_template
doc_type: template_doc
topic: Template for the staged skill stage index document
anchors:
- target: README_STAGE_SYSTEM_TEMPLATE.md
  relation: pairs_with
  direction: lateral
  reason: The stage index works with the stage system template.
- target: ../SKILL_TEMPLATE_STAGED.md
  relation: implements
  direction: upstream
  reason: The staged facade template routes readers into the stage index.
---

# Stage Index Template

## 顶层常驻文档
- `references/governance/SKILL_DOCSTRUCTURE_POLICY.md`
- `references/governance/SKILL_EXECUTION_RULES.md`
- `references/tooling/Cli_Toolbox_USAGE.md`

## 统一入口
- `<repo-root>/.venv_backend_skills/bin/python <repo-root>/Skills/${skill_name}/scripts/Cli_Toolbox.py stage-checklist --stage <stage> --json`
- `<repo-root>/.venv_backend_skills/bin/python <repo-root>/Skills/${skill_name}/scripts/Cli_Toolbox.py stage-doc-contract --stage <stage> --json`
- `<repo-root>/.venv_backend_skills/bin/python <repo-root>/Skills/${skill_name}/scripts/Cli_Toolbox.py stage-command-contract --stage <stage> --json`
- `<repo-root>/.venv_backend_skills/bin/python <repo-root>/Skills/${skill_name}/scripts/Cli_Toolbox.py stage-graph-contract --stage <stage> --json`

## 阶段集合
| stage_id | objective | checklist | doc_contract | command_contract | graph_contract | exit_signal |
|---|---|---|---|---|---|---|
| `replace_me` | `replace_me` | `replace_me` | `replace_me` | `replace_me` | `replace_me` | `replace_me` |

## resident docs 规则
- 跨阶段只保留顶层常驻文档。
- resident docs 负责维持全局边界，不负责承载某阶段细节。

## 切换规则
- 当前阶段完成后，显式丢弃上一阶段 checklist、stage docs、模板填写上下文与临时 focus。
- 下一阶段开始前，重新读取该阶段四类合同。
