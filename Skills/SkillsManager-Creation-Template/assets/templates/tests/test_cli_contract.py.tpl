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


def test_contract_returns_selected_profile() -> None:
    payload = run_cli("contract")
    assert payload["profile"]["doc_topology"] == "{{doc_topology}}"
    assert payload["profile"]["tooling_surface"] == "{{tooling_surface}}"
