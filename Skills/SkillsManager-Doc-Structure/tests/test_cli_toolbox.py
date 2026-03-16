from __future__ import annotations

import json
import subprocess
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
CLI_PATH = SKILL_ROOT / "scripts" / "Cli_Toolbox.py"
CREATION_CLI_PATH = (
    SKILL_ROOT.parent / "SkillsManager-Creation-Template" / "scripts" / "Cli_Toolbox.py"
)


def run_cli(*args: str) -> dict[str, object]:
    completed = subprocess.run(
        ["python3", str(CLI_PATH), *args, "--json"],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def scaffold_workflow_skill(tmp_path: Path) -> Path:
    completed = subprocess.run(
        [
            "python3",
            str(CREATION_CLI_PATH),
            "scaffold",
            "--skill-name",
            "Workflow-Demo",
            "--target-root",
            str(tmp_path),
            "--description",
            "Workflow demo skill.",
            "--doc-topology",
            "workflow_path",
            "--tooling-surface",
            "automation_cli",
            "--workflow-control",
            "compiled",
            "--overwrite",
            "--json",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return Path(json.loads(completed.stdout)["skill_root"])


def test_contract_exposes_topology_support() -> None:
    payload = run_cli("contract")
    assert payload["skill_role"] == "doc_governor"
    assert "workflow_path" in payload["profile_support"]["doc_topology"]


def test_inspect_detects_referenced_target() -> None:
    payload = run_cli("inspect", "--target", str(SKILL_ROOT.parent / "SkillsManager-Creation-Template"))
    assert payload["profile"]["doc_topology"] == "referenced"
    assert "routing" in payload["available_context_entries"]


def test_lint_passes_for_referenced_target() -> None:
    payload = run_cli("lint", "--target", str(SKILL_ROOT.parent / "SkillsManager-Creation-Template"))
    assert payload["status"] == "ok"


def test_compile_context_for_workflow_target(tmp_path: Path) -> None:
    workflow_root = scaffold_workflow_skill(tmp_path)
    payload = run_cli(
        "compile-context",
        "--target",
        str(workflow_root),
        "--entry",
        "development_loop",
        "--selection",
        "primary_step",
    )
    assert payload["status"] == "ok"
    assert any(item.endswith("20_WORKFLOW_INDEX.md") for item in payload["resolved_chain"])
