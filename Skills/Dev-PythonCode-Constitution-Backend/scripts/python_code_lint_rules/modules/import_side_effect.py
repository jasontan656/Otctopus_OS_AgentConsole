from __future__ import annotations

import ast
from pathlib import Path

from python_code_lint_rules.modules.concurrency_boundary import _collect_aliases as collect_concurrency_aliases
from python_code_lint_rules.modules.concurrency_boundary import _is_asyncio_create_task, _is_executor_constructor
from python_code_lint_rules.modules.io_boundary import _classify_call as classify_io_call
from python_code_lint_rules.modules.io_boundary import _collect_aliases as collect_io_aliases
from python_code_lint_rules.modules.time_random_boundary import _classify_call as classify_time_random_call
from python_code_lint_rules.modules.time_random_boundary import _collect_aliases as collect_time_random_aliases
from python_code_lint_rules.shared import (
    iter_files,
    line_hits_from_node,
    make_gate,
    make_violation,
    parse_python_ast,
    preview_from_node,
    rel,
)

RULE_FILE = "Dev-PythonCode-Constitution-Backend/scripts/python_code_lint_rules/modules/import_side_effect.py"


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
        io_aliases = collect_io_aliases(tree)
        time_random_aliases = collect_time_random_aliases(tree)
        asyncio_modules, create_task_aliases, executor_modules = collect_concurrency_aliases(tree)

        for stmt in tree.body:
            if isinstance(stmt, ast.If) and _is_main_guard(stmt):
                continue
            call = _top_level_call(stmt)
            if call is None:
                continue

            io_match = classify_io_call(call, *io_aliases)
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

            time_random_match = classify_time_random_call(call, *time_random_aliases)
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
