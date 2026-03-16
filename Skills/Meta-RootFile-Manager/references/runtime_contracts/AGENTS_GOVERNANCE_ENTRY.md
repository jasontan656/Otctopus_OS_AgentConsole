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
  reason: Payload-only surgery remains one downstream slice of the unified AGENTS entry.
- target: ./AGENTS_content_structure.md
  relation: routes_to
  direction: downstream
  reason: Structure contract remains one downstream slice of the unified AGENTS entry.
---

# AGENTS Governance Entry

## Scope
- Use this entry for governed `AGENTS.md` work inside `Meta-RootFile-Manager`.
- `AGENTS.md` is the special dual-surface channel in this skill.
- Its governed mapping is formed by a single canonical `AGENTS_human.md`.
- Parent `AGENTS.md` plus parent payload semantics form an inherited surface for child `AGENTS` targets.
- The stable daily maintenance entry is `agents-maintain`; it decides target path, hierarchy level, `Part A` or embedded payload placement, duplicate/inheritance outcome, and centered-push writeback in one chain.
- `agents-payload-contract` no longer owns the daily maintenance mainline. It remains only for explicit payload-only surgery when the caller already knows the exact governed target and exact embedded payload scope.
- This entry covers three AGENTS-specific slices only:
  - asset governance
  - payload-only surgery contract
  - structure contract

## Downstream Slices
- [AGENTS 资产治理模型](./AGENTS_ASSET_GOVERNANCE.md)
  - Use for `external / internal canonical markdown` surface roles, ownership, and maintenance boundaries.
- [AGENTS Payload 治理合同](./AGENTS_PAYLOAD_GOVERNANCE_CONTRACT_human.md)
  - Use only when the task is already narrowed to embedded `Part B` payload surgery for a known governed target.
- [AGENTS 结构合同](./AGENTS_content_structure.md)
  - Use for required blocks, wrappers, frontmatter, JSON fence shape, and lint structure rules.

## Executable Entry
- For normal AGENTS maintenance, start from:
  `./.venv_backend_skills/bin/python Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-maintain --intent "<natural language request>" --json`
- That entry is mandatory for daily maintenance and must execute the mainline:
  1. rank the governed AGENTS targets that already exist
  2. classify the request into `Part A` or embedded payload scope
  3. run ancestor inheritance and duplicate gating before mutation
  4. update the internal `AGENTS_human.md` truth source
  5. centered-push external `Part A`
  6. run `lint`
- Use `agents-payload-contract --source-path "<external AGENTS path>" --json` only when the caller explicitly narrows the task to payload-only surgery for a known target and does not need target ranking or placement-gate selection.
- `lint` is a hard gate for parent-child AGENTS deduplication:
  - if parent `AGENTS.md` or parent payload already contains a phrase-equivalent semantic, child `AGENTS` surfaces must not repeat it
  - the check applies across `Part A` and payload in both directions
  - skill entries are excluded from this parent-child duplicate gate because the same skill may appear in different containers for different purposes
  - the fixed `execution_modes.WRITE_EXEC` standard reminder is also excluded because it is intentionally repeated across governed payloads
- `collect` is not part of the normal AGENTS maintenance loop. For `AGENTS.md`, it remains only as an exceptional reverse-sync or recovery path when the external file must be re-imported.
