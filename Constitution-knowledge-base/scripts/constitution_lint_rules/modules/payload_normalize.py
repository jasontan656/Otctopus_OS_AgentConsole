from __future__ import annotations

from pathlib import Path

from constitution_lint_rules.shared import RAW_PAYLOAD_PATTERNS, SOURCE_EXTS, iter_files, make_gate, read_text, rel

NORMALIZER_HINTS = ("normalize", "normalizer", "mapper", "transport", "adapter", "webhook", "ingress")
REQUIRED_MARKERS = ("trace_id", "session_id", "actor_id", "channel", "payload_version", "schema_name", "raw_ref")


def lint(root: Path) -> dict[str, object]:
    violations = []
    checked = 0
    for path in iter_files(root, SOURCE_EXTS):
        text = read_text(path)
        lower_path = str(path).lower()
        is_normalizer = any(token in lower_path for token in NORMALIZER_HINTS)
        is_lint_internal = "constitution_lint_rules" in path.parts or "tests" in path.parts
        if any(marker in text for marker in RAW_PAYLOAD_PATTERNS) and not is_normalizer and not is_lint_internal:
            violations.append({"path": rel(path, root), "reason": "raw_payload_marker_outside_normalizer"})
        candidate = is_normalizer or any(marker in text for marker in ("payload_version", "schema_name", "raw_ref"))
        if not candidate:
            continue
        checked += 1
        missing = [marker for marker in REQUIRED_MARKERS if marker not in text]
        if missing:
            violations.append({"path": rel(path, root), "reason": f"missing_normalize_markers:{','.join(missing)}"})
    return make_gate("payload_normalize_gate", violations, checked)
