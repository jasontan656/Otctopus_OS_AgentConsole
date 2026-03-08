from __future__ import annotations

import re

# contract_name: octopus_backend_construction_plan_contract
# contract_version: 1.0.0
# validation_mode: strict
# required_fields:
#   - PACK_DIR_PATTERN
#   - ROOT_REQUIRED_FILES
#   - PACK_MARKDOWN_FILES
#   - PACK_MACHINE_FILES
#   - MANIFEST_REQUIRED_KEYS
#   - MANIFEST_MACHINE_FILE_MAP
#   - INNER_PHASE_REQUIRED_KEYS
# optional_fields: []

PACK_DIR_PATTERN = re.compile(r"^\d{2}_.+")
PACK_ID_PATTERN = re.compile(r"^PACK-\d{2}$")
INNER_PHASE_PATTERN = re.compile(r"^PHASE-\d{2}$")
ROOT_REQUIRED_FILES = ["00_index.md", "pack_registry.yaml"]
PACK_MARKDOWN_FILES = ["00_index.md", "01_scope_and_intent.md", "02_inner_dev_phases.md", "03_validation_and_writeback.md"]
PACK_MACHINE_FILES = ["pack_manifest.yaml", "inner_phase_plan.json", "phase_status.jsonl", "evidence_registry.json"]
GUIDANCE_MARKERS = ["replace_me_fill_rule:", "Remove this guidance block after drafting."]
MANIFEST_REQUIRED_KEYS = {
    "pack_id",
    "design_step_id",
    "pack_goal",
    "design_plan_refs",
    "target_requirement_atoms",
    "implementation_actions",
    "changed_files_boundary",
    "stage_acceptance_target",
    "machine_files",
}
MANIFEST_MACHINE_FILE_MAP = {
    "inner_phase_plan": "inner_phase_plan.json",
    "phase_status_ledger": "phase_status.jsonl",
    "evidence_registry": "evidence_registry.json",
}
INNER_PHASE_REQUIRED_KEYS = {
    "inner_phase_id",
    "phase_goal",
    "implementation_slice",
    "validation_slice",
    "evidence_writeback_slice",
    "phase_exit_signal",
}
PACK_ALLOWED_WRITEBACK_FILES = set(PACK_MARKDOWN_FILES + PACK_MACHINE_FILES)
