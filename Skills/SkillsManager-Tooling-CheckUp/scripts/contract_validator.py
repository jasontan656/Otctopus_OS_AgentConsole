from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import cast

from audit_models import AuditIssue, RuntimeContractPayload


def load_target_contract(target_root: Path) -> tuple[RuntimeContractPayload | None, str | None]:
    contract_path = target_root / "references" / "runtime_contracts" / "SKILL_RUNTIME_CONTRACT.json"
    if contract_path.is_file():
        return cast(RuntimeContractPayload, json.loads(contract_path.read_text(encoding="utf-8"))), "file"

    cli_path = target_root / "scripts" / "Cli_Toolbox.py"
    if not cli_path.is_file():
        return None, None
    completed = subprocess.run(
        ["python3", str(cli_path), "contract", "--json"],
        check=False,
        capture_output=True,
        text=True,
        cwd=target_root,
    )
    if completed.returncode != 0:
        return None, "cli_error"
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError:
        return None, "invalid_json"
    if not isinstance(payload, dict):
        return None, "invalid_json"
    return cast(RuntimeContractPayload, payload), "cli"


def validate_contract(payload: RuntimeContractPayload | None) -> list[AuditIssue]:
    if payload is None:
        return [AuditIssue("contract", "error", "missing runtime contract payload")]
    issues: list[AuditIssue] = []
    for field in ("skill_name", "tool_entry", "runtime_source_policy"):
        if field not in payload:
            issues.append(AuditIssue("contract", "error", f"missing contract field: {field}"))
    tool_entry = payload.get("tool_entry")
    if isinstance(tool_entry, dict):
        commands = tool_entry.get("commands")
        if not isinstance(commands, dict) or not commands:
            issues.append(AuditIssue("contract", "error", "contract tool_entry.commands must be a non-empty object"))
    else:
        issues.append(AuditIssue("contract", "error", "contract tool_entry must be an object"))
    if "artifact_policy" not in payload:
        issues.append(AuditIssue("contract", "warning", "artifact_policy is missing from the runtime contract"))
    return issues
