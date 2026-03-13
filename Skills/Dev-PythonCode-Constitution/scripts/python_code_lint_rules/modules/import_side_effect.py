from __future__ import annotations

import ast
from pathlib import Path

from python_code_lint_rules.modules.concurrency_boundary import _collect_aliases as collect_concurrency_aliases
from python_code_lint_rules.modules.concurrency_boundary import _is_asyncio_create_task, _is_executor_constructor
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

RULE_FILE = "Dev-PythonCode-Constitution/scripts/python_code_lint_rules/modules/import_side_effect.py"
HTTP_METHODS = {"get", "post", "put", "patch", "delete", "head", "options", "request"}
PATH_IO_METHODS = {"read_text", "read_bytes", "write_text", "write_bytes"}
RANDOM_FUNCTIONS = {"random", "randint", "randrange", "choice", "choices", "shuffle", "sample", "uniform"}


def _collect_io_aliases(tree: ast.AST) -> tuple[set[str], set[str], set[str], set[str], set[str], set[str], set[str], set[str]]:
    requests_modules = {"requests"}
    httpx_modules = {"httpx"}
    subprocess_modules = {"subprocess"}
    socket_modules = {"socket"}
    path_aliases = {"Path"}
    requests_funcs: set[str] = set()
    httpx_funcs: set[str] = set()
    client_aliases: set[str] = set()
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
                        client_aliases.add(local)
            elif node.module == "httpx":
                for alias in node.names:
                    local = alias.asname or alias.name
                    if alias.name in HTTP_METHODS:
                        httpx_funcs.add(local)
                    elif alias.name in {"Client", "AsyncClient"}:
                        client_aliases.add(local)
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
        client_aliases,
    )


def _collect_time_random_aliases(
    tree: ast.AST,
) -> tuple[set[str], set[str], set[str], set[str], set[str], set[str], set[str], set[str]]:
    datetime_aliases = {"datetime"}
    date_aliases = {"date"}
    time_modules = {"time"}
    time_func_aliases: set[str] = set()
    uuid_modules = {"uuid"}
    uuid4_aliases: set[str] = set()
    random_modules = {"random"}
    random_func_aliases: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "time":
                    time_modules.add(alias.asname or alias.name)
                elif alias.name == "uuid":
                    uuid_modules.add(alias.asname or alias.name)
                elif alias.name == "random":
                    random_modules.add(alias.asname or alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module == "datetime":
                for alias in node.names:
                    if alias.name == "datetime":
                        datetime_aliases.add(alias.asname or alias.name)
                    elif alias.name == "date":
                        date_aliases.add(alias.asname or alias.name)
            elif node.module == "time":
                for alias in node.names:
                    if alias.name in {"time", "time_ns"}:
                        time_func_aliases.add(alias.asname or alias.name)
            elif node.module == "uuid":
                for alias in node.names:
                    if alias.name == "uuid4":
                        uuid4_aliases.add(alias.asname or alias.name)
            elif node.module == "random":
                for alias in node.names:
                    if alias.name in RANDOM_FUNCTIONS:
                        random_func_aliases.add(alias.asname or alias.name)
    return (
        datetime_aliases,
        date_aliases,
        time_modules,
        time_func_aliases,
        uuid_modules,
        uuid4_aliases,
        random_modules,
        random_func_aliases,
    )


def _classify_import_io_call(
    node: ast.Call,
    requests_modules: set[str],
    httpx_modules: set[str],
    subprocess_modules: set[str],
    socket_modules: set[str],
    path_aliases: set[str],
    requests_funcs: set[str],
    httpx_funcs: set[str],
    client_aliases: set[str],
) -> tuple[str, str] | None:
    func = node.func
    name = dotted_name(func)

    if isinstance(func, ast.Name):
        if func.id == "open":
            return "module_import_performs_file_io", "module import should not read or write files directly"
        if func.id in requests_funcs or func.id in httpx_funcs:
            return "module_import_performs_network_io", "module import should not issue outbound HTTP requests"
        if func.id in client_aliases:
            return "module_import_constructs_runtime_client", "module import should not construct HTTP client/session objects"

    if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
        owner = func.value.id
        if owner in requests_modules and func.attr in HTTP_METHODS:
            return "module_import_performs_network_io", "module import should not issue outbound HTTP requests"
        if owner in httpx_modules and func.attr in HTTP_METHODS:
            return "module_import_performs_network_io", "module import should not issue outbound HTTP requests"
        if owner in requests_modules and func.attr == "Session":
            return "module_import_constructs_runtime_client", "module import should not construct HTTP client/session objects"
        if owner in httpx_modules and func.attr in {"Client", "AsyncClient"}:
            return "module_import_constructs_runtime_client", "module import should not construct HTTP client/session objects"
        if owner in subprocess_modules:
            return "module_import_spawns_subprocess_runtime", "module import should not spawn subprocess work"
        if owner in socket_modules:
            return "module_import_opens_socket_runtime", "module import should not open sockets"

    if isinstance(func, ast.Attribute):
        if func.attr in PATH_IO_METHODS:
            return "module_import_performs_file_io", "module import should not read or write files directly"
        if func.attr == "open":
            owner_name = dotted_name(func.value)
            if owner_name in path_aliases:
                return "module_import_performs_file_io", "module import should not read or write files directly"

    if name == "socket.create_connection":
        return "module_import_opens_socket_runtime", "module import should not open sockets"
    return None


def _classify_import_time_random_call(
    node: ast.Call,
    datetime_aliases: set[str],
    date_aliases: set[str],
    time_modules: set[str],
    time_func_aliases: set[str],
    uuid_modules: set[str],
    uuid4_aliases: set[str],
    random_modules: set[str],
    random_func_aliases: set[str],
) -> tuple[str, str] | None:
    func = node.func
    if isinstance(func, ast.Name):
        if func.id in time_func_aliases:
            return "module_import_reads_current_time", "module import should not capture current time as runtime state"
        if func.id in uuid4_aliases:
            return "module_import_generates_runtime_id", "module import should not mint UUID values as runtime state"
        if func.id in random_func_aliases:
            return "module_import_generates_random_runtime_state", "module import should not generate random values as runtime state"

    if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
        owner = func.value.id
        if owner in datetime_aliases and func.attr in {"now", "utcnow"}:
            return "module_import_reads_current_time", "module import should not capture current time as runtime state"
        if owner in date_aliases and func.attr == "today":
            return "module_import_reads_current_time", "module import should not capture current date as runtime state"
        if owner in time_modules and func.attr in {"time", "time_ns"}:
            return "module_import_reads_current_time", "module import should not capture current time as runtime state"
        if owner in uuid_modules and func.attr == "uuid4":
            return "module_import_generates_runtime_id", "module import should not mint UUID values as runtime state"
        if owner in random_modules and func.attr in RANDOM_FUNCTIONS:
            return "module_import_generates_random_runtime_state", "module import should not generate random values as runtime state"
    return None


def _top_level_call(stmt: ast.stmt) -> ast.Call | None:
    if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
        return stmt.value
    if isinstance(stmt, ast.Assign) and isinstance(stmt.value, ast.Call):
        return stmt.value
    if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.value, ast.Call):
        return stmt.value
    return None


def _is_main_guard(node: ast.If) -> bool:
    test = node.test
    if not isinstance(test, ast.Compare) or len(test.ops) != 1 or len(test.comparators) != 1:
        return False
    left = test.left
    right = test.comparators[0]
    if not isinstance(test.ops[0], ast.Eq):
        return False
    return (
        isinstance(left, ast.Name)
        and left.id == "__name__"
        and isinstance(right, ast.Constant)
        and right.value == "__main__"
    )


def lint(root: Path) -> dict[str, object]:
    violations = []
    checked = 0
    for path in iter_files(root, {".py"}):
        checked += 1
        tree, text = parse_python_ast(path)
        if tree is None or not isinstance(tree, ast.Module):
            continue
        path_text = rel(path, root)
        io_aliases = _collect_io_aliases(tree)
        time_random_aliases = _collect_time_random_aliases(tree)
        asyncio_modules, create_task_aliases, executor_modules = collect_concurrency_aliases(tree)

        for stmt in tree.body:
            if isinstance(stmt, ast.If) and _is_main_guard(stmt):
                continue
            call = _top_level_call(stmt)
            if call is None:
                continue

            io_match = _classify_import_io_call(call, *io_aliases)
            if io_match is not None:
                reason, why_flagged = io_match
                violations.append(
                    make_violation(
                        path_text,
                        f"import_side_effect:{reason}",
                        category="import_side_effect",
                        line_hits=line_hits_from_node(call),
                        matched_text_preview=preview_from_node(text, call),
                        why_flagged=f"module import should stay side-effect-light; {why_flagged}",
                        suggested_fix="move the call behind a function, factory, startup hook, or __main__ guard instead of executing it at import time",
                    )
                )
                continue

            if _is_asyncio_create_task(call, asyncio_modules, create_task_aliases):
                violations.append(
                    make_violation(
                        path_text,
                        "import_side_effect:module_import_starts_background_task",
                        category="import_side_effect",
                        line_hits=line_hits_from_node(call),
                        matched_text_preview=preview_from_node(text, call),
                        why_flagged="module import should not start background tasks before the application has established task ownership and shutdown policy",
                        suggested_fix="create background tasks inside an explicit startup hook or runtime owner instead of import time",
                    )
                )
                continue

            if _is_executor_constructor(call, executor_modules):
                violations.append(
                    make_violation(
                        path_text,
                        "import_side_effect:module_import_constructs_executor",
                        category="import_side_effect",
                        line_hits=line_hits_from_node(call),
                        matched_text_preview=preview_from_node(text, call),
                        why_flagged="module import should not allocate executors before runtime ownership and shutdown are established",
                        suggested_fix="construct the executor inside a function or startup boundary and own its shutdown explicitly",
                    )
                )
                continue

            time_random_match = _classify_import_time_random_call(call, *time_random_aliases)
            if time_random_match is not None:
                reason, why_flagged = time_random_match
                violations.append(
                    make_violation(
                        path_text,
                        f"import_side_effect:{reason}",
                        category="import_side_effect",
                        line_hits=line_hits_from_node(call),
                        matched_text_preview=preview_from_node(text, call),
                        why_flagged=f"module import should stay deterministic; {why_flagged}",
                        suggested_fix="defer clock/random/id generation until an explicit runtime function executes",
                    )
                )

    return make_gate("import_side_effect_gate", violations, checked, rule_file=RULE_FILE)
