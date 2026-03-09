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
        "code_abstractions/architecture": ("role", "boundary", "container_mapping", "visualization_mapping", "writeback_model"),
        "code_abstractions/stack": ("storage_model", "access_model", "graph_model", "indexing_model"),
        "code_abstractions/naming": ("directory_naming", "file_naming", "node_naming", "container_naming"),
        "code_abstractions/contracts": ("read_api", "writeback_api", "evidence_contract", "sync_contract"),
        "code_abstractions/operations": ("maintenance_entry", "query_commands", "change_policy", "recovery_entry"),
        "dev_canon": ("stack_selection_canon", "architecture_selection_canon", "automation_scope"),
        "development_logs": ("implementation_batches", "deployment_batches", "log_entry_contract", "comparison_basis"),
    },
    "UI": {
        "writing_guides": ("screen_doc_update_guide", "component_doc_update_guide"),
        "code_abstractions/architecture": ("screen_map", "component_layers", "state_boundary", "interaction_boundary"),
        "code_abstractions/stack": ("framework_stack", "styling_stack", "build_stack", "runtime_stack"),
        "code_abstractions/naming": ("route_naming", "component_naming", "state_naming", "event_naming"),
        "code_abstractions/contracts": ("backend_api_usage", "event_contract", "permission_contract", "error_feedback_contract"),
        "code_abstractions/operations": ("release_entry", "debug_commands", "environment_notes"),
        "dev_canon": ("stack_selection_canon", "architecture_selection_canon", "automation_scope"),
    },
    "Gateway": {
        "writing_guides": ("routing_doc_update_guide", "upstream_doc_update_guide"),
        "code_abstractions/architecture": ("routing_boundary", "upstream_map", "auth_forwarding", "traffic_boundary"),
        "code_abstractions/stack": ("gateway_stack", "deployment_mode", "runtime_profile"),
        "code_abstractions/naming": ("route_prefixes", "upstream_aliases", "header_naming"),
        "code_abstractions/contracts": ("inbound_contract", "upstream_contract", "auth_contract", "error_contract"),
        "code_abstractions/operations": ("rate_limit_policy", "debug_commands", "rollback_entry"),
        "dev_canon": ("stack_selection_canon", "architecture_selection_canon", "automation_scope"),
    },
    "Service": {
        "writing_guides": ("bounded_context_update_guide", "api_doc_update_guide"),
        "code_abstractions/architecture": ("bounded_context", "component_map", "dependency_boundary", "async_boundary"),
        "code_abstractions/stack": ("runtime_stack", "storage_stack", "transport_stack", "async_stack"),
        "code_abstractions/naming": ("entity_naming", "api_naming", "event_naming", "job_naming"),
        "code_abstractions/contracts": ("inbound_api", "outbound_api", "event_contract", "error_contract", "healthcheck_contract"),
        "code_abstractions/operations": ("deploy_entry", "healthcheck", "query_commands", "recovery_entry"),
        "dev_canon": ("stack_selection_canon", "architecture_selection_canon", "automation_scope"),
    },
    "Data_Infra": {
        "writing_guides": ("resource_doc_update_guide", "client_boundary_update_guide"),
        "code_abstractions/architecture": ("role", "ownership_boundary", "client_boundary", "data_boundary"),
        "code_abstractions/stack": ("engine_profile", "deployment_mode", "persistence_profile"),
        "code_abstractions/naming": ("resource_naming", "namespace_naming", "key_or_schema_naming"),
        "code_abstractions/contracts": ("access_policy", "client_contract", "backup_restore_contract", "retention_contract"),
        "code_abstractions/operations": ("query_commands", "maintenance_commands", "recovery_entry", "monitoring_entry"),
        "dev_canon": ("stack_selection_canon", "architecture_selection_canon", "automation_scope"),
    },
}


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
    return lines


def build_workspace_readme(name: str, document_dir: Path) -> list[str]:
    if name == "Mother_Doc":
        return [
            "Mother_Doc code container root.",
            f"Corresponding authored-doc root: `{document_dir.parent}`.",
            f"Corresponding container-doc directory: `{document_dir}`.",
            "Use `docs/` to carry the full authored Mother_Doc tree.",
            "Use `graph/` to carry OS_graph runtime assets and evidence-side graph artifacts.",
            "This container root does not carry `AGENTS.md`; recursive navigation files exist only under `docs/`.",
        ]
    return [
        "Stage-1 container directory.",
        f"Corresponding Mother_Doc path: `{document_dir}`.",
        "This workspace container does not carry `AGENTS.md`; recursive navigation files exist only under `Mother_Doc/`.",
    ]


def build_graph_readme() -> list[str]:
    return [
        "OS_graph asset root for the Mother_Doc container.",
        "This directory is not part of the authored-doc tree under `docs/`.",
        "Use it to carry graph runtime assets, graph writeback artifacts, and evidence-side structural outputs.",
    ]


def build_common_file_body(name: str, family: str, domain: str, topic: str) -> list[str]:
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
