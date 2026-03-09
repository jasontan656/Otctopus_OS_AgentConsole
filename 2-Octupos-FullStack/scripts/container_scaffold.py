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
        "architecture": ("role", "boundary", "container_mapping", "visualization_mapping", "writeback_model"),
        "stack": ("storage_model", "access_model", "graph_model", "indexing_model"),
        "naming": ("directory_naming", "file_naming", "node_naming", "container_naming"),
        "contracts": ("read_api", "writeback_api", "evidence_contract", "sync_contract"),
        "operations": ("maintenance_entry", "query_commands", "change_policy", "recovery_entry"),
    },
    "UI": {
        "architecture": ("screen_map", "component_layers", "state_boundary", "interaction_boundary"),
        "stack": ("framework_stack", "styling_stack", "build_stack", "runtime_stack"),
        "naming": ("route_naming", "component_naming", "state_naming", "event_naming"),
        "contracts": ("backend_api_usage", "event_contract", "permission_contract", "error_feedback_contract"),
        "operations": ("release_entry", "debug_commands", "environment_notes"),
    },
    "Gateway": {
        "architecture": ("routing_boundary", "upstream_map", "auth_forwarding", "traffic_boundary"),
        "stack": ("gateway_stack", "deployment_mode", "runtime_profile"),
        "naming": ("route_prefixes", "upstream_aliases", "header_naming"),
        "contracts": ("inbound_contract", "upstream_contract", "auth_contract", "error_contract"),
        "operations": ("rate_limit_policy", "debug_commands", "rollback_entry"),
    },
    "Service": {
        "architecture": ("bounded_context", "component_map", "dependency_boundary", "async_boundary"),
        "stack": ("runtime_stack", "storage_stack", "transport_stack", "async_stack"),
        "naming": ("entity_naming", "api_naming", "event_naming", "job_naming"),
        "contracts": ("inbound_api", "outbound_api", "event_contract", "error_contract", "healthcheck_contract"),
        "operations": ("deploy_entry", "healthcheck", "query_commands", "recovery_entry"),
    },
    "Data_Infra": {
        "architecture": ("role", "ownership_boundary", "client_boundary", "data_boundary"),
        "stack": ("engine_profile", "deployment_mode", "persistence_profile"),
        "naming": ("resource_naming", "namespace_naming", "key_or_schema_naming"),
        "contracts": ("access_policy", "client_contract", "backup_restore_contract", "retention_contract"),
        "operations": ("query_commands", "maintenance_commands", "recovery_entry", "monitoring_entry"),
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
    return [
        f"Mother_Doc entry for the `{name}` container.",
        f"Container family: `{family}`.",
        f"Corresponding workspace path: `{workspace_dir}`.",
        "This directory carries authored development and operations docs for the same-named container.",
        "Stable abstracted knowledge lives under `common/`.",
    ]


def build_workspace_readme(name: str, document_dir: Path) -> list[str]:
    return [
        "Stage-1 container directory.",
        f"Corresponding Mother_Doc path: `{document_dir}`.",
    ]


def build_common_file_body(name: str, family: str, domain: str, topic: str) -> list[str]:
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
    if container_name == "Mother_Doc":
        index_path = document_dir / "00_INDEX.md"
        created = ensure_markdown(
            index_path,
            title="Mother_Doc Index",
            body_lines=[
                "Index entry for the `Mother_Doc` container itself.",
                "Use this file as the self-description navigation root for the Mother_Doc container.",
                "The repository-level `Mother_Doc/README.md` remains the mirror-root explanation.",
            ],
            dry_run=dry_run,
        )
        if created:
            created_files.append(str(index_path))
    return created_files
