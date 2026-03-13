from __future__ import annotations

# contract_name: 2_octupos_fullstack_stage_contract_support
# contract_version: 1.0.0
# validation_mode: static_minimal
# required_fields: top_level_resident_docs,stage_order,stage_docs,stage_commands,stage_graph_contracts,stage_checklists
# optional_fields: none

from stage_contract_registry import (
    STAGE_CHECKLISTS,
    STAGE_COMMANDS,
    STAGE_DOCS,
    STAGE_GRAPH_CONTRACTS,
    STAGE_ORDER,
    STAGE_SCOPES,
    TOP_LEVEL_RESIDENT_DOCS,
)


def get_stage_checklist(stage_name: str) -> dict[str, object]:
    return STAGE_CHECKLISTS[stage_name]


def get_stage_doc_contract(stage_name: str) -> dict[str, object]:
    return {
        "stage": stage_name,
        "top_level_resident_docs": TOP_LEVEL_RESIDENT_DOCS,
        "stage_docs": STAGE_DOCS[stage_name],
        "phase_read_policy": "On stage switch, keep only top-level resident docs, then reload the current stage contracts.",
    }


def get_stage_command_contract(stage_name: str) -> dict[str, object]:
    return {
        "stage": stage_name,
        **STAGE_COMMANDS[stage_name],
    }


def get_stage_graph_contract(stage_name: str) -> dict[str, object]:
    return {
        "stage": stage_name,
        **STAGE_GRAPH_CONTRACTS[stage_name],
    }


def get_stage_summary(stage_name: str) -> dict[str, object]:
    checklist = get_stage_checklist(stage_name)
    if stage_name == "mother_doc":
        requires: list[str] = []
    elif stage_name == "implementation":
        requires = ["mother_doc stage outputs"]
    else:
        requires = ["mother_doc stage outputs", "implementation stage outputs"]
    return {
        "stage": stage_name,
        "command": f"{stage_name.replace('_', '-')}-stage",
        "scope": STAGE_SCOPES[stage_name],
        "must_load": TOP_LEVEL_RESIDENT_DOCS,
        "requires": requires,
        "produces": checklist["exit_requirements"],
        "doc_contract": STAGE_DOCS[stage_name],
        "stage_order": STAGE_ORDER,
    }
