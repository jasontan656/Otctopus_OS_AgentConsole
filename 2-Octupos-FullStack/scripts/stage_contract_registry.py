from __future__ import annotations

# contract_name: 2_octupos_fullstack_stage_contract_registry
# contract_version: 1.0.0
# validation_mode: static_minimal
# required_fields: top_level_resident_docs,stage_order,stage_scopes,stage_docs,stage_commands,stage_graph_contracts,stage_checklists
# optional_fields: none

TOP_LEVEL_RESIDENT_DOCS = [
    "rules/FULLSTACK_SKILL_HARD_RULES.md",
    "references/runtime/SKILL_RUNTIME_CONTRACT.md",
    "references/skill_native/00_SKILL_NATIVE_INDEX.md",
    "references/authored_domains/00_DOMAIN_INDEX.md",
    "references/tooling/SKILL_TOOLING_WORKFLOW_CONTRACT.md",
    "/home/jasontan656/AI_Projects/AGENTS.md",
]

STAGE_ORDER = ["mother_doc", "implementation", "evidence"]

STAGE_SCOPES = {
    "mother_doc": "strengthen user intent, recursively navigate Mother_Doc, and write back current-state document structure",
    "implementation": "act as an independent delivery-grade developer and reconcile Mother_Doc with the actual codebase while implementing changes",
    "evidence": "collect real witnesses, append logs, and bind them back through the unified OS_graph contract",
}

STAGE_DOCS = {
    "mother_doc": [
        "references/stages/MOTHER_DOC_STAGE.md",
        "references/mother_doc/00_MOTHER_DOC_BRANCH_INDEX.md",
        "references/mother_doc/CONTENT_WRITEBACK_BRANCH.md",
        "references/mother_doc/MOTHER_DOC_ENTRY_RULES.md",
        "references/mother_doc/AGENTS_MD_RULES.md",
        "references/mother_doc/DOC_STATUS_RULES.md",
        "references/mother_doc/README_MD_RULES.md",
        "references/mother_doc/SCOPE_ENTITY_MD_RULES.md",
        "references/mother_doc/MOTHER_DOC_WRITEBACK_RULES.md",
        "references/mother_doc/PHASE1_CONTAINER_NAMING_REFERENCE.md",
        "references/mother_doc/agents_branch/00_BRANCH_INDEX.md",
        "references/mother_doc/agents_branch/runtime/AGENTS_BRANCH_CONTRACT.md",
    ],
    "implementation": [
        "references/stages/IMPLEMENTATION_STAGE.md",
        "references/authored_domains/00_DOMAIN_INDEX.md",
        "references/implementation/IMPLEMENTATION_DELIVERY_RULES.md",
        "references/implementation/DOC_CODE_ALIGNMENT_RULES.md",
        "references/stages/MOTHER_DOC_STAGE.md",
    ],
    "evidence": [
        "references/stages/EVIDENCE_STAGE.md",
        "references/evidence/IMPLEMENTATION_LOG_RULES.md",
        "references/evidence/OS_GRAPH_RULES.md",
        "references/evidence/DEPLOYMENT_LOG_RULES.md",
        "references/stages/MOTHER_DOC_STAGE.md",
        "references/stages/IMPLEMENTATION_STAGE.md",
    ],
}

STAGE_COMMANDS = {
    "mother_doc": {
        "required_contract_reads": [
            "python3 scripts/Cli_Toolbox.py stage-checklist --stage mother_doc --json",
            "python3 scripts/Cli_Toolbox.py stage-doc-contract --stage mother_doc --json",
            "python3 scripts/Cli_Toolbox.py stage-command-contract --stage mother_doc --json",
            "python3 scripts/Cli_Toolbox.py stage-graph-contract --stage mother_doc --json",
        ],
        "stage_commands": [
            {
                "command": "python3 /home/jasontan656/.codex/skills/Meta-prompt-write/scripts/filter_active_invoke_output.py --mode active_invoke --input-text \"<RAW_PROMPT_OUTPUT>\"",
                "purpose": "strengthen the current user prompt with full repo context before selecting Mother_Doc scope",
            },
            {
                "command": "python3 scripts/Cli_Toolbox.py materialize-container-layout --container <Name> --json",
                "purpose": "materialize new container directories and initial authored-document skeletons once the semantic decision is made",
            },
            {
                "command": "python3 scripts/Cli_Toolbox.py sync-mother-doc-navigation --json",
                "purpose": "refresh README.md, AGENTS.md, and same-name scope markdown files across the Mother_Doc tree only",
            },
            {
                "command": "python3 scripts/Cli_Toolbox.py sync-mother-doc-status --stage mother_doc --path <relative-path> --sync-status pending_implementation --requires-development --json",
                "purpose": "mark affected Mother_Doc documents and block registries as requiring implementation after a document-side change",
            },
            {
                "command": "python3 scripts/Cli_Toolbox.py mother-doc-agents-directive --stage <scan|collect|push> --json",
                "purpose": "load the sub-branch directive when the current mother_doc task is specifically about AGENTS.md scaffolding management",
            },
            {
                "command": "python3 scripts/Cli_Toolbox.py mother-doc-agents-scan --json",
                "purpose": "discover the managed AGENTS.md files under Octopus_OS/Mother_Doc/docs only",
            },
            {
                "command": "python3 scripts/Cli_Toolbox.py mother-doc-agents-collect --json",
                "purpose": "collect current AGENTS.md files back into the skill-side registry when product-side AGENTS changed first",
            },
            {
                "command": "python3 scripts/Cli_Toolbox.py mother-doc-agents-push --json",
                "purpose": "push the skill-side AGENTS.md template back across the Mother_Doc docs tree and refresh the registry",
            },
        ],
    },
    "implementation": {
        "required_contract_reads": [
            "python3 scripts/Cli_Toolbox.py stage-checklist --stage implementation --json",
            "python3 scripts/Cli_Toolbox.py stage-doc-contract --stage implementation --json",
            "python3 scripts/Cli_Toolbox.py stage-command-contract --stage implementation --json",
            "python3 scripts/Cli_Toolbox.py stage-graph-contract --stage implementation --json",
        ],
        "stage_commands": [
            {
                "command": "python3 scripts/Cli_Toolbox.py implementation-stage --json",
                "purpose": "print the implementation-stage contract with independent developer obligations and delivery expectations",
            },
            {
                "command": "rg -n \"<target>\" /home/jasontan656/AI_Projects/Octopus_OS /home/jasontan656/AI_Projects/Octopus_OS/Mother_Doc/docs",
                "purpose": "inspect doc-code drift and locate implementation slices without scanning unrelated sibling repositories",
            },
            {
                "command": "project-native install / repair / test / bring-up commands chosen from the actual codebase",
                "purpose": "act like an independent human developer: install dependencies, repair runtime, run tests, bring up services, and verify real behavior",
            },
            {
                "command": "python3 scripts/Cli_Toolbox.py sync-mother-doc-status --stage implementation --path <relative-path> --sync-status aligned --no-requires-development --json",
                "purpose": "flip affected Mother_Doc documents from pending implementation to aligned after code and docs match again",
            },
        ],
    },
    "evidence": {
        "required_contract_reads": [
            "python3 scripts/Cli_Toolbox.py stage-checklist --stage evidence --json",
            "python3 scripts/Cli_Toolbox.py stage-doc-contract --stage evidence --json",
            "python3 scripts/Cli_Toolbox.py stage-command-contract --stage evidence --json",
            "python3 scripts/Cli_Toolbox.py stage-graph-contract --stage evidence --json",
        ],
        "stage_commands": [
            {
                "command": "python3 scripts/Cli_Toolbox.py evidence-stage --json",
                "purpose": "print the evidence-stage contract with writeback and witness requirements",
            },
            {
                "command": "project-native validation / smoke / test / health-check commands chosen from the actual codebase",
                "purpose": "collect real delivery witnesses after implementation bring-up instead of fabricating completion status",
            },
            {
                "command": "python3 scripts/Cli_Toolbox.py append-implementation-log --summary \"<summary>\" --doc-path <doc-path> --code-path <code-path> --json",
                "purpose": "append an implementation batch log after implementation has already aligned code and docs and evidence is closing the traceability loop",
            },
            {
                "command": "python3 scripts/Cli_Toolbox.py append-deployment-log --summary \"<summary>\" --doc-path <doc-path> --code-path <code-path> --json",
                "purpose": "append a deployment checkpoint once implementation becomes deployable or has been deployed with a real witness set",
            },
        ],
    },
}

STAGE_GRAPH_CONTRACTS = {
    "mother_doc": {
        "graph_name": "OS_graph",
        "stage_role": "author the documentation-side structural topology that later becomes part of the unified OS graph",
        "node_mapping": [
            "directory -> structural scope node",
            "README.md -> scope-purpose node",
            "AGENTS.md -> navigation-index node",
            "<folder_name>.md -> scope-entity node",
            "Document Status + Block Registry -> mechanical change-detection node",
        ],
        "tooling_mode": "contract_first",
        "action_rule": "keep the Mother_Doc tree structurally complete and mark changed document blocks as pending implementation so later code and evidence can map onto the same graph",
    },
    "implementation": {
        "graph_name": "OS_graph",
        "stage_role": "use the unified document structure as the implementation map and reconcile Mother_Doc with the actual codebase",
        "node_mapping": [
            "module directory -> module node",
            "module markdown -> module contract node",
            "helper markdown -> helper contract node",
            "code file / package / runtime artifact -> implementation node",
        ],
        "tooling_mode": "contract_first",
        "action_rule": "detect doc-code drift, align code and Mother_Doc to the same current-state structure, and flip block statuses before handing the aligned scope to evidence for traceability",
    },
    "evidence": {
        "graph_name": "OS_graph",
        "stage_role": "merge document graph and code graph into a delivery-state explanation layer with evidence bindings",
        "node_mapping": [
            "directory -> scope node",
            "<folder_name>.md -> module or black-box description node",
            "code modules and helpers -> implementation nodes under the same hierarchy",
            "implementation_batches.md entries -> implementation timeline node",
            "witnesses -> evidence nodes bound back to the same hierarchy",
            "deployment_batches.md entries -> deployment checkpoint node",
        ],
        "tooling_mode": "contract_first_until_os_graph_runtime_lands",
        "action_rule": "treat OS_graph as the combined doc+code graph contract, bind evidence to the corresponding structural nodes, and record deployment checkpoints as timeline witnesses",
    },
}

STAGE_CHECKLISTS = {
    "mother_doc": {
        "stage": "mother_doc",
        "stage_order": STAGE_ORDER,
        "top_level_resident_docs": TOP_LEVEL_RESIDENT_DOCS,
        "stage_docs": STAGE_DOCS["mother_doc"],
        "entry_requirements": [
            "load top-level resident docs",
            "strengthen the user prompt with Meta-prompt-write",
            "read root README.md and AGENTS.md inside Mother_Doc before selecting scope",
            "if the task is about AGENTS scaffolding itself, enter the mother_doc AGENTS sub-branch before editing",
        ],
        "exit_requirements": [
            "updated Mother_Doc current-state content",
            "updated README.md, AGENTS.md, and <folder_name>.md for affected Mother_Doc scopes only",
            "affected non-AGENTS Mother_Doc markdown files are marked as pending implementation in their document/block status sections",
            "implementation inputs ready",
        ],
    },
    "implementation": {
        "stage": "implementation",
        "stage_order": STAGE_ORDER,
        "top_level_resident_docs": TOP_LEVEL_RESIDENT_DOCS,
        "stage_docs": STAGE_DOCS["implementation"],
        "entry_requirements": [
            "load top-level resident docs",
            "read implementation-specific stage contracts",
            "carry forward current-state outputs from mother_doc",
            "load the matching authored domain family rules before entering a specific container",
            "inspect codebase and runtime to locate doc-code drift before editing",
        ],
        "exit_requirements": [
            "code and Mother_Doc are aligned to the same current-state structure",
            "affected document/block statuses are flipped away from pending implementation where implementation actually landed",
            "dependencies, runtime, and tests are handled to product-delivery standard within local control",
            "the aligned implementation scope is ready for evidence-stage traceability",
            "evidence inputs are ready",
        ],
    },
    "evidence": {
        "stage": "evidence",
        "stage_order": STAGE_ORDER,
        "top_level_resident_docs": TOP_LEVEL_RESIDENT_DOCS,
        "stage_docs": STAGE_DOCS["evidence"],
        "entry_requirements": [
            "load top-level resident docs",
            "read evidence-specific stage contracts",
            "carry forward current-state outputs from mother_doc and implementation",
        ],
        "exit_requirements": [
            "real witnesses are bound back to the same Mother_Doc hierarchy",
            "OS_graph contract is updated at the contract level for the current delivery state",
            "implementation batch logs are appended under Mother_Doc/docs/Mother_Doc/common/development_logs",
            "deployment checkpoints are appended under Mother_Doc/docs/Mother_Doc/common/development_logs when deployment-level evidence exists",
            "writeback is complete without introducing internal version branches",
        ],
    },
}
