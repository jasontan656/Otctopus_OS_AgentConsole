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

RULE_FILE = "Dev-PythonCode-Constitution-Backend/scripts/python_code_lint_rules/modules/http_timeout.py"
HTTP_METHODS = {"get", "post", "put", "patch", "delete", "head", "options", "request"}


def _is_none_literal(node: ast.AST | None) -> bool:
    return isinstance(node, ast.Constant) and node.value is None


def _timeout_keyword(node: ast.Call) -> ast.AST | None:
    for keyword in node.keywords:
        if keyword.arg == "timeout":
            return keyword.value
    return None


def _collect_aliases(tree: ast.AST) -> tuple[set[str], set[str], set[str], set[str], set[str], set[str]]:
    requests_modules = {"requests"}
    httpx_modules = {"httpx"}
    requests_funcs: set[str] = set()
    httpx_funcs: set[str] = set()
    requests_session_aliases: set[str] = set()
    httpx_client_aliases: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "requests":
                    requests_modules.add(alias.asname or alias.name)
                if alias.name == "httpx":
                    httpx_modules.add(alias.asname or alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module == "requests":
                for alias in node.names:
                    local = alias.asname or alias.name
                    if alias.name in HTTP_METHODS:
                        requests_funcs.add(local)
                    elif alias.name == "Session":
                        requests_session_aliases.add(local)
            elif node.module == "httpx":
                for alias in node.names:
                    local = alias.asname or alias.name
                    if alias.name in HTTP_METHODS:
                        httpx_funcs.add(local)
                    elif alias.name in {"Client", "AsyncClient"}:
                        httpx_client_aliases.add(local)
    return requests_modules, httpx_modules, requests_funcs, httpx_funcs, requests_session_aliases, httpx_client_aliases


def _requests_session_constructor(node: ast.Call, requests_modules: set[str], requests_session_aliases: set[str]) -> bool:
    func = node.func
    if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
        return func.value.id in requests_modules and func.attr == "Session"
    return isinstance(func, ast.Name) and func.id in requests_session_aliases


def _httpx_client_constructor(node: ast.Call, httpx_modules: set[str], httpx_client_aliases: set[str]) -> bool:
    func = node.func
    if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
        return func.value.id in httpx_modules and func.attr in {"Client", "AsyncClient"}
    return isinstance(func, ast.Name) and func.id in httpx_client_aliases


def _collect_client_variables(
    tree: ast.AST,
    requests_modules: set[str],
    httpx_modules: set[str],
    requests_session_aliases: set[str],
    httpx_client_aliases: set[str],
) -> tuple[set[str], set[str]]:
    request_session_vars: set[str] = set()
    httpx_client_vars: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign) or len(node.targets) != 1 or not isinstance(node.targets[0], ast.Name):
            continue
        target = node.targets[0].id
        if isinstance(node.value, ast.Call):
            if _requests_session_constructor(node.value, requests_modules, requests_session_aliases):
                request_session_vars.add(target)
            if _httpx_client_constructor(node.value, httpx_modules, httpx_client_aliases):
                httpx_client_vars.add(target)
    return request_session_vars, httpx_client_vars


def lint(root: Path) -> dict[str, object]:
    violations = []
    checked = 0
    for path in iter_files(root, {".py"}):
        checked += 1
        tree, text = parse_python_ast(path)
        if tree is None:
            continue
        path_text = rel(path, root)
        requests_modules, httpx_modules, requests_funcs, httpx_funcs, requests_session_aliases, httpx_client_aliases = _collect_aliases(tree)
        requests_session_vars, httpx_client_vars = _collect_client_variables(
            tree,
            requests_modules,
            httpx_modules,
            requests_session_aliases,
            httpx_client_aliases,
        )

        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue

            if _httpx_client_constructor(node, httpx_modules, httpx_client_aliases) and _is_none_literal(_timeout_keyword(node)):
                violations.append(
                    make_violation(
                        path_text,
                        "httpx_client_timeout_none_forbidden",
                        category="http_timeout_disabled",
                        line_hits=line_hits_from_node(node),
                        matched_text_preview=preview_from_node(text, node),
                        why_flagged="HTTPX enforces timeouts by default, and timeout=None disables that safety net for the entire client",
                        suggested_fix="keep HTTPX defaults or set an explicit timeout instead of timeout=None",
                    )
                )
                continue

            func = node.func
            timeout_value = _timeout_keyword(node)

            if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
                owner = func.value.id
                method = func.attr
                if method not in HTTP_METHODS:
                    continue
                if owner in requests_modules or owner in requests_session_vars:
                    if timeout_value is None:
                        violations.append(
                            make_violation(
                                path_text,
                                "requests_timeout_required",
                                category="http_timeout_missing",
                                line_hits=line_hits_from_node(node),
                                matched_text_preview=preview_from_node(text, node),
                                why_flagged="Requests does not time out by default, so outbound HTTP calls should declare a timeout explicitly",
                                suggested_fix="add timeout=<seconds> or timeout=(connect, read) to the requests call",
                            )
                        )
                    elif _is_none_literal(timeout_value):
                        violations.append(
                            make_violation(
                                path_text,
                                "requests_timeout_none_forbidden",
                                category="http_timeout_disabled",
                                line_hits=line_hits_from_node(node),
                                matched_text_preview=preview_from_node(text, node),
                                why_flagged="requests timeout=None disables the timeout safety boundary and may leave the call hanging indefinitely",
                                suggested_fix="set a real timeout value instead of timeout=None",
                            )
                        )
                elif owner in httpx_modules or owner in httpx_client_vars:
                    if _is_none_literal(timeout_value):
                        violations.append(
                            make_violation(
                                path_text,
                                "httpx_timeout_none_forbidden",
                                category="http_timeout_disabled",
                                line_hits=line_hits_from_node(node),
                                matched_text_preview=preview_from_node(text, node),
                                why_flagged="HTTPX already has safe default timeouts, so timeout=None should not disable them without an explicit exemption",
                                suggested_fix="remove timeout=None or replace it with an explicit timeout value",
                            )
                        )
                continue

            if isinstance(func, ast.Name):
                if func.id in requests_funcs:
                    if timeout_value is None:
                        violations.append(
                            make_violation(
                                path_text,
                                "requests_timeout_required",
                                category="http_timeout_missing",
                                line_hits=line_hits_from_node(node),
                                matched_text_preview=preview_from_node(text, node),
                                why_flagged="Requests does not time out by default, so outbound HTTP calls should declare a timeout explicitly",
                                suggested_fix="add timeout=<seconds> or timeout=(connect, read) to the requests call",
                            )
                        )
                    elif _is_none_literal(timeout_value):
                        violations.append(
                            make_violation(
                                path_text,
                                "requests_timeout_none_forbidden",
                                category="http_timeout_disabled",
                                line_hits=line_hits_from_node(node),
                                matched_text_preview=preview_from_node(text, node),
                                why_flagged="requests timeout=None disables the timeout safety boundary and may leave the call hanging indefinitely",
                                suggested_fix="set a real timeout value instead of timeout=None",
                            )
                        )
                elif func.id in httpx_funcs and _is_none_literal(timeout_value):
                    violations.append(
                        make_violation(
                            path_text,
                            "httpx_timeout_none_forbidden",
                            category="http_timeout_disabled",
                            line_hits=line_hits_from_node(node),
                            matched_text_preview=preview_from_node(text, node),
                            why_flagged="HTTPX already has safe default timeouts, so timeout=None should not disable them without an explicit exemption",
                            suggested_fix="remove timeout=None or replace it with an explicit timeout value",
                        )
                    )
    return make_gate("http_timeout_gate", violations, checked, rule_file=RULE_FILE)
