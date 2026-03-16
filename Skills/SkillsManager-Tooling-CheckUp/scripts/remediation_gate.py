from __future__ import annotations

from audit_models import AuditIssue


def build_remediation(issues: list[AuditIssue]) -> list[str]:
    remediation: list[str] = []
    scopes = {issue.scope for issue in issues}
    if "contract" in scopes:
        remediation.append("补齐 runtime contract，并优先以 JSON contract 作为 machine truth source。")
    if "surface" in scopes:
        remediation.append("补齐 CLI/tooling surface 的 tests 与 references/tooling 文档。")
    if "artifact_policy" in scopes:
        remediation.append("移除绝对路径，改为 resolver-based artifact policy。")
    if remediation:
        remediation.append("若拓扑本身有问题，先转入 SkillsManager-Doc-Structure 处理文档结构。")
    return remediation
