from __future__ import annotations

import ast
from pathlib import Path

from python_code_lint_rules.shared import (
    has_package_ancestor,
    iter_files,
    line_hits_from_node,
    make_gate,
    make_violation,
    parse_python_ast,
    preview_from_node,
    rel,
)

RULE_FILE = "Dev-PythonCode-Constitution-Backend/scripts/python_code_lint_rules/modules/resource_loading.py"
RESOURCE_METHODS = {"read_text", "read_bytes", "open"}


def _node_mentions_dunder_file(node: ast.AST) -> bool:
    return any(isinstance(child, ast.Name) and child.id == "__file__" for child in ast.walk(node))


def _uses_importlib_resources(tree: ast.AST) -> bool:
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "importlib.resources":
                    return True
        elif isinstance(node, ast.ImportFrom) and node.module == "importlib":
            if any(alias.name == "resources" for alias in node.names):
                return True
        elif isinstance(node, ast.ImportFrom) and node.module == "importlib.resources":
            return True
    return False


def lint(root: Path) -> dict[str, object]:
    violations = []
    checked = 0
    for path in iter_files(root, {".py"}):
        if not has_package_ancestor(path, root):
            continue
        checked += 1
        tree, text = parse_python_ast(path)
        if tree is None or _uses_importlib_resources(tree):
            continue
        path_text = rel(path, root)
        flagged = False
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if node.func.attr in RESOURCE_METHODS and _node_mentions_dunder_file(node.func.value):
                    violations.append(
                        make_violation(
                            path_text,
                            "package_resource_should_use_importlib_resources",
                            category="importlib_resources",
                            line_hits=line_hits_from_node(node),
                            matched_text_preview=preview_from_node(text, node),
                            why_flagged="package-local resource files should be loaded through importlib.resources instead of filesystem paths derived from __file__",
                            suggested_fix="replace __file__-relative package resource loading with importlib.resources.files()/read_text()/as_file()",
                        )
                    )
                    flagged = True
                    break
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "open" and node.args:
                if _node_mentions_dunder_file(node.args[0]):
                    violations.append(
                        make_violation(
                            path_text,
                            "package_resource_should_use_importlib_resources",
                            category="importlib_resources",
                            line_hits=line_hits_from_node(node),
                            matched_text_preview=preview_from_node(text, node),
                            why_flagged="package-local resource files should be loaded through importlib.resources instead of filesystem paths derived from __file__",
                            suggested_fix="replace __file__-relative package resource loading with importlib.resources.files()/read_text()/as_file()",
                        )
                    )
                    flagged = True
                    break
        if flagged:
            continue
    return make_gate("resource_loading_gate", violations, checked, rule_file=RULE_FILE)
