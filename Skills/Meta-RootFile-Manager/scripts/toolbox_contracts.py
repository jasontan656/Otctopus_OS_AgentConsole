from __future__ import annotations

from pathlib import Path
from typing import TypedDict

from rootfile_runtime import read_json, resolve_target_contract


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
RUNTIME_CONTRACTS_ROOT = SKILL_ROOT / "references" / "runtime_contracts"
SKILL_RUNTIME_CONTRACT_PATH = RUNTIME_CONTRACTS_ROOT / "SKILL_RUNTIME_CONTRACT.json"


class AgentsPayloadMetaRootFileManagerCommands(TypedDict):
    target_contract: str
    agents_payload_contract: str
    agents_domain_contract: str
    lint: str


class AgentsPayloadMetaEnhancePromptCommands(TypedDict):
    contract: str
    directive: str


class AgentsPayloadToolEntry(TypedDict):
    meta_rootfile_manager: AgentsPayloadMetaRootFileManagerCommands
    meta_enhance_prompt: AgentsPayloadMetaEnhancePromptCommands


class AgentsPayloadWritebackPolicy(TypedDict):
    canonical_truth_surface: str
    part_b_container: str
    external_part_a_surface: str


class AgentsPayloadContractPayload(TypedDict):
    contract_name: str
    contract_version: str
    skill_name: str
    source_path: str
    channel_id: str
    mapping_mode: str
    owner: str
    managed_files: dict[str, str]
    tool_entry: AgentsPayloadToolEntry
    workflow: list[str]
    secondary_contract_reads: list[dict[str, str]]
    writeback_policy: AgentsPayloadWritebackPolicy
    rules: list[str]


def load_skill_runtime_contract() -> object:
    return read_json(SKILL_RUNTIME_CONTRACT_PATH)


def build_agents_payload_contract(paths: object, source_path: Path) -> AgentsPayloadContractPayload:
    result = resolve_target_contract(paths, source_path)
    if result.get("channel_id") != "AGENTS_MD" or result.get("mapping_mode") != "agents_ab":
        raise ValueError("agents_payload_contract_requires_agents_target")

    return {
        "contract_name": "meta_rootfile_manager_agents_payload_governance_contract",
        "contract_version": "1.0.0",
        "skill_name": "Meta-RootFile-Manager",
        "source_path": str(source_path),
        "channel_id": result["channel_id"],
        "mapping_mode": result["mapping_mode"],
        "owner": result["owner"],
        "managed_files": result["managed_files"],
        "tool_entry": {
            "meta_rootfile_manager": {
                "target_contract": (
                    "./.venv_backend_skills/bin/python "
                    "Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py "
                    f"target-contract --source-path \"{source_path}\" --json"
                ),
                "agents_payload_contract": (
                    "./.venv_backend_skills/bin/python "
                    "Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py "
                    f"agents-payload-contract --source-path \"{source_path}\" --json"
                ),
                "agents_domain_contract": (
                    "./.venv_backend_skills/bin/python "
                    "Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py "
                    f"agents-domain-contract --source-path \"{source_path}\" --domain \"<domain_id>\" --json"
                ),
                "lint": (
                    "./.venv_backend_skills/bin/python "
                    "Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py "
                    f"lint --source-path \"{source_path}\" --json"
                ),
            },
            "meta_enhance_prompt": {
                "contract": (
                    "./.venv_backend_skills/bin/python "
                    "Skills/Meta-Enhance-Prompt/scripts/Cli_Toolbox.py contract --json"
                ),
                "directive": (
                    "./.venv_backend_skills/bin/python "
                    "Skills/Meta-Enhance-Prompt/scripts/Cli_Toolbox.py "
                    "directive --topic skill-directive --json"
                ),
            },
        },
        "workflow": [
            "First resolve the governed AGENTS target and managed contract block paths from this contract.",
            "Before interpreting the user request, load Meta-Enhance-Prompt contract and its skill-directive entry.",
            "Treat the user request as literal by default and rewrite it into the smallest precise domain-contract semantics only.",
            "Do not add process reminders, extra governance notes, extra routing, or extra obligations that the user did not request.",
            "If the intended shape is still unclear after intent normalization, inspect sibling domain blocks for style only; do not invent new semantics.",
            "Edit only the governed AGENTS_human.md Part B domain block for the requested change scope.",
            "Run lint for the same external AGENTS.md before closing the turn.",
        ],
        "secondary_contract_reads": result.get("secondary_contract_reads", []),
        "writeback_policy": {
            "canonical_truth_surface": result["managed_files"]["human"],
            "part_b_container": result["managed_files"]["human"],
            "external_part_a_surface": str(source_path),
        },
        "rules": [
            "Part A contract body is the primary visible hook contract; reminder text may follow only after the contract body ends.",
            "Part B must be split into domain-specific contract blocks instead of one flat payload blob.",
            "Each Part B block must carry its own read_command_preview and machine contract body.",
            "Do not add anything beyond the user request by default.",
            "Do not treat oral wording as permission to expand scope or complete hidden intent.",
            "Use addition only when the user explicitly requested a new semantic.",
        ],
    }
