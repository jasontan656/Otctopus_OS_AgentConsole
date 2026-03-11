from __future__ import annotations

import re
from pathlib import Path


VALID_NAME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")
DISCOURAGED_PREFIXES = ("Shared_", "Business_", "Runtime_")
PREFERRED_SUFFIXES = (
    "_UI",
    "_Gateway",
    "_Service",
    "_DB",
    "_Cache",
    "_Broker",
    "_Storage",
)

FAMILY_FILE_MAP: dict[str, dict[str, tuple[str, ...]]] = {
    "Mother_Doc": {
        "writing_guides": ("docs_root_update_guide", "docs_navigation_update_guide", "graph_asset_update_guide"),
        "code_abstractions/architecture": ("role", "boundary", "container_mapping", "visualization_mapping", "writeback_model", "authored_doc_layer_model", "question_backfill_model"),
        "code_abstractions/stack": ("storage_model", "access_model", "graph_model", "indexing_model"),
        "code_abstractions/naming": ("directory_naming", "file_naming", "node_naming", "container_naming"),
        "code_abstractions/contracts": ("read_api", "writeback_api", "evidence_contract", "sync_contract", "doc_code_binding_contract", "document_lifecycle_status_contract"),
        "code_abstractions/operations": ("deployment_guide", "operation_commands", "recovery_guide", "change_policy"),
        "dev_canon": ("stack_selection_canon", "architecture_selection_canon", "automation_scope"),
        "development_logs": ("implementation_batches", "deployment_batches", "log_entry_contract", "comparison_basis"),
    },
    "UI": {
        "writing_guides": ("screen_doc_update_guide", "component_doc_update_guide"),
        "code_abstractions/architecture": ("screen_map", "component_layers", "state_boundary", "interaction_boundary"),
        "code_abstractions/stack": ("framework_stack", "styling_stack", "build_stack", "runtime_stack"),
        "code_abstractions/naming": ("route_naming", "component_naming", "state_naming", "event_naming"),
        "code_abstractions/contracts": ("backend_api_usage", "event_contract", "permission_contract", "error_feedback_contract"),
        "code_abstractions/operations": ("deployment_guide", "operation_commands", "recovery_guide", "environment_notes"),
        "dev_canon": ("stack_selection_canon", "architecture_selection_canon", "automation_scope"),
    },
    "Gateway": {
        "writing_guides": ("routing_doc_update_guide", "upstream_doc_update_guide"),
        "code_abstractions/architecture": ("routing_boundary", "upstream_map", "auth_forwarding", "traffic_boundary"),
        "code_abstractions/stack": ("gateway_stack", "runtime_profile"),
        "code_abstractions/naming": ("route_prefixes", "upstream_aliases", "header_naming"),
        "code_abstractions/contracts": ("inbound_contract", "upstream_contract", "auth_contract", "error_contract"),
        "code_abstractions/operations": ("deployment_guide", "operation_commands", "recovery_guide", "rate_limit_policy"),
        "dev_canon": ("stack_selection_canon", "architecture_selection_canon", "automation_scope"),
    },
    "Service": {
        "writing_guides": ("bounded_context_update_guide", "api_doc_update_guide"),
        "code_abstractions/architecture": ("bounded_context", "component_map", "dependency_boundary", "async_boundary"),
        "code_abstractions/stack": ("runtime_stack", "storage_stack", "transport_stack", "async_stack"),
        "code_abstractions/naming": ("entity_naming", "api_naming", "event_naming", "job_naming"),
        "code_abstractions/contracts": ("inbound_api", "outbound_api", "event_contract", "error_contract", "healthcheck_contract"),
        "code_abstractions/operations": ("deployment_guide", "operation_commands", "recovery_guide", "healthcheck"),
        "dev_canon": ("stack_selection_canon", "architecture_selection_canon", "automation_scope"),
    },
    "Data_Infra": {
        "writing_guides": ("resource_doc_update_guide", "client_boundary_update_guide"),
        "code_abstractions/architecture": ("role", "ownership_boundary", "client_boundary", "data_boundary"),
        "code_abstractions/stack": ("engine_profile", "persistence_profile"),
        "code_abstractions/naming": ("resource_naming", "namespace_naming", "key_or_schema_naming"),
        "code_abstractions/contracts": ("access_policy", "client_contract", "backup_restore_contract", "retention_contract"),
        "code_abstractions/operations": ("deployment_guide", "operation_commands", "recovery_guide", "monitoring_entry"),
        "dev_canon": ("stack_selection_canon", "architecture_selection_canon", "automation_scope"),
    },
}

CONTENT_LAYER_FILE_MAP: dict[str, tuple[str, ...]] = {
    "overview": ("container_overview", "capability_map", "surface_index"),
    "features": ("feature_catalog", "active_requirements", "open_questions"),
    "shared": ("api_surfaces", "event_and_message_flows", "shared_contracts", "cross_container_dependencies", "open_questions"),
}

MOTHER_DOC_PROJECT_BASELINE_FILES: tuple[str, ...] = (
    "project_positioning",
    "operating_model",
    "impact_selection_baseline",
    "current_project_development_baseline",
    "dynamic_document_growth",
    "front_end_dynamic_consumption",
)


def validate_container_name(name: str) -> list[str]:
    warnings: list[str] = []
    if not VALID_NAME_RE.fullmatch(name):
        raise ValueError(f"invalid container name: {name}")
    if name == "Mother_Doc":
        return warnings
    if any(name.startswith(prefix) for prefix in DISCOURAGED_PREFIXES):
        warnings.append(f"discouraged bucket-style name: {name}")
    if not any(name.endswith(suffix) for suffix in PREFERRED_SUFFIXES):
        warnings.append(f"name does not use a preferred stage-1 suffix: {name}")
    return warnings


def detect_family(name: str) -> str:
    if name == "Mother_Doc":
        return "Mother_Doc"
    if name.endswith("_UI"):
        return "UI"
    if name.endswith("_Gateway"):
        return "Gateway"
    if name.endswith("_Service"):
        return "Service"
    if name.endswith(("_DB", "_Cache", "_Broker", "_Storage")):
        return "Data_Infra"
    raise ValueError(f"cannot infer family for container: {name}")


def ensure_markdown(path: Path, *, title: str, body_lines: list[str], dry_run: bool) -> bool:
    if path.exists():
        return False
    if dry_run:
        return True
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join([f"# {title}", "", *body_lines, ""]), encoding="utf-8")
    return True


def build_document_readme(name: str, workspace_dir: Path, family: str) -> list[str]:
    lines = [
        f"Mother_Doc entry for the `{name}` container.",
        f"Container family: `{family}`.",
        f"Corresponding workspace path: `{workspace_dir}`.",
        "This directory carries authored development and operations docs for the same-named container.",
        "`overview/` carries human-readable top-level summaries and capability overviews for the current container.",
        "`features/` carries concrete feature documents, active requirements, and unresolved question backfill for the current container.",
        "`shared/` carries dynamic shared layers such as APIs, events, contracts, and cross-container dependency notes for the current container.",
        "Stable abstracted knowledge lives under `common/`.",
        "`common/writing_guides/` carries authored-doc update guidance for the current domain family.",
        "`common/code_abstractions/` carries code abstraction, code-to-doc mapping, and reusable code-facing structure contracts for the current domain family.",
        "`common/dev_canon/` carries the development canon subset that has been recovered into Octopus OS for automation.",
        f"`{name}.md` in this directory describes the container itself as the authored module entity.",
        "Use the peer `AGENTS.md` in this directory as the recursive navigation index.",
    ]
    if family == "Mother_Doc":
        lines.append("`common/development_logs/` carries append-oriented implementation and deployment checkpoints for document-led delivery.")
        lines.append("This authored tree lives under the `docs/` subdirectory because the Mother_Doc container root is reserved for code/runtime assets.")
        lines.append("`project_baseline/` carries the always-load project baseline before any container-specific scope selection.")
    return lines


def build_workspace_readme(name: str, document_dir: Path) -> list[str]:
    if name == "Mother_Doc":
        return [
            "Mother_Doc code container root.",
            f"Corresponding authored-doc root: `{document_dir.parent}`.",
            f"Corresponding container-doc directory: `{document_dir}`.",
            "Use `docs/` to carry the full authored Mother_Doc tree.",
            "Use `graph/` to carry OS_graph runtime assets and evidence-side graph artifacts.",
            "This container root no longer carries its own root-level `AGENTS.md`; the only external AGENTS target is `Octopus_OS/AGENTS.md`.",
        ]
    return [
        "Stage-1 container directory.",
        f"Corresponding Mother_Doc path: `{document_dir}`.",
        "This container root does not carry its own `AGENTS.md`; root runtime governance is centralized at `Octopus_OS/AGENTS.md`.",
    ]


def build_graph_readme() -> list[str]:
    return [
        "OS_graph asset root for the Mother_Doc container.",
        "This directory is not part of the authored-doc tree under `docs/`.",
        "Use it to carry graph runtime assets, graph writeback artifacts, and evidence-side structural outputs.",
    ]


def build_common_file_body(name: str, family: str, domain: str, topic: str) -> list[str]:
    if domain == "code_abstractions/contracts" and topic == "doc_code_binding_contract":
        return [
            "## Contract Markers",
            "",
            "contract_name: doc_code_binding_contract",
            "contract_version: v0",
            "validation_mode: placeholder",
            "required_fields:",
            "- semantic_unit_id",
            "- document_nodes",
            "- implementation_nodes",
            "optional_fields:",
            "- contract_nodes",
            "- evidence_nodes",
            "",
            f"This file defines `{topic}` for the `{name}` container's code abstraction layer.",
            f"Container family: `{family}`.",
            "Use it to define how semantic documentation units bind to implementation slices and later evidence/graph nodes.",
            "This file is part of the authored Mother_Doc template and is not the implementation-stage execution rule itself.",
        ]
    if domain == "code_abstractions/contracts" and topic == "document_lifecycle_status_contract":
        return [
            "## Contract Markers",
            "",
            "contract_name: document_lifecycle_status_contract",
            "contract_version: v0",
            "validation_mode: placeholder",
            "required_fields:",
            "- lifecycle_state",
            "- doc_requires_development",
            "- sync_status",
            "optional_fields:",
            "- transition_rule",
            "- stage_owner",
            "",
            f"This file defines `{topic}` for the `{name}` container's code abstraction layer.",
            f"Container family: `{family}`.",
            "Use it to define the three-state lifecycle model: modified, developed, and null.",
            "mother_doc derives modified/null from local git-backed diff, implementation consumes modified, and evidence closes the loop by writing developed.",
        ]
    if domain == "code_abstractions/architecture" and topic == "authored_doc_layer_model":
        return [
            "## Permission Markers",
            "",
            "actor_id: octopus_mother_doc_stage",
            "authz_result: allow",
            "deny_code: none",
            "policy_version: v0",
            "scope: authored_doc_layer_model",
            "",
            f"This file defines `{topic}` for the `{name}` container's code abstraction layer.",
            f"Container family: `{family}`.",
            "Use it to define the authored-doc layer stack: overview, features, shared, and common.",
            "This file exists so the Mother_Doc stage can update the correct document layer without mixing unrelated scopes.",
        ]
    if domain == "writing_guides":
        return [
            f"This file defines `{topic}` for the `{name}` container's authored-doc update workflow.",
            f"Container family: `{family}`.",
            "Use it to constrain how this domain updates its own documentation shape and replaceable sections.",
            "Keep the rule focused on authored content for this domain family, not on other families.",
        ]
    if domain.startswith("code_abstractions"):
        abstract_domain = domain.split("/", 1)[1] if "/" in domain else "code_abstractions"
        return [
            f"This file defines `{topic}` for the `{name}` container's code abstraction layer.",
            f"Container family: `{family}`.",
            f"Code abstraction domain: `{abstract_domain}`.",
            "Use it to describe reusable code-facing structure, mapping, and constraints for the current container.",
            "This file is part of the authored Mother_Doc template and is not the implementation-stage execution rule itself.",
        ]
    if domain == "dev_canon":
        return [
            f"This file stores the recovered development canon topic `{topic}` for the `{name}` container.",
            f"Container family: `{family}`.",
            "Only development-related canon that should be automated belongs here.",
            "Anything not yet canonized must remain `replace_me` and should not be auto-filled by the skill.",
        ]
    if domain == "development_logs":
        if topic == "implementation_batches":
            return [
                "This file records implementation batches after Mother_Doc updates.",
                "Only evidence, or linked implementation-to-evidence writeback, may append entries here.",
                "Compare current code first, then compare the updated Mother_Doc state, and let implementation produce aligned scope for evidence-side logging.",
                "When there is no code yet, record the current authored-document state as the initial implementation batch against the empty code baseline.",
                "Log entries keep only summary-level traceability; the summary must match the Git commit message for the same write turn.",
            ]
        if topic == "deployment_batches":
            return [
                "This file records deployment checkpoints once the project reaches a deployable state.",
                "Only evidence may append entries here.",
                "Each entry acts as an operational release checkpoint without introducing internal document version branches.",
                "Bind each deployment checkpoint back to the corresponding implementation batch and runtime witness.",
                "Log entries keep only summary-level traceability; the summary must match the Git commit message for the same write turn.",
            ]
        if topic == "log_entry_contract":
            return [
                "## Contract Markers",
                "",
                "contract_name: Mother_Doc_development_log_entry_contract",
                "contract_version: v0",
                "validation_mode: placeholder",
                "required_fields:",
                "- entry_kind",
                "- comparison_order",
                "- summary",
                "- doc_paths",
                "- code_paths",
                "optional_fields:",
                "- witness_refs",
                "",
                "This file defines the fixed fields required for implementation and deployment log entries.",
                "Only evidence may write entries under this contract.",
                "Each log entry must remain append-oriented and mechanically readable.",
                "The `summary` field is the local log summary and must exactly match the Git commit message for the same write turn.",
                "Detailed file/code changes stay in Git and GitHub history; the log only keeps the summary-level breadcrumb.",
                "Keep the contract aligned with the actual logging workflow where implementation produces aligned scope and evidence performs the trace writeback.",
            ]
        if topic == "comparison_basis":
            return [
                "This file defines the comparison order for drift resolution.",
                "Read current code first, then read the updated Mother_Doc state, and derive the implementation gap from that delta.",
                "Implementation uses this comparison basis to produce aligned change scope; evidence then records the trace.",
                "Use the same comparison basis for first-time implementation when code is still empty.",
            ]
    return [
        f"This file defines the `{topic}` abstraction for the `{name}` container.",
        f"Container family: `{family}`.",
        f"Common domain: `{domain}`.",
        "Keep the content stable, reusable, and independent from feature-specific implementation detail.",
    ]


def build_content_file_body(name: str, family: str, layer: str, topic: str) -> list[str]:
    if layer == "shared" and topic == "shared_contracts":
        return [
            "## Contract Markers",
            "",
            "contract_name: shared_contracts",
            "contract_version: v0",
            "validation_mode: placeholder",
            "required_fields:",
            "- contract_scope",
            "- participating_containers",
            "- interface_or_event_refs",
            "optional_fields:",
            "- dependency_notes",
            "- unresolved_items",
            "",
            f"This file defines `{topic}` for the `{name}` container's shared integration layer.",
            f"Container family: `{family}`.",
            "Use it for APIs, events, shared contracts, and cross-container dependency notes that are dynamically consumed during development.",
            "Keep the content aligned with both human-readable authored docs and future OS_graph bindings.",
        ]
    if layer == "overview":
        return [
            f"This file defines `{topic}` for the `{name}` container's top-level human overview layer.",
            f"Container family: `{family}`.",
            "Use it for human-readable summaries, capability maps, and scope-level overviews before entering deeper feature or shared documents.",
            "Keep it broad, observable, and suitable for admin-panel browsing.",
        ]
    if layer == "features":
        return [
            f"This file defines `{topic}` for the `{name}` container's feature layer.",
            f"Container family: `{family}`.",
            "Use it for concrete feature scopes, current requirements, and unresolved feature questions.",
            "A single feature document may cover one file, many files, or a semantic slice that spans multiple implementation files.",
        ]
    if layer == "shared":
        return [
            f"This file defines `{topic}` for the `{name}` container's shared integration layer.",
            f"Container family: `{family}`.",
            "Use it for APIs, events, shared contracts, and cross-container dependency notes that are dynamically consumed during development.",
            "Keep the content aligned with both human-readable authored docs and future OS_graph bindings.",
        ]
    return [
        f"This file defines `{topic}` for the `{name}` container.",
        f"Container family: `{family}`.",
        f"Layer: `{layer}`.",
    ]


def build_project_baseline_file_body(topic: str) -> list[str]:
    if topic == "project_positioning":
        return [
            "This file defines the top-level project positioning for Octopus_OS.",
            "Use it to explain what the project is, why it is operated through Octopus OS, and how the container set belongs to one evolving project.",
            "Keep it human-readable first while preserving stable anchors for later OS_graph binding.",
        ]
    if topic == "operating_model":
        return [
            "This file defines the operating model where humans issue intent and the Octopus AI writes docs, implements code, tests, deploys, and later operates the system.",
            "Keep the responsibilities explicit and aligned with the current project baseline.",
        ]
    if topic == "impact_selection_baseline":
        return [
            "This file defines the project-wide impact selection rule.",
            "Always start from default_all_relevant and only then prune by highest-probability-unrelated scopes.",
            "Do not collapse this rule into a guessed short list of related containers.",
        ]
    if topic == "current_project_development_baseline":
        return [
            "This file records the current project objective, current delivery focus, and current readable inclusion/exclusion judgment for the active requirement set.",
            "Refresh it whenever a new project-level requirement changes the likely impact surface.",
        ]
    if topic == "dynamic_document_growth":
        return [
            "This file defines how the authored-doc tree is allowed to grow new branches over time.",
            "Growth must stay rule-driven, navigable, and compatible with future OS_graph bindings.",
        ]
    if topic == "front_end_dynamic_consumption":
        return [
            "This file defines how Admin_UI and other front-end consumers discover and compose dynamic authored docs.",
            "Offline storage stays fragmented and machine-first; online presentation may aggregate and visualize the same content for human reading.",
        ]
    return [
        f"This file defines the `{topic}` project-baseline slice for the Mother_Doc container.",
    ]


def scaffold_common_tree(*, container_name: str, document_dir: Path, family: str, dry_run: bool) -> list[str]:
    created_files: list[str] = []
    for domain, topics in FAMILY_FILE_MAP[family].items():
        for topic in topics:
            target = document_dir / "common" / domain / f"{topic}.md"
            created = ensure_markdown(
                target,
                title=topic,
                body_lines=build_common_file_body(container_name, family, domain, topic),
                dry_run=dry_run,
            )
            if created:
                created_files.append(str(target))
    return created_files


def scaffold_content_tree(*, container_name: str, document_dir: Path, family: str, dry_run: bool) -> list[str]:
    created_files: list[str] = []
    for layer, topics in CONTENT_LAYER_FILE_MAP.items():
        for topic in topics:
            target = document_dir / layer / f"{topic}.md"
            created = ensure_markdown(
                target,
                title=topic,
                body_lines=build_content_file_body(container_name, family, layer, topic),
                dry_run=dry_run,
            )
            if created:
                created_files.append(str(target))
    if family == "Mother_Doc":
        for topic in MOTHER_DOC_PROJECT_BASELINE_FILES:
            target = document_dir / "project_baseline" / f"{topic}.md"
            created = ensure_markdown(
                target,
                title=topic,
                body_lines=build_project_baseline_file_body(topic),
                dry_run=dry_run,
            )
            if created:
                created_files.append(str(target))
    return created_files
