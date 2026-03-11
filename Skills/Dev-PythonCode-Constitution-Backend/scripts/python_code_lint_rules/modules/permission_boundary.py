from __future__ import annotations

from pathlib import Path

from python_code_lint_rules.shared import SOURCE_EXTS, iter_files, make_gate, read_text, rel

AUTH_HINTS = ("auth", "authz", "permission", "policy", "guard")
REQUIRED_MARKERS = ("actor_id", "role", "scope", "action", "policy_version", "authz_result")
HIGH_RISK_MARKERS = ("high_risk", "write_high_risk", "critical_action")


def lint(root: Path) -> dict[str, object]:
    violations = []
    checked = 0
    for path in iter_files(root, SOURCE_EXTS):
        text = read_text(path)
        lower = str(path).lower()
        candidate = any(token in lower for token in AUTH_HINTS) or any(marker in text for marker in ("policy_version", "authz_result", "approval_ref", "deny_code"))
        if not candidate:
            continue
        checked += 1
        missing = [marker for marker in REQUIRED_MARKERS if marker not in text]
        if "deny_code" not in text:
            missing.append("deny_code")
        if any(marker in text for marker in HIGH_RISK_MARKERS) and "approval_ref" not in text:
            missing.append("approval_ref")
        if missing:
            violations.append({"path": rel(path, root), "reason": f"missing_permission_markers:{','.join(sorted(set(missing)))}"})
    return make_gate("permission_boundary_gate", violations, checked)
