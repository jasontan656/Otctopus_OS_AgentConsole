---
doc_id: meta_rootfile_manager.references_stages_push_flow
doc_type: topic_atom
topic: Push Workflow
anchors:
- target: ../../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# Push Workflow

1. Open the internal AGENTS human template.
2. Render the final visible contract surface from the internal source.
3. Strip internal frontmatter metadata and the `<part_A> ... </part_A>` shell.
4. Write only the rendered visible contract surface to the external AGENTS target.
5. Leave the internal split `Part B` domain blocks untouched.
