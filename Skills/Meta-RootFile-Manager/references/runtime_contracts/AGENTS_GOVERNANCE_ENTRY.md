---
doc_id: meta_rootfile_manager.references_runtime_contracts_agents_governance_entry
doc_type: topic_atom
topic: AGENTS Governance Entry
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
- target: ./AGENTS_ASSET_GOVERNANCE.md
  relation: routes_to
  direction: downstream
  reason: Asset governance remains one downstream slice of the unified AGENTS entry.
- target: ./AGENTS_PAYLOAD_GOVERNANCE_CONTRACT_human.md
  relation: routes_to
  direction: downstream
  reason: Payload writeback workflow remains one downstream slice of the unified AGENTS entry.
- target: ./AGENTS_content_structure.md
  relation: routes_to
  direction: downstream
  reason: Structure contract remains one downstream slice of the unified AGENTS entry.
---

# AGENTS Governance Entry

## Scope
- Use this entry for governed `AGENTS.md` work inside `Meta-RootFile-Manager`.
- It covers three AGENTS-specific slices only:
  - asset governance
  - payload governance
  - structure contract

## Downstream Slices
- [AGENTS 资产治理模型](./AGENTS_ASSET_GOVERNANCE.md)
  - Use for `external / internal human / internal machine` surface roles, ownership, and maintenance boundaries.
- [AGENTS Payload 治理合同](./AGENTS_PAYLOAD_GOVERNANCE_CONTRACT_human.md)
  - Use for `AGENTS_machine.json` payload semantics and the mandatory `$Meta-Enhance-Prompt -> writeback -> collect -> lint` workflow.
- [AGENTS 结构合同](./AGENTS_content_structure.md)
  - Use for required blocks, wrappers, frontmatter, JSON fence shape, and lint structure rules.

## Executable Entry
- If the task changes `AGENTS_machine.json` payload content, start from:
  `./.venv_backend_skills/bin/python Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-payload-contract --source-path "<external AGENTS path>" --json`
