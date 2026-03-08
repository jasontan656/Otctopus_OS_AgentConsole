from __future__ import annotations

from pathlib import Path

from constitution_lint_rules.shared import IO_PATTERNS, SOURCE_EXTS, iter_files, make_gate, read_text, rel


def lint(root: Path) -> dict[str, object]:
    violations = []
    checked = 0
    for path in iter_files(root, SOURCE_EXTS):
        checked += 1
        text = read_text(path)
        lower = path.name.lower()
        if any(token in lower for token in ("domain", "helper")) and any(pattern in text for pattern in IO_PATTERNS):
            violations.append({"path": rel(path, root), "reason": "domain_or_helper_contains_io"})
        if any(token in lower for token in ("controller", "handler", "route")) and any(token in text for token in ("_repo", "Repository(", "adapter", "sqlalchemy", "psycopg")):
            violations.append({"path": rel(path, root), "reason": "controller_bypasses_orchestrator_boundary"})
        if any(token in lower for token in ("page", "panel")) and any(token in text for token in ("fetch(", "axios(", "httpx.", "requests.")):
            violations.append({"path": rel(path, root), "reason": "view_layer_contains_direct_network_io"})
    return make_gate("modularity_gate", violations, checked)
