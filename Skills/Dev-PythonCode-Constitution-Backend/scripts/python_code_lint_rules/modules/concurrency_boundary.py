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

RULE_FILE = "Dev-PythonCode-Constitution-Backend/scripts/python_code_lint_rules/modules/concurrency_boundary.py"
EXECUTOR_BASE_TYPES = {"ThreadPoolExecutor", "ProcessPoolExecutor"}


def _collect_aliases(tree: ast.AST) -> tuple[set[str], set[str], set[str]]:
    asyncio_modules = {"asyncio"}
    create_task_aliases: set[str] = set()
    executor_modules = {"concurrent.futures"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "asyncio":
                    asyncio_modules.add(alias.asname or alias.name)
                if alias.name == "concurrent.futures":
                    executor_modules.add(alias.asname or alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module == "asyncio":
                for alias in node.names:
                    if alias.name == "create_task":
                        create_task_aliases.add(alias.asname or alias.name)
            elif node.module == "concurrent.futures":
                for alias in node.names:
                    if alias.name in EXECUTOR_BASE_TYPES:
                        executor_modules.add(alias.asname or alias.name)
    return asyncio_modules, create_task_aliases, executor_modules


def _build_parent_map(tree: ast.AST) -> dict[ast.AST, ast.AST]:
    parents: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parents[child] = parent
    return parents


def _is_asyncio_create_task(node: ast.Call, asyncio_modules: set[str], create_task_aliases: set[str]) -> bool:
    func = node.func
    if isinstance(func, ast.Name):
        return func.id in create_task_aliases
    name = dotted_name(func)
    if name is None:
        return False
    return any(name == f"{module}.create_task" for module in asyncio_modules)


def _is_executor_constructor(node: ast.Call, executor_modules: set[str]) -> bool:
    name = dotted_name(node.func)
    if name in EXECUTOR_BASE_TYPES:
        return True
    if name is None:
        return False
    return any(name == f"{module}.{executor_type}" for module in executor_modules for executor_type in EXECUTOR_BASE_TYPES)


def _is_with_context_call(node: ast.Call, parents: dict[ast.AST, ast.AST]) -> bool:
    parent = parents.get(node)
    return isinstance(parent, ast.withitem) and parent.context_expr is node


def lint(root: Path) -> dict[str, object]:
    violations = []
    checked = 0
    for path in iter_files(root, {".py"}):
        checked += 1
        tree, text = parse_python_ast(path)
        if tree is None:
            continue
        path_text = rel(path, root)
        asyncio_modules, create_task_aliases, executor_modules = _collect_aliases(tree)
        parents = _build_parent_map(tree)

        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue

            if _is_asyncio_create_task(node, asyncio_modules, create_task_aliases) and isinstance(parents.get(node), ast.Expr):
                violations.append(
                    make_violation(
                        path_text,
                        "asyncio_create_task_requires_explicit_task_owner",
                        category="concurrency_orphan_task",
                        line_hits=line_hits_from_node(node),
                        matched_text_preview=preview_from_node(text, node),
                        why_flagged="fire-and-forget create_task calls lose lifecycle and exception ownership unless the task handle is retained or managed by a task group",
                        suggested_fix="store the task handle, return it to a caller, or move the work under asyncio.TaskGroup instead of discarding create_task(...)",
                    )
                )

            if _is_executor_constructor(node, executor_modules) and not _is_with_context_call(node, parents):
                violations.append(
                    make_violation(
                        path_text,
                        "executor_constructor_requires_context_manager",
                        category="concurrency_executor_lifecycle",
                        line_hits=line_hits_from_node(node),
                        matched_text_preview=preview_from_node(text, node),
                        why_flagged="executor lifecycles should be bound to a context manager so shutdown and worker cleanup remain explicit",
                        suggested_fix="wrap ThreadPoolExecutor/ProcessPoolExecutor construction in with ... as executor:",
                    )
                )

    return make_gate("concurrency_boundary_gate", violations, checked, rule_file=RULE_FILE)
