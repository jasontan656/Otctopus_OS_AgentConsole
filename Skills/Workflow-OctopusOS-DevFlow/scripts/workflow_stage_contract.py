from __future__ import annotations
from workflow_policy_contract import PHASE_READ_POLICY
from workflow_template_contract import TEMPLATES
# contract_name: octopus_devflow_workflow_stage_contract
# contract_version: 1.2.0
# validation_mode: strict
# required_fields:
#   - STAGES
# optional_fields:
#   - TEMPLATES
TOP_LEVEL_RESIDENT_DOCS = PHASE_READ_POLICY["top_level_resident_docs"]
GRAPH_STAGE_ROLES = {
    "mother_doc": {"read_policy": "read graph context in this stage to reconcile existing code reality with the mother doc", "update_policy": "do_not_update_graph_in_this_stage"},
    "construction_plan": {"read_policy": "read graph context in this stage to decompose execution atom packs against real module boundaries and dependencies", "update_policy": "do_not_update_graph_in_this_stage"},
    "implementation": {"read_policy": "do_not_read_graph_as_a_stage_artifact; implementation must read concrete code directly", "update_policy": "do_not_update_graph_in_this_stage"},
    "acceptance": {"read_policy": "do_not_read_graph_as_acceptance_evidence", "update_policy": "after acceptance evidence is complete, run graph-postflight to refresh downstream maintenance context"},
}
STAGES = {
    "mother_doc": {
        "objective": "Create or refine the tree-first directory-based mother doc until every required chapter entry exists, every replace_me is gone, each atomic doc carries frontmatter state, and each stage has explicit goals, assertions, tests, and exit evidence. For iterative projects, mother_doc must first absorb the latest archived iteration history and current code reality before drafting the next round.",
        "required_outputs": [
            "Development_Docs/<module_dir>/mother_doc/ directory",
            "fully filled project description chapters",
            "atomic docs with doc_work_state/doc_pack_refs frontmatter",
            "stage-by-stage goals/assertions/tests/exit evidence",
            "requirement atom inventory",
        ],
        "resident_docs": TOP_LEVEL_RESIDENT_DOCS,
        "stage_docs": [
            "Development_Docs/<module_dir>/mother_doc/00_index.md",
            "Development_Docs/<module_dir>/mother_doc/*",
            "Development_Docs/<module_dir>/<latest_NN_slug>/* when present",
            "assets/templates/mother_doc/*",
            "Meta-code-graph-base context/resource when available",
        ],
        "graph_role": GRAPH_STAGE_ROLES["mother_doc"],
        "stage_entry_actions": [
            "run target-runtime-contract before reading or writing stage artifacts",
            "confirm docs_root through Dev-OctopusOS-Constitution-ProjectStructure when the project has already fixed a custom development-doc container",
            "if Development_Docs/<module_dir>/mother_doc is missing, run target-scaffold",
            "read Development_Docs/<module_dir>/mother_doc/00_index.md",
            "if numbered archived docs directories exist, inspect the latest archived sibling before drafting the new iteration",
            "if execution packs already exist, treat them as the current task-pack lineage rather than creating a disconnected second pack tree",
            "extract reusable target state, architecture decisions, blockers, and unfinished delivery deltas from the latest archive when present",
            "if the repo already has graph context, read it after archive review and before finalizing target state and architecture chapters",
            "run mother-doc-lint before leaving the stage",
        ],
        "stage_exit_gate": [
            "mother-doc-lint passes",
            "required chapter entries exist as files or 00_index-based directories",
            "no replace_me remains",
            "atomic docs expose doc_work_state/doc_pack_refs frontmatter",
            "current mother_doc reflects inherited or superseded decisions from the latest archived iteration when such an archive exists",
            "08_dev_execution_plan.md defines stage_goal/stage_assertions/stage_tests/stage_exit_evidence for mother_doc/construction_plan/implementation/acceptance",
        ],
        "drop_on_stage_switch": [
            "mother_doc chapter drafting focus",
            "mother_doc template fill guidance",
        ],
    },
    "construction_plan": {
        "objective": "Read the completed mother doc design plan plus current modified docs, then write separate Execution_atom_plan&validation_packs for the AI to use during implementation and stage acceptance without severing the mother doc requirement source.",
        "required_outputs": [
            "Development_Docs/<module_dir>/mother_doc/execution_atom_plan_validation_packs/ directory",
            "00_index.md plus numbered pack directories",
            "per-pack markdown anchors and machine-writeable manifests/ledgers",
            "source_mother_doc_refs carried by each numbered pack",
        ],
        "resident_docs": TOP_LEVEL_RESIDENT_DOCS,
        "stage_docs": [
            "Development_Docs/<module_dir>/mother_doc/* with doc_work_state=modified|planned|ref as needed",
            "Development_Docs/<module_dir>/mother_doc/08_dev_execution_plan.md",
            "Development_Docs/<module_dir>/mother_doc/execution_atom_plan_validation_packs/00_index.md",
            "Development_Docs/<module_dir>/mother_doc/execution_atom_plan_validation_packs/*",
            "assets/templates/execution_atom_plan_validation_packs/*",
            "Meta-code-graph-base context/resource when available",
            "codebase files only after mother-doc-lint passes",
        ],
        "graph_role": GRAPH_STAGE_ROLES["construction_plan"],
        "stage_entry_actions": [
            "run target-runtime-contract before touching execution packs",
            "reload the construction_plan stage checklist before reading execution packs",
            "read graph context before pack decomposition when the codebase already exists",
            "decompose only the current modified mother_doc slice into new or updated packs; do not batch-flip unrelated docs to planned",
            "reuse existing execution_atom_plan_validation_packs when present; run target-scaffold only when the pack root is missing",
            "run construction-plan-lint before leaving the stage",
        ],
        "stage_exit_gate": [
            "construction plan root is separate from mother doc design plan",
            "each numbered pack directory contains its own markdown anchors and machine files",
            "each numbered pack declares source_mother_doc_refs for implementation readback",
            "each pack defines inner development phases, validation slices, evidence writeback, and stage acceptance",
        ],
        "drop_on_stage_switch": [
            "mother_doc drafting focus",
            "construction_plan pack decomposition focus once the next stage checklist is loaded",
        ],
    },
    "implementation": {
        "objective": "Implement strictly according to the active execution atom pack, read only the mother_doc atoms explicitly referenced by that pack, update its ledgers and evidence files pack-by-pack, and prove each test result matches design intent rather than only checking that a feature appears to work.",
        "required_outputs": [
            "code",
            "tests",
            "updated Development_Docs/<module_dir>/mother_doc/execution_atom_plan_validation_packs/*",
            "linked mother_doc docs advanced from planned to developed when the active pack is implemented and locally validated",
            "ADR records when architecture decisions change",
        ],
        "resident_docs": TOP_LEVEL_RESIDENT_DOCS,
        "stage_docs": [
            "Development_Docs/<module_dir>/mother_doc/execution_atom_plan_validation_packs/00_index.md",
            "Development_Docs/<module_dir>/mother_doc/execution_atom_plan_validation_packs/<active_pack>/*",
            "Development_Docs/<module_dir>/mother_doc/<source_mother_doc_refs declared by active_pack>",
            "Development_Docs/<module_dir>/mother_doc/<ref docs when explicitly needed>",
            "concrete codebase files needed by the active pack and inner phase",
        ],
        "graph_role": GRAPH_STAGE_ROLES["implementation"],
        "stage_entry_actions": [
            "run target-runtime-contract before reading the active pack so implementation stays attached to the current task lineage",
            "reload the implementation checklist and discard construction_plan decomposition notes that are not part of the active pack",
            "do not pull graph context into implementation focus; read concrete code and tests directly",
            "read only the active pack plus the source_mother_doc_refs declared by that pack; do not sweep unrelated modified docs into implementation focus",
            "run phase validation before moving to the next inner phase or pack",
        ],
        "stage_exit_gate": [
            "current pack and inner phase code/tests are on disk",
            "phase_status.jsonl and evidence_registry.json reflect sequencing changes and evidence refs",
            "relevant tests have already been run before moving to the next inner phase or pack",
            "linked mother_doc docs can advance from planned to developed only after local implementation plus validation complete",
            "the active pack explains why the changed result and tests satisfy design intent and stage acceptance",
        ],
        "drop_on_stage_switch": [
            "completed pack execution focus after acceptance starts",
            "implementation-only local debugging notes not required by acceptance evidence",
        ],
    },
    "acceptance": {
        "objective": "Bring the locally controllable runtime all the way to production-like readiness, then decide delivery against the mother doc and real witness evidence. Acceptance must finish local configuration, secrets resolution, resident services, health checks, simulated human interaction, evidence writeback, and graph postflight before mother_doc docs advance into ref state; if the run is closed, archive mother_doc into the next numbered docs directory during evidence closeout.",
        "required_outputs": ["acceptance report", "acceptance matrix"],
        "resident_docs": TOP_LEVEL_RESIDENT_DOCS,
        "stage_docs": [
            "Development_Docs/<module_dir>/mother_doc/* with doc_work_state=developed|ref as needed",
            "Development_Docs/<module_dir>/mother_doc/execution_atom_plan_validation_packs/<active_or_completed_pack>/*",
            "Development_Docs/<module_dir>/mother_doc/acceptance/*",
            "test outputs and live witness evidence",
        ],
        "graph_role": GRAPH_STAGE_ROLES["acceptance"],
        "stage_entry_actions": [
            "run target-runtime-contract before reading acceptance artifacts so delivery remains attached to the current task lineage",
            "reload the acceptance checklist before reading acceptance artifacts",
            "discard implementation-only editing focus and keep only evidence needed for delivery judgement",
            "finish all locally controllable environment bring-up work before allowing needs_real_env",
            "resolve project-declared local secrets, credentials, and runtime endpoints from ignored env files or other non-git secret sources declared in 07_env_and_deploy.md and project AGENTS",
            "start and verify the project-declared resident runtime surfaces until health, dependency connectivity, and observable runtime signals are available",
            "run at least one simulated human or operator path through the real local stack and capture logs, files, service traces, UI witness, or delivery refs as the project requires",
            "run acceptance-lint before final closure",
        ],
        "stage_exit_gate": [
            "acceptance-lint passes",
            "requirement-level evidence is linked",
            "all locally controllable configuration is applied and documented, including env files, credentials, startup settings, and runtime endpoints declared by the project",
            "local runtime surfaces are running and have passed health and connectivity checks required by the project",
            "at least one simulated usage flow has traversed the intended runtime path and produced real witness refs",
            "blocked states are explicit where witness is still unavailable",
            "graph-postflight is triggered during closeout after acceptance evidence is complete",
            "linked mother_doc docs advance from developed to ref only after acceptance evidence and graph postflight are complete",
            "optional closeout archive happens only after evidence is complete",
        ],
        "drop_on_stage_switch": [
            "implementation editing focus",
            "unfinished stage-local hypotheses that are not backed by acceptance evidence",
        ],
    },
}
