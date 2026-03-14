---
doc_work_state: modified
doc_pack_refs: []
doc_id: workflow_centralflow1_octopusos.assets_templates_mother_doc_00_index
doc_type: example_doc
topic: Mother Doc Index
anchors:
- target: ../../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# Mother Doc Index

```python
# replace_me_fill_rule:
# - Replace every replace_me token in this file and linked chapters before the AI writes execution_atom_plan_validation_packs.
# - When the user fills this document via Q&A, answer with bounded options first, then rewrite this file with the chosen facts.
# - This file governs the mother_doc stage and defines how later stages should read the project description.
# - `08_dev_execution_plan.md` is the design-phase plan inside mother_doc; it is not the AI execution packs root.
# - Remove this guidance block after drafting.
```

## 1. 项目说明入口
- project_name: replace_me
- project_scope: replace_me
- delivery_definition: replace_me
- primary_user_or_operator: replace_me

## 2. 阶段读取规则
| stage_id | stage_goal | stage_read_scope | stage_exit_signal |
|---|---|---|---|
| `mother_doc` | `replace_me` | `replace_me` | `replace_me` |
| `construction_plan` | `replace_me` | `replace_me` | `replace_me` |
| `implementation` | `replace_me` | `replace_me` | `replace_me` |
| `acceptance` | `replace_me` | `replace_me` | `replace_me` |

## 3. 章节索引
| file | purpose | owner_stage |
|---|---|---|
| `00_index.md` | `replace_me` | `mother_doc` |
| `01_target_state.md` | `replace_me` | `mother_doc` |
| `02_architecture_overview.md` | `replace_me` | `mother_doc` |
| `03_runtime_flow.md` | `replace_me` | `mother_doc` |
| `04_stack_decisions.md` | `replace_me` | `mother_doc` |
| `05_domain_contracts.md` | `replace_me` | `mother_doc` |
| `06_acceptance_contract.md` | `replace_me` | `acceptance` |
| `07_env_and_deploy.md` | `replace_me` | `implementation` |
| `08_dev_execution_plan.md` | `replace_me` | `mother_doc` |
| `09_regression_baseline.md` | `replace_me` | `implementation` |
| `10_observability_and_evidence.md` | `replace_me` | `acceptance` |
| `11_risks_and_blockers.md` | `replace_me` | `mother_doc` |

## 4. construction_plan 进入条件
- mother_doc_lint_status: replace_me
- no_replace_me_remaining: replace_me
- user_alignment_or_qna_status: replace_me
- design_phase_plan_ready: replace_me
