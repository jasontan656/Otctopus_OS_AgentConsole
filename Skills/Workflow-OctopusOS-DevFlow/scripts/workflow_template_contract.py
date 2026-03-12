from __future__ import annotations

from pathlib import Path

# contract_name: octopus_devflow_workflow_template_contract
# contract_version: 1.0.0
# validation_mode: strict
# required_fields:
#   - TEMPLATES
# optional_fields: []

SKILL_ROOT = Path(__file__).resolve().parents[1]
MOTHER_DOC_TEMPLATE_ROOT = SKILL_ROOT / "assets" / "templates" / "mother_doc"

TEMPLATES = {
    "mother_doc_root": MOTHER_DOC_TEMPLATE_ROOT,
    "mother_doc_index": MOTHER_DOC_TEMPLATE_ROOT / "00_index.md",
    "mother_doc_target_state": MOTHER_DOC_TEMPLATE_ROOT / "01_target_state.md",
    "mother_doc_architecture_overview": MOTHER_DOC_TEMPLATE_ROOT / "02_architecture_overview.md",
    "mother_doc_runtime_flow": MOTHER_DOC_TEMPLATE_ROOT / "03_runtime_flow.md",
    "mother_doc_stack_decisions": MOTHER_DOC_TEMPLATE_ROOT / "04_stack_decisions.md",
    "mother_doc_domain_contracts": MOTHER_DOC_TEMPLATE_ROOT / "05_domain_contracts.md",
    "mother_doc_acceptance_contract": MOTHER_DOC_TEMPLATE_ROOT / "06_acceptance_contract.md",
    "mother_doc_env_and_deploy": MOTHER_DOC_TEMPLATE_ROOT / "07_env_and_deploy.md",
    "mother_doc_dev_execution_plan": MOTHER_DOC_TEMPLATE_ROOT / "08_dev_execution_plan.md",
    "mother_doc_regression_baseline": MOTHER_DOC_TEMPLATE_ROOT / "09_regression_baseline.md",
    "mother_doc_observability_and_evidence": MOTHER_DOC_TEMPLATE_ROOT / "10_observability_and_evidence.md",
    "mother_doc_risks_and_blockers": MOTHER_DOC_TEMPLATE_ROOT / "11_risks_and_blockers.md",
    "requirement_atom": SKILL_ROOT / "assets" / "templates" / "REQUIREMENT_ATOM_TEMPLATE.md",
    "construction_plan_root": SKILL_ROOT / "assets" / "templates" / "execution_atom_plan_validation_packs",
    "construction_plan_index": SKILL_ROOT / "assets" / "templates" / "execution_atom_plan_validation_packs" / "00_index.md",
    "execution_atom_pack_template_root": SKILL_ROOT / "assets" / "templates" / "execution_atom_plan_validation_packs" / "PACK_TEMPLATE",
    "agents_external_entry": SKILL_ROOT / "assets" / "templates" / "agents" / "EXTERNAL_AGENTS.md",
    "agents_machine_payload": SKILL_ROOT / "assets" / "templates" / "agents" / "AGENTS_MACHINE_TEMPLATE.json",
    "adr_record": MOTHER_DOC_TEMPLATE_ROOT / "12_adrs" / "ADR_TEMPLATE.md",
    "acceptance_report": SKILL_ROOT / "assets" / "templates" / "ACCEPTANCE_REPORT_TEMPLATE.md",
    "acceptance_matrix": SKILL_ROOT / "assets" / "templates" / "ACCEPTANCE_MATRIX_TEMPLATE.md",
}
