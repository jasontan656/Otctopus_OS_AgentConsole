from __future__ import annotations

from runstate_models import GovernedTypeDefinition


RUNSTATE_TEMPLATES = {
    "Skills_runtime_checklist": "references/runstates/templates/Skills_runtime_checklist.yaml",
    "workflow_runtime_checklist": "references/runstates/templates/workflow_runtime_checklist.yaml",
    "stage_runtime_checklist": "references/runstates/templates/stage_runtime_checklist.yaml",
}


GOVERNED_TYPES: dict[str, GovernedTypeDefinition] = {
    "not_applicable": {
        "governed_type": "not_applicable",
        "applicability": "not_applicable",
        "required_checklists": [],
        "template_files": [],
        "success_criteria": [
            "Target skill is not workflow-bearing and therefore does not need runstate files.",
            "No fake workflow/stage/skill-flow checklist requirement is introduced.",
        ],
    },
    "workflow_runtime": {
        "governed_type": "workflow_runtime",
        "applicability": "applicable",
        "required_checklists": [
            "workflow_runtime_checklist",
            "stage_runtime_checklist",
        ],
        "template_files": [
            RUNSTATE_TEMPLATES["workflow_runtime_checklist"],
            RUNSTATE_TEMPLATES["stage_runtime_checklist"],
        ],
        "success_criteria": [
            "Workflow and stage runstate templates exist.",
            "Target markdown references workflow_runtime_checklist and stage_runtime_checklist as consumed artifacts.",
            "Target markdown requires each next step to consume previous output and to write back after each atomic step.",
        ],
    },
    "skill_flow_orchestrator": {
        "governed_type": "skill_flow_orchestrator",
        "applicability": "applicable",
        "required_checklists": [
            "Skills_runtime_checklist",
            "workflow_runtime_checklist",
            "stage_runtime_checklist",
        ],
        "template_files": [
            RUNSTATE_TEMPLATES["Skills_runtime_checklist"],
            RUNSTATE_TEMPLATES["workflow_runtime_checklist"],
            RUNSTATE_TEMPLATES["stage_runtime_checklist"],
        ],
        "success_criteria": [
            "Skill-flow, workflow, and stage runstate templates all exist.",
            "Host skill markdown references Skills_runtime_checklist, workflow_runtime_checklist, and stage_runtime_checklist as active governance artifacts.",
            "Host skill markdown states that downstream skill outputs and prior-stage outputs must be consumed before continuing.",
            "Host skill markdown states that writeback drives the next step and forbids step skipping or parallel completion.",
        ],
    },
}


def governed_type_definition(governed_type: str) -> GovernedTypeDefinition:
    return GOVERNED_TYPES[governed_type]
