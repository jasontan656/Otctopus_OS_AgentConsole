from __future__ import annotations

import ast
from pathlib import Path

from python_code_lint_rules.shared import (
    iter_files,
    line_hits_from_node,
    make_gate,
    make_violation,
    parse_python_ast,
    preview_from_node,
    rel,
)

RULE_FILE = "Dev-PythonCode-Constitution/scripts/python_code_lint_rules/modules/exception_governance.py"


def _handler_type_names(node: ast.ExceptHandler) -> set[str]:
    if node.type is None:
        return set()
    if isinstance(node.type, ast.Name):
        return {node.type.id}
    if isinstance(node.type, ast.Tuple):
        names: set[str] = set()
        for element in node.type.elts:
            if isinstance(element, ast.Name):
                names.add(element.id)
        return names
    return set()


def _body_has_raise(body: list[ast.stmt]) -> bool:
    return any(isinstance(child, ast.Raise) for stmt in body for child in ast.walk(stmt))


def lint(root: Path) -> dict[str, object]:
    violations = []
    checked = 0
    for path in iter_files(root, {".py"}):
        checked += 1
        tree, text = parse_python_ast(path)
        if tree is None:
            continue
        path_text = rel(path, root)
        for node in ast.walk(tree):
            if not isinstance(node, ast.ExceptHandler):
                continue
            type_names = _handler_type_names(node)
            if node.type is None:
                violations.append(
                    make_violation(
                        path_text,
                        "bare_except_forbidden",
                        category="exception_bare_except",
                        line_hits=line_hits_from_node(node),
                        matched_text_preview=preview_from_node(text, node),
                        why_flagged="bare except catches system-exiting exceptions and hides the actual failure boundary",
                        suggested_fix="catch a specific exception type or, if you truly mean unexpected non-fatal errors, catch Exception and re-raise after handling",
                    )
                )
                continue
            if "BaseException" in type_names:
                violations.append(
                    make_violation(
                        path_text,
                        "baseexception_handler_forbidden",
                        category="exception_baseexception",
                        line_hits=line_hits_from_node(node),
                        matched_text_preview=preview_from_node(text, node),
                        why_flagged="BaseException also covers SystemExit and KeyboardInterrupt, which are normally not meant to be swallowed by backend code",
                        suggested_fix="catch a specific non-fatal exception type instead of BaseException",
                    )
                )
            if "Exception" in type_names and not _body_has_raise(node.body):
                violations.append(
                    make_violation(
                        path_text,
                        "broad_exception_without_reraise",
                        category="exception_broad_handler",
                        line_hits=line_hits_from_node(node),
                        matched_text_preview=preview_from_node(text, node),
                        why_flagged="broad Exception handlers should normally log/contextualize and then re-raise unexpected failures",
                        suggested_fix="narrow the exception type or re-raise after adding context, for example with raise or raise ... from exc",
                    )
                )
    return make_gate("exception_governance_gate", violations, checked, rule_file=RULE_FILE)
