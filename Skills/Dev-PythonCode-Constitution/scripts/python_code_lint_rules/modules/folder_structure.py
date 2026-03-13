from __future__ import annotations

from pathlib import Path

from python_code_lint_rules.shared import iter_tree, make_gate, rel

FORBIDDEN_DIR_TOKENS = {"misc", "other", "new_folder", "newfolder", "folder2", "tmp2"}
CODE_EXTS = {".py"}


def lint(root: Path) -> dict[str, object]:
    violations = []
    checked = 0
    for path in iter_tree(root):
        checked += 1
        if path.is_dir() and (" " in path.name or path.name.lower() in FORBIDDEN_DIR_TOKENS):
            violations.append({"path": rel(path, root), "reason": "unstable_directory_name"})
        if path.is_file() and path.suffix.lower() in CODE_EXTS and "tmp" in path.parts:
            violations.append({"path": rel(path, root), "reason": "source_file_forbidden_under_tmp"})
        if path.is_file() and path.suffix.lower() in CODE_EXTS and "rules" in path.parts:
            violations.append({"path": rel(path, root), "reason": "source_file_forbidden_under_rules"})
    return make_gate("folder_structure_gate", violations, checked)
