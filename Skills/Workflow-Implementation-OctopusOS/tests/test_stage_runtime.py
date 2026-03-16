from __future__ import annotations

from pathlib import Path
import sys

SKILL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_ROOT.parents[0] / "_shared" / "octopus_os_workflow_runtime" / "tests_support"))

from workflow_test_support import run_cli, run_cli_raw


def test_contract_and_read_context_are_stage_local() -> None:
    payload = run_cli(SKILL_ROOT, "contract")
    assert payload["active_stage"] == "implementation"
    compiled = run_cli(SKILL_ROOT, "read-contract-context", "--entry", "stage_flow")
    assert compiled["status"] == "ok"


def test_stage_command_contract_is_stage_local() -> None:
    payload = run_cli(SKILL_ROOT, "stage-command-contract", "--stage", "implementation")
    assert payload["stage"] == "implementation"
