---
doc_id: meta_rootfile_manager.references_stages_scan_rules
doc_type: topic_atom
topic: Scan Rules
anchors:
- target: ../../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# Scan Rules

- Scan remains a discovery-only phase.
- Scan must not create or overwrite managed copies.
- Scan must restrict the active governed result set to the exact external source paths declared in the scan rule asset.
- Scan must read blacklists and keyword rules from external scan rule assets.
- `AGENTS.md` is currently the only governed filename that requires structure lint.
- If a new governed filename is added later, a matching structure template must exist before scan may pass.
- Missing structure templates are hard errors, not warnings.
