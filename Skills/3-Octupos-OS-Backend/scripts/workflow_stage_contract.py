from __future__ import annotations
from workflow_policy_contract import PHASE_READ_POLICY
from workflow_template_contract import TEMPLATES
# contract_name: octopus_backend_workflow_stage_contract
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
        "objective": "Create or refine the directory-based mother doc until every required chapter exists, every replace_me is gone, and each stage has explicit goals, assertions, tests, and exit evidence. For iterative projects, mother_doc must first absorb the latest archived iteration history and current code reality before drafting the next round.",
        "required_outputs": [
            "docs/mother_doc/ directory",
            "fully filled project description chapters",
            "stage-by-stage goals/assertions/tests/exit evidence",
            "requirement atom inventory",
        ],
        "resident_docs": TOP_LEVEL_RESIDENT_DOCS,
        "stage_docs": [
            "docs/mother_doc/00_index.md",
            "docs/mother_doc/*",
            "docs/<latest_NN_slug>/* when present",
            "assets/templates/mother_doc/*",
            "Meta-code-graph-base context/resource when available",
        ],
        "graph_role": GRAPH_STAGE_ROLES["mother_doc"],
        "stage_entry_actions": [
            "if docs/mother_doc is missing, run mother-doc-init",
            "read docs/mother_doc/00_index.md",
            "if numbered archived docs directories exist, inspect the latest archived sibling before drafting the new iteration",
            "extract reusable target state, architecture decisions, blockers, and unfinished delivery deltas from the latest archive when present",
            "if the repo already has graph context, read it after archive review and before finalizing target state and architecture chapters",
            "run mother-doc-lint before leaving the stage",
        ],
        "stage_exit_gate": [
            "mother-doc-lint passes",
            "required chapter files exist",
            "no replace_me remains",
            "current mother_doc reflects inherited or superseded decisions from the latest archived iteration when such an archive exists",
            "08_dev_execution_plan.md defines stage_goal/stage_assertions/stage_tests/stage_exit_evidence for mother_doc/construction_plan/implementation/acceptance",
        ],
        "drop_on_stage_switch": [
            "mother_doc chapter drafting focus",
            "mother_doc template fill guidance",
        ],
    },
    "construction_plan": {
        "objective": "Read the completed mother doc design plan and write separate Execution_atom_plan&validation_packs for the AI to use during implementation and stage acceptance.",
        "required_outputs": [
            "docs/mother_doc/execution_atom_plan_validation_packs/ directory",
            "00_index.md plus numbered pack directories",
            "per-pack markdown anchors and machine-writeable manifests/ledgers",
        ],
        "resident_docs": TOP_LEVEL_RESIDENT_DOCS,
        "stage_docs": [
            "docs/mother_doc/*",
            "docs/mother_doc/08_dev_execution_plan.md",
            "docs/mother_doc/execution_atom_plan_validation_packs/00_index.md",
            "docs/mother_doc/execution_atom_plan_validation_packs/*",
            "assets/templates/execution_atom_plan_validation_packs/*",
            "Meta-code-graph-base context/resource when available",
            "codebase files only after mother-doc-lint passes",
        ],
        "graph_role": GRAPH_STAGE_ROLES["construction_plan"],
        "stage_entry_actions": [
            "reload the construction_plan stage checklist before reading execution packs",
            "read graph context before pack decomposition when the codebase already exists",
            "run construction-plan-init if docs/mother_doc/execution_atom_plan_validation_packs is missing",
            "run construction-plan-lint before leaving the stage",
        ],
        "stage_exit_gate": [
            "construction plan root is separate from mother doc design plan",
            "each numbered pack directory contains its own markdown anchors and machine files",
            "each pack defines inner development phases, validation slices, evidence writeback, and stage acceptance",
        ],
        "drop_on_stage_switch": [
            "mother_doc drafting focus",
            "construction_plan pack decomposition focus once the next stage checklist is loaded",
        ],
    },
    "implementation": {
        "objective": "Implement strictly according to the active execution atom pack, update its ledgers and evidence files pack-by-pack, and prove each test result matches design intent rather than only checking that a feature appears to work.",
        "required_outputs": [
            "code",
            "tests",
            "updated docs/mother_doc/execution_atom_plan_validation_packs/*",
            "ADR records when architecture decisions change",
        ],
        "resident_docs": TOP_LEVEL_RESIDENT_DOCS,
        "stage_docs": [
            "docs/mother_doc/*",
            "docs/mother_doc/execution_atom_plan_validation_packs/00_index.md",
            "docs/mother_doc/execution_atom_plan_validation_packs/<active_pack>/*",
            "concrete codebase files needed by the active pack and inner phase",
        ],
        "graph_role": GRAPH_STAGE_ROLES["implementation"],
        "stage_entry_actions": [
            "reload the implementation checklist and discard construction_plan decomposition notes that are not part of the active pack",
            "do not pull graph context into implementation focus; read concrete code and tests directly",
            "read only the active pack plus the mother_doc sections required by that pack",
            "run phase validation before moving to the next inner phase or pack",
        ],
        "stage_exit_gate": [
            "current pack and inner phase code/tests are on disk",
            "phase_status.jsonl and evidence_registry.json reflect sequencing changes and evidence refs",
            "relevant tests have already been run before moving to the next inner phase or pack",
            "the active pack explains why the changed result and tests satisfy design intent and stage acceptance",
        ],
        "drop_on_stage_switch": [
            "completed pack execution focus after acceptance starts",
            "implementation-only local debugging notes not required by acceptance evidence",
        ],
    },
    "acceptance": {
        "objective": "Bring the locally controllable runtime all the way to production-like readiness, then decide delivery against the mother doc and real witness evidence. Acceptance must finish local configuration, secrets resolution, resident services, health checks, simulated human interaction, and evidence writeback before closure; if the run is closed, archive mother_doc into the next numbered docs directory during evidence closeout.",
        "required_outputs": ["acceptance report", "acceptance matrix"],
        "resident_docs": TOP_LEVEL_RESIDENT_DOCS,
        "stage_docs": [
            "docs/mother_doc/*",
            "docs/mother_doc/execution_atom_plan_validation_packs/<active_or_completed_pack>/*",
            "docs/mother_doc/acceptance/*",
            "test outputs and live witness evidence",
        ],
        "graph_role": GRAPH_STAGE_ROLES["acceptance"],
        "stage_entry_actions": [
            "reload the acceptance checklist before reading acceptance artifacts",
            "discard implementation-only editing focus and keep only evidence needed for delivery judgement",
            "finish all locally controllable environment bring-up work before allowing needs_real_env",
            "resolve tokens, webhook secrets, owner allowlists, and runtime endpoints from local ignored env files or other non-git secret sources declared in 07_env_and_deploy.md and codebase AGENTS",
            "start and verify resident services inside the local WSL environment until healthz, webhook ingress, worker lanes, database, redis, mq, and outbound paths all expose observable runtime signals",
            "run at least one simulated human interaction through the real local stack and capture database, queue, redis, service, and outbound witness refs",
            "run acceptance-lint before final closure",
        ],
        "stage_exit_gate": [
            "acceptance-lint passes",
            "requirement-level evidence is linked",
            "all locally controllable configuration is applied and documented, including env files, tokens, webhook secrets, owner allowlists, and runtime endpoints",
            "local WSL resident services are running and have passed health and connectivity checks",
            "at least one simulated human usage flow has traversed the intended runtime path and produced real witness refs",
            "blocked states are explicit where witness is still unavailable",
            "graph-postflight is triggered during closeout after acceptance evidence is complete",
            "optional closeout archive happens only after evidence is complete",
        ],
        "drop_on_stage_switch": [
            "implementation editing focus",
            "unfinished stage-local hypotheses that are not backed by acceptance evidence",
        ],
    },
}
