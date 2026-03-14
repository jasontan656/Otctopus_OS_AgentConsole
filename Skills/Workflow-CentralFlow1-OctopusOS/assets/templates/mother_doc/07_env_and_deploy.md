---
doc_work_state: modified
doc_pack_refs: []
doc_id: workflow_centralflow1_octopusos.assets_templates_mother_doc_07_env_and_deploy
doc_type: example_doc
topic: 07 Env And Deploy
anchors:
- target: ../../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# 07 Env And Deploy

```python
# replace_me_fill_rule:
# - Replace every replace_me token with real environment, deployment, and operator assumptions.
# - Keep this file explicit enough to reveal which blockers are local versus truly external.
# - This file is written in mother_doc and exercised heavily during implementation.
# - Remove this guidance block after drafting.
```

## 1. 本地与远端环境
- local_runtime_contract: replace_me
- required_env_vars_or_secrets: replace_me
- external_dependencies: replace_me

## 2. 部署与上线条件
- deployment_shape: replace_me
- rollout_constraints: replace_me
- rollback_entrypoints: replace_me

## 3. 阻塞判定
- what_counts_as_needs_input: replace_me
- what_counts_as_needs_real_env: replace_me
- what_must_be_solved_locally_first: replace_me
