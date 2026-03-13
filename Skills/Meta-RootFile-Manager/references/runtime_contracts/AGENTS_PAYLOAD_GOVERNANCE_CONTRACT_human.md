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

- Entry command:
  `./.venv_backend_skills/bin/python Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-payload-contract --source-path "<external AGENTS path>" --json`
- Use this entry whenever the task changes any governed `AGENTS_machine.json` payload.
- The workflow is mandatory:
  1. Load the target-specific payload contract.
  2. Load `$Meta-Enhance-Prompt` contract plus its `skill-directive` entry.
  3. Compress the user request into the smallest precise payload semantics only.
  4. Edit only the governed `AGENTS_machine.json` payload scope.
  5. Run `collect` for the same external `AGENTS.md` to re-render `AGENTS_human.md`.
  6. Run `lint` for the same external `AGENTS.md`.

## Hard Constraints
- Do not add reminders, process notes, extra routing, or extra obligations beyond the user request.
- Do not treat oral wording as permission to expand hidden intent.
- If the intended shape is still unclear after normalization, inspect sibling payload entries for style only; do not invent new semantics.
- If a skill name plus minimal description is already recorded in `default_meta_skill_order`, do not repeat or paraphrase that reminder in other payload fields.
