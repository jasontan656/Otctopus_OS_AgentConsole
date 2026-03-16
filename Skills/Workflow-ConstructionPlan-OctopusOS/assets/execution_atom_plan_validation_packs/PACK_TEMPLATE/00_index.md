---
doc_id: workflow_centralflow2_octppusos.assets_templates_execution_atom_plan_validation_packs_pack_template_00_index
doc_type: example_doc
topic: Execution Atom Pack Index
anchors:
- target: ../../../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# Execution Atom Pack Index

```python
# replace_me_fill_rule:
# - Replace every replace_me token before this pack can be executed.
# - This is the human-facing facade for one execution atom pack. Keep it concise and traceable.
# - The machine-facing files in this same folder are the source for scripts and structured writeback.
# - Remove this guidance block after drafting.
```

## 1. Pack Identity
- pack_id: replace_me
- design_step_id: replace_me
- plan_kind: replace_me
- pack_state: replace_me
- execution_eligible: replace_me
- state_sync_eligible: replace_me
- reusable_as_official_plan: false
- pack_goal: replace_me
- current_progress_state: replace_me

## 2. Read/Write Contract
- human_anchor_docs:
  - `01_scope_and_intent.md`
  - `02_inner_dev_phases.md`
  - `03_validation_and_writeback.md`
- machine_anchor_files:
  - `pack_manifest.yaml`
  - `inner_phase_plan.json`
  - `phase_status.jsonl`
  - `evidence_registry.json`

## 下一跳列表
- [pack 正文与 machine files 由同目录下其余模板文件组成。]
