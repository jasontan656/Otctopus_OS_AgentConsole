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

RULE_FILE = "Dev-PythonCode-Constitution-Backend/scripts/python_code_lint_rules/modules/subprocess_safety.py"


def _collect_subprocess_aliases(tree: ast.AST) -> tuple[set[str], set[str], set[str]]:
    module_aliases = {"subprocess"}
    run_aliases: set[str] = set()
    popen_aliases: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "subprocess":
                    module_aliases.add(alias.asname or alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module == "subprocess":
            for alias in node.names:
                local_name = alias.asname or alias.name
                if alias.name == "run":
                    run_aliases.add(local_name)
                elif alias.name == "Popen":
                    popen_aliases.add(local_name)
    return module_aliases, run_aliases, popen_aliases


def _call_kind(node: ast.Call, module_aliases: set[str], run_aliases: set[str], popen_aliases: set[str]) -> str | None:
    func = node.func
    if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name) and func.value.id in module_aliases:
        if func.attr == "run":
            return "run"
        if func.attr == "Popen":
            return "popen"
    if isinstance(func, ast.Name):
        if func.id in run_aliases:
            return "run"
        if func.id in popen_aliases:
            return "popen"
    return None


def _has_shell_true(node: ast.Call) -> bool:
    for keyword in node.keywords:
        if keyword.arg != "shell":
            continue
        return isinstance(keyword.value, ast.Constant) and keyword.value.value is True
    return False


def lint(root: Path) -> dict[str, object]:
    violations = []
    checked = 0
    for path in iter_files(root, {".py"}):
        checked += 1
        tree, text = parse_python_ast(path)
        if tree is None:
            continue
        path_text = rel(path, root)
        module_aliases, run_aliases, popen_aliases = _collect_subprocess_aliases(tree)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            kind = _call_kind(node, module_aliases, run_aliases, popen_aliases)
            if kind is None:
                continue
            if kind == "popen":
                violations.append(
                    make_violation(
                        path_text,
                        "prefer_subprocess_run_over_popen",
                        category="subprocess_popen_usage",
                        line_hits=line_hits_from_node(node),
                        matched_text_preview=preview_from_node(text, node),
                        why_flagged="subprocess.run is the preferred high-level API for most child-process calls",
                        suggested_fix="use subprocess.run for simple command execution and keep Popen for the rare streaming or incremental IO case",
                    )
                )
            if _has_shell_true(node):
                violations.append(
                    make_violation(
                        path_text,
                        "subprocess_shell_true_forbidden",
                        category="subprocess_shell_true",
                        line_hits=line_hits_from_node(node),
                        matched_text_preview=preview_from_node(text, node),
                        why_flagged="shell=True widens command-injection risk and should stay out of default Python backend code",
                        suggested_fix="pass argv as a list and remove shell=True unless the command genuinely requires a shell",
                    )
                )
    return make_gate("subprocess_safety_gate", violations, checked, rule_file=RULE_FILE)
