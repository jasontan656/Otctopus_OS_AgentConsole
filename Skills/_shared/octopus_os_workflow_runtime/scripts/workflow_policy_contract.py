from __future__ import annotations

# permission_boundary_markers:
#   - actor_id
#   - role
#   - authz_result
#   - deny_code
#   - policy_version

from skill_runtime_context import top_level_resident_docs
from workflow_policy_paths import resolve_product_root


PRODUCT_ROOT = resolve_product_root()
ROOT_AGENTS_PATH = (PRODUCT_ROOT / "AGENTS.md").resolve()


DISCOVERY_SCOPE_POLICY = {
    "allowed_roots": [
        "<target_root as repo_root_boundary>",
        "<docs_root>",
        "<mother_doc_root>",
        "<codebase_root>",
        "current_skill_files",
        "required_graph_skill_files",
        "Dev-ProjectStructure-Constitution when docs_root is not yet fixed",
    ],
    "workspace_container_root": str(PRODUCT_ROOT),
    "workspace_container_root_is_discovery_target": False,
    "fixed_startup_paths": [
        "<mother_doc_root>/00_index.md when present",
        "<docs_root>/AGENTS.md when present",
        "Dev-ProjectStructure-Constitution/SKILL.md when docs_root must be chosen",
    ],
    "required_startup_sequence": [
        "run_target_runtime_contract_for_current_target",
        "confirm_or_override_docs_root_before_any_write",
        "run_meta_impact_investigation_in_write_intent_mode",
        "read_resident_overview_index_and_common_rule_docs_before_deepening_any_specific_topic",
        "read_mother_doc_index_or_directory",
        "inspect_latest_archived_mother_doc_if_present",
        "inspect_existing_execution_packs_if_present",
        "derive_requirement_source_from_live_request_current_docs_and_latest_archive",
        "check_or_initialize_code_graph_runtime_when_repo_is_substantive",
        "read_graph_context_for_current_code_reality_when_available_and_reusable",
        "decide_if_structure_governance_is_needed",
        "when_a_new_anchor_doc_is_needed_require_the_user_to_name_the_next_doc_topic_before_creating_it",
        "decide_growth_path_and_smallest_write_slice_before_real_edit",
        "sync_overview_index_and_architecture_map_docs_after_topic_level_writeback_when_global_shape_changed",
        "run_mother_doc_lint_before_stage_exit_and_invoke_mother_doc_audit_only_for_explicit_governance_needs",
        "only_then_read_concrete_codebase_files_if_construction_plan_or_implementation_requires_them",
    ],
    "forbidden_roots": [
        str((PRODUCT_ROOT / "Human_Work_Zone").resolve()),
        str((PRODUCT_ROOT / "GoogleDriveDump").resolve()),
    ],
    "repo_wide_container_scan_allowed": False,
}

PHASE_READ_POLICY = {
    "top_level_resident_docs": top_level_resident_docs()
    + [
        str(ROOT_AGENTS_PATH),
        "<docs_root>/AGENTS.md when present",
        "Dev-ProjectStructure-Constitution/SKILL.md when docs_root is not yet fixed",
    ],
    "single_stage_rule": "read only the current stage checklist and the artifacts required by that stage",
    "multi_stage_rule": "when switching stages, reload the new stage checklist and discard the previous stage instruction focus",
    "stage_switch_protocol": [
        "keep only top_level_resident_docs across stage switches",
        "reload the target stage checklist before reading any target stage docs",
        "discard previous stage temporary notes, checklists, and artifact-specific focus unless the new stage explicitly requires them",
    ],
    "question_answer_rule": "when the user is filling mother doc chapters interactively, answer with bounded options or structured prompts rather than free-form essays; if the next deeper anchor topic is still undefined, ask for that topic explicitly instead of auto-inventing it",
}

MOTHER_DOC_GOVERNANCE_POLICY = {
    "primary_requirement_sources": [
        "live user task or current turn request",
        "<docs_root>/AGENTS.md and project runtime constraints when present",
        "resident mother_doc overview/index/common-rule branches that already define the stable documentation spine",
        "current <docs_root>/mother_doc tree",
        "latest archived mother_doc iteration when present",
        "current code reality and graph context only as reconciliation evidence",
    ],
    "mandatory_actions": [
        "treat mother_doc as a writing flow that places requirement semantics into the current doc system rather than as a giant all-in-one knowledge tree",
        "derive the intended semantic move from the live need before writing or restructuring the tree",
        "keep top-level documents focused on resident norms, product baseline, common rules, and index/navigation duties",
        "let documents descend from human narrative to machine narrative as they move downward through the tree",
        "when the next deeper anchor doc is needed, require the user to specify that topic explicitly before creating the new anchor node",
        "after a deeper topic write changes the global architecture shape, sync the related overview, index, and entry-map docs in the same turn",
        "run mother-doc-lint before leaving the mother_doc stage",
        "refresh 00_index.md after any structural write",
        "sync the client mirror after real mother_doc edits",
    ],
    "optional_governance_actions": [
        "invoke mother-doc-audit when the tree is overloaded, ambiguous, drifting, or undergoing a substantial rewrite",
        "reuse registry-backed split proposals when they help, but keep the live requirement intent primary",
    ],
    "forbidden_patterns": [
        "treating mother-doc-audit as a fixed prerequisite before understanding the request",
        "treating audit output as a replacement for the real requirement source",
        "using audit to hide main-flow mother_doc design defects that should be solved in the stage contract itself",
        "building a giant mixed tree that writes frontend, backend, implementation, and acceptance semantics into the same uncontrolled branch",
        "auto-creating the next deeper anchor topic without explicit user selection",
        "turning mother_doc evidence writeback into construction-log prose or implementation流水",
    ],
}

MOTHER_DOC_FRONTMATTER_FIELDS = [
    "doc_work_state",
    "doc_pack_refs",
    "doc_kind",
    "content_family",
    "thumb_title",
    "thumb_summary",
    "display_layer",
    "always_read",
    "anchors_down",
    "anchors_support",
    "branch_family(optional)",
]

MOTHER_DOC_WORK_STATES = [
    "modified",
    "planned",
    "developed",
    "ref",
]

REQUIREMENT_ATOM_FIELDS = [
    "requirement_atom_id",
    "source_clause",
    "behavior",
    "non_goals",
    "failure_semantics",
    "acceptance_rule",
    "witness_type",
    "dependencies",
    "owner_package_id",
]

BASELINE_MODES = ["empty_baseline", "real_codebase"]

IMPLEMENTATION_SOURCE_POLICY = {
    "default_for_near_empty_worktree": "empty_baseline",
    "implementation_source_scope": "current_worktree_only",
    "mother_doc_read_scope": "active_pack_declared_source_mother_doc_refs_plus_ref_docs_when_needed",
    "forbidden_actions": [
        "reading non-worktree source artifacts as implementation material",
        "reading non-worktree tests as implementation material",
        "reading unrelated modified mother_doc docs during implementation",
        "reading the whole mother_doc tree instead of pack-declared source refs",
    ],
}

BLOCKED_STATES = [
    "clear_to_proceed",
    "needs_input",
    "needs_real_env",
    "needs_baseline_decision",
]

DESIGN_PHASE_PLAN_SECTIONS = [
    "阶段总览",
    "design_step_id",
    "目标 requirement_atoms",
    "前置依赖",
    "实施动作",
    "阶段断言",
    "阶段测试",
    "阶段验收",
    "上线交付 witness",
    "风险与回滚",
]

EXECUTION_ATOM_PACK_ROOT_FILES = ["00_index.md", "pack_registry.yaml"]
EXECUTION_ATOM_PLAN_KIND_VALUES = ["official_plan", "preview_skeleton"]
EXECUTION_ATOM_ROOT_STATE_VALUES = ["planned_unused", "in_execution", "implemented", "accepted", "retired", "preview_only"]
EXECUTION_ATOM_PACK_STATE_VALUES = ["planned_unused", "in_execution", "implemented", "accepted", "retired", "preview_only"]

EXECUTION_ATOM_PACK_MARKDOWN_FILES = [
    "00_index.md",
    "01_scope_and_intent.md",
    "02_inner_dev_phases.md",
    "03_validation_and_writeback.md",
]

EXECUTION_ATOM_PACK_MACHINE_FILES = [
    "pack_manifest.yaml",
    "inner_phase_plan.json",
    "phase_status.jsonl",
    "evidence_registry.json",
]

EXECUTION_ATOM_PHASE_FIELDS = [
    "inner_phase_id",
    "phase_goal",
    "implementation_slice",
    "validation_slice",
    "evidence_writeback_slice",
    "phase_exit_signal",
]

EXECUTION_ATOM_PLAN_LIFECYCLE_RULES = {
    "official_plan_prerequisite": "mother_doc must already exist, mother-doc-lint must pass, and at least one mother_doc atom must be marked modified so construction_plan can cluster the changed slice into packs",
    "preview_skeleton_usage": "preview_skeleton is display-only scaffolding and cannot be used for implementation, state sync, or active pack selection",
    "fresh_plan_rule": "official construction plans start at planned_unused and become in_execution only when implementation consumes them",
    "non_reuse_rule": "accepted or retired official plans cannot be recycled as the fresh input of a new construction round; generate a new official plan instead",
}

ACCEPTANCE_FIELDS = [
    "plan_step_id",
    "implemented_files",
    "tests_run",
    "real_witnesses",
    "residual_risks",
    "rollback_notes",
]

ACCEPTANCE_MATRIX_FIELDS = [
    "requirement_atom_id",
    "implemented",
    "tested",
    "witnessed",
    "blocked_state",
    "evidence_refs",
]

ACCEPTANCE_LINT_POLICY = {
    "implemented_true_requires_existing_non_doc_evidence": True,
    "tested_true_requires_existing_test_evidence": True,
    "witnessed_true_forbidden_when_blocked_state_needs_real_env": True,
    "acceptance_docs_must_follow_implementation": True,
    "ref_state_requires_acceptance_closeout": True,
    "ref_state_requires_graph_postflight": True,
}

ADR_REQUIRED_SECTIONS = [
    "adr_id",
    "title",
    "context",
    "decision",
    "consequences",
    "status",
]
