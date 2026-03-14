from __future__ import annotations

import os
import re
from pathlib import Path
from typing import TypedDict

from runtime_context_support import is_indexed, repo_has_substantial_code


def _resolve_repo_root() -> Path:
    script_path = Path(__file__).resolve()
    repo_root = next(
        (parent for parent in script_path.parents if parent.name == "Otctopus_OS_AgentConsole"),
        None,
    )
    if repo_root is None:
        raise RuntimeError("cannot resolve repo root from Workflow-CentralFlow1-OctopusOS script path")
    return repo_root


REPO_ROOT = _resolve_repo_root()
WORKSPACE_ROOT = REPO_ROOT.parent
ROOT_AGENTS_PATH = (WORKSPACE_ROOT / "AGENTS.md").resolve()


def _resolve_codex_home() -> Path:
    local_codex_home = (WORKSPACE_ROOT / ".codex").resolve()
    if local_codex_home.exists():
        return local_codex_home
    env_home = os.environ.get("CODEX_HOME", "").strip()
    if env_home:
        return Path(env_home).expanduser().resolve()
    return (Path.home() / ".codex").resolve()


PROJECT_STRUCTURE_SKILL_PATH = (
    _resolve_codex_home() / "skills" / "Dev-ProjectStructure-Constitution" / "SKILL.md"
)
DEVELOPMENT_DOCS_DIRNAME = "Development_Docs"

ARCHIVE_DIR_PATTERN = re.compile(r"^(\d{2})_.+")
PACK_DIR_PATTERN = re.compile(r"^\d{2}_.+")


class TargetRuntimeRecord(TypedDict):
    target_root: Path
    development_docs_root: Path
    module_dir: str | None
    docs_root: Path
    docs_root_source: str
    codebase_root: Path
    graph_runtime_root: Path
    mother_doc_root: Path
    mother_doc_index: Path
    construction_plan_root: Path
    construction_plan_index: Path
    acceptance_root: Path
    acceptance_matrix_path: Path
    acceptance_report_path: Path
    project_agents_path: Path | None
    root_agents_path: Path
    workspace_root: Path
    project_structure_skill_path: Path
    mother_doc_exists: bool
    mother_doc_index_exists: bool
    latest_archived_iteration: Path | None
    construction_plan_exists: bool
    pack_registry_exists: bool
    numbered_pack_dirs: list[Path]
    acceptance_exists: bool
    graph_registry_exists: bool
    graph_indexed_for_codebase: bool
    substantial_codebase: bool
    missing_prerequisites: list[str]
    ready_for_service: bool


class TargetRuntimeContractPayload(TypedDict):
    status: str
    target_root: str
    development_docs_root: str
    module_dir: str | None
    docs_root: str
    docs_root_source: str
    docs_root_resolution_rule: str
    module_dir_role: str
    project_structure_skill_path: str
    workspace_root: str
    root_agents_path: str
    project_agents_path: str | None
    codebase_root: str
    graph_runtime_root: str
    mother_doc_root: str
    mother_doc_index: str
    mother_doc_exists: bool
    latest_archived_iteration: str | None
    construction_plan_root: str
    construction_plan_index: str
    construction_plan_exists: bool
    pack_registry_exists: bool
    numbered_pack_dirs: list[str]
    active_task_pack_exists: bool
    acceptance_root: str
    acceptance_exists: bool
    graph_registry_exists: bool
    graph_indexed_for_codebase: bool
    substantial_codebase: bool
    missing_prerequisites: list[str]
    ready_for_service: bool
    reuse_actions: list[str]
    first_actions: list[str]


def _resolve_optional(path: str | Path | None) -> Path | None:
    if path is None:
        return None
    return Path(path).resolve()


def latest_archived_iteration(mother_doc_root: Path) -> Path | None:
    docs_root = mother_doc_root.parent
    if not docs_root.exists():
        return None
    candidates: list[tuple[int, Path]] = []
    for child in docs_root.iterdir():
        if not child.is_dir() or child.name == mother_doc_root.name:
            continue
        match = ARCHIVE_DIR_PATTERN.match(child.name)
        if match:
            candidates.append((int(match.group(1)), child))
    if not candidates:
        return None
    candidates.sort(key=lambda item: item[0], reverse=True)
    return candidates[0][1]


def numbered_pack_dirs(construction_plan_root: Path) -> list[Path]:
    if not construction_plan_root.exists():
        return []
    return sorted(
        [
            child
            for child in construction_plan_root.iterdir()
            if child.is_dir() and PACK_DIR_PATTERN.match(child.name)
        ]
    )


def _default_docs_root(
    target_root: Path,
    explicit_codebase_root: Path | None,
) -> Path:
    if explicit_codebase_root is not None:
        return (explicit_codebase_root / DEVELOPMENT_DOCS_DIRNAME).resolve()
    return (target_root / DEVELOPMENT_DOCS_DIRNAME).resolve()


def _infer_module_dir(docs_root: Path, codebase_root: Path, explicit_module_dir: str | None) -> str | None:
    if explicit_module_dir:
        return explicit_module_dir
    if docs_root.name == DEVELOPMENT_DOCS_DIRNAME:
        return codebase_root.name
    return docs_root.name


def resolve_target_runtime(
    *,
    target_root: str | Path | None = None,
    development_docs_root: str | Path | None = None,
    docs_root: str | Path | None = None,
    module_dir: str | None = None,
    codebase_root: str | Path | None = None,
    graph_runtime_root: str | Path | None = None,
    project_agents: str | Path | None = None,
) -> TargetRuntimeRecord:
    resolved_target_root = Path(target_root or WORKSPACE_ROOT).resolve()
    explicit_codebase_root = _resolve_optional(codebase_root)
    explicit_docs_root = _resolve_optional(docs_root)
    explicit_development_docs_root = _resolve_optional(development_docs_root)

    if explicit_docs_root is not None:
        resolved_docs_root = explicit_docs_root
    elif explicit_development_docs_root is not None:
        resolved_docs_root = explicit_development_docs_root
    else:
        resolved_docs_root = _default_docs_root(resolved_target_root, explicit_codebase_root)

    resolved_development_docs_root = (
        explicit_development_docs_root or resolved_docs_root
    )

    if explicit_docs_root is not None and explicit_development_docs_root is not None:
        docs_roots_match = explicit_docs_root == explicit_development_docs_root
    else:
        docs_roots_match = True

    resolved_codebase_root = (
        explicit_codebase_root
        if explicit_codebase_root is not None
        else resolved_docs_root.parent.resolve()
    )
    inferred_module_dir = _infer_module_dir(resolved_docs_root, resolved_codebase_root, module_dir)
    resolved_graph_runtime_root = (
        Path(graph_runtime_root).resolve()
        if graph_runtime_root
        else (resolved_docs_root / "graph").resolve()
    )
    resolved_mother_doc_root = resolved_docs_root / "mother_doc"
    resolved_construction_plan_root = (
        resolved_mother_doc_root / "execution_atom_plan_validation_packs"
    )
    resolved_acceptance_root = resolved_mother_doc_root / "acceptance"

    resolved_project_agents = _resolve_optional(project_agents)
    if resolved_project_agents is None:
        implicit_agents = resolved_docs_root / "AGENTS.md"
        resolved_project_agents = implicit_agents if implicit_agents.exists() else None

    latest_archive = latest_archived_iteration(resolved_mother_doc_root)
    pack_dirs = numbered_pack_dirs(resolved_construction_plan_root)
    pack_registry = resolved_construction_plan_root / "pack_registry.yaml"
    graph_registry = resolved_graph_runtime_root / "registry" / "registry.json"
    graph_indexed = (
        is_indexed(resolved_codebase_root, resolved_graph_runtime_root)
        if graph_registry.exists()
        else False
    )
    substantial_codebase = repo_has_substantial_code(resolved_codebase_root)

    missing_prerequisites: list[str] = []
    if not resolved_target_root.exists():
        missing_prerequisites.append("target_root_missing")
    if not docs_roots_match:
        missing_prerequisites.append("development_docs_root_must_equal_docs_root")
    if not resolved_docs_root.is_relative_to(resolved_target_root):
        missing_prerequisites.append("docs_root_outside_target_root")
    if not resolved_docs_root.exists():
        missing_prerequisites.append("docs_root_missing")
    if not resolved_codebase_root.is_relative_to(resolved_target_root):
        missing_prerequisites.append("codebase_root_outside_target_root")

    ready_for_service = not missing_prerequisites

    return {
        "target_root": resolved_target_root,
        "development_docs_root": resolved_docs_root,
        "module_dir": inferred_module_dir,
        "docs_root": resolved_docs_root,
        "docs_root_source": (
            "explicit_docs_root"
            if explicit_docs_root is not None
            else "explicit_development_docs_root"
            if explicit_development_docs_root is not None
            else "target_root_default_development_docs"
        ),
        "codebase_root": resolved_codebase_root,
        "graph_runtime_root": resolved_graph_runtime_root,
        "mother_doc_root": resolved_mother_doc_root,
        "mother_doc_index": resolved_mother_doc_root / "00_index.md",
        "construction_plan_root": resolved_construction_plan_root,
        "construction_plan_index": resolved_construction_plan_root / "00_index.md",
        "acceptance_root": resolved_acceptance_root,
        "acceptance_matrix_path": resolved_acceptance_root / "acceptance_matrix.md",
        "acceptance_report_path": resolved_acceptance_root / "acceptance_report.md",
        "project_agents_path": resolved_project_agents,
        "root_agents_path": ROOT_AGENTS_PATH,
        "workspace_root": WORKSPACE_ROOT,
        "project_structure_skill_path": PROJECT_STRUCTURE_SKILL_PATH,
        "mother_doc_exists": resolved_mother_doc_root.exists(),
        "mother_doc_index_exists": (resolved_mother_doc_root / "00_index.md").exists(),
        "latest_archived_iteration": latest_archive,
        "construction_plan_exists": resolved_construction_plan_root.exists(),
        "pack_registry_exists": pack_registry.exists(),
        "numbered_pack_dirs": pack_dirs,
        "acceptance_exists": resolved_acceptance_root.exists(),
        "graph_registry_exists": graph_registry.exists(),
        "graph_indexed_for_codebase": graph_indexed,
        "substantial_codebase": substantial_codebase,
        "missing_prerequisites": missing_prerequisites,
        "ready_for_service": ready_for_service,
    }


def target_runtime_contract_payload(
    *,
    target_root: str | Path | None = None,
    development_docs_root: str | Path | None = None,
    docs_root: str | Path | None = None,
    module_dir: str | None = None,
    codebase_root: str | Path | None = None,
    graph_runtime_root: str | Path | None = None,
    project_agents: str | Path | None = None,
) -> TargetRuntimeContractPayload:
    runtime = resolve_target_runtime(
        target_root=target_root,
        development_docs_root=development_docs_root,
        docs_root=docs_root,
        module_dir=module_dir,
        codebase_root=codebase_root,
        graph_runtime_root=graph_runtime_root,
        project_agents=project_agents,
    )
    numbered_pack_dirs_value = [str(path) for path in runtime["numbered_pack_dirs"]]
    latest_archive = runtime["latest_archived_iteration"]
    project_agents_path = runtime["project_agents_path"]

    reuse_actions: list[str] = []
    if runtime["mother_doc_exists"]:
        reuse_actions.append("reuse_existing_mother_doc_container")
    else:
        reuse_actions.append("initialize_mother_doc_container")
    if runtime["construction_plan_exists"] and numbered_pack_dirs_value:
        reuse_actions.append("reuse_existing_execution_packs")
    else:
        reuse_actions.append("initialize_execution_packs_when_stage_requires")
    if runtime["graph_indexed_for_codebase"]:
        reuse_actions.append("reuse_existing_graph_context")
    elif runtime["substantial_codebase"]:
        reuse_actions.append("build_or_refresh_graph_before_pack_decomposition")
    else:
        reuse_actions.append("allow_graph_skip_for_near_empty_target")

    return {
        "status": "pass" if runtime["ready_for_service"] else "fail",
        "target_root": str(runtime["target_root"]),
        "development_docs_root": str(runtime["development_docs_root"]),
        "module_dir": runtime["module_dir"],
        "docs_root": str(runtime["docs_root"]),
        "docs_root_source": runtime["docs_root_source"],
        "docs_root_resolution_rule": (
            "treat <target_root> as the repo/workspace boundary inside AI_Projects, "
            "treat <docs_root> as the current code object's single governed Development_Docs root, "
            "resolve <development_docs_root> to the same filesystem root as <docs_root> rather than an extra parent container, "
            "treat <module_dir> only as an optional logical topic identifier and never as a required filesystem segment, "
            "and default codebase_root to the parent of docs_root"
        ),
        "module_dir_role": "optional_logical_topic_identifier_not_used_as_filesystem_segment",
        "project_structure_skill_path": str(runtime["project_structure_skill_path"]),
        "workspace_root": str(runtime["workspace_root"]),
        "root_agents_path": str(runtime["root_agents_path"]),
        "project_agents_path": str(project_agents_path) if project_agents_path is not None else None,
        "codebase_root": str(runtime["codebase_root"]),
        "graph_runtime_root": str(runtime["graph_runtime_root"]),
        "mother_doc_root": str(runtime["mother_doc_root"]),
        "mother_doc_index": str(runtime["mother_doc_index"]),
        "mother_doc_exists": runtime["mother_doc_exists"],
        "latest_archived_iteration": str(latest_archive) if latest_archive is not None else None,
        "construction_plan_root": str(runtime["construction_plan_root"]),
        "construction_plan_index": str(runtime["construction_plan_index"]),
        "construction_plan_exists": runtime["construction_plan_exists"],
        "pack_registry_exists": runtime["pack_registry_exists"],
        "numbered_pack_dirs": numbered_pack_dirs_value,
        "active_task_pack_exists": bool(numbered_pack_dirs_value),
        "acceptance_root": str(runtime["acceptance_root"]),
        "acceptance_exists": runtime["acceptance_exists"],
        "graph_registry_exists": runtime["graph_registry_exists"],
        "graph_indexed_for_codebase": runtime["graph_indexed_for_codebase"],
        "substantial_codebase": runtime["substantial_codebase"],
        "missing_prerequisites": runtime["missing_prerequisites"],
        "ready_for_service": runtime["ready_for_service"],
        "reuse_actions": reuse_actions,
        "first_actions": [
            "treat <target_root> as the repo/workspace boundary under AI_Projects, not as the code repo itself",
            "validate that the resolved docs_root already exists and sits inside target_root; otherwise refuse service",
            "inspect existing mother_doc, archived iterations, execution packs, AGENTS governance state, and graph state before deciding whether to init or reuse",
            "reuse existing task packs and graph context when they are already present; do not fork a second disconnected documentation line",
        ],
    }


target_runtime_contract_document = target_runtime_contract_payload
