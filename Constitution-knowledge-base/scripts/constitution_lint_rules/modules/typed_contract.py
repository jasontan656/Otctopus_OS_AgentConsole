from __future__ import annotations

from pathlib import Path

from constitution_lint_rules.shared import SOURCE_EXTS, iter_files, make_gate, read_text, rel

CONTRACT_HINTS = ("contract", "schema", "dto")
REQUIRED_MARKERS = ("contract_name", "contract_version", "validation_mode")
FIELD_MARKERS = (("required_fields", "required_keys"), ("optional_fields", "optional_keys"))


def lint(root: Path) -> dict[str, object]:
    violations = []
    checked = 0
    for path in iter_files(root, SOURCE_EXTS):
        text = read_text(path)
        lower = path.name.lower()
        candidate = any(token in lower for token in CONTRACT_HINTS) or any(marker in text for marker in REQUIRED_MARKERS)
        if not candidate:
            continue
        checked += 1
        missing = [marker for marker in REQUIRED_MARKERS if marker not in text]
        if not any(any(option in text for option in group) for group in FIELD_MARKERS):
            missing.append("required_fields/optional_fields")
        if missing:
            violations.append({"path": rel(path, root), "reason": f"missing_contract_markers:{','.join(missing)}"})
    return make_gate("typed_contract_gate", violations, checked)
