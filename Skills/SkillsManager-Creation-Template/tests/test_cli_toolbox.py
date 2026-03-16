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


def test_contract_exposes_profile_support() -> None:
    payload = run_cli("contract")
    assert payload["skill_role"] == "creation_scaffold_governor"
    assert "referenced" in payload["profile_support"]["doc_topology"]
    assert "scaffold" in payload["tool_entry"]["commands"]


def test_profile_catalog_returns_default_profile() -> None:
    payload = run_cli("profile")
    assert payload["default_profile"]["doc_topology"] == "referenced"
    assert any(item["name"] == "workflow_automation" for item in payload["profiles"])


def test_scaffold_generates_referenced_contract_skill(tmp_path: Path) -> None:
    payload = run_cli(
        "scaffold",
        "--skill-name",
        "Demo-Skill",
        "--target-root",
        str(tmp_path),
        "--description",
        "Demo referenced governance skill.",
        "--doc-topology",
        "referenced",
        "--tooling-surface",
        "contract_cli",
        "--workflow-control",
        "guardrailed",
        "--overwrite",
    )
    skill_root = Path(payload["skill_root"])
    assert (skill_root / "references" / "runtime_contracts" / "SKILL_RUNTIME_CONTRACT.json").is_file()
    assert (skill_root / "tests" / "test_cli_toolbox.py").is_file()
    assert not (skill_root / "path").exists()


def test_scaffold_generates_workflow_path_skill(tmp_path: Path) -> None:
    payload = run_cli(
        "scaffold",
        "--skill-name",
        "Demo-Workflow",
        "--target-root",
        str(tmp_path),
        "--description",
        "Demo workflow skill.",
        "--doc-topology",
        "workflow_path",
        "--tooling-surface",
        "automation_cli",
        "--workflow-control",
        "compiled",
        "--overwrite",
    )
    skill_root = Path(payload["skill_root"])
    assert (skill_root / "path" / "development_loop" / "20_WORKFLOW_INDEX.md").is_file()
    assert (skill_root / "scripts" / "Cli_Toolbox.py").is_file()
