---
doc_id: meta_rootfile_manager.references_runtime_contracts_agents_payload_archive
doc_type: topic_atom
topic: AGENTS_PAYLOAD_ARCHIVE
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# AGENTS_PAYLOAD_ARCHIVE

Human mirror for `AGENTS_PAYLOAD_ARCHIVE.json`.

```json
{
  "status": "archived_payload_and_contract_seed",
  "archived_on": "2026-03-10",
  "purpose": "Preserve payload history and current contract seeds so future tooling can rebuild from static assets instead of deleted code.",
  "canonical_governance_contract": {
    "external_agents_shape": "part_a_only",
    "internal_agents_human_shape": "part_a_plus_part_b",
    "internal_agents_machine_shape": "part_b_only",
    "part_a_allows": [
      "human-readable entry commands",
      "language rules",
      "managed boundary notes",
      "multi-agent handling notes"
    ],
    "part_b_allows": [
      "structured runtime payload fields",
      "execution mode objects",
      "must-use rules",
      "forbidden patterns",
      "turn contracts"
    ],
    "governance_priority": "AGENTS_ASSET_GOVERNANCE.md overrides archived historical snapshots when they conflict"
  },
  "runtime_source_policy": {
    "runtime_rule_source": "CLI_JSON",
    "audit_fields_are_not_primary_runtime_instructions": true,
    "path_metadata_is_not_action_guidance": true
  },
  "default_meta_skill_order": [
    "$Meta-Semantic-Collection (understand human expressed meaning and update it according to its rule)",
    "$Meta-Enhance-Prompt (strengthen user intent and understand the real need)",
    "$Meta-Impact-Investigation (ensure the coverage of user request before conclusion or edits)",
    "$Meta-Architect-MindModel (think from the architecture level and reject one-sided thinking)",
    "$Meta-reasoningchain (project the future shape to align the target state)",
    "$Meta-keyword-first-edit (prefer delete > replace > add when editing)",
    "$Meta-Agent-Browser (applicable only when the task is frontend or browser-related)"
  ],
  "root_agents_payload_snapshot": {
    "entry_role": "workspace_root_runtime_entry",
    "runtime_source_policy": {
      "runtime_rule_source": "CLI_JSON",
      "audit_fields_are_not_primary_runtime_instructions": true,
      "path_metadata_is_not_action_guidance": true
    },
    "default_meta_skill_order": [
      "$Meta-Semantic-Collection (understand human expressed meaning and update it according to its rule)",
      "$Meta-Enhance-Prompt (strengthen user intent and understand the real need)",
      "$Meta-Impact-Investigation (ensure the coverage of user request before conclusion or edits)",
      "$Meta-Architect-MindModel (think from the architecture level and reject one-sided thinking)",
      "$Meta-reasoningchain (project the future shape to align the target state)",
      "$Meta-keyword-first-edit (prefer delete > replace > add when editing)",
      "$Meta-Agent-Browser (applicable only when the task is frontend or browser-related)"
    ],
    "turn_start_actions": [
      "validate root AGENTS exists",
      "classify the turn as READ_EXEC or WRITE_EXEC",
      "apply the default meta sequence before concrete execution"
    ],
    "runtime_constraints": [
      "treat CLI JSON as the primary runtime rule source",
      "do not use audit markdown as the primary execution guide",
      "choose READ_EXEC or WRITE_EXEC by actual write intent, not by file type alone",
      "when a concrete repo path becomes active, load that repo-local contract before repo-specific write, lint, or Git actions"
    ],
    "execution_modes": {
      "READ_EXEC": {
        "goal": "answer, inspect, classify, or route without changing files",
        "default_actions": [
          "prefer direct CLI contract output over opening markdown rule files",
          "open extra files only when the direct contract still leaves a real gap"
        ]
      },
      "WRITE_EXEC": {
        "goal": "default to full-coverage edits for the intended change",
        "default_actions": [
          "Default to full-coverage edits, proactively explore to avoid omissions, and use the meta skill stack to strengthen the result."
        ]
      }
    },
    "repo_local_contract_handoff": [
      "if work enters a repo with its own AGENTS runtime entry, load that repo-local target-contract before following repo-specific rules",
      "repo-local contract may add stricter lint, delivery, or Git rules for that repo only",
      "when repo-local and workspace-root rules overlap, keep the workspace-root boundary and add the repo-local concrete duties"
    ],
    "forbidden_primary_runtime_pattern": [
      "Do not treat audit markdown paths as the main runtime instructions.",
      "Do not require the model to open a chain of markdown files just to learn the next skill to use.",
      "Do not emit only path metadata when the real need is direct action guidance."
    ],
    "turn_end_actions": [
      "print TURN_END guardrails",
      "defer repo-specific lint or Git duties to the concrete repo-local contract when applicable"
    ]
  },
  "repo_agents_payload_templates": {
    "generic_repo": {
      "entry_role": "repo_runtime_entry",
      "runtime_source_policy": {
        "runtime_rule_source": "CLI_JSON",
        "audit_fields_are_not_primary_runtime_instructions": true,
        "path_metadata_is_not_action_guidance": true
      },
      "default_meta_skill_order": [
        "$meta-github-operation (after any write to Codex_Skills_Mirror, commit-and-push the mirror repo for Git traceability; Git push is not a substitute for syncing the codex installation directory)",
        "$SkillsManager-Mirror-To-Codex (edit skills only in Codex_Skills_Mirror mirror paths, never directly in the codex installation directory; after editing, use Push for already-installed skills and Install for newly created skills)",
        "$SkillsManager-Creation-Template ( should be considered to imply if there is no specific user request on how skill should be created (prioritize user request than template) )",
        "$skill-creator (for skill standard formatter to ensure codex reads it properly, do not use its template for skill creation)",
        "$Dev-PythonCode-Constitution (for Python-related skill lints )"
      ],
      "peer_summary_policy_template": {
        "available": "<bool>",
        "relation": "same_level_summary",
        "read_policy": "<dynamic>",
        "guidance": "<dynamic>"
      },
      "turn_start_actions": [
        "use the returned target contract JSON as the runtime rule source",
        "classify the turn as READ_EXEC or WRITE_EXEC"
      ],
      "runtime_constraints": [
        "treat CLI JSON as the primary runtime rule source",
        "do not use audit markdown as the primary execution guide",
        "stay within the concrete repo-local boundary defined by this payload",
        "choose READ_EXEC or WRITE_EXEC by actual write intent, not by file type alone"
      ],
      "execution_modes": {
        "READ_EXEC": {
          "goal": "answer, inspect, classify, or route without changing files",
          "default_actions": [
            "prefer direct CLI contract output over opening markdown rule files",
            "open extra files only when the direct contract still leaves a real gap"
          ]
        },
        "WRITE_EXEC": {
          "goal": "default to full-coverage edits for the intended change",
          "default_actions": [
            "Default to full-coverage edits, proactively explore to avoid omissions, and use the meta skill stack to strengthen the result."
          ]
        }
      },
      "forbidden_primary_runtime_pattern": [
        "Do not treat audit markdown paths as the main runtime instructions.",
        "Do not require the model to open a chain of markdown files just to learn the next skill to use.",
        "Do not emit only path metadata when the real need is direct action guidance."
      ],
      "turn_end_actions": [
        "follow repo-specific lint or Git duties only when they are explicitly listed in this payload"
      ],
      "repo_name": "<dynamic>"
    },
    "Codex_Skills_Mirror_snapshot": {
      "entry_role": "repo_runtime_entry",
      "runtime_source_policy": {
        "runtime_rule_source": "CLI_JSON",
        "audit_fields_are_not_primary_runtime_instructions": true,
        "path_metadata_is_not_action_guidance": true
      },
      "default_meta_skill_order": [
        "$meta-github-operation (after any write to Codex_Skills_Mirror, commit-and-push the mirror repo for Git traceability; Git push is not a substitute for syncing the codex installation directory)",
        "$SkillsManager-Mirror-To-Codex (edit skills only in Codex_Skills_Mirror mirror paths, never directly in the codex installation directory; after editing, use Push for already-installed skills and Install for newly created skills)",
        "$SkillsManager-Creation-Template ( should be considered to imply if there is no specific user request on how skill should be created (prioritize user request than template) )",
        "$skill-creator (for skill standard formatter to ensure codex reads it properly, do not use its template for skill creation)",
        "$Dev-PythonCode-Constitution (for Python-related skill lints )"
      ],
      "peer_summary_policy": {
        "available": false,
        "relation": "same_level_summary",
        "read_policy": "not_available",
        "guidance": "same-level README.md is not available for this target"
      },
      "turn_start_actions": [
        "use the returned target contract JSON as the runtime rule source",
        "classify the turn as READ_EXEC or WRITE_EXEC",
        "if the turn will write Codex_Skills_Mirror, plan same-turn Constitution lint and Git traceability from the start",
        "if the turn will edit a skill, treat the mirror copy in Codex_Skills_Mirror as the only editable source and determine whether downstream sync must be Push or Install"
      ],
      "runtime_constraints": [
        "treat CLI JSON as the primary runtime rule source",
        "do not use audit markdown as the primary execution guide",
        "stay within the concrete repo-local boundary defined by this payload",
        "choose READ_EXEC or WRITE_EXEC by actual write intent, not by file type alone",
        "when this repo is written, keep same-turn Constitution lint and Git traceability in scope",
        "for skill changes, edit the mirror copy under Codex_Skills_Mirror and never directly edit the codex installation directory",
        "after skill edits, use SkillsManager-Mirror-To-Codex Push for already-installed skills or Install for newly created skills before closing the turn"
      ],
      "execution_modes": {
        "READ_EXEC": {
          "goal": "answer, inspect, classify, or route without changing files",
          "default_actions": [
            "prefer direct CLI contract output over opening markdown rule files",
            "open extra files only when the direct contract still leaves a real gap"
          ]
        },
        "WRITE_EXEC": {
          "goal": "default to full-coverage edits for the intended change",
          "default_actions": [
            "Default to full-coverage edits, proactively explore to avoid omissions, and use the meta skill stack to strengthen the result."
          ]
        }
      },
      "forbidden_primary_runtime_pattern": [
        "Do not treat audit markdown paths as the main runtime instructions.",
        "Do not require the model to open a chain of markdown files just to learn the next skill to use.",
        "Do not emit only path metadata when the real need is direct action guidance."
      ],
      "turn_end_actions": [
        "run Constitution lint on the concrete Codex_Skills_Mirror target root",
        "if the turn edited a skill, complete SkillsManager-Mirror-To-Codex Push or Install before closing the turn",
        "if the turn wrote Codex_Skills_Mirror, complete same-turn commit-and-push before closing the turn"
      ],
      "repo_name": "Codex_Skills_Mirror"
    }
  }
}
```
