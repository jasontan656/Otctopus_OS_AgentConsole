from __future__ import annotations

# contract_name: octopus_devflow_mother_doc_contract
# contract_version: 2.0.0
# validation_mode: strict
# required_fields:
#   - MOTHER_DOC_REQUIRED_FILES
#   - MOTHER_DOC_REQUIRED_ENTRY_ALTERNATIVES
#   - MOTHER_DOC_REQUIRED_SIGNALS
#   - MOTHER_DOC_FORBIDDEN_TERMS
#   - MOTHER_DOC_REQUIRED_STAGE_IDS
#   - MOTHER_DOC_STAGE_PLAN_MARKERS
#   - MOTHER_DOC_GUIDANCE_MARKERS
#   - MOTHER_DOC_FRONTMATTER_REQUIRED_FIELDS
#   - MOTHER_DOC_WORK_STATES
#   - MOTHER_DOC_STATE_TRANSITIONS
# optional_fields: []

MOTHER_DOC_REQUIRED_FILES = [
    "00_index.md",
    "01_target_state.md",
    "02_architecture_overview.md",
    "03_runtime_flow.md",
    "04_stack_decisions.md",
    "05_domain_contracts.md",
    "06_acceptance_contract.md",
    "07_env_and_deploy.md",
    "08_dev_execution_plan.md",
    "09_regression_baseline.md",
    "10_observability_and_evidence.md",
    "11_risks_and_blockers.md",
    "12_adrs/ADR_TEMPLATE.md",
]

MOTHER_DOC_REQUIRED_ENTRY_ALTERNATIVES = {
    "00_index": ["00_index.md"],
    "01_target_state": ["01_target_state.md", "01_target_state/00_index.md"],
    "02_architecture_overview": ["02_architecture_overview.md", "02_architecture_overview/00_index.md"],
    "03_runtime_flow": ["03_runtime_flow.md", "03_runtime_flow/00_index.md"],
    "04_stack_decisions": ["04_stack_decisions.md", "04_stack_decisions/00_index.md"],
    "05_domain_contracts": ["05_domain_contracts.md", "05_domain_contracts/00_index.md"],
    "06_acceptance_contract": ["06_acceptance_contract.md", "06_acceptance_contract/00_index.md"],
    "07_env_and_deploy": ["07_env_and_deploy.md", "07_env_and_deploy/00_index.md"],
    "08_dev_execution_plan": ["08_dev_execution_plan.md", "08_dev_execution_plan/00_index.md"],
    "09_regression_baseline": ["09_regression_baseline.md", "09_regression_baseline/00_index.md"],
    "10_observability_and_evidence": [
        "10_observability_and_evidence.md",
        "10_observability_and_evidence/00_index.md",
    ],
    "11_risks_and_blockers": ["11_risks_and_blockers.md", "11_risks_and_blockers/00_index.md"],
    "12_adrs_template": ["12_adrs/ADR_TEMPLATE.md"],
}

MOTHER_DOC_FRONTMATTER_REQUIRED_FIELDS = [
    "doc_work_state",
    "doc_pack_refs",
]

MOTHER_DOC_WORK_STATES = [
    "modified",
    "planned",
    "developed",
    "ref",
]

MOTHER_DOC_STATE_TRANSITIONS = {
    "modified": ["planned"],
    "planned": ["modified", "developed"],
    "developed": ["modified", "ref"],
    "ref": ["modified"],
}

MOTHER_DOC_REQUIRED_SIGNALS = [
    "生产级",
    "requirement_atom",
    "阶段断言",
    "阶段测试",
    "阶段验收",
    "上线可交付",
]

MOTHER_DOC_FORBIDDEN_TERMS = [
    "最小闭环",
    "最小实现",
    "mvp",
    "test profile",
    "test-profile",
    "demo only",
    "样板实现",
]

MOTHER_DOC_REQUIRED_STAGE_IDS = [
    "mother_doc",
    "construction_plan",
    "implementation",
    "acceptance",
]

MOTHER_DOC_STAGE_PLAN_MARKERS = [
    "stage_id",
    "stage_goal",
    "stage_assertions",
    "stage_tests",
    "stage_exit_evidence",
]

MOTHER_DOC_GUIDANCE_MARKERS = [
    "fill_rule:",
    "Replace every replace_me token",
    "Remove this guidance block after drafting.",
]
