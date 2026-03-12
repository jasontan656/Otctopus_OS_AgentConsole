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
    path_looks_like_boundary_layer,
    preview_from_node,
    rel,
)

RULE_FILE = "Dev-PythonCode-Constitution-Backend/scripts/python_code_lint_rules/modules/io_boundary.py"
PURE_LAYER_TOKENS = ("domain", "entity", "model", "value_object", "valueobject", "policy", "specification")
HTTP_METHODS = {"get", "post", "put", "patch", "delete", "head", "options", "request"}
PATH_IO_METHODS = {"read_text", "read_bytes", "write_text", "write_bytes"}


def _collect_aliases(tree: ast.AST) -> tuple[set[str], set[str], set[str], set[str], set[str], set[str], set[str], set[str]]:
    requests_modules = {"requests"}
    httpx_modules = {"httpx"}
    subprocess_modules = {"subprocess"}
    socket_modules = {"socket"}
    path_aliases = {"Path"}
    requests_funcs: set[str] = set()
    httpx_funcs: set[str] = set()
    session_client_aliases: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "requests":
                    requests_modules.add(alias.asname or alias.name)
                elif alias.name == "httpx":
                    httpx_modules.add(alias.asname or alias.name)
                elif alias.name == "subprocess":
                    subprocess_modules.add(alias.asname or alias.name)
                elif alias.name == "socket":
                    socket_modules.add(alias.asname or alias.name)
                elif alias.name == "pathlib":
                    path_aliases.add(f"{alias.asname or alias.name}.Path")
        elif isinstance(node, ast.ImportFrom):
            if node.module == "requests":
                for alias in node.names:
                    local = alias.asname or alias.name
                    if alias.name in HTTP_METHODS:
                        requests_funcs.add(local)
                    elif alias.name == "Session":
                        session_client_aliases.add(local)
            elif node.module == "httpx":
                for alias in node.names:
                    local = alias.asname or alias.name
                    if alias.name in HTTP_METHODS:
                        httpx_funcs.add(local)
                    elif alias.name in {"Client", "AsyncClient"}:
                        session_client_aliases.add(local)
            elif node.module == "pathlib":
                for alias in node.names:
                    if alias.name == "Path":
                        path_aliases.add(alias.asname or alias.name)
    return (
        requests_modules,
        httpx_modules,
        subprocess_modules,
        socket_modules,
        path_aliases,
        requests_funcs,
        httpx_funcs,
        session_client_aliases,
    )


def _is_pathlike_call(node: ast.AST, path_aliases: set[str]) -> bool:
    name = dotted_name(node)
    if name is None:
        return False
    return name in path_aliases


def _classify_call(
    node: ast.Call,
    requests_modules: set[str],
    httpx_modules: set[str],
    subprocess_modules: set[str],
    socket_modules: set[str],
    path_aliases: set[str],
    requests_funcs: set[str],
    httpx_funcs: set[str],
    session_client_aliases: set[str],
) -> tuple[str, str] | None:
    func = node.func
    name = dotted_name(func)

    if isinstance(func, ast.Name):
        if func.id == "open":
            return "pure_layer_contains_file_io", "pure layer files should not perform file reads or writes directly"
        if func.id in requests_funcs or func.id in httpx_funcs:
            return "pure_layer_contains_network_io", "pure layer files should delegate outbound HTTP calls to adapters or gateways"
        if func.id in session_client_aliases:
            return "pure_layer_constructs_runtime_client", "pure layer files should not construct HTTP client/session objects directly"

    if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
        owner = func.value.id
        if owner in requests_modules and func.attr in HTTP_METHODS:
            return "pure_layer_contains_network_io", "pure layer files should delegate outbound HTTP calls to adapters or gateways"
        if owner in httpx_modules and func.attr in HTTP_METHODS:
            return "pure_layer_contains_network_io", "pure layer files should delegate outbound HTTP calls to adapters or gateways"
        if owner in requests_modules and func.attr == "Session":
            return "pure_layer_constructs_runtime_client", "pure layer files should not construct HTTP client/session objects directly"
        if owner in httpx_modules and func.attr in {"Client", "AsyncClient"}:
            return "pure_layer_constructs_runtime_client", "pure layer files should not construct HTTP client/session objects directly"
        if owner in subprocess_modules:
            return "pure_layer_contains_subprocess_io", "pure layer files should not spawn subprocess work directly"
        if owner in socket_modules:
            return "pure_layer_contains_network_io", "pure layer files should not open sockets directly"

    if isinstance(func, ast.Attribute):
        if func.attr in PATH_IO_METHODS:
            return "pure_layer_contains_file_io", "pure layer files should not perform file reads or writes directly"
        if func.attr == "open" and _is_pathlike_call(func.value, path_aliases):
            return "pure_layer_contains_file_io", "pure layer files should not perform file reads or writes directly"

    if name == "socket.create_connection":
        return "pure_layer_contains_network_io", "pure layer files should not open sockets directly"
    return None


def lint(root: Path) -> dict[str, object]:
    violations = []
    checked = 0
    for path in iter_files(root, {".py"}):
        if not path_looks_like_boundary_layer(path, root, PURE_LAYER_TOKENS):
            continue
        checked += 1
        tree, text = parse_python_ast(path)
        if tree is None:
            continue
        aliases = _collect_aliases(tree)
        path_text = rel(path, root)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            match = _classify_call(node, *aliases)
            if match is None:
                continue
            reason, why_flagged = match
            violations.append(
                make_violation(
                    path_text,
                    reason,
                    category="io_boundary",
                    line_hits=line_hits_from_node(node),
                    matched_text_preview=preview_from_node(text, node),
                    why_flagged=why_flagged,
                    suggested_fix="move the side effect into an adapter, gateway, repository, or CLI/bootstrap boundary and pass the result into the pure layer",
                )
            )
    return make_gate("io_boundary_gate", violations, checked, rule_file=RULE_FILE)
