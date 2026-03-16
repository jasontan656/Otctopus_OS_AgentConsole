from __future__ import annotations

import re
import shutil
from pathlib import Path

from acceptance_contract_support import acceptance_lint_result
from construction_plan_rendering import PREVIEW_PLAN_KIND
from construction_plan_support import construction_plan_init_result, construction_plan_lint_summary
from devflow_agents_support import scaffold_and_collect_devflow_agents
from mother_doc_audit_support import mother_doc_audit_summary
from mother_doc_contract import (
    MOTHER_DOC_ANCHOR_FIELDS,
    MOTHER_DOC_ALLOWED_BRANCH_FAMILIES,
    MOTHER_DOC_ALLOWED_CONTENT_FAMILIES,
    MOTHER_DOC_ALLOWED_DOC_KINDS,
    MOTHER_DOC_ALLOWED_DOC_ROLES,
    MOTHER_DOC_DIRECTORY_NAME_PATTERN,
    MOTHER_DOC_FILE_BASENAME_PATTERN,
    MOTHER_DOC_FRONTMATTER_REQUIRED_FIELDS,
    MOTHER_DOC_REQUIRED_ENTRY_ALTERNATIVES,
    MOTHER_DOC_REQUIRED_ROOT_INDEX_RULES,
    MOTHER_DOC_ROOT_REQUIRED_FILES,
    MOTHER_DOC_WORK_STATES,
)
from mother_doc_lint_support import mother_doc_lint_summary
from mother_doc_root_index_support import refresh_root_index_result
from mother_doc_state_support import mark_docs_modified, sync_doc_states
from runtime_context_support import graph_postflight_summary as build_graph_postflight_summary
from runtime_context_support import graph_preflight_summary as build_graph_preflight_summary
from target_runtime_support import (
    ROOT_AGENTS_PATH,
    latest_archived_iteration,
    resolve_target_runtime,
    target_runtime_contract_payload,
)
from workflow_contract_data import ACCEPTANCE_FIELDS, ACCEPTANCE_LINT_POLICY, ACCEPTANCE_MATRIX_FIELDS
from workflow_contract_data import ADR_REQUIRED_SECTIONS, BASELINE_MODES, BLOCKED_STATES
from workflow_contract_data import DESIGN_PHASE_PLAN_SECTIONS, DISCOVERY_SCOPE_POLICY
from workflow_contract_data import EXECUTION_ATOM_PACK_MACHINE_FILES, EXECUTION_ATOM_PACK_MARKDOWN_FILES
from workflow_contract_data import EXECUTION_ATOM_PACK_ROOT_FILES, EXECUTION_ATOM_PHASE_FIELDS
from workflow_contract_data import IMPLEMENTATION_SOURCE_POLICY, PHASE_READ_POLICY
from workflow_contract_data import REQUIREMENT_ATOM_FIELDS, STAGES, TEMPLATES


DEFAULT_RUNTIME = resolve_target_runtime()
RUNTIME_ROOT = Path(DEFAULT_RUNTIME["target_root"])
CODEBASE_ROOT = Path(DEFAULT_RUNTIME["codebase_root"])
GRAPH_RUNTIME_ROOT = Path(DEFAULT_RUNTIME["graph_runtime_root"])
MOTHER_DOC_ROOT = Path(DEFAULT_RUNTIME["mother_doc_root"])
MOTHER_DOC_PATH = Path(DEFAULT_RUNTIME["mother_doc_index"])
CONSTRUCTION_PLAN_ROOT = Path(DEFAULT_RUNTIME["construction_plan_root"])
CONSTRUCTION_PLAN_INDEX_PATH = Path(DEFAULT_RUNTIME["construction_plan_index"])
ACCEPTANCE_ROOT = Path(DEFAULT_RUNTIME["acceptance_root"])
ACCEPTANCE_MATRIX_PATH = Path(DEFAULT_RUNTIME["acceptance_matrix_path"])
ACCEPTANCE_REPORT_PATH = Path(DEFAULT_RUNTIME["acceptance_report_path"])
ARCHIVE_DIR_PATTERN = re.compile(r"^(\d{2})_.+")


def mother_doc_init_result(target: Path, force: bool) -> tuple[dict, int]:
    preexisting_items = [child for child in target.iterdir()] if target.exists() else []
    if preexisting_items and not force:
        return {
            "status": "fail",
            "target": str(target),
            "reason": "target_not_empty",
            "hint": "rerun with --force to overwrite the directory-based mother doc skeleton",
        }, 1

    created_files: list[str] = []
    target.mkdir(parents=True, exist_ok=True)
    refresh_document, refresh_status = refresh_root_index_result(target)
    if refresh_status != 0:
        return refresh_document, refresh_status
    created_files.append(str(target / "00_index.md"))

    return {
        "status": "pass",
        "target": str(target),
        "created_files": created_files,
        "root_index_refresh": refresh_document,
        "lint_command": f"./.venv_backend_skills/bin/python Skills/Workflow-CentralFlow2-OctppusOS/scripts/Cli_Toolbox.py mother-doc-lint --path {target} --json",
    }, 0


def target_scaffold_result(runtime: dict[str, object], force: bool) -> tuple[dict, int]:
    if not runtime["ready_for_service"]:
        return {
            "status": "fail",
            "reason": "target_runtime_not_ready",
            "missing_prerequisites": runtime["missing_prerequisites"],
            "hint": "create the current docs_root container first, then rerun target-scaffold",
        }, 1

    created_items: list[str] = []
    operations: list[dict[str, object]] = []
    agents_result = scaffold_and_collect_devflow_agents(runtime)
    operations.append({"kind": "agents_governance", **agents_result})
    created_items.append(str(Path(runtime["docs_root"]) / "AGENTS.md"))

    graph_root = Path(runtime["graph_runtime_root"])
    graph_root.mkdir(parents=True, exist_ok=True)
    created_items.append(str(graph_root))

    mother_doc_root = Path(runtime["mother_doc_root"])
    if not mother_doc_root.exists():
        mother_doc_result, mother_doc_status = mother_doc_init_result(mother_doc_root, force=False)
        if mother_doc_status != 0:
            return {"status": "fail", "reason": "mother_doc_init_failed", "result": mother_doc_result}, 1
        operations.append({"kind": "mother_doc_init", "result": mother_doc_result})
        created_items.extend(mother_doc_result["created_files"])

    return {
        "status": "pass",
        "target_root": str(runtime["target_root"]),
        "development_docs_root": str(runtime["development_docs_root"]),
        "docs_root": str(runtime["docs_root"]),
        "graph_root": str(graph_root),
        "created_or_verified": created_items,
        "operations": operations,
    }, 0


def _slugify_archive_name(text: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
    return cleaned or "project"


def _mother_doc_archive_slug(root: Path, override_slug: str | None) -> str:
    if override_slug:
        return _slugify_archive_name(override_slug)
    index_path = root / "00_index.md"
    if not index_path.exists():
        return "project"
    for line in index_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("- project_name:"):
            return _slugify_archive_name(line.split(":", 1)[1].strip())
    return "project"


def mother_doc_archive_result(active_root: Path, force: bool, archive_slug: str | None) -> tuple[dict, int]:
    if not active_root.exists():
        return {"status": "fail", "target": str(active_root), "reason": "mother_doc_missing"}, 1
    docs_root = active_root.parent
    max_index = 0
    for child in docs_root.iterdir():
        if not child.is_dir() or child.name == active_root.name:
            continue
        match = ARCHIVE_DIR_PATTERN.match(child.name)
        if match:
            max_index = max(max_index, int(match.group(1)))
    archive_dir = docs_root / f"{max_index + 1:02d}_{_mother_doc_archive_slug(active_root, archive_slug)}"
    if archive_dir.exists() and not force:
        return {"status": "fail", "archive_dir": str(archive_dir), "reason": "archive_target_exists"}, 1
    if archive_dir.exists() and force:
        shutil.rmtree(archive_dir)
    active_root.rename(archive_dir)
    init_result, init_status = mother_doc_init_result(active_root, force=False)
    if init_status != 0:
        return {
            "status": "fail",
            "archive_dir": str(archive_dir),
            "reason": "archive_created_but_reinit_failed",
            "reinit_result": init_result,
        }, 1
    return {
        "status": "pass",
        "archived_root": str(archive_dir),
        "reinitialized_root": str(active_root),
        "archive_index": max_index + 1,
        "archive_slug": archive_dir.name.split("_", 1)[1],
    }, 0


def workflow_contract_document(
    *,
    target_root: str | Path | None = None,
    development_docs_root: str | Path | None = None,
    docs_root: str | Path | None = None,
    module_dir: str | None = None,
    codebase_root: str | Path | None = None,
    graph_runtime_root: str | Path | None = None,
    project_agents: str | Path | None = None,
) -> dict:
    runtime = resolve_target_runtime(
        target_root=target_root,
        development_docs_root=development_docs_root,
        docs_root=docs_root,
        module_dir=module_dir,
        codebase_root=codebase_root,
        graph_runtime_root=graph_runtime_root,
        project_agents=project_agents,
    )
    top_level_resident_docs = [
        "path/development_loop/10_CONTRACT.md",
        "path/development_loop/15_TOOLS.md",
        str(ROOT_AGENTS_PATH),
    ]
    project_agents_path = runtime["project_agents_path"]
    if project_agents_path is not None:
        top_level_resident_docs.append(str(project_agents_path))
    top_level_resident_docs.append(
        f"{runtime['project_structure_skill_path']} when docs_root must be chosen or overridden"
    )
    return {
        "stage_order": list(STAGES.keys()),
        "stage_objectives": {name: data["objective"] for name, data in STAGES.items()},
        "discovery_scope_policy": DISCOVERY_SCOPE_POLICY,
        "phase_read_policy": PHASE_READ_POLICY,
        "stage_specific_contract_tools": [
            "target-runtime-contract",
            "target-scaffold",
            "stage-checklist",
            "stage-doc-contract",
            "stage-command-contract",
            "stage-graph-contract",
            "template-index",
            "mother-doc-audit",
            "mother-doc-refresh-root-index",
            "mother-doc-mark-modified",
            "mother-doc-sync-client-copy",
        ],
        "top_level_resident_docs": top_level_resident_docs,
        "stage_switch_protocol": PHASE_READ_POLICY["stage_switch_protocol"],
        "target_runtime_contract": target_runtime_contract_payload(
            target_root=target_root,
            development_docs_root=development_docs_root,
            docs_root=docs_root,
            module_dir=module_dir,
            codebase_root=codebase_root,
            graph_runtime_root=graph_runtime_root,
            project_agents=project_agents,
        ),
        "stage_read_boundaries": {
            name: {
                "resident_docs": data["resident_docs"],
                "stage_docs": data["stage_docs"],
                "graph_role": data["graph_role"],
                "drop_on_stage_switch": data["drop_on_stage_switch"],
            }
            for name, data in STAGES.items()
        },
        "stage_graph_roles": {name: data["graph_role"] for name, data in STAGES.items()},
        "mother_doc_required_files": MOTHER_DOC_ROOT_REQUIRED_FILES,
        "mother_doc_required_entry_alternatives": MOTHER_DOC_REQUIRED_ENTRY_ALTERNATIVES,
        "mother_doc_frontmatter_required_fields": MOTHER_DOC_FRONTMATTER_REQUIRED_FIELDS,
        "mother_doc_anchor_fields": MOTHER_DOC_ANCHOR_FIELDS,
        "mother_doc_allowed_doc_roles": MOTHER_DOC_ALLOWED_DOC_ROLES,
        "mother_doc_allowed_doc_kinds": MOTHER_DOC_ALLOWED_DOC_KINDS,
        "mother_doc_allowed_branch_families": MOTHER_DOC_ALLOWED_BRANCH_FAMILIES,
        "mother_doc_allowed_content_families": MOTHER_DOC_ALLOWED_CONTENT_FAMILIES,
        "mother_doc_required_root_index_rules": MOTHER_DOC_REQUIRED_ROOT_INDEX_RULES,
        "mother_doc_file_basename_pattern": MOTHER_DOC_FILE_BASENAME_PATTERN,
        "mother_doc_directory_name_pattern": MOTHER_DOC_DIRECTORY_NAME_PATTERN,
        "mother_doc_work_states": MOTHER_DOC_WORK_STATES,
        "requirement_atom_required_fields": REQUIREMENT_ATOM_FIELDS,
        "baseline_mode_policy": BASELINE_MODES,
        "implementation_source_policy": IMPLEMENTATION_SOURCE_POLICY,
        "blocked_state_policy": BLOCKED_STATES,
        "graph_preflight_policy": "indexed=use_context, missing+substantial=run_analyze, missing+empty=skip_non_blocking",
        "graph_postflight_policy": "after implementation, prefer detect-changes when indexed and read resource/context only when needed",
        "required_templates": {name: str(path) for name, path in TEMPLATES.items()},
        "construction_plan_root": str(runtime["construction_plan_root"]),
        "construction_plan_index": str(runtime["construction_plan_index"]),
        "design_phase_plan_required_sections": DESIGN_PHASE_PLAN_SECTIONS,
        "construction_plan_required_sections": EXECUTION_ATOM_PACK_ROOT_FILES
        + EXECUTION_ATOM_PACK_MARKDOWN_FILES
        + EXECUTION_ATOM_PACK_MACHINE_FILES
        + EXECUTION_ATOM_PHASE_FIELDS,
        "acceptance_required_fields": ACCEPTANCE_FIELDS,
        "acceptance_matrix_required_fields": ACCEPTANCE_MATRIX_FIELDS,
        "acceptance_lint_policy": ACCEPTANCE_LINT_POLICY,
        "adr_required_sections": ADR_REQUIRED_SECTIONS,
    }


def mother_doc_state_sync_result(
    root: Path,
    doc_refs: list[str],
    from_state: str,
    to_state: str,
    pack_ref: str | None,
) -> dict:
    result = sync_doc_states(root, doc_refs, from_state, to_state, pack_ref)
    result.update(
        {
            "root": str(root),
            "doc_refs": doc_refs,
            "allowed_states": MOTHER_DOC_WORK_STATES,
            "frontmatter_fields": MOTHER_DOC_FRONTMATTER_REQUIRED_FIELDS,
        }
    )
    return result


def mother_doc_mark_modified_result(
    root: Path,
    doc_refs: list[str],
    repo_root: Path | None,
    auto_from_git: bool,
) -> dict:
    result = mark_docs_modified(root, doc_refs, repo_root=repo_root, auto_from_git=auto_from_git)
    result.update(
        {
            "root": str(root),
            "repo_root": str(repo_root) if repo_root is not None else None,
            "allowed_states": MOTHER_DOC_WORK_STATES,
            "frontmatter_fields": MOTHER_DOC_FRONTMATTER_REQUIRED_FIELDS,
        }
    )
    return result


def graph_preflight_summary(repo: Path, allow_missing_index: bool, graph_runtime_root: Path) -> dict:
    return build_graph_preflight_summary(repo, allow_missing_index, graph_runtime_root)


def graph_postflight_summary(repo: Path, graph_runtime_root: Path) -> dict:
    return build_graph_postflight_summary(repo, graph_runtime_root)
