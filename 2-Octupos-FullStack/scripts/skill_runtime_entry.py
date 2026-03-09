from __future__ import annotations

import json
from pathlib import Path

from stage_contract_registry import STAGE_COMMANDS, STAGE_ORDER, STAGE_SCOPES, TOP_LEVEL_RESIDENT_DOCS

ROLE_DEFINITION_EN = (
    "An operations-facing AI embedded in the future admin panel, responsible for maintaining Mother_Doc, "
    "driving implementation, and writing back evidence."
)

RULE_LAYERS_EN = {
    "skill_native_rules": "How this skill operates, maintains Mother_Doc, and closes the implementation-to-evidence loop.",
    "authored_rules": "Architecture, stack, naming, contract, operations, and runtime rules defined in authored container documents.",
}

EXECUTION_MODEL_EN = (
    "Documentation is code; code structure ultimately aligns to Mother_Doc; implementation operates to independent developer "
    "standards; evidence unifies the document graph and code graph through OS_graph."
)

GOVERNANCE_RULES_EN = [
    "Before entering any stage, always load stage-checklist, stage-doc-contract, stage-command-contract, and stage-graph-contract.",
    "When switching stages, retain only the top-level resident documents and then reload the current stage contracts.",
    "AGENTS.md is allowed at the Octopus_OS root, each container root, and across the Octopus_OS/Mother_Doc/docs tree.",
    "Every Mother_Doc directory layer must contain README.md, AGENTS.md, and <folder_name>.md.",
    "Every container document directory must contain overview/, features/, shared/, and common/.",
    "All Mother_Doc markdown other than AGENTS.md must contain Document Status + Block Registry for mechanical change detection.",
    "Project baseline belongs to the always-load layer and must be read before entering any concrete container or domain.",
    "The mother_doc stage must first strengthen user intent with Meta-prompt-write, then read the mother_doc branch entry before choosing a task chain.",
    "The mother_doc stage must first choose direct_writeback, question_backfill, or AGENTS/README manager; do not mix branches.",
    "Impact selection in mother_doc is fixed as: default all-relevant, then subtract high-probability-irrelevant scopes.",
    "The AGENTS/README manager centrally governs AGENTS.md + README.md across the Octopus_OS root, container roots, and Mother_Doc/docs using scan / collect / push.",
    "direct_writeback writes only explicit content; question_backfill closes only unresolved design gaps.",
    "After mother_doc updates documents, the local git-backed status script must run; changed docs become modified and empty placeholders become null.",
    "The mother_doc stage must not write implementation logs, deployment logs, or Git / GitHub traceability records.",
    "The implementation stage must operate like an independent developer and proactively fix doc-code drift.",
    "Implementation consumes modified state and completes code alignment, but does not write back developed in that stage.",
    "The implementation stage must not write implementation logs, deployment logs, or Git / GitHub traceability records.",
    "The evidence stage must unify the document graph, code graph, and evidence bindings through OS_graph.",
    "OS_graph is fixed to narrative_layer, contract_layer, implementation_layer, and evidence_layer.",
    "After evidence closes the loop, the corresponding documents and blocks must be written back as developed.",
    "The evidence stage exclusively owns implementation batch logs, deployment checkpoints, and Git / GitHub traceability records.",
    "Once a deployment-level witness exists, a deployment checkpoint log must be appended.",
    "Implementation and deployment logs store summary only; the summary must equal the same-turn Git commit message, while Git / GitHub holds the detailed diff.",
    "All writeback uses overwrite semantics and preserves current state only; internal document version history is not kept, but logs preserve the timeline.",
]


def resolve_skill_root(raw_root: str | None) -> Path:
    if raw_root:
        return Path(raw_root).expanduser().resolve()
    return Path(__file__).resolve().parent.parent


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_skill_runtime_contract(skill_root: Path) -> dict[str, object]:
    payload = _load_json(skill_root / "references" / "runtime" / "SKILL_RUNTIME_CONTRACT.json")
    payload["role_definition_en"] = ROLE_DEFINITION_EN
    payload["rule_layers_en"] = RULE_LAYERS_EN
    payload["execution_model_en"] = EXECUTION_MODEL_EN
    payload["governance_rules_en"] = GOVERNANCE_RULES_EN
    payload["runtime_source_policy"] = {
        "skill_runtime_source": "CLI_JSON",
        "skill_markdown_role": "human_navigation_only",
        "audit_markdown_allowed_for_humans": True,
        "model_must_prefer_cli_runtime_output": True,
        "preferred_runtime_language": "en",
    }
    payload["recommended_entry_commands"] = [
        "python3 scripts/Cli_Toolbox.py skill-runtime-contract --json",
        "python3 scripts/Cli_Toolbox.py skill-facade-contract --json",
    ]
    payload["audit_source_language"] = "zh-CN"
    payload["skill_root"] = str(skill_root)
    return payload


def _stage_entry(stage: str) -> dict[str, object]:
    command_block = STAGE_COMMANDS[stage]
    if stage == "mother_doc":
        stage_command = "mother-doc-stage"
    else:
        stage_command = f"{stage.replace('_', '-')}-stage"
    summary_command = f"python3 scripts/Cli_Toolbox.py {stage_command} --json"
    return {
        "stage": stage,
        "scope": STAGE_SCOPES[stage],
        "required_contract_reads": command_block["required_contract_reads"],
        "summary_command": summary_command,
        "operation_commands": command_block["stage_commands"],
    }


def load_skill_facade_contract(skill_root: Path) -> dict[str, object]:
    return {
        "schema_version": 1,
        "owner_skill": "2-Octupos-FullStack",
        "runtime_source_policy": {
            "skill_runtime_source": "CLI_JSON",
            "facade_markdown_role": "human_navigation_only",
            "load_map_markdown_role": "human_audit_navigation_only",
            "model_must_not_use_markdown_as_runtime_rule_source": True,
        },
        "entry_sequence": [
            {
                "command": "python3 scripts/Cli_Toolbox.py skill-runtime-contract --json",
                "purpose": "load the skill-level runtime contract before following any stage-specific path",
            },
            {
                "command": "python3 scripts/Cli_Toolbox.py skill-facade-contract --json",
                "purpose": "load the runtime routing map for stages, stage contracts, and specialized sub-branches",
            },
        ],
        "top_level_resident_docs": TOP_LEVEL_RESIDENT_DOCS,
        "stage_order": STAGE_ORDER,
        "stages": [_stage_entry(stage) for stage in STAGE_ORDER],
        "specialized_runtime_entries": {
            "mother_doc_agents_manager": {
                "branch_contract_command": "python3 scripts/Cli_Toolbox.py mother-doc-agents-contract --json",
                "stage_directive_command": "python3 scripts/Cli_Toolbox.py mother-doc-agents-directive --stage <scan|collect|push> --json",
                "target_contract_command": "python3 scripts/Cli_Toolbox.py mother-doc-agents-target-contract --relative-path \"<PATH>\" --file-kind <agents|readme> --json",
            }
        },
        "audit_markdown_sources": [
            "SKILL.md",
            "references/runtime/SKILL_RUNTIME_CONTRACT.md",
            "references/skill_native/01_FACADE_LOAD_MAP.md",
        ],
        "skill_root": str(skill_root),
    }
