---
doc_id: meta_rootfile_manager.references_stages_scan_flow
doc_type: topic_atom
topic: Scan Workflow
anchors:
- target: ../../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# Scan Workflow

1. Load the active scan rule assets.
2. Restrict the active candidate set to the declared governed source paths.
3. Match governed files by exact filename rules and optional keyword rules.
4. Apply the disallowed path list.
5. Produce a human-reviewable managed target list.
6. Lint every discovered managed file against its structure template.
7. Output either stdout or a json result file under the corresponding `Codex_Skill_Runtime` folder.
