from __future__ import annotations

from pathlib import Path
import re

from constitution_lint_rules.shared import SOURCE_EXTS, iter_files, make_gate, rel

RULE_SUFFIXES = ("rule", "constitution", "lint")
RULE_EXTS = {".md", ".yaml", ".yml", ".json"}


def _name_tokens(name: str) -> set[str]:
    stem = Path(name).stem.lower()
    return {token for token in re.split(r"[_\W]+", stem) if token}


def lint(root: Path) -> dict[str, object]:
    violations = []
    checked = 0
    for path in iter_files(root, SOURCE_EXTS):
        checked += 1
        name = path.name
        lower = name.lower()
        tokens = _name_tokens(name)
        if "controller" in lower and not lower.endswith("_controller.py"):
            violations.append({"path": rel(path, root), "reason": "controller_name_must_end_with__controller.py"})
        if "orchestrator" in lower and not lower.endswith("_orchestrator.py"):
            violations.append({"path": rel(path, root), "reason": "orchestrator_name_must_end_with__orchestrator.py"})
        if lower.endswith(".py") and "domain" in tokens and not lower.endswith("_domain.py"):
            violations.append({"path": rel(path, root), "reason": "domain_name_must_end_with__domain.py"})
        if ("repo" in tokens or "repository" in tokens) and not lower.endswith("_repo.py"):
            violations.append({"path": rel(path, root), "reason": "repo_name_must_end_with__repo.py"})
        if "helper" in lower and not (lower.endswith("_helper.py") or lower.endswith(".helper.ts") or lower.endswith(".helper.js")):
            violations.append({"path": rel(path, root), "reason": "helper_name_must_use_helper_suffix"})
        if name.endswith(".vue") and "Page" in name and not name.endswith("Page.vue"):
            violations.append({"path": rel(path, root), "reason": "page_component_must_end_with_Page.vue"})
        if name.endswith(".vue") and "Panel" in name and "Panel" not in name:
            violations.append({"path": rel(path, root), "reason": "panel_component_must_include_Panel"})
        if path.suffix.lower() in RULE_EXTS and any(token in lower for token in RULE_SUFFIXES) and "rules" not in path.parts:
            violations.append({"path": rel(path, root), "reason": "rule_like_file_must_live_under_rules"})
    return make_gate("file_structure_gate", violations, checked)
