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

RULE_FILE = "Dev-PythonCode-Constitution-Backend/scripts/python_code_lint_rules/modules/time_random_boundary.py"
CORE_LOGIC_TOKENS = ("domain", "entity", "model", "policy", "service", "use_case", "usecase")
RANDOM_FUNCTIONS = {"random", "randint", "randrange", "choice", "choices", "shuffle", "sample", "uniform"}


def _collect_aliases(
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


def _classify_call(
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
    name = dotted_name(func)

    if isinstance(func, ast.Name):
        if func.id in time_func_aliases:
            return "time_now_requires_clock_boundary", "core logic should receive time from an explicit clock boundary instead of reading it directly"
        if func.id in uuid4_aliases:
            return "uuid4_requires_id_provider_boundary", "core logic should receive ids from an explicit provider instead of minting them inline"
        if func.id in random_func_aliases:
            return "randomness_requires_explicit_rng_boundary", "core logic should receive randomness from an explicit rng/provider boundary"

    if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
        owner = func.value.id
        if owner in datetime_aliases and func.attr in {"now", "utcnow"}:
            return "datetime_now_requires_clock_boundary", "core logic should receive time from an explicit clock boundary instead of reading datetime.now()/utcnow()"
        if owner in date_aliases and func.attr == "today":
            return "date_today_requires_clock_boundary", "core logic should receive dates from an explicit clock boundary instead of reading date.today()"
        if owner in time_modules and func.attr in {"time", "time_ns"}:
            return "time_now_requires_clock_boundary", "core logic should receive time from an explicit clock boundary instead of reading it directly"
        if owner in uuid_modules and func.attr == "uuid4":
            return "uuid4_requires_id_provider_boundary", "core logic should receive ids from an explicit provider instead of minting them inline"
        if owner in random_modules and func.attr in RANDOM_FUNCTIONS:
            return "randomness_requires_explicit_rng_boundary", "core logic should receive randomness from an explicit rng/provider boundary"
    if name == "uuid.uuid4":
        return "uuid4_requires_id_provider_boundary", "core logic should receive ids from an explicit provider instead of minting them inline"
    return None


def lint(root: Path) -> dict[str, object]:
    violations = []
    checked = 0
    for path in iter_files(root, {".py"}):
        if not path_looks_like_boundary_layer(path, root, CORE_LOGIC_TOKENS):
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
                    category="time_random_boundary",
                    line_hits=line_hits_from_node(node),
                    matched_text_preview=preview_from_node(text, node),
                    why_flagged=why_flagged,
                    suggested_fix="inject a clock, id provider, or rng into the core logic instead of calling time/random APIs inline",
                )
            )
    return make_gate("time_random_boundary_gate", violations, checked, rule_file=RULE_FILE)
