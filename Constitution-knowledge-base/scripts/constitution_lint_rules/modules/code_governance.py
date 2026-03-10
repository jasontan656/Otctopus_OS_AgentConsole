from __future__ import annotations

from pathlib import Path
import re

from constitution_lint_rules.shared import SOURCE_EXTS, iter_files, make_gate, read_text, rel

WAIVER_PATTERNS = (
    re.compile(r"\bwaiver approved\b", re.IGNORECASE),
    re.compile(r"\bapprove(?:d)? waiver\b", re.IGNORECASE),
    re.compile(r"\bgrant(?:ed)? waiver\b", re.IGNORECASE),
    re.compile(r"\btemporary bypass\b", re.IGNORECASE),
    re.compile(r"允许临时放行"),
    re.compile(r"可临时放行"),
    re.compile(r"先上线后补"),
    re.compile(r"批准豁免"),
    re.compile(r"申请豁免"),
)


def lint(root: Path) -> dict[str, object]:
    violations = []
    checked = 0
    for path in iter_files(root, SOURCE_EXTS):
        if "constitution_lint_rules" in path.parts:
            continue
        checked += 1
        text = read_text(path)
        if any(pattern.search(text) for pattern in WAIVER_PATTERNS):
            violations.append({"path": rel(path, root), "reason": "waiver_language_detected"})
    return make_gate("code_governance_gate", violations, checked)
