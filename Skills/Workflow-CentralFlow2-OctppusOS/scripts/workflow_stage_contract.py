from __future__ import annotations

from workflow_policy_contract import PHASE_READ_POLICY


TOP_LEVEL_RESIDENT_DOCS = PHASE_READ_POLICY["top_level_resident_docs"]

GRAPH_STAGE_ROLES = {
    "mother_doc": {
        "read_policy": "read graph context in this stage to reconcile existing code reality with the mother doc",
        "update_policy": "do_not_update_graph_in_this_stage",
    },
    "construction_plan": {
        "read_policy": "read graph context in this stage to decompose execution atom packs against real module boundaries and dependencies",
        "update_policy": "do_not_update_graph_in_this_stage",
    },
    "implementation": {
        "read_policy": "do_not_read_graph_as_a_stage_artifact; implementation must read concrete code directly",
        "update_policy": "do_not_update_graph_in_this_stage",
    },
    "acceptance": {
        "read_policy": "do_not_read_graph_as_acceptance_evidence",
        "update_policy": "after acceptance evidence is complete, run graph-postflight to refresh downstream maintenance context",
    },
}

STAGES = {
    "mother_doc": {
        "objective": "Create or refine the protocol-driven mother doc tree under <docs_root>/mother_doc as the only write source of truth. The mother_doc flow must first lock runtime, then analyze impact, then reconcile code graph reality, then decide whether the tree should extend vertically, branch horizontally, reuse current nodes, migrate nodes, or delete nodes, and only then perform the smallest safe write slice. Any newly introduced vertical layer or horizontal branch family must be registered in the skill before it is used by real mother_doc docs, and every such addition must be reusable for sibling semantics rather than serving a single ad hoc node. The root index must be auto-regenerated from the current folder tree, then the tree is synced into <target_root>/Client_Applications/mother_doc as the viewer mirror copy.",
        "required_outputs": [
            "<docs_root>/mother_doc/ directory",
            "<target_root>/Client_Applications/mother_doc mirror refreshed from <docs_root>/mother_doc",
            "00_index.md auto-generated root folder graph",
            "protocol-governed atomic docs with status, viewer, and anchor frontmatter",
            "free-growth document tree that remains script-scannable",
        ],
        "resident_docs": TOP_LEVEL_RESIDENT_DOCS,
        "stage_docs": [
            "<docs_root>/mother_doc/00_index.md",
            "<docs_root>/mother_doc/*",
            "<docs_root>/<latest_NN_slug>/* when present",
            "path/development_loop/steps/mother_doc/templates/mother_doc/*",
            "path/development_loop/steps/mother_doc/templates/agents/*",
            "path/development_loop/steps/mother_doc/templates/REQUIREMENT_ATOM_TEMPLATE.md",
            "Meta-code-graph-base context/resource when available",
        ],
        "graph_role": GRAPH_STAGE_ROLES["mother_doc"],
        "stage_entry_actions": [
            "run target-runtime-contract before reading or writing stage artifacts",
            "confirm docs_root through Dev-ProjectStructure-Constitution when the project has already fixed a custom development-doc container",
            "if <docs_root>/mother_doc is missing, run target-scaffold",
            "run Meta-Impact-Investigation in WRITE_INTENT mode before deciding any mother_doc write scope",
            "if the repo already has substantive code, check Meta-code-graph-base runtime first and initialize it when missing",
            "read <docs_root>/mother_doc/00_index.md",
            "if numbered archived docs directories exist, inspect the latest archived sibling before drafting the new iteration",
            "if execution packs already exist, treat them as the current task-pack lineage rather than creating a disconnected second pack tree",
            "extract reusable target state, architecture decisions, blockers, and unfinished delivery deltas from the latest archive when present",
            "if the repo already has graph context, read it after archive review and before finalizing target state and architecture chapters",
            "decide how deep to read the current mother_doc tree based on impact, anchors, and graph context rather than blindly sweeping the full tree",
            "before creating a new vertical layer or horizontal branch family, register it in the skill and confirm it is reusable for sibling semantics",
            "before any real write, reduce the current change into the smallest mother_doc slice that can still close the intended semantic move",
            "after any mother_doc structural write, run mother-doc-refresh-root-index so 00_index.md is regenerated from folders only",
            "after the root index refresh, run mother-doc-sync-client-copy so the Client_Applications viewer mirror is force-overwritten from the Development_Docs source tree",
            "run mother-doc-lint before leaving the stage",
        ],
        "stage_exit_gate": [
            "mother-doc-lint passes",
            "<docs_root>/mother_doc remains the only write source of truth and the client mirror has been refreshed after this turn's mother_doc edits",
            "00_index.md exists as the fixed root placeholder and is refreshed from the current folder structure",
            "no replace_me remains",
            "atomic docs expose the minimal frontmatter + anchor protocol",
            "any newly introduced vertical layer or horizontal branch family has been registered in the skill and is reusable beyond a single node",
            "current mother_doc reflects inherited or superseded decisions from the latest archived iteration when such an archive exists",
        ],
        "drop_on_stage_switch": [
            "mother_doc chapter drafting focus",
            "mother_doc template fill guidance",
        ],
    },
    "construction_plan": {
        "objective": "Read the completed protocol-driven mother doc tree, crawl the full document set, locate the current modified docs, understand their anchor-linked context, then generate an official Execution_atom_plan&validation_packs tree for implementation and stage acceptance. Preview skeletons are allowed only as non-executable display scaffolds and must never be mistaken for official plans.",
        "required_outputs": [
            "<docs_root>/mother_doc/execution_atom_plan_validation_packs/ directory",
            "00_index.md plus numbered pack directories",
            "per-pack markdown anchors and machine-writeable manifests/ledgers",
            "source_mother_doc_refs carried by each numbered pack",
            "pack decomposition decided from the current modified mother_doc slice rather than a fixed planning document path",
        ],
        "resident_docs": TOP_LEVEL_RESIDENT_DOCS,
        "stage_docs": [
            "<docs_root>/mother_doc/* with doc_work_state=modified|planned|ref as needed",
            "<docs_root>/mother_doc/execution_atom_plan_validation_packs/00_index.md",
            "<docs_root>/mother_doc/execution_atom_plan_validation_packs/*",
            "path/development_loop/steps/construction_plan/templates/execution_atom_plan_validation_packs/*",
            "Meta-code-graph-base context/resource when available",
            "codebase files only after mother-doc-lint passes",
        ],
        "graph_role": GRAPH_STAGE_ROLES["construction_plan"],
        "stage_entry_actions": [
            "run target-runtime-contract before touching execution packs",
            "reload the construction_plan stage checklist before reading execution packs",
            "read graph context before pack decomposition when the codebase already exists",
            "scan the complete mother_doc tree instead of assuming a fixed planning document path",
            "use doc_work_state=modified as the seed set, then cluster those docs with their anchor-linked context into packs; do not batch-flip unrelated docs to planned",
            "classify any existing execution_atom_plan_validation_packs root before reuse: preview_skeleton must be replaced, accepted/retired plans must not be reused as fresh construction input",
            "only an official_plan with plan_state=planned_unused or in_execution and current pack coverage may remain as the current round plan root",
            "run target-scaffold only when the mother_doc root itself is missing; construction plan roots are initialized explicitly, not as a side effect of mother_doc scaffold",
            "run construction-plan-lint before leaving the stage",
        ],
        "stage_exit_gate": [
            "construction plan root is separate from mother doc design plan",
            "construction plan root is explicitly classified as official_plan or preview_skeleton",
            "each numbered pack directory contains its own markdown anchors and machine files",
            "each numbered pack declares source_mother_doc_refs for implementation readback",
            "each pack defines inner development phases, validation slices, evidence writeback, and stage acceptance",
            "official packs were derived from the current modified mother_doc slice rather than copied from a single planning doc",
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
            "updated <docs_root>/mother_doc/execution_atom_plan_validation_packs/*",
            "linked mother_doc docs advanced from planned to developed when the active pack is implemented and locally validated",
            "ADR records when architecture decisions change",
        ],
        "resident_docs": TOP_LEVEL_RESIDENT_DOCS,
        "stage_docs": [
            "<docs_root>/mother_doc/execution_atom_plan_validation_packs/00_index.md",
            "<docs_root>/mother_doc/execution_atom_plan_validation_packs/<active_pack>/*",
            "<docs_root>/mother_doc/<source_mother_doc_refs declared by active_pack>",
            "<docs_root>/mother_doc/<ref docs when explicitly needed>",
            "concrete codebase files needed by the active pack and inner phase",
        ],
        "graph_role": GRAPH_STAGE_ROLES["implementation"],
        "stage_entry_actions": [
            "run target-runtime-contract before reading the active pack so implementation stays attached to the current task lineage",
            "reload the implementation checklist and discard construction_plan decomposition notes that are not part of the active pack",
            "do_not_pull_graph_context_into_implementation_focus; read concrete code and tests directly",
            "read only an execution-eligible official active pack plus the source_mother_doc_refs declared by that pack; do not sweep unrelated modified docs into implementation focus",
            "preview_skeleton or accepted/retired plan roots must be rejected before implementation starts",
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
            "<docs_root>/mother_doc/* with doc_work_state=developed|ref as needed",
            "<docs_root>/mother_doc/execution_atom_plan_validation_packs/<active_or_completed_pack>/*",
            "<docs_root>/mother_doc/acceptance/*",
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
