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

## Purpose
- This is the single human entry for governed `AGENTS.md` work inside `Meta-RootFile-Manager`.
- Use this entry instead of choosing between multiple parallel AGENTS references in `SKILL.md`.

## When To Use
- You need to understand how governed `AGENTS.md` assets are organized.
- You need to change `AGENTS_machine.json` payload content.
- You need to validate the required `AGENTS.md` / `AGENTS_human.md` / `AGENTS_machine.json` structure.

## Downstream Slices
- [AGENTS 资产治理模型](./AGENTS_ASSET_GOVERNANCE.md)
  - Use when the task is about `external / internal human / internal machine` surface roles, ownership, or maintenance boundaries.
- [AGENTS Payload 治理合同](./AGENTS_PAYLOAD_GOVERNANCE_CONTRACT_human.md)
  - Use when the task changes `AGENTS_machine.json` payload semantics or needs the mandatory `$Meta-Enhance-Prompt -> writeback -> collect -> lint` workflow.
- [AGENTS 结构合同](./AGENTS_content_structure.md)
  - Use when the task is about required blocks, wrappers, frontmatter, JSON fence shape, or lint structure rules.

## Entry Rule
- Treat this file as the only human entry for AGENTS governance from `SKILL.md`.
- If the task changes `AGENTS_machine.json` payload content, the executable runtime entry is still:
  `./.venv_backend_skills/bin/python Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-payload-contract --source-path "<external AGENTS path>" --json`
