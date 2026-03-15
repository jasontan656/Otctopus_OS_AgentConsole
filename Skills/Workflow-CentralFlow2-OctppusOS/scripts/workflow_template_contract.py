from __future__ import annotations

from pathlib import Path

# contract_name: octopus_devflow_workflow_template_contract
# contract_version: 1.0.0
# validation_mode: strict
# required_fields:
#   - TEMPLATES
# optional_fields: []

SKILL_ROOT = Path(__file__).resolve().parents[1]
MOTHER_DOC_TEMPLATE_ROOT = (
    SKILL_ROOT / "path" / "development_loop" / "steps" / "mother_doc" / "templates" / "mother_doc"
)

TEMPLATES = {
    "mother_doc_root": MOTHER_DOC_TEMPLATE_ROOT,
    "mother_doc_index": MOTHER_DOC_TEMPLATE_ROOT / "00_index.md",
    "requirement_atom": SKILL_ROOT / "path" / "development_loop" / "steps" / "mother_doc" / "templates" / "REQUIREMENT_ATOM_TEMPLATE.md",
    "construction_plan_root": SKILL_ROOT / "path" / "development_loop" / "steps" / "construction_plan" / "templates" / "execution_atom_plan_validation_packs",
    "construction_plan_index": SKILL_ROOT / "path" / "development_loop" / "steps" / "construction_plan" / "templates" / "execution_atom_plan_validation_packs" / "00_index.md",
    "execution_atom_pack_template_root": SKILL_ROOT / "path" / "development_loop" / "steps" / "construction_plan" / "templates" / "execution_atom_plan_validation_packs" / "PACK_TEMPLATE",
    "agents_external_entry": SKILL_ROOT / "path" / "development_loop" / "steps" / "mother_doc" / "templates" / "agents" / "EXTERNAL_AGENTS.md",
    "agents_machine_payload": SKILL_ROOT / "path" / "development_loop" / "steps" / "mother_doc" / "templates" / "agents" / "AGENTS_MACHINE_TEMPLATE.json",
    "acceptance_report": SKILL_ROOT / "path" / "development_loop" / "steps" / "acceptance" / "templates" / "ACCEPTANCE_REPORT_TEMPLATE.md",
    "acceptance_matrix": SKILL_ROOT / "path" / "development_loop" / "steps" / "acceptance" / "templates" / "ACCEPTANCE_MATRIX_TEMPLATE.md",
}
