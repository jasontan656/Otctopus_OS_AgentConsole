from __future__ import annotations

import re
import shutil
from pathlib import Path

from acceptance_contract_support import acceptance_lint_payload
from construction_plan_support import construction_plan_init_payload, construction_plan_lint_payload
from mother_doc_contract import MOTHER_DOC_FORBIDDEN_TERMS, MOTHER_DOC_REQUIRED_FILES, MOTHER_DOC_REQUIRED_SIGNALS
from mother_doc_lint_support import mother_doc_lint_payload
from runtime_context_support import graph_postflight_payload as build_graph_postflight_payload
from runtime_context_support import graph_preflight_payload as build_graph_preflight_payload
from workflow_contract_data import ACCEPTANCE_LINT_POLICY, ADR_REQUIRED_SECTIONS, ACCEPTANCE_FIELDS
from workflow_contract_data import ACCEPTANCE_MATRIX_FIELDS, BASELINE_MODES, BLOCKED_STATES
from workflow_contract_data import DESIGN_PHASE_PLAN_SECTIONS, DISCOVERY_SCOPE_POLICY
from workflow_contract_data import EXECUTION_ATOM_PACK_MACHINE_FILES, EXECUTION_ATOM_PACK_MARKDOWN_FILES
from workflow_contract_data import EXECUTION_ATOM_PACK_ROOT_FILES, EXECUTION_ATOM_PHASE_FIELDS, PHASE_READ_POLICY
from workflow_contract_data import IMPLEMENTATION_SOURCE_POLICY
from workflow_contract_data import REQUIREMENT_ATOM_FIELDS, STAGES, TEMPLATES


def _resolve_product_root() -> Path:
    script_path = Path(__file__).resolve()
    repo_root = next((parent for parent in script_path.parents if parent.name == "Otctopus_OS_AgentConsole"), None)
    if repo_root is None:
        raise RuntimeError("cannot resolve product root from Disabled-Octupos-OS-Backend script path")
    return repo_root.parent


PRODUCT_ROOT = _resolve_product_root()
RUNTIME_ROOT = (PRODUCT_ROOT / "OctuposOS_Runtime_Backend").resolve()
CODEBASE_ROOT = (PRODUCT_ROOT / "Octopus_CodeBase_Backend").resolve()
GRAPH_RUNTIME_ROOT = RUNTIME_ROOT / "code_graph_runtime"
MOTHER_DOC_ROOT = RUNTIME_ROOT / "docs" / "mother_doc"
MOTHER_DOC_PATH = MOTHER_DOC_ROOT / "00_index.md"
CONSTRUCTION_PLAN_ROOT = MOTHER_DOC_ROOT / "execution_atom_plan_validation_packs"
CONSTRUCTION_PLAN_INDEX_PATH = CONSTRUCTION_PLAN_ROOT / "00_index.md"
ACCEPTANCE_ROOT = MOTHER_DOC_ROOT / "acceptance"
ACCEPTANCE_MATRIX_PATH = ACCEPTANCE_ROOT / "acceptance_matrix.md"
ACCEPTANCE_REPORT_PATH = ACCEPTANCE_ROOT / "acceptance_report.md"
ARCHIVE_DIR_PATTERN = re.compile(r"^(\d{2})_.+")


def mother_doc_init_payload(target: Path, force: bool) -> tuple[dict, int]:
    template_root = Path(TEMPLATES["mother_doc_root"]).resolve()
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
    for source in sorted(template_root.rglob("*")):
        relative_path = source.relative_to(template_root)
        destination = target / relative_path
        if source.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        created_files.append(str(destination))

    return {
        "status": "pass",
        "target": str(target),
        "created_files": created_files,
        "lint_command": f"./.venv_backend_skills/bin/python Skills/Disabled-Octupos-OS-Backend/scripts/Cli_Toolbox.py mother-doc-lint --path {target} --json",
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


def mother_doc_archive_payload(active_root: Path, force: bool, archive_slug: str | None) -> tuple[dict, int]:
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
    init_payload, init_status = mother_doc_init_payload(active_root, force=False)
    if init_status != 0:
        return {"status": "fail", "archive_dir": str(archive_dir), "reason": "archive_created_but_reinit_failed", "reinit_payload": init_payload}, 1
    return {
        "status": "pass",
        "archived_root": str(archive_dir),
        "reinitialized_root": str(active_root),
        "archive_index": max_index + 1,
        "archive_slug": archive_dir.name.split("_", 1)[1],
    }, 0

def workflow_contract_payload() -> dict:
    return {
        "stage_order": list(STAGES.keys()),
        "stage_objectives": {name: data["objective"] for name, data in STAGES.items()},
        "discovery_scope_policy": DISCOVERY_SCOPE_POLICY,
        "phase_read_policy": PHASE_READ_POLICY,
        "stage_specific_contract_tools": [
            "stage-checklist",
            "stage-doc-contract",
            "stage-command-contract",
            "stage-graph-contract",
            "template-index",
        ],
        "top_level_resident_docs": PHASE_READ_POLICY["top_level_resident_docs"],
        "stage_switch_protocol": PHASE_READ_POLICY["stage_switch_protocol"],
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
        "mother_doc_required_files": MOTHER_DOC_REQUIRED_FILES,
        "mother_doc_required_signals": MOTHER_DOC_REQUIRED_SIGNALS,
        "mother_doc_forbidden_terms": MOTHER_DOC_FORBIDDEN_TERMS,
        "requirement_atom_required_fields": REQUIREMENT_ATOM_FIELDS,
        "baseline_mode_policy": BASELINE_MODES,
        "implementation_source_policy": IMPLEMENTATION_SOURCE_POLICY,
        "blocked_state_policy": BLOCKED_STATES,
        "graph_preflight_policy": "indexed=use_context, missing+substantial=run_analyze, missing+empty=skip_non_blocking",
        "graph_postflight_policy": "after implementation, prefer detect-changes/map/wiki when indexed",
        "required_templates": {name: str(path) for name, path in TEMPLATES.items()},
        "construction_plan_root": str(CONSTRUCTION_PLAN_ROOT),
        "construction_plan_index": str(CONSTRUCTION_PLAN_INDEX_PATH),
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


def graph_preflight_payload(repo: Path, allow_missing_index: bool) -> dict:
    return build_graph_preflight_payload(repo, allow_missing_index, GRAPH_RUNTIME_ROOT)


def graph_postflight_payload(repo: Path) -> dict:
    return build_graph_postflight_payload(repo, GRAPH_RUNTIME_ROOT)
