---
doc_id: meta_rootfile_manager.references_stages_scaffold_flow
doc_type: topic_atom
topic: Scaffold Workflow
anchors:
- target: ../../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# Scaffold Workflow

1. Receive the user-specified external target directory.
2. Choose one governed file kind or all currently supported kinds.
3. Create the external skeleton files.
4. Create the first matching internal `治理映射模版` files.
5. Update rule assets and sync the installed skill.
6. Validate the dry-run result before real overwrite is accepted.
