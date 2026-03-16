from __future__ import annotations

from pathlib import Path

from artifact_audit import validate_artifact_policy
from audit_models import AuditIssue, AuditPayload, SurfaceProbe
from contract_validator import load_target_contract, validate_contract
from remediation_gate import build_remediation
from runtime_probe import detect_surface


def _surface_issues(surface: SurfaceProbe) -> list[AuditIssue]:
    issues: list[AuditIssue] = []
    if not surface["scripts_present"]:
        return issues
    if surface["cli_path"] is None:
        issues.append(AuditIssue("surface", "error", "scripts/ exists but Cli_Toolbox.py is missing"))
    if not surface["tooling_docs_present"]:
        issues.append(AuditIssue("surface", "error", "tooling docs are missing under references/tooling"))
    if not surface["tests_present"]:
        issues.append(AuditIssue("surface", "error", "tests/ are missing for a scripted skill"))
    return issues


def _status_for(issues: list[AuditIssue]) -> str:
    severities = {issue.severity for issue in issues}
    if "error" in severities:
        return "error"
    if "warning" in severities:
        return "warning"
    return "ok"


def audit_target(target_root: Path) -> AuditPayload:
    surface = detect_surface(target_root)
    contract_payload, contract_source = load_target_contract(target_root)
    issues: list[AuditIssue] = []
    issues.extend(validate_contract(contract_payload) if surface["scripts_present"] else [])
    issues.extend(_surface_issues(surface))
    issues.extend(validate_artifact_policy(contract_payload))
    tooling_surface = "none"
    if surface["scripts_present"]:
        commands: dict[str, str] = {}
        if contract_payload is not None:
            tool_entry = contract_payload.get("tool_entry")
            if isinstance(tool_entry, dict):
                candidate_commands = tool_entry.get("commands", {})
                if isinstance(candidate_commands, dict):
                    commands = candidate_commands
        if any(name not in {"contract", "directive"} for name in commands):
            tooling_surface = "automation_cli"
        else:
            tooling_surface = "contract_cli"
    return {
        "status": _status_for(issues),
        "target_skill_root": str(target_root),
        "tooling_surface": tooling_surface,
        "contract_source": contract_source,
        "surface": surface,
        "issues": [issue.as_dict() for issue in issues],
        "remediation_gate": build_remediation(issues),
    }
