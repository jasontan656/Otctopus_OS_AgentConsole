from __future__ import annotations

from pathlib import Path

from constitution_lint_rules.shared import SOURCE_EXTS, iter_files, make_gate, rel, should_skip

FORBIDDEN_DIR_TOKENS = {"misc", "other", "new_folder", "newfolder", "folder2", "tmp2"}
CODE_EXTS = {".py", ".ts", ".tsx", ".js", ".jsx", ".vue", ".go", ".rs"}


def lint(root: Path) -> dict[str, object]:
    violations = []
    checked = 0
    for path in root.rglob("*"):
        if any(part.startswith(".") and part not in {".", ".."} for part in path.parts) or should_skip(path, root):
            continue
        checked += 1
        if path.is_dir() and (" " in path.name or path.name.lower() in FORBIDDEN_DIR_TOKENS):
            violations.append({"path": rel(path, root), "reason": "unstable_directory_name"})
        if path.is_file() and path.suffix.lower() in CODE_EXTS and "tmp" in path.parts:
            violations.append({"path": rel(path, root), "reason": "source_file_forbidden_under_tmp"})
        if path.is_file() and path.suffix.lower() in CODE_EXTS and "rules" in path.parts:
            violations.append({"path": rel(path, root), "reason": "source_file_forbidden_under_rules"})
    return make_gate("folder_structure_gate", violations, checked)
