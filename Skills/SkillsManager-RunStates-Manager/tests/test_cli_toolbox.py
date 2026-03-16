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


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _workflow_skill_fixture(root: Path, orchestrator: bool) -> Path:
    skill_root = root / ("Demo-Orchestrator" if orchestrator else "Demo-Workflow")
    _write(
        skill_root / "SKILL.md",
        """---
name: Demo
metadata:
  skill_profile:
    doc_topology: workflow_path
    tooling_surface: automation_cli
    workflow_control: compiled
---

# Demo
""",
    )
    marker_line = "本技能的下游治理链需要显式启用相关治理技能。" if orchestrator else "本技能以 workflow_runtime_checklist 与 stage_runtime_checklist 治理步骤。"
    _write(
        skill_root / "path" / "analysis_loop" / "10_CONTRACT.md",
        f"""# contract

- {marker_line}
- 下一步必须消费上一步产物。
- 每个原子步骤结束后立即回填 checklist，并由回填结果驱动下一步。
- Skills_runtime_checklist
- workflow_runtime_checklist
- stage_runtime_checklist
""",
    )
    return skill_root


def test_contract_exposes_runstate_schema() -> None:
    payload = run_cli("contract")
    schema = payload["runstate_contract_schema"]
    assert "Skills_runtime_checklist" in schema["checklist_fields"]
    assert payload["creation_chain_position"]["insert_before"] == "SkillsManager-Tooling-CheckUp"


def test_inspect_returns_not_applicable_for_non_workflow_skill(tmp_path: Path) -> None:
    skill_root = tmp_path / "Demo-Referenced"
    _write(
        skill_root / "SKILL.md",
        """---
name: Demo-Referenced
metadata:
  skill_profile:
    doc_topology: referenced
    tooling_surface: none
    workflow_control: guardrailed
---

# Demo
""",
    )
    payload = run_cli("inspect", "--target-skill-root", str(skill_root))
    assert payload["governed_type"] == "not_applicable"
    assert payload["applicability"] == "not_applicable"


def test_scaffold_and_audit_workflow_skill(tmp_path: Path) -> None:
    skill_root = _workflow_skill_fixture(tmp_path, orchestrator=False)
    scaffold_payload = run_cli("scaffold", "--target-skill-root", str(skill_root))
    assert scaffold_payload["status"] == "ok"
    assert "references/runstates/RUNSTATE_METHOD_CONTRACT.json" in scaffold_payload["written_files"]

    audit_payload = run_cli("audit", "--target-skill-root", str(skill_root))
    assert audit_payload["status"] == "ok"
    assert audit_payload["governed_type"] == "workflow_runtime"


def test_scaffold_and_audit_skill_flow_orchestrator(tmp_path: Path) -> None:
    skill_root = _workflow_skill_fixture(tmp_path, orchestrator=True)
    scaffold_payload = run_cli("scaffold", "--target-skill-root", str(skill_root))
    assert scaffold_payload["status"] == "ok"
    assert any("Skills_runtime_checklist.yaml" in item for item in scaffold_payload["written_files"])

    audit_payload = run_cli("audit", "--target-skill-root", str(skill_root))
    assert audit_payload["status"] == "ok"
    assert audit_payload["governed_type"] == "skill_flow_orchestrator"
