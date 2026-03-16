---
doc_id: meta_rootfile_manager.references_runtime_contracts_agents_payload_governance_contract
doc_type: topic_atom
topic: AGENTS Payload Governance Contract
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# AGENTS Payload Governance Contract

- This contract is no longer the daily AGENTS maintenance entry. It remains only for payload-only surgery when the caller already knows the exact governed target and exact embedded `Part B` scope.
- Entry command:
  `./.venv_backend_skills/bin/python Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-payload-contract --source-path "<external AGENTS path>" --json`
- Use this entry whenever the task changes any governed embedded `Part B` payload in `AGENTS_human.md`.
- The workflow is mandatory:
  1. Load the target-specific payload contract.
  2. Load `$Meta-Enhance-Prompt` contract plus its `skill-directive` entry.
  3. Compress the user request into the smallest precise payload semantics only.
  4. Edit only the governed embedded `Part B` payload scope inside `AGENTS_human.md`.
  5. Run `lint` for the same external `AGENTS.md`.
- If the task still needs target ranking, `Part A` vs payload placement, inheritance review, or centered-push execution, use `agents-maintain` instead of this narrow contract.

## Hard Constraints
- Do not add reminders, process notes, extra routing, or extra obligations beyond the user request.
- Do not treat oral wording as permission to expand hidden intent.
- If the intended shape is still unclear after normalization, inspect sibling payload entries for style only; do not invent new semantics.
- If a skill name plus minimal description is already recorded in `default_meta_skill_order`, do not repeat or paraphrase that reminder in other payload fields.
- For any payload that carries `execution_modes.WRITE_EXEC`, keep the standard fixed block:
  - `goal`: `default to full-coverage edits for the intended change`
  - `default_actions`: `["Default to full-coverage edits, proactively explore to avoid omissions, and use the meta skill stack to strengthen the result."]`
  - This repeated reminder is intentional and is exempt from the parent-child duplicate gate.
