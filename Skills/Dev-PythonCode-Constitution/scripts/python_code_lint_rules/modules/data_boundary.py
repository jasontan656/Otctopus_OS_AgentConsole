from __future__ import annotations

import ast
from pathlib import Path

from python_code_lint_rules.shared import (
    dotted_name,
    iter_files,
    line_hits_from_node,
    make_gate,
    make_violation,
    parse_python_ast,
    preview_from_node,
    rel,
)

RULE_FILE = "Dev-PythonCode-Constitution/scripts/python_code_lint_rules/modules/data_boundary.py"
PAYLOAD_LIKE_ARG_NAMES = {"payload", "body", "event", "message", "update", "record", "envelope"}
PAYLOAD_LIKE_RETURN_TOKENS = ("payload", "event", "message", "update", "record", "envelope")
RAW_MAPPING_TYPES = {
    "dict",
    "typing.Dict",
    "Mapping",
    "typing.Mapping",
    "collections.abc.Mapping",
    "MutableMapping",
    "typing.MutableMapping",
    "collections.abc.MutableMapping",
}


def _annotation_mentions_raw_mapping(annotation: ast.AST | None) -> bool:
    if annotation is None:
        return False
    direct = dotted_name(annotation)
    if direct in RAW_MAPPING_TYPES:
        return True
    if isinstance(annotation, ast.Subscript):
        return _annotation_mentions_raw_mapping(annotation.value) or _annotation_mentions_raw_mapping(annotation.slice)
    if isinstance(annotation, ast.BinOp) and isinstance(annotation.op, ast.BitOr):
        return _annotation_mentions_raw_mapping(annotation.left) or _annotation_mentions_raw_mapping(annotation.right)
    if isinstance(annotation, ast.Tuple):
        return any(_annotation_mentions_raw_mapping(element) for element in annotation.elts)
    return any(_annotation_mentions_raw_mapping(child) for child in ast.iter_child_nodes(annotation))


class _DataBoundaryVisitor(ast.NodeVisitor):
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

        for arg in [*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs]:
            if arg.arg in {"self", "cls"} or arg.arg not in PAYLOAD_LIKE_ARG_NAMES:
                continue
            if not _annotation_mentions_raw_mapping(arg.annotation):
                continue
            self.violations.append(
                make_violation(
                    self.path_text,
                    f"payload_like_argument_uses_mapping_contract:{arg.arg}",
                    category="data_boundary_payload_mapping",
                    line_hits=line_hits_from_node(node),
                    matched_text_preview=preview_from_node(self.text, node),
                    why_flagged="payload-like public interfaces should expose explicit structured contracts instead of raw mapping types",
                    suggested_fix="replace the payload-like dict/Mapping annotation with a TypedDict, dataclass, or explicit schema/model type",
                )
            )

        lowered_name = node.name.lower()
        if node.returns is None or not any(token in lowered_name for token in PAYLOAD_LIKE_RETURN_TOKENS):
            return
        if _annotation_mentions_raw_mapping(node.returns):
            self.violations.append(
                make_violation(
                    self.path_text,
                    "payload_like_return_uses_mapping_contract",
                    category="data_boundary_payload_mapping",
                    line_hits=line_hits_from_node(node),
                    matched_text_preview=preview_from_node(self.text, node),
                    why_flagged="payload-like public return contracts should stay explicit and machine-checkable instead of returning raw dict/Mapping shapes",
                    suggested_fix="return a TypedDict, dataclass, or explicit model type rather than dict/Mapping",
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
        visitor = _DataBoundaryVisitor(rel(path, root), text)
        visitor.visit(tree)
        violations.extend(visitor.violations)
    return make_gate("data_boundary_gate", violations, checked, rule_file=RULE_FILE)
