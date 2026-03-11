from __future__ import annotations

from pathlib import Path
import re

from python_code_lint_rules.shared import SOURCE_EXTS, iter_files, make_gate, rel


def _name_has(path: Path, *tokens: str) -> bool:
    name_tokens = {token for token in re.split(r"[_\\W]+", path.name.lower()) if token}
    return any(token in name_tokens for token in tokens)


def _name_has_flow_role(path: Path) -> bool:
    name = path.name.lower()
    return "orchestrator" in name or name.endswith("_flow.py") or name.startswith("flow_")


def _text_signals_cli(path: Path) -> bool:
    if "tests" in path.parts:
        return False
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return False
    return any(
        signal in text
        for signal in (
            "argparse",
            "__main__",
            "add_argument(",
            "ArgumentParser(",
            "subparsers",
        )
    )


THRESHOLDS = [
    ("rule_definition_file", 1000, lambda p: "rules" in p.parts or _name_has(p, "rule", "constitution", "lint")),
    ("integration_e2e_test_file", 420, lambda p: "tests" in p.parts and _name_has(p, "integration", "e2e")),
    ("unit_test_file", 260, lambda p: "tests" in p.parts),
    ("runtime_config_file", 180, lambda p: p.suffix in {".yaml", ".yml", ".json", ".toml"} and _name_has(p, "config", "settings", "env")),
    ("schema_or_contract_file", 300, lambda p: _name_has(p, "schema", "contract", "dto", "payload")),
    ("workflow_or_contract_support", 240, lambda p: "scripts" in p.parts and _name_has(p, "workflow", "policy", "support")),
    ("registry_or_contract_data", 280, lambda p: "scripts" in p.parts and _name_has(p, "registry", "data")),
    ("db_migration_file", 180, lambda p: _name_has(p, "migration", "migrate")),
    ("backend_helper", 140, lambda p: _name_has(p, "helper")),
    ("backend_adapter_client", 220, lambda p: _name_has(p, "adapter", "client")),
    ("backend_repository_or_model", 220, lambda p: _name_has(p, "repo", "repository", "model")),
    ("backend_domain_service", 260, lambda p: _name_has(p, "domain", "service")),
    ("backend_orchestrator", 180, lambda p: _name_has_flow_role(p)),
    ("backend_api_controller", 220, lambda p: _name_has(p, "controller", "route", "handler", "api")),
    (
        "cli_or_task_script",
        420,
        lambda p: ("tests" not in p.parts and _name_has(p, "cli", "task", "runner"))
        or ("scripts" in p.parts and _text_signals_cli(p)),
    ),
]


def lint(root: Path) -> dict[str, object]:
    violations = []
    checked = 0
    for path in iter_files(root, SOURCE_EXTS):
        checked += 1
        lines = sum(1 for _ in path.open("r", encoding="utf-8", errors="ignore"))
        for category, limit, matcher in THRESHOLDS:
            if matcher(path) and lines > limit:
                violations.append({"path": rel(path, root), "reason": f"{category}>{limit}", "line_count": str(lines)})
                break
    return make_gate("fat_file_gate", violations, checked)
