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

RULE_FILE = "Dev-PythonCode-Constitution/scripts/python_code_lint_rules/modules/logging_boundary.py"
ROOT_METHODS = {"debug", "info", "warning", "error", "exception", "critical", "log"}


def _is_cli_entrypoint(path: Path) -> bool:
    name = path.name.lower()
    stem = path.stem.lower()
    return name == "__main__.py" or any(token in stem for token in ("cli", "runner", "task", "manage"))


def _collect_logging_aliases(tree: ast.AST) -> tuple[set[str], set[str], set[str], set[str]]:
    module_aliases = {"logging"}
    root_method_aliases: set[str] = set()
    basic_config_aliases: set[str] = set()
    get_logger_aliases: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "logging":
                    module_aliases.add(alias.asname or alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module == "logging":
            for alias in node.names:
                local_name = alias.asname or alias.name
                if alias.name in ROOT_METHODS:
                    root_method_aliases.add(local_name)
                elif alias.name == "basicConfig":
                    basic_config_aliases.add(local_name)
                elif alias.name == "getLogger":
                    get_logger_aliases.add(local_name)
    return module_aliases, root_method_aliases, basic_config_aliases, get_logger_aliases


def _is_root_method_call(node: ast.Call, module_aliases: set[str], root_method_aliases: set[str]) -> bool:
    func = node.func
    if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
        return func.value.id in module_aliases and func.attr in ROOT_METHODS
    return isinstance(func, ast.Name) and func.id in root_method_aliases


def _is_basic_config_call(node: ast.Call, module_aliases: set[str], basic_config_aliases: set[str]) -> bool:
    func = node.func
    if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
        return func.value.id in module_aliases and func.attr == "basicConfig"
    return isinstance(func, ast.Name) and func.id in basic_config_aliases


def _is_get_logger_call(node: ast.Call, module_aliases: set[str], get_logger_aliases: set[str]) -> bool:
    func = node.func
    if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
        return func.value.id in module_aliases and func.attr == "getLogger"
    return isinstance(func, ast.Name) and func.id in get_logger_aliases


def _uses_explicit_logger_name(node: ast.Call) -> bool:
    if not node.args:
        return False
    first = node.args[0]
    if isinstance(first, ast.Constant):
        return isinstance(first.value, str) and first.value != ""
    return True


def lint(root: Path) -> dict[str, object]:
    violations = []
    checked = 0
    for path in iter_files(root, {".py"}):
        checked += 1
        tree, text = parse_python_ast(path)
        if tree is None:
            continue
        path_text = rel(path, root)
        is_cli_entrypoint = _is_cli_entrypoint(path)
        module_aliases, root_method_aliases, basic_config_aliases, get_logger_aliases = _collect_logging_aliases(tree)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if not is_cli_entrypoint and _is_root_method_call(node, module_aliases, root_method_aliases):
                violations.append(
                    make_violation(
                        path_text,
                        "root_logger_call_forbidden",
                        category="logging_root_logger",
                        line_hits=line_hits_from_node(node),
                        matched_text_preview=preview_from_node(text, node),
                        why_flagged="library-style Python code should emit logs through a named logger instead of the root logger",
                        suggested_fix="create logger = logging.getLogger(__name__) and call logger.info/debug/... instead of logging.info/debug/...",
                    )
                )
            if not is_cli_entrypoint and _is_basic_config_call(node, module_aliases, basic_config_aliases):
                violations.append(
                    make_violation(
                        path_text,
                        "logging_basicconfig_forbidden_in_library_code",
                        category="logging_basic_config",
                        line_hits=line_hits_from_node(node),
                        matched_text_preview=preview_from_node(text, node),
                        why_flagged="library-style Python modules should not configure global logging handlers or root logging state",
                        suggested_fix="move logging.basicConfig into the real CLI entrypoint or application bootstrap layer",
                    )
                )
            if _is_get_logger_call(node, module_aliases, get_logger_aliases) and not _uses_explicit_logger_name(node):
                violations.append(
                    make_violation(
                        path_text,
                        "logging_getlogger_requires_explicit_name",
                        category="logging_logger_name",
                        line_hits=line_hits_from_node(node),
                        matched_text_preview=preview_from_node(text, node),
                        why_flagged="named loggers keep module ownership clear and avoid falling back to the unnamed root logger",
                        suggested_fix="call logging.getLogger(__name__) or another explicit logger name instead of logging.getLogger()",
                    )
                )
    return make_gate("logging_boundary_gate", violations, checked, rule_file=RULE_FILE)
