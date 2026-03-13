---
doc_id: meta_rootfile_manager.references_runtime_contracts_skill_runtime_contract
doc_type: topic_atom
topic: Skill Runtime Contract
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# Skill Runtime Contract

- skill_name: `Meta-RootFile-Manager`
- runtime_kind: `channelized_root_file_governance`

## Summary
- This skill governs workspace root files through file-type channels.
- `AGENTS.md` remains a special `A/B` channel.
- Every other supported root file type uses a single internal mapped copy.

## Managed Asset Rule
- External root files remain the files actually consumed by repos.
- Skill-internal assets are mapping versions stored under `assets/managed_targets/AI_Projects/...`.
- Non-`AGENTS.md` managed assets must use explicit governed-mapping filenames instead of the raw external filename.

## Runtime Source Rule
- `rules/scan_rules.json` is the channel registry truth source.
- `target-contract` must return the resolved channel and managed asset paths for the requested external path.
