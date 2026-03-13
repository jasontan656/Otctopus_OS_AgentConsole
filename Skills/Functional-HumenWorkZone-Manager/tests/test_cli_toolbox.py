from __future__ import annotations

import json
import subprocess
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
CLI_PATH = SKILL_ROOT / "scripts" / "Cli_Toolbox.py"


def run_cli(*args: str) -> dict[str, object]:
    completed = subprocess.run(
        ["python3", str(CLI_PATH), *args, "--json"],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def test_contract_exposes_cli_first_entry() -> None:
    payload = run_cli("contract")
    commands = payload["tool_entry"]["commands"]
    assert "contract" in commands
    assert "directive" in commands
    assert "paths" in commands
    assert payload["managed_root"] == "/home/jasontan656/AI_Projects/Human_Work_Zone"


def test_directive_returns_task_routing_payload() -> None:
    payload = run_cli("directive", "--topic", "task-routing")
    assert payload["topic"] == "task-routing"
    assert payload["doc_kind"] == "guide"
    assert any("external reports" in item.lower() for item in payload["workflow"])


def test_paths_returns_managed_zones() -> None:
    payload = run_cli("paths")
    assert payload["managed_root"] == "/home/jasontan656/AI_Projects/Human_Work_Zone"
    assert payload["zones"]["external_research_reports"].endswith("/External_Research_Reports")
