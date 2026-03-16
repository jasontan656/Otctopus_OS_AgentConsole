from __future__ import annotations

from audit_models import AuditIssue, RuntimeContractPayload


def _collect_strings(value: object) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        result: list[str] = []
        for child in value.values():
            result.extend(_collect_strings(child))
        return result
    if isinstance(value, list):
        result: list[str] = []
        for child in value:
            result.extend(_collect_strings(child))
        return result
    return []


def validate_artifact_policy(payload: RuntimeContractPayload | None) -> list[AuditIssue]:
    if payload is None:
        return []
    policy = payload.get("artifact_policy")
    if policy is None:
        return [AuditIssue("artifact_policy", "warning", "artifact_policy is not declared")]
    strings = _collect_strings(policy)
    issues: list[AuditIssue] = []
    for value in strings:
        if value.startswith("/"):
            issues.append(
                AuditIssue("artifact_policy", "error", f"absolute path is forbidden in artifact_policy: {value}")
            )
    return issues
