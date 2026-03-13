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

RULE_FILE = "Dev-PythonCode-Constitution/scripts/python_code_lint_rules/modules/typing_governance.py"


def _annotation_mentions_any(text: str, annotation: ast.AST | None) -> bool:
    if annotation is None:
        return False
    segment = ast.get_source_segment(text, annotation) or ""
    return "Any" in segment


def _missing_annotation_parts(node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[str]:
    missing: list[str] = []
    args = [*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs]
    for arg in args:
        if arg.arg in {"self", "cls"}:
            continue
        if arg.annotation is None:
            missing.append(f"arg:{arg.arg}")
    if node.args.vararg and node.args.vararg.annotation is None:
        missing.append(f"vararg:{node.args.vararg.arg}")
    if node.args.kwarg and node.args.kwarg.annotation is None:
        missing.append(f"kwarg:{node.args.kwarg.arg}")
    if node.returns is None:
        missing.append("return")
    return missing


class _TypingVisitor(ast.NodeVisitor):
    def __init__(self, path_text: str, text: str) -> None:
        self.path_text = path_text
        self.text = text
        self.function_depth = 0
        self.violations: list[dict[str, object]] = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._check_function(node)
        self.function_depth += 1
        self.generic_visit(node)
        self.function_depth -= 1

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._check_function(node)
        self.function_depth += 1
        self.generic_visit(node)
        self.function_depth -= 1

    def _check_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        if self.function_depth > 0 or node.name.startswith("_"):
            return

        missing = _missing_annotation_parts(node)
        if missing:
            self.violations.append(
                make_violation(
                    self.path_text,
                    f"public_function_missing_type_hints:{','.join(missing)}",
                    category="missing_type_hints",
                    line_hits=line_hits_from_node(node),
                    matched_text_preview=preview_from_node(self.text, node),
                    why_flagged="public Python functions should expose complete parameter and return annotations",
                    suggested_fix="add explicit annotations for every public parameter and return value",
                )
            )

        annotations = [node.returns, *(arg.annotation for arg in [*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs])]
        if node.args.vararg:
            annotations.append(node.args.vararg.annotation)
        if node.args.kwarg:
            annotations.append(node.args.kwarg.annotation)
        if any(_annotation_mentions_any(self.text, annotation) for annotation in annotations):
            self.violations.append(
                make_violation(
                    self.path_text,
                    "public_function_signature_uses_any",
                    category="typing_any_in_public_signature",
                    line_hits=line_hits_from_node(node),
                    matched_text_preview=preview_from_node(self.text, node),
                    why_flagged="public Python signatures should avoid unbounded Any and keep contracts machine-checkable",
                    suggested_fix="replace Any in the public signature with a concrete type, TypedDict, Protocol, or a constrained generic",
                )
            )


def lint(root: Path) -> dict[str, object]:
    violations = []
    checked = 0
    for path in iter_files(root, {".py"}):
        checked += 1
        tree, text = parse_python_ast(path)
        if tree is None:
            continue
        visitor = _TypingVisitor(rel(path, root), text)
        visitor.visit(tree)
        violations.extend(visitor.violations)
    return make_gate("typing_governance_gate", violations, checked, rule_file=RULE_FILE)
