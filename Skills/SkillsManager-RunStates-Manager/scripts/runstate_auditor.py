from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from governed_type_registry import RUNSTATE_TEMPLATES, governed_type_definition
from runstate_models import AuditIssue, AuditPayload
from target_inspector import inspect_target


RUNSTATE_CONTRACT_PATH = Path("references/runstates/RUNSTATE_METHOD_CONTRACT.json")
RUNSTATE_MARKERS = [
    "上一步产物",
    "consume previous output",
    "回填",
    "writeback",
    "驱动下一步",
    "next step",
]


def _status_for(issues: list[AuditIssue]) -> str:
    severities = {issue.severity for issue in issues}
    if "error" in severities:
        return "error"
    if "warning" in severities:
        return "warning"
    return "ok"


def _load_runstate_contract(target_root: Path) -> dict[str, Any] | None:
    path = target_root / RUNSTATE_CONTRACT_PATH
    if not path.exists():
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else None


def _combined_host_markdown(target_root: Path) -> str:
    texts: list[str] = []
    for markdown_path in sorted(target_root.rglob("*.md")):
        if "references/runstates/" in markdown_path.as_posix():
            continue
        texts.append(markdown_path.read_text(encoding="utf-8"))
    return "\n".join(texts)


def _validate_contract_schema(contract_payload: dict[str, Any] | None, governed_type: str) -> list[AuditIssue]:
    issues: list[AuditIssue] = []
    definition = governed_type_definition(governed_type)
    if contract_payload is None:
        issues.append(AuditIssue("contract", "error", "RUNSTATE_METHOD_CONTRACT.json is missing."))
        return issues
    if contract_payload.get("governed_type") != governed_type:
        issues.append(AuditIssue("contract", "error", "governed_type in RUNSTATE_METHOD_CONTRACT.json does not match the target inference."))
    checklist_schema = contract_payload.get("checklist_schema")
    if not isinstance(checklist_schema, dict):
        issues.append(AuditIssue("contract", "error", "checklist_schema is missing or invalid."))
        return issues
    for checklist in definition["required_checklists"]:
        entry = checklist_schema.get(checklist)
        if not isinstance(entry, dict) or entry.get("required") is not True:
            issues.append(AuditIssue("contract", "error", f"{checklist} is not marked as required in checklist_schema."))
    behavior_contract = contract_payload.get("behavior_contract")
    if not isinstance(behavior_contract, dict):
        issues.append(AuditIssue("contract", "error", "behavior_contract is missing or invalid."))
        return issues
    for field in (
        "must_consume_previous_output",
        "must_writeback_after_each_atomic_step",
        "must_drive_next_step_from_writeback",
        "prohibit_step_skip_or_parallel_completion",
    ):
        if behavior_contract.get(field) is not True:
            issues.append(AuditIssue("contract", "error", f"{field} must be true for applicable governed targets."))
    return issues


def _validate_templates(target_root: Path, governed_type: str) -> list[AuditIssue]:
    issues: list[AuditIssue] = []
    definition = governed_type_definition(governed_type)
    for checklist in definition["required_checklists"]:
        template_path = target_root / RUNSTATE_TEMPLATES[checklist]
        if not template_path.exists():
            issues.append(AuditIssue("templates", "error", f"missing template: {template_path.relative_to(target_root)}"))
    return issues


def _validate_host_markers(target_root: Path, governed_type: str) -> list[AuditIssue]:
    issues: list[AuditIssue] = []
    definition = governed_type_definition(governed_type)
    host_text = _combined_host_markdown(target_root)
    for checklist in definition["required_checklists"]:
        if checklist not in host_text:
            issues.append(AuditIssue("host_markdown", "warning", f"{checklist} is not referenced by host skill markdown."))
    if not any(marker in host_text for marker in RUNSTATE_MARKERS):
        issues.append(AuditIssue("host_markdown", "warning", "host skill markdown does not show consume/writeback/next-step markers."))
    return issues


def _build_remediation(issues: list[AuditIssue], applicability: str) -> list[str]:
    if applicability == "not_applicable":
        return ["No runstate remediation is required for a not_applicable target."]
    messages: list[str] = []
    if any(issue.scope == "contract" for issue in issues):
        messages.append("Run scaffold or repair references/runstates/RUNSTATE_METHOD_CONTRACT.json first.")
    if any(issue.scope == "templates" for issue in issues):
        messages.append("Regenerate the governed checklist templates for the target skill.")
    if any(issue.scope == "host_markdown" for issue in issues):
        messages.append("Update host workflow/stage docs so the runstate checklists and consume/writeback rules are explicitly consumed.")
    if not messages:
        messages.append("Runstate governance is aligned.")
    return messages


def audit_target(target_root: Path) -> AuditPayload:
    target_root = target_root.resolve()
    inspect_payload = inspect_target(target_root)
    if inspect_payload["status"] == "error":
        return {
            "status": "error",
            "target_skill_root": str(target_root),
            "skill_name": target_root.name,
            "governed_type": "not_applicable",
            "applicability": "not_applicable",
            "issues": [AuditIssue("target", "error", "Invalid target skill root.").as_dict()],
            "remediation_gate": ["Fix the target skill root before auditing runstates."],
            "evidence": {},
        }
    governed_type = str(inspect_payload["governed_type"])
    applicability = str(inspect_payload["applicability"])
    if applicability == "not_applicable":
        return {
            "status": "ok",
            "target_skill_root": str(target_root),
            "skill_name": target_root.name,
            "governed_type": governed_type,
            "applicability": applicability,
            "issues": [],
            "remediation_gate": ["No runstate scaffolding is required for this target."],
            "evidence": {
                "detection_source": inspect_payload["detection_source"],
                "reasons": inspect_payload["reasons"],
            },
        }

    issues: list[AuditIssue] = []
    contract_payload = _load_runstate_contract(target_root)
    issues.extend(_validate_contract_schema(contract_payload, governed_type))
    issues.extend(_validate_templates(target_root, governed_type))
    issues.extend(_validate_host_markers(target_root, governed_type))
    return {
        "status": _status_for(issues),
        "target_skill_root": str(target_root),
        "skill_name": target_root.name,
        "governed_type": governed_type,
        "applicability": applicability,
        "issues": [issue.as_dict() for issue in issues],
        "remediation_gate": _build_remediation(issues, applicability),
        "evidence": {
            "detection_source": inspect_payload["detection_source"],
            "required_checklists": inspect_payload["required_checklists"],
            "success_criteria": inspect_payload["success_criteria"],
        },
    }
