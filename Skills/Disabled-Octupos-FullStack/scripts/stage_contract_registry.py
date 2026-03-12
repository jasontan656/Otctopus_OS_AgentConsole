from __future__ import annotations
# contract_name: 2_octupos_fullstack_stage_contract_registry
# contract_version: 2.0.0
# validation_mode: static_minimal
# required_fields: top_level_resident_docs,stage_order,stage_scopes,stage_docs,stage_commands,stage_graph_contracts,stage_checklists

from pathlib import Path

from stage_contract_graph_data import EVIDENCE_GRAPH_COMMANDS, EVIDENCE_GRAPH_DOCS


def _resolve_product_root() -> Path:
    script_path = Path(__file__).resolve()
    repo_root = next((parent for parent in script_path.parents if parent.name == "octopus-os-agent-console"), None)
    if repo_root is None:
        raise RuntimeError("cannot resolve product root from Disabled-Octupos-FullStack script path")
    return repo_root.parent


PRODUCT_ROOT = _resolve_product_root()
ROOT_AGENTS_PATH = (PRODUCT_ROOT / "AGENTS.md").resolve()
OCTOPUS_OS_ROOT = (PRODUCT_ROOT / "Octopus_OS").resolve()
OCTOPUS_OS_DOCS_ROOT = (OCTOPUS_OS_ROOT / "Mother_Doc" / "docs").resolve()
LOCAL_CODEX_HOME = (PRODUCT_ROOT / ".codex").resolve()

TOP_LEVEL_RESIDENT_DOCS = [
    "rules/FULLSTACK_SKILL_HARD_RULES.md",
    "references/runtime/SKILL_RUNTIME_CONTRACT.md",
    "references/skill_native/00_SKILL_NATIVE_INDEX.md",
    "references/skill_native/10_PROJECT_BASELINE_INDEX.md",
    "references/authored_domains/00_DOMAIN_INDEX.md",
    "references/tooling/SKILL_TOOLING_WORKFLOW_CONTRACT.md",
    str(ROOT_AGENTS_PATH),
]

STAGE_ORDER = ["mother_doc", "implementation", "evidence"]

STAGE_SCOPES = {
    "mother_doc": "strengthen user intent, maintain Mother_Doc current-state structure, and govern the single Octopus_OS root AGENTS target when needed",
    "implementation": "act as an independent delivery-grade developer and reconcile Mother_Doc with the actual codebase while implementing changes",
    "evidence": "collect real witnesses, append logs, and bind them back through the unified OS_graph contract",
}

STAGE_DOCS = {
    "mother_doc": [
        "references/stages/MOTHER_DOC_STAGE.md",
        "references/mother_doc/AGENTS_MD_RULES.md",
        "references/mother_doc/DOC_STATUS_RULES.md",
        "references/mother_doc/SCOPE_ENTITY_MD_RULES.md",
        "references/mother_doc/MOTHER_DOC_WRITEBACK_RULES.md",
        "references/mother_doc/PHASE1_CONTAINER_NAMING_REFERENCE.md",
        "references/mother_doc/agents_branch/runtime/AGENTS_BRANCH_CONTRACT.md",
    ],
    "implementation": [
        "references/stages/IMPLEMENTATION_STAGE.md",
        "references/authored_domains/00_DOMAIN_INDEX.md",
        "references/implementation/IMPLEMENTATION_DELIVERY_RULES.md",
        "references/implementation/DOC_CODE_ALIGNMENT_RULES.md",
    ],
    "evidence": [
        "references/stages/EVIDENCE_STAGE.md",
        *EVIDENCE_GRAPH_DOCS,
        "references/evidence/OS_GRAPH_LAYER_MODEL.md",
        "references/evidence/DOC_CODE_BINDING_RULES.md",
        "references/evidence/IMPLEMENTATION_LOG_RULES.md",
        "references/evidence/OS_GRAPH_RULES.md",
        "references/evidence/DEPLOYMENT_LOG_RULES.md",
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
                "command": (
                    f"python3 ${{CODEX_HOME:-{LOCAL_CODEX_HOME}}}/skills/"
                    "Meta-prompt-write/scripts/filter_active_invoke_output.py "
                    '--mode active_invoke --input-text "<RAW_PROMPT_OUTPUT>"'
                ),
                "purpose": "strengthen the current user prompt with full repo context before selecting Mother_Doc scope",
            },
            {
                "command": "read references/skill_native/10_PROJECT_BASELINE_INDEX.md",
                "purpose": "load the project-wide operating model and impact pruning baseline before choosing concrete container scope",
            },
            {
                "command": "direct_writeback -> update overview/features/shared/common for the affected container scopes only",
                "purpose": "write the explicit user-described content into the correct authored-doc layers without inventing missing detail",
            },
            {
                "command": "question_backfill -> ask unresolved design questions after initial writeback and then overwrite the same authored-doc files with the answers",
                "purpose": "close open design gaps iteratively while staying inside mother_doc and without starting implementation or evidence",
            },
            {
                "command": "python3 scripts/Cli_Toolbox.py mother-doc-agents-directive --stage <scan|collect|push> --json",
                "purpose": "load the AGENTS manager directive when the current task is specifically about the single governed root AGENTS target",
            },
            {
                "command": "python3 scripts/Cli_Toolbox.py mother-doc-agents-scan --json",
                "purpose": "discover the single managed Octopus_OS root AGENTS target and report forbidden extra AGENTS.md files under Octopus_OS",
            },
            {
                "command": "python3 scripts/Cli_Toolbox.py mother-doc-agents-collect --json",
                "purpose": "collect the current Octopus_OS root AGENTS file back into the skill-side managed human/machine pair",
            },
            {
                "command": "python3 scripts/Cli_Toolbox.py mother-doc-agents-push --json",
                "purpose": "push the managed root AGENTS payload back to Octopus_OS and delete forbidden extra AGENTS.md files",
            },
            {
                "command": (
                    f"python3 scripts/Cli_Toolbox.py sync-mother-doc-status-from-git "
                    f"--repo-root {OCTOPUS_OS_ROOT} --stage mother_doc --path <relative-path> --json"
                ),
                "purpose": "derive modified / developed / null lifecycle states from local git-backed diff after mother_doc writeback",
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
                "command": f'rg -n "<target>" {OCTOPUS_OS_ROOT} {OCTOPUS_OS_DOCS_ROOT}',
                "purpose": "inspect doc-code drift and locate implementation slices without scanning unrelated sibling repositories",
            },
            {
                "command": "project-native install / repair / test / bring-up commands chosen from the actual codebase",
                "purpose": "act like an independent human developer: install dependencies, repair runtime, run tests, bring up services, and verify real behavior",
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
            *EVIDENCE_GRAPH_COMMANDS,
            {
                "command": "project-native validation / smoke / test / health-check commands chosen from the actual codebase",
                "purpose": "collect real delivery witnesses after implementation bring-up instead of fabricating completion status",
            },
            {
                "command": "python3 scripts/Cli_Toolbox.py sync-mother-doc-status --stage evidence --path <relative-path> --lifecycle-state developed --json",
                "purpose": "flip affected Mother_Doc documents and block registries to developed once evidence closes the loop",
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
            "<folder_name>.md -> scope-entity node",
            "Document Status + Block Registry -> mechanical change-detection node",
        ],
        "tooling_mode": "contract_first",
        "action_rule": "keep the Mother_Doc tree structurally complete and mark changed document blocks as modified so later code and evidence can map onto the same graph",
    },
    "implementation": {
        "graph_name": "OS_graph",
        "stage_role": "use the unified document structure as the implementation map and reconcile Mother_Doc with the actual codebase",
        "node_mapping": [
            "module directory -> module node",
            "module markdown -> module contract node",
            "code file / package / runtime artifact -> implementation node",
        ],
        "tooling_mode": "contract_first",
        "action_rule": "detect doc-code drift, align code and Mother_Doc to the same current-state structure, and hand the aligned scope to evidence",
    },
    "evidence": {
        "graph_name": "OS_graph",
        "stage_role": "merge document graph and code graph into a delivery-state explanation layer with evidence bindings and four explicit graph layers",
        "node_mapping": [
            "overview/*.md -> narrative_layer nodes",
            "features/*.md and shared/*.md -> contract_layer nodes",
            "code modules, helpers, and runtime artifacts -> implementation_layer nodes",
            "implementation/deployment logs and witnesses -> evidence_layer nodes",
        ],
        "tooling_mode": "contract_first_with_os_graph_runtime",
        "action_rule": "treat OS_graph as the combined doc+code graph contract and keep the four graph layers readable to humans and machines",
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
            "load the project baseline before selecting container scope",
            "strengthen the user prompt with Meta-prompt-write",
            "choose direct_writeback, question_backfill, or the root-only AGENTS manager by actual task intent",
        ],
        "exit_requirements": [
            "updated Mother_Doc current-state content",
            "affected overview/features/shared/common docs are aligned with the current explicit user intent",
            "affected Mother_Doc markdown files are marked as modified/null/developed according to the git-backed lifecycle status rules",
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
            "retain the project baseline before selecting implementation scope",
            "read implementation-specific stage contracts",
            "inspect codebase and runtime to locate doc-code drift before editing",
        ],
        "exit_requirements": [
            "code and Mother_Doc are aligned to the same current-state structure",
            "dependencies, runtime, and tests are handled to product-delivery standard within local control",
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
            "writeback is complete without introducing internal version branches",
        ],
    },
}
