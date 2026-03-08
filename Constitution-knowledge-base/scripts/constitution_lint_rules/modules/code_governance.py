from __future__ import annotations

from pathlib import Path

from constitution_lint_rules.shared import SOURCE_EXTS, iter_files, make_gate, read_text, rel

WAIVER_PATTERNS = ("waiver", "豁免", "临时放行", "先上线后补", "temporary bypass")


def lint(root: Path) -> dict[str, object]:
    violations = []
    checked = 0
    for path in iter_files(root, SOURCE_EXTS):
        checked += 1
        text = read_text(path)
        if any(pattern in text for pattern in WAIVER_PATTERNS):
            violations.append({"path": rel(path, root), "reason": "waiver_language_detected"})
    return make_gate("code_governance_gate", violations, checked)
