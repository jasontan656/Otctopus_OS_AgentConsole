from __future__ import annotations

import json
from pathlib import Path

import yaml

from governed_type_registry import RUNSTATE_TEMPLATES, governed_type_definition
from runstate_models import ScaffoldPayload
from target_inspector import inspect_target


def _runstate_contract_payload(skill_name: str, governed_type: str) -> dict[str, object]:
    definition = governed_type_definition(governed_type)
    applicable = definition["applicability"] == "applicable"
    checklist_schema = {
        "Skills_runtime_checklist": {
            "required": "Skills_runtime_checklist" in definition["required_checklists"],
            "level": "skill_flow",
            "purpose": "govern skill-orchestration flow steps",
        },
        "workflow_runtime_checklist": {
            "required": "workflow_runtime_checklist" in definition["required_checklists"],
            "level": "workflow",
            "purpose": "govern workflow-level state handoff and writeback",
        },
        "stage_runtime_checklist": {
            "required": "stage_runtime_checklist" in definition["required_checklists"],
            "level": "stage",
            "purpose": "govern stage-local atomic steps and writeback",
        },
    }
    return {
        "skill_name": skill_name,
        "governed_type": governed_type,
        "applicability": definition["applicability"],
        "naming_policy": {
            "runtime_dir_pattern": "Codex_Skill_Runtime/<skill_name>/NNN_slug",
            "checklist_file_pattern": "NNN_slug/<checklist_name>.yaml",
            "notes": [
                "Use NNN_SLUG naming for new intermediate state files.",
                "Do not create parallel or unnamed runtime artifacts.",
            ],
        },
        "checklist_schema": checklist_schema,
        "behavior_contract": {
            "must_consume_previous_output": applicable,
            "must_writeback_after_each_atomic_step": applicable,
            "must_drive_next_step_from_writeback": applicable,
            "prohibit_step_skip_or_parallel_completion": applicable,
        },
        "success_criteria": definition["success_criteria"],
    }


def _runstate_contract_markdown(skill_name: str, governed_type: str) -> str:
    definition = governed_type_definition(governed_type)
    lines = [
        "# Runstate Method Contract",
        "",
        f"- target skill: `{skill_name}`",
        f"- governed_type: `{governed_type}`",
        f"- applicability: `{definition['applicability']}`",
        "",
        "## Required Checklists",
    ]
    if definition["required_checklists"]:
        for checklist in definition["required_checklists"]:
            lines.append(f"- `{checklist}`")
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "## Behavior Contract",
            "- 下一步必须消费上一步产物。",
            "- 每个原子步骤结束后立即回填 checklist。",
            "- 回填结果继续驱动下一步，而不是允许模型跳步或并步。",
            "",
            "## Success Criteria",
        ]
    )
    for item in definition["success_criteria"]:
        lines.append(f"- {item}")
    return "\n".join(lines) + "\n"


def _checklist_template(checklist_name: str, level: str) -> dict[str, object]:
    return {
        "checklist_name": checklist_name,
        "level": level,
        "status": "pending",
        "current_step": "",
        "previous_output_ref": "",
        "writeback_ref": "",
        "must_consume_previous_output": True,
        "must_writeback_after_each_atomic_step": True,
        "must_drive_next_step_from_writeback": True,
        "items": [
            {
                "step_id": "fill_me",
                "status": "pending",
                "expected_input_ref": "",
                "produced_output_ref": "",
                "writeback_ref": "",
                "notes": "",
            }
        ],
    }


def _success_doc(governed_type: str) -> str:
    definition = governed_type_definition(governed_type)
    lines = [
        "# Runstate Success Criteria",
        "",
        f"- governed_type: `{governed_type}`",
        "",
        "## Governance Success",
    ]
    for item in definition["success_criteria"]:
        lines.append(f"- {item}")
    return "\n".join(lines) + "\n"


def scaffold_target(target_root: Path, governed_type: str, force: bool = False) -> ScaffoldPayload:
    target_root = target_root.resolve()
    inspect_payload = inspect_target(target_root)
    if inspect_payload["status"] == "error":
        return {
            "status": "error",
            "target_skill_root": str(target_root),
            "skill_name": target_root.name,
            "governed_type": "not_applicable",
            "applicability": "not_applicable",
            "written_files": [],
            "skipped": True,
            "message": "Target skill root is invalid.",
        }
    chosen_type = inspect_payload["governed_type"] if governed_type == "auto" else governed_type
    definition = governed_type_definition(chosen_type)
    if definition["applicability"] == "not_applicable":
        return {
            "status": "ok",
            "target_skill_root": str(target_root),
            "skill_name": target_root.name,
            "governed_type": chosen_type,
            "applicability": "not_applicable",
            "written_files": [],
            "skipped": True,
            "message": "Target skill is not workflow-bearing; no runstate files were scaffolded.",
        }

    runstates_root = target_root / "references" / "runstates"
    templates_root = runstates_root / "templates"
    contract_json_path = runstates_root / "RUNSTATE_METHOD_CONTRACT.json"
    contract_md_path = runstates_root / "RUNSTATE_METHOD_CONTRACT.md"
    success_md_path = runstates_root / "RUNSTATE_SUCCESS_CRITERIA.md"
    paths = [contract_json_path, contract_md_path, success_md_path]
    paths.extend(target_root / template for template in definition["template_files"])
    existing = [path for path in paths if path.exists()]
    if existing and not force:
        return {
            "status": "warning",
            "target_skill_root": str(target_root),
            "skill_name": target_root.name,
            "governed_type": chosen_type,
            "applicability": definition["applicability"],
            "written_files": [],
            "skipped": True,
            "message": "Runstate files already exist; rerun with --force to overwrite.",
        }

    templates_root.mkdir(parents=True, exist_ok=True)
    contract_json_path.write_text(
        json.dumps(_runstate_contract_payload(target_root.name, chosen_type), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    contract_md_path.write_text(_runstate_contract_markdown(target_root.name, chosen_type), encoding="utf-8")
    success_md_path.write_text(_success_doc(chosen_type), encoding="utf-8")

    written_files = [
        str(contract_json_path.relative_to(target_root)),
        str(contract_md_path.relative_to(target_root)),
        str(success_md_path.relative_to(target_root)),
    ]

    for checklist_name in definition["required_checklists"]:
        template_path = target_root / RUNSTATE_TEMPLATES[checklist_name]
        template_path.parent.mkdir(parents=True, exist_ok=True)
        level = "skill_flow" if checklist_name == "Skills_runtime_checklist" else "workflow" if checklist_name == "workflow_runtime_checklist" else "stage"
        template_path.write_text(
            yaml.safe_dump(_checklist_template(checklist_name, level), sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )
        written_files.append(str(template_path.relative_to(target_root)))

    return {
        "status": "ok",
        "target_skill_root": str(target_root),
        "skill_name": target_root.name,
        "governed_type": chosen_type,
        "applicability": definition["applicability"],
        "written_files": written_files,
        "skipped": False,
        "message": "Runstate contract and templates were scaffolded into the target skill.",
    }
